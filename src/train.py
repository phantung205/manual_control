import argparse
import torch
from sympy.printing import c
from torch.utils.checkpoint import checkpoint

from src import dataloader,dataset
from model.lstm_model import HandLSTM
from configs import config
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import shutil
import os

def get_args():
    parser = argparse.ArgumentParser(description="train pose estimation")
    parser.add_argument("--dir_train","-t",type=str,default=config.dir_train)
    parser.add_argument("--dir_val","-v",type=str,default=config.dir_val)
    parser.add_argument("--batch_size","-b",type=int,default=config.batch_size)
    parser.add_argument("--epoch","-e",type=int,default=config.num_epochs)
    parser.add_argument("--learning_rate","-l",type=float,default=config.learning_rate)
    parser.add_argument("--save_model","-s",type=str,default=config.dir_save_model)
    parser.add_argument("--path_tensorboard","-p",type=str,default=config.dir_tensorboard)
    parser.add_argument("--checkpoint","-c",type=str,default=None)
    return parser.parse_args()

def train(args):
    # sử dụng gpu nếu có
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # tạo thư mục lưu model nếu chưa có
    os.makedirs(args.save_model,exist_ok=True)

    #xóa tensorboard cũ nếu train lại từ đầu
    if args.checkpoint is None:
        if os.path.isdir(args.path_tensorboard):
            shutil.rmtree(args.path_tensorboard)

    # khởi tạo tensorboard
    writer = SummaryWriter(args.path_tensorboard)

    # load dataset
    train_dataset = dataset.HandDataset(args.dir_train)
    val_dataset = dataset.HandDataset(args.dir_val)

    # load dataloader
    train_dataloader = dataloader.create_dataloader(dataset=train_dataset,batch_size=args.batch_size,shuffle=True)
    val_dataloader = dataloader.create_dataloader(dataset=val_dataset,batch_size=args.batch_size,shuffle=False)

    # model
    model = HandLSTM(num_classes=config.num_class).to(device)

    # loss function
    criterion = torch.nn.CrossEntropyLoss()

    #optimizer
    optimizer = torch.optim.Adam(model.parameters(),lr=args.learning_rate)

    # load checkpoint cũ nếu có
    if args.checkpoint:
        checkpoint = torch.load(args.checkpoint,map_location=device)
        start_epoch = checkpoint["epoch"]
        best_acc = checkpoint["best_acc"]
        optimizer.load_state_dict(checkpoint["optimizer"])
        model.load_state_dict(checkpoint["model"])
    else:
        start_epoch = 0
        best_acc = 0

    num_iters_per_epoch = len(train_dataloader)

    for epoch in range(start_epoch,args.epoch):
        model.train()
        progress_bar = tqdm(train_dataloader,colour="yellow")
        for iter,(x, y) in enumerate(progress_bar):
            # Đưa data lên device
            x = x.to(device)
            y = y.to(device)

            # forward
            ouputs = model(x)

            # tính loss
            loss = criterion(ouputs,y)

            # xóa gradient cũ
            optimizer.zero_grad()

            # back ward
            loss.backward()

            # Cập nhật weight
            optimizer.step()


            # ghi loss vào progress bar
            progress_bar.set_description("Epoch: {}/{} .loss: {:0.4f} ".format(epoch+1,args.epoch,loss.item()))
            # ghi loss vào tensorboard
            writer.add_scalar("train/loss",loss.item(),epoch*num_iters_per_epoch+iter)



        model.eval()
        with torch.no_grad():
            val_correct = 0
            val_total = 0
            progress_bar = tqdm(val_dataloader, colour="green")
            for x, y in progress_bar:
                # Đưa data lên device
                x = x.to(device)
                y = y.to(device)

                # Forward
                outputs = model(x)

                # Loss
                loss = criterion(outputs,y)

                # Accuracy
                _, predicted = torch.max(outputs,dim=1)
                val_total += y.size(0)
                val_correct += (predicted == y).sum().item()

            # VALIDATION METRICS
            val_accuracy = (val_correct / val_total)

            writer.add_scalar("val/accuracy",val_accuracy,epoch)

            print("accuracy của epoch: {} . accuracy: {} ".format(epoch,val_accuracy))

            # save checkpoint last
            checkpoint = {
                "epoch": epoch + 1,
                "best_acc": val_accuracy,
                "model":model.state_dict(),
                "optimizer": optimizer.state_dict()
            }
            torch.save(checkpoint, "{}/last_hands.pt".format(args.save_model))

            # save best checkpoint model
            if val_accuracy > best_acc:
                best_acc = val_accuracy
                checkpoint = {
                    "epoch": epoch + 1,
                    "best_acc": best_acc,
                    "model":model.state_dict(),
                    "optimizer": optimizer.state_dict()
                }
                torch.save(checkpoint, "{}/best_hands.pt".format(args.save_model))



if __name__ == '__main__':
    args = get_args()
    train(args)












