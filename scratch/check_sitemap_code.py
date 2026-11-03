import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('scripts/build_technology_subpages.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// 7. 更新 sitemap.xml')
print(text[idx:idx+1500])
