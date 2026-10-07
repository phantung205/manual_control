import requests
import threading
import time

esp32_ip = "172.20.10.2"

# Quản lý thời gian gửi lệnh cuối cùng để tránh spam (cooldown 3s)
last_command_time = {}

def send_request_async(urls):
    def task():
        for url in urls:
            try:
                requests.get(url, timeout=3)
            except Exception as e:
                print(f"Lỗi kết nối {url}:", e)
    threading.Thread(target=task).start()

def should_send(command_key):
    global last_command_time
    now = time.time()
    if command_key in last_command_time:
        if now - last_command_time[command_key] < 3.0:
            return False # Đang trong thời gian cooldown
    last_command_time[command_key] = now
    return True

# ==================================
# ĐIỀU KHIỂN LED XANH
# ==================================
def turn_on_led_xanh():
    if should_send('led_xanh_on'):
        print("ESP32: Gửi lệnh BẬT ĐÈN XANH")
        send_request_async([f"http://{esp32_ip}/led_xanh/on"])

def turn_off_led_xanh():
    if should_send('led_xanh_off'):
        print("ESP32: Gửi lệnh TẮT ĐÈN XANH")
        send_request_async([f"http://{esp32_ip}/led_xanh/off"])

# ==================================
# ĐIỀU KHIỂN LED ĐỎ
# ==================================
def turn_on_led_do():
    if should_send('led_do_on'):
        print("ESP32: Gửi lệnh BẬT ĐÈN ĐỎ")
        send_request_async([f"http://{esp32_ip}/led_do/on"])

def turn_off_led_do():
    if should_send('led_do_off'):
        print("ESP32: Gửi lệnh TẮT ĐÈN ĐỎ")
        send_request_async([f"http://{esp32_ip}/led_do/off"])

# ==================================
# ĐIỀU KHIỂN QUẠT (Ép sang MANUAL rồi mới BẬT/TẮT)
# ==================================
def turn_on_quat():
    if should_send('quat_on'):
        print("ESP32: Gửi lệnh BẬT QUẠT")
        send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/on"])

def turn_off_quat():
    if should_send('quat_off'):
        print("ESP32: Gửi lệnh TẮT QUẠT")
        send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/off"])

# ==================================
# ĐIỀU KHIỂN CỬA (SERVO)
# ==================================
def open_cua():
    if should_send('cua_open'):
        print("ESP32: Gửi lệnh MỞ CỬA")
        send_request_async([f"http://{esp32_ip}/cua/open"])

def close_cua():
    if should_send('cua_close'):
        print("ESP32: Gửi lệnh ĐÓNG CỬA")
        send_request_async([f"http://{esp32_ip}/cua/close"])

# ==================================
# ĐIỀU KHIỂN MÁY BƠM (Ép sang MANUAL rồi mới BẬT/TẮT)
# ==================================
def turn_on_pump():
    if should_send('pump_on'):
        print("ESP32: Gửi lệnh BẬT MÁY BƠM")
        send_request_async([f"http://{esp32_ip}/bom/on"])

def turn_off_pump():
    if should_send('pump_off'):
        print("ESP32: Gửi lệnh TẮT MÁY BƠM")
        send_request_async([f"http://{esp32_ip}/bom/off"])

# ==================================
# ĐIỀU KHIỂN CÒI (BUZZER)
# ==================================
def turn_on_coi():
    if should_send('coi_on'):
        print("ESP32: Gửi lệnh BẬT CÒI")
        send_request_async([f"http://{esp32_ip}/coi/on"])

def turn_off_coi():
    if should_send('coi_off'):
        print("ESP32: Gửi lệnh TẮT CÒI")
        send_request_async([f"http://{esp32_ip}/coi/off"])

# ==================================
# PROXY COMMAND CHO UI
# ==================================
def send_command(endpoint):
    try:
        # Tự động vô hiệu hóa AUTO của Quạt khi có bất kỳ lệnh bật/tắt quạt nào
        if endpoint in ["quat/on", "quat/off"]:
            try:
                requests.get(f"http://{esp32_ip}/quat/manual", timeout=2)
            except:
                pass
                
        response = requests.get(f"http://{esp32_ip}/{endpoint}", timeout=2)
        return response.ok, response.text
    except requests.RequestException as e:
        print(f"Lỗi kết nối {endpoint}:", e)
        return False, str(e)
