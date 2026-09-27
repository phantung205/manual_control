import requests

esp32_ip = "172.20.10.2"
led_state = None

def turn_on():
    global led_state

    # nếu đèn đã bật thì ko gửi request nữa
    if led_state == "on":
        return

    try:
        response = requests.get(f"http://{esp32_ip}/on",timeout=2)

        if response.ok:
            led_state = "on"
            print("ESP32: Đèn BẬT")

    except requests.RequestException as e:
        print("Không kết nối được ESP32:", e)

def turn_off():
    global led_state

    # Nếu đèn đã tắt thì không gửi request nữa
    if led_state == "off":
        return

    try:
        response = requests.get(f"http://{esp32_ip}/off",timeout=2)

        if response.ok:
            led_state = "off"
            print("ESP32: Đèn TẮT")

    except requests.RequestException as e:
        print("Không kết nối được ESP32:", e)
