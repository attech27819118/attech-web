with open(r'D:\Jay\vscode\attech0824 - test\index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="tab-technology"')
idx_next = text.find('id="tab-partners"')
print(text[idx:idx+1500])

