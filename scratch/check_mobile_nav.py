with open(r'D:\Jay\vscode\attech0824 - test\index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('mobile-nav')
print(text[idx-50:idx+1500])

