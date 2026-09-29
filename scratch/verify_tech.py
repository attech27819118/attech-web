with open('technology/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

anchors = [
    'tech-tyzor',
    'tech-silane',
    'tech-chain',
    'tech-carbon-black',
    'tech-wax',
    'tech-matting',
    'tech-maleic',
    'tech-adhesion',
    'tech-powder',
    'tech-px',
    'tech-polyester'
]

print("=== Checking technology/index.html ===")
for a in anchors:
    count = text.count(f'id="{a}"')
    print(f"  {a}: found {count} times")

print("\n=== Checking Tyzor images ===")
for img in ['catalyst.webp', 'crosslinker.webp', 'adhesion.webp', 'surface_treatment.webp']:
    print(f"  {img}: found {text.count(img)} times")

print("\n=== Checking Scripts ===")
print("  showTyzorPage:", 'function showTyzorPage' in text)
print("  openTechImageModal:", 'function openTechImageModal' in text)
print("  tech-image-modal element:", 'id="tech-image-modal"' in text)

print("\n=== Checking index.html ===")
with open('index.html', 'r', encoding='utf-8') as f2:
    text2 = f2.read()
for a in anchors:
    count = text2.count(f'id="{a}"')
    if count != 1:
        print(f"  WARNING in index.html for {a}: found {count}")
print("  index.html anchors all present:", all(text2.count(f'id="{a}"') == 1 for a in anchors))
print("  index.html tab-technology has 'active':", 'id="tab-technology" class="tab-content active"' in text2)
print("  technology/index.html tab-technology has 'active':", 'id="tab-technology" class="tab-content active"' in text)
