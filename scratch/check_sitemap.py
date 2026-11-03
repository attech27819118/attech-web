with open('sitemap.xml', encoding='utf-8') as f:
    text = f.read()

import re
locs = re.findall(r'<loc>(.*?)</loc>', text)
tech_locs = [l for l in locs if 'technology' in l]
print(f"Total URLs in sitemap: {len(locs)}")
print(f"Technology URLs in sitemap ({len(tech_locs)}):")
for tl in tech_locs:
    print(" ", tl)

