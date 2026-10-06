// ============================================================
//  Lấy các phần tử HTML
// ============================================================
const video       = document.getElementById('camera');
const drawCanvas  = document.getElementById('canvas');
const drawCtx     = drawCanvas.getContext('2d');

const gestureEl   = document.getElementById('gesture');
const gestureCmd  = document.getElementById('gestureCommand');
const messageEl   = document.getElementById('message');
const handEl      = document.getElementById('hand');
const framesEl    = document.getElementById('frames');

// ============================================================
//  Kết nối 21 điểm khung xương bàn tay (MediaPipe)
// ============================================================
const HAND_CONNECTIONS = [
    [0,1],[1,2],[2,3],[3,4],       // ngón cái
    [0,5],[5,6],[6,7],[7,8],       // ngón trỏ
    [5,9],[9,10],[10,11],[11,12],  // ngón giữa
    [9,13],[13,14],[14,15],[15,16],// ngón áp út
    [13,17],[17,18],[18,19],[19,20],// ngón út
    [0,17]                         // lòng bàn tay
];

// ============================================================
//  Manual Commands
// ============================================================
function sendCommand(endpoint) {
    if (endpoint.startsWith('/')) {
        endpoint = endpoint.substring(1);
    }
    
    // Giả định proxy từ Python
    fetch('/proxy/' + endpoint)
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            if(messageEl) messageEl.innerText = 'Gửi lệnh: /' + endpoint;
        } else {
            if(messageEl) messageEl.innerText = 'Lỗi khi gửi lệnh: /' + endpoint;
        }
    })
    .catch(err => {
        if(messageEl) messageEl.innerText = 'Lỗi mạng!';
    });
}

function changeFanMode(switchEl) {
    const modeText = document.getElementById('fanModeText');
    const manualBtns = document.getElementById('fanManualButtons');
    if(switchEl.checked) {
        modeText.innerText = 'THỦ CÔNG';
        manualBtns.style.display = 'flex';
        sendCommand('/quat/manual');
    } else {
        modeText.innerText = 'TỰ ĐỘNG';
        manualBtns.style.display = 'none';
        sendCommand('/quat/auto');
    }
}

function changePumpMode(switchEl) {
    const modeText = document.getElementById('pumpModeText');
    const manualBtns = document.getElementById('pumpManualButtons');
    if(switchEl.checked) {
        modeText.innerText = 'THỦ CÔNG';
        manualBtns.style.display = 'flex';
        sendCommand('/bom/manual');
    } else {
        modeText.innerText = 'TỰ ĐỘNG';
        manualBtns.style.display = 'none';
        sendCommand('/bom/auto');
    }
}

function changeStairMode(switchEl) {
    const modeText = document.getElementById('stairModeText');
    const manualBtns = document.getElementById('stairManualButtons');
    if(switchEl.checked) {
        modeText.innerText = 'THỦ CÔNG';
        manualBtns.style.display = 'flex';
        sendCommand('/cauthang/manual');
    } else {
        modeText.innerText = 'TỰ ĐỘNG';
        manualBtns.style.display = 'none';
        sendCommand('/cauthang/auto');
    }
}

// ============================================================
//  Bật camera
// ============================================================
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.onloadedmetadata = () => sendFrameLoop();
    } catch (err) {
        console.error(err);
    }
}

// ============================================================
//  Vẽ khung xương tay lên canvas
// ============================================================
function drawLandmarks(landmarks) {
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    if (!landmarks || landmarks.length === 0) return;

    // Chuyển tọa độ [0-1] → pixel
    const pts = landmarks.map(lm => ({
        x: lm.x * drawCanvas.width,
        y: lm.y * drawCanvas.height
    }));

    // Vẽ đường nối
    drawCtx.strokeStyle = '#00FF00';
    drawCtx.lineWidth = 2;
    for (const [i, j] of HAND_CONNECTIONS) {
        drawCtx.beginPath();
        drawCtx.moveTo(pts[i].x, pts[i].y);
        drawCtx.lineTo(pts[j].x, pts[j].y);
        drawCtx.stroke();
    }

    // Vẽ các khớp
    drawCtx.fillStyle = '#FF0000';
    for (const p of pts) {
        drawCtx.beginPath();
        drawCtx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
        drawCtx.fill();
    }
}

