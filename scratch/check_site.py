import os, sys

test_path = r"D:\Jay\vscode\attech0824 - test\technology\tyzor\index.html"
with open(test_path, encoding="utf-8") as f:
    text = f.read()

print("Has contact-form-card:", "contact-form-card" in text)
print("Has tab-technology:", "tab-technology" in text)
print("Has tab-technology active:", 'id="tab-technology" class="tab-content active"' in text)
print("Has tab-about active:", 'id="tab-about" class="tab-content active"' in text)

