import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the fan section manually
start_str = '''                    <div class="device-status">
                        Trạng thái:
                        <span id="fan">--</span>
                    </div>'''

end_str = '''                        <button
                            class="on"
                            onclick="sendCommand('/quat/on')">
                            BẬT
                        </button>'''

replacement = start_str + '''

                    <div class="buttons">

''' + end_str

# We can just regex replace everything between start_str and end_str
pattern = re.escape(start_str) + r'.*?' + re.escape(end_str)
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
