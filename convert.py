import pyperclip, sys

def convert_to_dict(text):
    lines = ['dict = {']
    for line in text.split('\n'):
        if line and not line.startswith('#'):
            line = line.lstrip('-').strip()
            r = line.split(' - ')
            if len(r) == 2:
                key, value = r
                lines.append(f"    '{key}': '{value}',")
    lines.append('}')
    lines = '\n'.join(lines)
    pyperclip.copy(lines)
    return lines

s = pyperclip.paste()
a = sys.argv[1] if len(sys.argv) > 1 else ''
r = convert_to_dict(a or s or '')
print(r)
