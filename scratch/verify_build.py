with open(r'D:\Jay\vscode\attech0824\index.html', encoding='utf-8') as f:
    text = f.read()

print("Comment count in index.html:", text.count("Tab: 技術專區"))
print("Has contact-success-state:", "contact-success-state" in text)
print("Has nav-technology:", "nav-technology" in text)
print("Has mobile-nav-technology:", "mobile-nav-technology" in text)