// ============================================================
//  Cập nhật UI kết quả AI
// ============================================================
function updateUI(data) {
    if(framesEl) framesEl.innerText = data.frames + '/30';

    if (!data.detected) {
        if(gestureEl) gestureEl.innerText = 'Chưa thấy tay';
        if(gestureCmd) gestureCmd.innerText = '--';
        if(handEl) handEl.innerText = '--';
        return;
    }
    
    if(handEl) handEl.innerText = data.hand || '--';

    if (!data.ready) {
        if(gestureEl) gestureEl.innerText = 'Đang thu thập...';
        if(gestureCmd) gestureCmd.innerText = '--';
        return;
    }

    let hand = data.hand;
    let label = data.label;
    if(gestureEl) gestureEl.innerText = label;
    
    let commandText = '';
    if (hand === 'Right') {
        if (label === 'zero_finger') commandText = 'BẬT CÒI';
        else if (label === 'one_finger') commandText = 'BẬT ĐÈN XANH';
        else if (label === 'two_finger') commandText = 'BẬT ĐÈN ĐỎ';
        else if (label === 'three_finger') commandText = 'BẬT QUẠT';
        else if (label === 'four_finger') commandText = 'MỞ CỬA';
        else if (label === 'five_finger') commandText = 'BẬT BƠM';
    } else if (hand === 'Left') {
        if (label === 'zero_finger') commandText = 'TẮT CÒI';
        else if (label === 'one_finger') commandText = 'TẮT ĐÈN XANH';
        else if (label === 'two_finger') commandText = 'TẮT ĐÈN ĐỎ';
        else if (label === 'three_finger') commandText = 'TẮT QUẠT';
        else if (label === 'four_finger') commandText = 'ĐÓNG CỬA';
        else if (label === 'five_finger') commandText = 'TẮT BƠM';
    }
    
    if(gestureCmd) gestureCmd.innerText = commandText;
}

// ============================================================
//  Chụp frame → flip ngang → gửi lên server
// ============================================================
function captureFlippedFrame() {
    const tmp = document.createElement('canvas');
    tmp.width  = 320;
    tmp.height = 240;
    const ctx  = tmp.getContext('2d');

    ctx.translate(tmp.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, tmp.width, tmp.height);

    return tmp;
}

async function sendFrameLoop() {
    if (video.videoWidth === 0) {
        setTimeout(sendFrameLoop, 100);
        return;
    }

    const flippedCanvas = captureFlippedFrame();

    flippedCanvas.toBlob(async (blob) => {
        if (blob) {
            const form = new FormData();
            form.append('image', blob, 'frame.jpg');

            try {
                const res  = await fetch('/predict_hand', { method: 'POST', body: form });
                const data = await res.json();
                drawLandmarks(data.landmarks);
                updateUI(data);
            } catch (err) {
                console.error(err);
            }
        }

        setTimeout(sendFrameLoop, 100);
    }, 'image/jpeg', 0.5);
}

startCamera();


// ============================================================
//  Lấy trạng thái từ ESP32 (Sensors & Devices)
// ============================================================
function updateStatus() {
    fetch('/proxy/status')
    .then(res => res.json())
    .then(data => {
        if(data.success && data.response) {
            try {
                let status = JSON.parse(data.response);
                
                // Cảm biến
                if (document.getElementById('temperature')) document.getElementById('temperature').innerText = (status.temperature !== null ? status.temperature : '--') + ' °C';
                if (document.getElementById('humidity')) document.getElementById('humidity').innerText = (status.humidity !== null ? status.humidity : '--') + ' %';
                if (document.getElementById('gas')) document.getElementById('gas').innerText = status.gas;
                if (document.getElementById('soil')) document.getElementById('soil').innerText = status.soil;
                
                // Trạng thái thiết bị
                if (document.getElementById('fan')) document.getElementById('fan').innerText = status.fan;
                if (document.getElementById('pump')) document.getElementById('pump').innerText = status.pump;
                if (document.getElementById('stair')) document.getElementById('stair').innerText = status.stair;
                if (document.getElementById('greenLed')) document.getElementById('greenLed').innerText = status.led_green;
                if (document.getElementById('redLed')) document.getElementById('redLed').innerText = status.led_red;
                if (document.getElementById('buzzer')) document.getElementById('buzzer').innerText = status.buzzer;
                if (document.getElementById('door')) document.getElementById('door').innerText = status.door;
                if (document.getElementById('oled')) document.getElementById('oled').innerText = status.oled;
                
                // Connection status
                if (document.getElementById('connection')) document.getElementById('connection').innerText = '✅ ESP32 Đang kết nối';
            } catch(e) {
                console.error('Lỗi parse JSON status:', e);
            }
        } else {
            if (document.getElementById('connection')) document.getElementById('connection').innerText = '❌ Mất kết nối ESP32';
        }
    })
    .catch(err => {
        if (document.getElementById('connection')) document.getElementById('connection').innerText = '❌ Lỗi mạng khi gọi ESP32';
    });
}

// Cập nhật mỗi 2 giây
setInterval(updateStatus, 2000);
