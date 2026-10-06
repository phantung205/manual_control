import requests

esp32_ip = "192.168.37.106"

# Quản lý trạng thái riêng biệt cho từng đèn
led_xanh_state = None
led_do_state = None

# ==================================
# ĐIỀU KHIỂN LED XANH
# ==================================
def turn_on_led_xanh():
    global led_xanh_state
    if led_xanh_state == "on":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/led_xanh/on", timeout=2)
        if response.ok:
            led_xanh_state = "on"
            print("ESP32: Đèn XANH đã BẬT")
    except requests.RequestException as e:
        print("Lỗi kết nối LED Xanh:", e)

def turn_off_led_xanh():
    global led_xanh_state
    if led_xanh_state == "off":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/led_xanh/off", timeout=2)
        if response.ok:
            led_xanh_state = "off"
            print("ESP32: Đèn XANH đã TẮT")
    except requests.RequestException as e:
        print("Lỗi kết nối LED Xanh:", e)

# ==================================
# ĐIỀU KHIỂN LED ĐỎ
# ==================================
def turn_on_led_do():
    global led_do_state
    if led_do_state == "on":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/led_do/on", timeout=2)
        if response.ok:
            led_do_state = "on"
            print("ESP32: Đèn ĐỎ đã BẬT (Cảnh báo!)")
    except requests.RequestException as e:
        print("Lỗi kết nối LED Đỏ:", e)

def turn_off_led_do():
    global led_do_state
    if led_do_state == "off":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/led_do/off", timeout=2)
        if response.ok:
            led_do_state = "off"
            print("ESP32: Đèn ĐỎ đã TẮT")
    except requests.RequestException as e:
        print("Lỗi kết nối LED Đỏ:", e)

# ==================================
# ĐIỀU KHIỂN QUẠT
# ==================================
quat_state = None
def turn_on_quat():
    global quat_state
    if quat_state == "on":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/quat/on", timeout=2)
        if response.ok:
            quat_state = "on"
            print("ESP32: QUẠT đã BẬT")
    except requests.RequestException as e:
        print("Lỗi kết nối Quạt:", e)

def turn_off_quat():
    global quat_state
    if quat_state == "off":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/quat/off", timeout=2)
        if response.ok:
            quat_state = "off"
            print("ESP32: QUẠT đã TẮT")
    except requests.RequestException as e:
        print("Lỗi kết nối Quạt:", e)

# ==================================
# ĐIỀU KHIỂN CỬA (SERVO)
# ==================================
cua_state = None
def open_cua():
    global cua_state
    if cua_state == "open":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/cua/open", timeout=2)
        if response.ok:
            cua_state = "open"
            print("ESP32: CỬA đã MỞ")
    except requests.RequestException as e:
        print("Lỗi kết nối Cửa:", e)

def close_cua():
    global cua_state
    if cua_state == "close":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/cua/close", timeout=2)
        if response.ok:
            cua_state = "close"
            print("ESP32: CỬA đã ĐÓNG")
    except requests.RequestException as e:
        print("Lỗi kết nối Cửa:", e)

# ==================================
# ĐIỀU KHIỂN MÁY BƠM
# ==================================
bom_state = None
def turn_on_pump():
    global bom_state
    if bom_state == "on":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/bom/on", timeout=2)
        if response.ok:
            bom_state = "on"
            print("ESP32: MÁY BƠM đã BẬT")
    except requests.RequestException as e:
        print("Lỗi kết nối Máy bơm:", e)

def turn_off_pump():
    global bom_state
    if bom_state == "off":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/bom/off", timeout=2)
        if response.ok:
            bom_state = "off"
            print("ESP32: MÁY BƠM đã TẮT")
    except requests.RequestException as e:
        print("Lỗi kết nối Máy bơm:", e)

# ==================================
# ĐIỀU KHIỂN CÒI (BUZZER)
# ==================================
coi_state = None
def turn_on_coi():
    global coi_state
    if coi_state == "on":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/coi/on", timeout=2)
        if response.ok:
            coi_state = "on"
            print("ESP32: CÒI đã BẬT")
    except requests.RequestException as e:
        print("Lỗi kết nối Còi:", e)

def turn_off_coi():
    global coi_state
    if coi_state == "off":
        return
    try:
        response = requests.get(f"http://{esp32_ip}/coi/off", timeout=2)
        if response.ok:
            coi_state = "off"
            print("ESP32: CÒI đã TẮT")
    except requests.RequestException as e:
        print("Lỗi kết nối Còi:", e)

# ==================================
# PROXY COMMAND CHO UI
# ==================================
def send_command(endpoint):
    try:
        response = requests.get(f"http://{esp32_ip}/{endpoint}", timeout=2)
        return response.ok, response.text
    except requests.RequestException as e:
        print(f"Lỗi kết nối {endpoint}:", e)
        return False, str(e)
