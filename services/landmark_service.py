def extract_landmarks(hand_landmarks):
    """chuyển mediapipe hand thành 63 feature"""

    # lấy cổ tay làm gốc
    wrist = hand_landmarks.landmark[0]
    # tạo một list chứa 63 tọa độ của 21 điểm bàn tay
    landmarks = []

    # Lấy 21 landmarks
    for lm in hand_landmarks.landmark:
        # Đưa tọa độ về tương đối với wrist
        x = lm.x - wrist.x
        y = lm.y - wrist.y
        z = lm.z - wrist.z

        landmarks.append(x)
        landmarks.append(y)
        landmarks.append(z)

    # Kiểm tra
    if len(landmarks) != 63:
        raise ValueError(
            f"Landmarks phải có 63 giá trị, "
            f"nhưng nhận được {len(landmarks)}"
        )

    return landmarks