import cv2
import mediapipe as mp
import numpy as np
import os
from configs import config

# nhập vào class bạn muốn tạo
label = input("nhập vào class bạn muốn tạo: ").strip()
path_data = os.path.join(config.dir_raw_data,label)
os.makedirs(path_data, exist_ok=True)

# khởi tạo mediapipe
mp_hands = mp.solutions.hands # chọn giải pháp .hands
# lấy công cụ vẽ landmark
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=config.max_num_hands, # muốn một hay hai bàn tay
    min_detection_confidence=config.min_detection_confidence, # dộ phát hiện bàn tay trên 50% mới nhận là bàn tay
    min_tracking_confidence=config.min_tracking_confidence # múc tin tường bàn tay từ ban đầu theo dõi ko bị đổi khi có tay mới
)

# đọc video từ camera máy tính
cap = cv2.VideoCapture(0)
sequence = [] # Dùng để lưu 30 frame của một sequence
sequence_count = 0 # dùng đếm xem đã thu đc bao nhiều sequence
recording = False # sác định xem hiện tại có dang nghi hình hay ko

# độ dài của frame lấy liên tục
sequence_length = config.sequence_length
# số lần lấy dữ liệu cho frame đó
number_of_sequences = config.number_of_sequences

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Lật ảnh giống camera trước
    frame = cv2.flip(frame, 1)

    # BGR -> RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # MediaPipe nhận diện bàn tay
    results = hands.process(frame_rgb)


    # kiểm tra nếu phát hiện bàn tay trả về true
    if results.multi_hand_landmarks:
        # lấy ra bàn tay đầu tiên
        hand_landmarks = results.multi_hand_landmarks[0]

        # vẽ các điểm và các đường nối lên chính hình ảnh camera
        mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

        # Nếu đang ghi dữ liệu
        if recording:
            # Lấy phần cổ tay làm gốc
            wrist = hand_landmarks.landmark[0]

            # chứa 63 tọa độ điểm
            landmarks = []

            # Lấy 21 landmarks
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

    # hiển thị thông tin
    if recording:
        cv2.putText(frame,
            f"Recording: {len(sequence)}/{sequence_length}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
    else:
        cv2.putText(
            frame,
            f"Label: {label}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Sequence: {sequence_count}/{number_of_sequences}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            "SPACE = Start",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # ĐỦ 30 FRAME
    if len(sequence) == sequence_length:
        sequence_count += 1

        # Chuyển thành numpy
        sequence_data = np.array(sequence, dtype=np.float32)

        # Lưu file
        file_path = os.path.join(path_data,f"sequence_{sequence_count:03d}.npy")

        np.save(file_path, sequence_data)

        print(f"Saved: {file_path} - Shape: {sequence_data.shape}")

        # Xóa sequence cũ
        sequence = []

        # Dừng ghi
        recording = False

    # HIỂN THỊ CAMERA
    cv2.imshow("Collect Data", frame)
    key = cv2.waitKey(1) & 0xFF
    # Nhấn Q để thoát
    if key == ord("q"):
        break

    # Nhấn SPACE để bắt đầu thu
    if key == ord(" ") and not recording:

        if sequence_count < number_of_sequences:
            sequence = []
            recording = True
            print(f"Start recording sequence {sequence_count + 1}")

    # Đã thu đủ dữ liệu
    if sequence_count >= number_of_sequences:
        print("Đã thu đủ dữ liệu!")
        break

cap.release()
cv2.destroyAllWindows()
hands.close()