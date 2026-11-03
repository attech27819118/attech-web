with open('sitemap.xml', encoding='utf-8') as f:
    text = f.read()

print("Contains about:", "about" in text)
import re
print("First 5 locs:", re.findall(r'<loc>(.*?)</loc>', text)[:5])

