import os
import numpy as np
import torch
from torch.utils.data import Dataset
from configs import config_hands


class HandDataset(Dataset):
    def __init__(self, data_dir):

        self.data_dir = data_dir

        # Danh sách class
        self.classes = config_hands.categories

        # Chuyển class thành label
        #
        # Ví dụ:
        # fist       -> 0
        # open_hand  -> 1
        # peace      -> 2
        self.class_to_idx = {
            class_name: idx
            for idx, class_name in enumerate(self.classes)
        }


        # Danh sách:
        # [
        #   (".../fist/sequence_001.npy", 0),
        #   (".../fist/sequence_002.npy", 0),
        #   (".../open_hand/sequence_001.npy", 1),
        # ]
        self.samples = []


        # Duyệt từng class
        for class_name in self.classes:
            class_dir = os.path.join(data_dir,class_name)

            # Nếu thư mục class không tồn tại
            if not os.path.isdir(class_dir):
                continue

            # Label của class
            label = self.class_to_idx[class_name]


            # Duyệt các file .npy
            for file_name in sorted(os.listdir(class_dir)):
                if file_name.endswith(".npy"):
                    file_path = os.path.join(class_dir,file_name)
                    self.samples.append((file_path, label))


    def __len__(self):
        return len(self.samples)


    def __getitem__(self, index):
        # Lấy đường dẫn và label
        file_path, label = self.samples[index]

        # Đọc file .npy
        data = np.load(file_path)

        # numpy → torch tensor
        data = torch.tensor(data,dtype=torch.float32)

        # label → torch tensor
        label = torch.tensor(label,dtype=torch.long)

        return data, label


