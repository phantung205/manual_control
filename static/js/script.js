const video = document.getElementById("camera");

const drawCanvas = document.getElementById("canvas");
const drawCtx = drawCanvas.getContext("2d");

const captureCanvas = document.getElementById("captureCanvas");
const captureCtx = captureCanvas.getContext("2d");

const statusEl = document.getElementById("status");
const framesEl = document.getElementById("frames");
const labelEl = document.getElementById("label");
const confidenceEl = document.getElementById("confidence");
const handEl = document.getElementById("hand");

// HAND CONNECTIONS
const HAND_CONNECTIONS = [
    [0, 1], [1, 2], [2, 3], [3, 4],
    [0, 5], [5, 6], [6, 7], [7, 8],
    [5, 9], [9, 10], [10, 11], [11, 12],
    [9, 13], [13, 14], [14, 15], [15, 16],
    [13, 17], [17, 18], [18, 19], [19, 20],
    [0, 17]
];


// CAMERA SETUP
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        video.srcObject = stream;
        statusEl.innerText = "Camera đã sẵn sàng";

        video.onloadedmetadata = () => {
            sendFrameLoop();
        };
    } catch (error) {
        console.error(error);
        statusEl.innerText = "Không thể mở camera";
        statusEl.style.color = "red";
    }
}


// DRAW LANDMARKS
function drawLandmarks(landmarks) {
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

    if (!landmarks || landmarks.length === 0) {
        return;
    }

    const points = landmarks.map(lm => ({
        x: lm.x * drawCanvas.width,
        y: lm.y * drawCanvas.height
    }));

    // Draw Skeleton Lines
    drawCtx.strokeStyle = "#00FF00";
    drawCtx.lineWidth = 2;

    HAND_CONNECTIONS.forEach(pair => {
        const p1 = points[pair[0]];
        const p2 = points[pair[1]];

        if (!p1 || !p2) return;

        drawCtx.beginPath();
        drawCtx.moveTo(p1.x, p1.y);
        drawCtx.lineTo(p2.x, p2.y);
        drawCtx.stroke();
    });

    // Draw 21 Joints
    drawCtx.fillStyle = "#FF0000";

    points.forEach(point => {
        drawCtx.beginPath();
        drawCtx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
        drawCtx.fill();
    });
}


// HANDLE PREDICTION UI
function handlePrediction(data) {

    // Không phát hiện tay
    if (!data.detected) {
        statusEl.innerText = "Không phát hiện bàn tay";
        handEl.innerText = "---";
        labelEl.innerText = "---";
        confidenceEl.innerText = "0%";
        return;
    }

    // Đã phát hiện tay nhưng chưa đủ 30 frame
    if (!data.ready) {
        statusEl.innerText = "Đang thu thập frames...";
        handEl.innerText = data.hand || "---";
        labelEl.innerText = "---";
        confidenceEl.innerText = "0%";
        return;
    }

    // Đã nhận diện
    statusEl.innerText = "Đã nhận diện!";
    handEl.innerText = data.hand || "---";
    labelEl.innerText = data.label || "---";
    confidenceEl.innerText =((data.confidence || 0) * 100).toFixed(2) + "%";
}

// SEND FRAME LOOP -> FLASK
function sendFrameLoop() {
    if (video.videoWidth === 0) {
        setTimeout(sendFrameLoop, 100);
        return;
    }

    captureCtx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);

    captureCanvas.toBlob(async (blob) => {
        if (!blob) {
            setTimeout(sendFrameLoop, 100);
            return;
        }

        const formData = new FormData();
        formData.append("image", blob, "frame.jpg");

        try {
            const response = await fetch("/predict_hand", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            framesEl.innerText = `${data.frames}/30`;
            drawLandmarks(data.landmarks);
            handlePrediction(data);

        } catch (error) {
            console.error("Lỗi server:", error);
            statusEl.innerText = "Lỗi kết nối Server";
        }

        setTimeout(sendFrameLoop, 100);

    }, "image/jpeg", 0.5);
}

// INITIALIZATION
startCamera();