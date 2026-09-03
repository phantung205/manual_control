// Các phần tử DOM
const video = document.getElementById("camera");

const drawCanvas = document.getElementById("canvas");
const drawCtx = drawCanvas.getContext("2d");

const captureCanvas = document.getElementById("captureCanvas");
const captureCtx = captureCanvas.getContext("2d");

const statusEl = document.getElementById("status");
const framesEl = document.getElementById("frames");
const labelEl = document.getElementById("label");
const confidenceEl = document.getElementById("confidence");

// Các cặp điểm kết nối ngón tay (Hand Connections trong MediaPipe)
const HAND_CONNECTIONS = [
    [0,1], [1,2], [2,3], [3,4],       // Ngón cái
    [0,5], [5,6], [6,7], [7,8],       // Ngón trỏ
    [5,9], [9,10], [10,11], [11,12],  // Ngón giữa
    [9,13], [13,14], [14,15], [15,16],// Ngón áp út
    [13,17], [17,18], [18,19], [19,20], [0,17] // Ngón út & lòng bàn tay
];

// 1. KHỞI ĐỘNG CAMERA
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        statusEl.innerText = "Camera đã sẵn sàng";

        // Đợi video chạy rồi mới bắt đầu loop gửi frame
        video.onloadedmetadata = () => {
            sendFrameLoop();
        };
    } catch (error) {
        console.error(error);
        statusEl.innerText = "Lỗi: Không thể mở camera";
        statusEl.style.color = "red";
    }
}

// 2. VẼ KHUNG XƯƠNG BÀN TAY (LANDMARKS)
function drawLandmarks(landmarks) {
    // Xóa bản vẽ cũ
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    if (!landmarks || landmarks.length === 0) return;

    // MediaPipe trả về tọa độ chuẩn hóa (0.0 -> 1.0). Cần nhân với kích thước canvas.
    const points = landmarks.map(lm => ({
        x: lm.x * drawCanvas.width,
        y: lm.y * drawCanvas.height
    }));

    // Vẽ các đường nối (xương)
    drawCtx.strokeStyle = "#00FF00"; // Màu xanh lá
    drawCtx.lineWidth = 2;
    HAND_CONNECTIONS.forEach(pair => {
        const p1 = points[pair[0]];
        const p2 = points[pair[1]];
        if (p1 && p2) {
            drawCtx.beginPath();
            drawCtx.moveTo(p1.x, p1.y);
            drawCtx.lineTo(p2.x, p2.y);
            drawCtx.stroke();
        }
    });

    // Vẽ các điểm (khớp)
    drawCtx.fillStyle = "#FF0000"; // Màu đỏ
    points.forEach(point => {
        drawCtx.beginPath();
        drawCtx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
        drawCtx.fill();
    });
}

// 3. GỬI FRAME LÊN SERVER (FLASK) VÀ NHẬN KẾT QUẢ
function sendFrameLoop() {
    // Nếu video chưa thu được ảnh thì gọi lại sau
    if (video.videoWidth === 0) {
        setTimeout(sendFrameLoop, 50);
        return;
    }

    // Copy frame từ video ra canvas ẩn
    captureCtx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);

    captureCanvas.toBlob(async (blob) => {
        if (!blob) return;

        const formData = new FormData();
        formData.append("image", blob, "frame.jpg");

        try {
            const response = await fetch("/predict_hand", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            // Cập nhật giao diện
            framesEl.innerText = `${data.frames}/30`;

            // Vẽ các điểm trên tay (nếu có)
            drawLandmarks(data.landmarks);

            if (!data.detected) {
                statusEl.innerText = "Không phát hiện bàn tay";
                labelEl.innerText = "---";
                confidenceEl.innerText = "0%";
            }
            else if (!data.ready) {
                statusEl.innerText = "Đang thu thập đủ 30 frames...";
                labelEl.innerText = "---";
                confidenceEl.innerText = "0%";
            }
            else {
                statusEl.innerText = "Đã nhận diện!";
                labelEl.innerText = data.label || "Chưa xác định";
                confidenceEl.innerText = (data.confidence * 100).toFixed(2) + "%";
            }

        } catch (error) {
            console.error("Lỗi kết nối server:", error);
            statusEl.innerText = "Lỗi kết nối Server";
        }

        // Chạy tiếp vòng lặp (khoảng 100ms)
        setTimeout(sendFrameLoop, 50);

    }, "image/jpeg", 0.5);
}

// CHẠY CHƯƠNG TRÌNH
startCamera();