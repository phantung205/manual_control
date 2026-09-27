import cv2
import mediapipe as mp
import torch

from model.lstm_model import HandLSTM
from configs import config_hands
import numpy as np


# chọn thiết bị cpu hay gpu
device = "cuda" if torch.cuda.is_available() else "cpu"

# load model
model = HandLSTM(num_classes=config_hands.num_class).to(device)
checkpoint = torch.load(config_hands.path_best_model,map_location=device)
model.load_state_dict(checkpoint["model"])

model.eval()

#load model mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=config_hands.max_num_hands, # muốn một hay hai bàn tay
    min_detection_confidence=config_hands.min_detection_confidence, # dộ phát hiện bàn tay trên 50% mới nhận là bàn tay
    min_tracking_confidence=config_hands.min_tracking_confidence # múc tin tường bàn tay từ ban đầu theo dõi ko bị đổi khi có tay mới
)

# camera
cap = cv2.VideoCapture(0)

#sequence
sequence = [] # lưu 30 frame
sequence_length = config_hands.sequence_length # độ dài của frame

#confidence theshold
confidence_threshold = config_hands.confidence_threshold

current_label = "Unknown"
current_confidence = 0.0

while True:
    ret,frame = cap.read()

    if not ret:
        break

    # flip camera
    frame = cv2.flip(frame,1)

    # convert BGR - RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # đựa qua mediapipe để tìm các điểm trên frame
    results = hands.process(frame_rgb)

    # kiểm tra nếu phát hiện bàn tay
    if results.multi_hand_landmarks:
        # lấy ra bàn tay đầu tiên
        hand_landmarks = results.multi_hand_landmarks[0]

        # lấy ra đang dùng tay trái hay phải
        hand_label = results.multi_handedness[0].classification[0].label
        # nghi ra tên tay nào
        cv2.putText(
            frame,
            f"Hand: {hand_label}",
            (10, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # vẽ các đường nối lên camera
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Lấy phần cổ tay làm gốc
        wrist = hand_landmarks.landmark[0]

        # chứa 63 tọa độ điểm
        landmarks = []

        # Lấy  duyện qua 21 landmarks
        for lm in hand_landmarks.landmark:
            # tọa độ xyz từ cổ tay gốc
            x = lm.x - wrist.x
            y = lm.y - wrist.y
            z = lm.z - wrist.z

            landmarks.append(x)
            landmarks.append(y)
            landmarks.append(z)

        # Thêm frame hiện tại vào sequence
        sequence.append(landmarks)

        # chỉ lấy 30 frame cuối
        if len(sequence) > sequence_length:
            sequence = sequence[-sequence_length:]

        # dự đoán 30 frame cuối
        if len(sequence) == sequence_length:
            input_data = np.array(sequence,dtype=np.float32)

            # chuyển thành dạng tensor (30,63)
            input_tensor = torch.tensor(input_data,dtype=torch.float32)

            # thêm chiều batch size
            input_tensor = input_tensor.unsqueeze(0)

            # cho sang gpu
            input_tensor = input_tensor.to(device)

            # quá trình inference
            with torch.no_grad():
                outputs = model(input_tensor)

                # đưa qua sort max để cho biết mỗi class tính là bn %
                probabilities = torch.softmax(outputs,dim=1)

                # lấy ra % lớn của class lớn nhất
                confidence, predicted = torch.max(probabilities,dim=1)

                confidence = confidence.item()
                predicted = predicted.item()

                # kiểm tra xem có lớn hơn ngưỡng ko nếu ko lớn hơn thì để là chưa biết
                if confidence >= confidence_threshold:
                    current_label = (config_hands.categories[predicted])
                    current_confidence = confidence

                else:
                    current_label = "Unknown"
                    current_confidence = confidence

    # nếu ko phát hiện tay
    else:
        current_label = "No hand"
        current_confidence = 0.0
        sequence = []


    # vẽ lên frame
    cv2.rectangle(frame,(0, 0),(400, 90),(0, 0, 0),-1)

    cv2.putText(frame,f"Prediction: {current_label}",(10, 35),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0, 255, 0),2)

    cv2.putText(frame,f"Confidence: {current_confidence * 100:.1f}%",(10, 70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 255),2)

    # Sequence progress
    cv2.putText(frame,f"Frames: {len(sequence)}/{sequence_length}",(10, 120),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 255),2)

    # show camera
    cv2.imshow("Hand LSTM Inference",frame)

    # nhấn q để thoát
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# giải phóng bộ nhớ sau khi thoát
cap.release()
cv2.destroyAllWindows()
hands.close()