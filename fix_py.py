import re

with open('services/esp32_service.py', 'r', encoding='utf-8') as f:
    py = f.read()

py = py.replace('send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/on"])', 'send_request_async([f"http://{esp32_ip}/quat/on"])')
py = py.replace('send_request_async([f"http://{esp32_ip}/quat/manual", f"http://{esp32_ip}/quat/off"])', 'send_request_async([f"http://{esp32_ip}/quat/off"])')
py = py.replace('send_request_async([f"http://{esp32_ip}/bom/manual", f"http://{esp32_ip}/bom/on"])', 'send_request_async([f"http://{esp32_ip}/bom/on"])')
py = py.replace('send_request_async([f"http://{esp32_ip}/bom/manual", f"http://{esp32_ip}/bom/off"])', 'send_request_async([f"http://{esp32_ip}/bom/off"])')

with open('services/esp32_service.py', 'w', encoding='utf-8') as f:
    f.write(py)
