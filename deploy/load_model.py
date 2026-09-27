from model.lstm_model import HandLSTM
import torch
from configs import config_hands


def load_model_device(checkpoint_path):
    # device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # model
    model = HandLSTM(num_classes=config_hands.num_class).to(device)

    # checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model.load_state_dict(checkpoint["model"])

    # bật chế độ eval
    model.eval()

    return model, device