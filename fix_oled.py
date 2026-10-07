import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_oled_pattern = r'(\s*)<div class="buttons">\s*<button\s*class="on"\s*onclick="sendCommand\(\'/oled/on\'\)">'

fixed_oled = r'''\1<!-- ========================= -->
\1<!-- OLED -->
\1<!-- ========================= -->
\1<div class="device">
\1    <div class="device-name">
\1        📺 Màn hình OLED
\1    </div>
\1    <div class="device-status">
\1        Trạng thái:
\1        <span id="oled\">--</span>
\1    </div>
\1    <div class="buttons">
\1        <button
\1            class="on"
\1            onclick="sendCommand('/oled/on')">'''

html = re.sub(bad_oled_pattern, fixed_oled, html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
