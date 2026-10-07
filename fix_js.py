import re

with open('static/js/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove changeFanMode function
js = re.sub(r'function changeFanMode\(switchEl\).*?\}', '', js, flags=re.DOTALL)

# Remove fanSwitch sync logic
js = re.sub(r'// Đồng bộ Switch Mode \(Quạt\).*?if \(fanSwitch\) \{.*?\}', '', js, flags=re.DOTALL)

with open('static/js/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
