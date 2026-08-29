import cv2
import mediapipe as mp
import numpy as np
import torch
from model.lstm_model import HandLSTM
from configs import config

# DEVICE
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# LOAD MODEL
model = HandLSTM(num_classes=config.num_class).to(device)

checkpoint = torch.load(config.dir_save_model + "/best_hands.pt",map_location=device)

model.load_state_dict(checkpoint["model"])
model.eval()


# MEDIAPIPE
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# CAMERA
cap = cv2.VideoCapture(0)

# SEQUENCE
sequence = []
sequence_length = config.sequence_length


# CONFIDENCE THRESHOLD
confidence_threshold = 0.8


# PREDICTION
current_label = "Unknown"
current_confidence = 0.0


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip camera
    frame= cv2.flip(frame, 1)

    # BGR → RGB
    frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    # MediaPipe
    results = hands.process(frame_rgb)

    # IF HAND DETECTED
    if results.multi_hand_landmarks:
        hand_landmarks = (results.multi_hand_landmarks[0])

        # Draw landmarks
        mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

        # Wrist
        wrist = hand_landmarks.landmark[0]

        # Get 63 features
        landmarks = []
        for lm in hand_landmarks.landmark:
            x = lm.x - wrist.x
            y = lm.y - wrist.y
            z = lm.z - wrist.z

            landmarks.append(x)
            landmarks.append(y)
            landmarks.append(z)


        # Add frame
        sequence.append(landmarks)


        # Keep only latest 30 frames
        if len(sequence) > sequence_length:
            sequence = sequence[-sequence_length:]


        # ENOUGH 30 FRAMES → PREDICT
        if len(sequence) == sequence_length:
            # numpy
            input_data = np.array(sequence,dtype=np.float32)

            # Shape:
            # (30, 63)
            input_tensor = torch.tensor(input_data,dtype=torch.float32)

            # Add batch dimension
            # (30,63)
            # ↓
            # (1,30,63)
            input_tensor = input_tensor.unsqueeze(0)

            input_tensor = input_tensor.to(device)

            # Inference
            with torch.no_grad():
                outputs = model(input_tensor)

                # Softmax
                probabilities = torch.softmax(outputs,dim=1)

                # Get prediction
                confidence, predicted = torch.max(probabilities,dim=1)
                confidence = confidence.item()
                predicted = predicted.item()

            # Confidence threshold
            if confidence >= confidence_threshold:
                current_label = (config.categories[predicted])
                current_confidence = confidence
            else:
                current_label = "Unknown"
                current_confidence = confidence

    else:
        # Không phát hiện tay
        current_label = "No hand"
        current_confidence = 0.0
        sequence = []


    # DISPLAY
    cv2.rectangle(frame,(0, 0),(400, 90), (0, 0, 0), -1)
    cv2.putText(
        frame,
        f"Prediction: {current_label}",
        (10, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {current_confidence * 100:.1f}%",
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Sequence progress
    cv2.putText(
        frame,
        f"Frames: {len(sequence)}/{sequence_length}",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # SHOW CAMERA
    cv2.imshow("Hand LSTM Inference",frame)

    # QUIT
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# RELEASE
cap.release()
cv2.destroyAllWindows()
hands.close()