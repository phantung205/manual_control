import torch.nn as nn


class HandLSTM(nn.Module):
    def __init__(self,num_classes):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=63, # Số lượng feature
            hidden_size=128, #LSTM sẽ sử dụng bao nhiêu giá trị để lưu trữ thông tin mà nó đã học được từ chuỗi
            num_layers=2, # số lần lstm trồng lên nhau
            batch_first=True, # để lstm nhận theo (batch, sequence, features)
            dropout=0.3
        )

        self.fc1 = nn.Linear(128,64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(64,num_classes)

    def forward(self, x):

        # x:
        # (batch, 30, 63)

        output, (hidden, cell) = self.lstm(x)
        # lấy output của frame cuối
        x = output[:, -1, :]
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)

        return x