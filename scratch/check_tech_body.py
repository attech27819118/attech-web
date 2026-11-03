with open('js/technology.js', encoding='utf-8') as f:
    text = f.read()

for i, line in enumerate(text.splitlines()):
    if 'document.body' in line:
        print(f"Line {i+1}: {line}")

