from services import load_model_service,inference_service,landmark_service,esp32_service,hand_label_service
from flask import Blueprint,render_template, request,jsonify
import mediapipe as mp
import numpy as np
from configs import config_hands
import cv2

# load luôn model một lần
model, device = load_model_service.load_model_service(config.path_best_model)

# blueprint
hand_bp = Blueprint("hand",__name__)


#  mediapipe
mp_hands = mp.solutions.hands # chọn giải pháp .hands

hands = mp_hands.Hands(
    max_num_hands=config.max_num_hands, # muốn một hay hai bàn tay
    min_detection_confidence=config.min_detection_confidence, # dộ phát hiện bàn tay trên 50% mới nhận là bàn tay
    min_tracking_confidence=config.min_tracking_confidence # múc tin tường bàn tay từ ban đầu theo dõi ko bị đổi khi có tay mới
)

#sequence
sequence = []

@hand_bp.route("/")
def home():
    return  render_template("index.html")

@hand_bp.route("/predict_hand",methods=["POST"])
def predict():
    global sequence

    # Lấy image từ request
    if "image" not in request.files:
        return jsonify({"error": "Không tìm thấy image"}), 400

    file = request.files["image"]

    # Image → numpy
    # đọc ảnh thành dạng byte
    image_bytes = file.read()
    # chuyển ảnh sang numpy
    image_array = np.frombuffer(image_bytes,dtype=np.uint8)
    # giải mã nó thành ảnh opencv
    frame = cv2.imdecode(image_array,cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Không đọc được image"}), 400

    # BGR → RGB
    frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    # MediaPipe phát hiện bàn tay
    results = hands.process(frame_rgb)

    # Không phát hiện tay
    if not results.multi_hand_landmarks:
        sequence.clear()

        return jsonify({
            "detected": False,
            "ready": False,
            "frames": 0,
            "label": None,
            "hand": None,
            "confidence": 0,
            "landmarks": []
        })


    # Lấy bàn tay đầu tiên
    hand_landmarks = results.multi_hand_landmarks[0]

    # xác định tay trái hay phải bằng pose
    hand_label = hand_label_service.get_hand_label(results,0)

    # Lấy tọa độ để VẼ lên Web
    points = []
    for lm in hand_landmarks.landmark:
        points.append({
            "x": lm.x,
            "y": lm.y
        })

    # MediaPipe → 63 features
    landmarks = landmark_service.extract_landmarks(hand_landmarks)


    # Thêm frame vào sequence
    sequence.append(landmarks)

    # Chỉ giữ 30 frame cuối
    if len(sequence) > 30:
        sequence.pop(0)

    # Chưa đủ 30 frame
    if len(sequence) < config.sequence_length:
        return jsonify({
            "detected": True,
            "ready": False,
            "frames": len(sequence),
            "label": None,
            "hand": hand_label,
            "confidence": 0,
            "landmarks": points
        })


    # Prediction
    result = inference_service.predict_service(model,device,np.array(sequence, dtype=np.float32))

    label = result["label"]
    confidence = result["confidence"]

    # Camera web đang hiển thị dạng gương → đảo lại Left/Right
    if hand_label == "Left":
        hand_label = "Right"
    elif hand_label == "Right":
        hand_label = "Left"

    # ĐIỀU KHIỂN ESP32
    if hand_label == "Right" and label == "one_finger":
        esp32_service.turn_on()
    elif hand_label == "Left" and label == "one_finger":
        esp32_service.turn_off()

    # TRẢ KẾT QUẢ CHO JS
    return jsonify({
        "detected": True,
        "ready": True,
        "frames": len(sequence),
        "label": label,
        "hand": hand_label,
        "confidence": confidence,
        "landmarks": points
    })


