import urllib.request
import re

url = 'http://localhost:3000/technology/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        print(f"Status Code: {resp.status}")
        print(f"Content Length: {len(content)} bytes")
except Exception as e:
    print(f"Request failed: {e}")
    exit(1)

products = [
    ("tech-tyzor", "鈦酸酯與鋯酸酯", True),
    ("tech-silane", "矽烷偶合劑", False),
    ("tech-chain", "擴鏈劑", False),
    ("tech-carbon-black", "特級碳黑", False),
    ("tech-wax", "微粉蠟", False),
    ("tech-matting", "消光粉", False),
    ("tech-maleic", "馬林酸樹脂", False),
    ("tech-adhesion", "密著樹脂", False),
    ("tech-powder", "粉體塗料專用助劑", False),
    ("tech-px", "PX 潤滑油添加劑", False),
    ("tech-polyester", "聚酯樹脂", False)
]

print("\n--- 檢查 11 大產品技術分頁 ---")
for pid, name, has_data in products:
    found_id = f'id="{pid}"' in content
    if has_data:
        # Check Tyzor 4 thumbnails
        has_imgs = ('catalyst.webp' in content and 'crosslinker.webp' in content and
                    'adhesion.webp' in content and 'surface_treatment.webp' in content)
        print(f"[{'PASS' if found_id and has_imgs else 'FAIL'}] {pid} ({name}): 錨點存在={found_id}, 4張圖完備={has_imgs}")
    else:
        # Check empty gallery state with "暫無資料"
        sec_match = re.search(rf'<section id="{pid}".*?</section>', content, re.DOTALL)
        if sec_match:
            sec_text = sec_match.group(0)
            has_no_data = "暫無資料" in sec_text
            has_card_title = "原廠技術圖解與機理展位" in sec_text
            print(f"[{'PASS' if has_no_data and has_card_title else 'FAIL'}] {pid} ({name}): 暫無資料標註={has_no_data}, 圖上方標題={has_card_title}")
        else:
            print(f"[FAIL] {pid} ({name}): Section not found")

print("\n--- 檢查全螢幕 Lightbox Modal ---")
has_modal = 'id="tech-image-modal"' in content
has_script = 'function openTechImageModal' in content
print(f"Modal 容器存在: {has_modal}")
print(f"Modal 控制腳本存在: {has_script}")

# Count total occurrences of "暫無資料"
no_data_count = content.count("暫無資料")
print(f"\n全頁『暫無資料』標籤數量: {no_data_count} (預期 10 個產品均包含)")
