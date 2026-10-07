import re

with open('services/esp32_service.py', 'r', encoding='utf-8') as f:
    py = f.read()

# Update send_command to intercept quat/on and quat/off
old_send = '''def send_command(endpoint):
    try:
        response = requests.get(f"http://{esp32_ip}/{endpoint}", timeout=2)
        return response.ok, response.text
    except requests.RequestException as e:
        print(f"Lỗi kết nối {endpoint}:", e)
        return False, str(e)'''

new_send = '''def send_command(endpoint):
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
        return False, str(e)'''

py = py.replace(old_send, new_send)

# Also update the async functions for AI gesture
py = py.replace('send_request_async([f"http://{esp32_ip}/quat/on"])', 'send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/on"])')
py = py.replace('send_request_async([f"http://{esp32_ip}/quat/off"])', 'send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/off"])')

with open('services/esp32_service.py', 'w', encoding='utf-8') as f:
    f.write(py)
