with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('id="oled\\"', 'id="oled"')

# Let's also clean up the huge amounts of empty lines.
import re
html = re.sub(r'\n\s*\n\s*\n+', '\n\n', html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
