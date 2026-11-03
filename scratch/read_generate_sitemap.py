import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('scripts/generate_sitemap.js', encoding='utf-8') as f:
    print(f.read())

