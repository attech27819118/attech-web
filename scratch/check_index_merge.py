import re

with open(r'D:\Jay\vscode\attech0824\index.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

with open(r'D:\Jay\vscode\attech0824 - test\index.html', 'r', encoding='utf-8') as f:
    test_html = f.read()

print("Orig has contact-success-state:", "contact-success-state" in orig_html)
print("Orig has nav-technology:", "nav-technology" in orig_html)

# 1. Extract Mega Menu & nav-technology from test_html
nav_tech_match = re.search(r'(\s*<!-- 導覽列技術項目 \(包含 Mega Menu\) -->[\s\S]*?</div>\s*</div>)', test_html)
if nav_tech_match:
    print("Found nav-technology block, length:", len(nav_tech_match.group(1)))
else:
    print("WARNING: nav-technology block NOT found in test_html")

# 2. Extract mobile nav technology button
mobile_tech_match = re.search(r'(\s*<a href="technology/tyzor/" id="mobile-nav-technology"[\s\S]*?</a>)', test_html)
if mobile_tech_match:
    print("Found mobile-nav-technology, length:", len(mobile_tech_match.group(1)))
else:
    print("WARNING: mobile-nav-technology NOT found in test_html")

# 3. Extract tab-technology section
# In test_html, clean out duplicate comments first
clean_test = re.sub(r'(\s*<!-- Tab: 技術專區[^\n]*-->)+', '\n    <!-- Tab: 技術專區 (Technology) - 獨立分頁一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->', test_html)
sec_tech_match = re.search(r'(<!-- Tab: 技術專區[\s\S]*?<section id="tab-technology"[\s\S]*?</section>)', clean_test)
if sec_tech_match:
    print("Found tab-technology section, length:", len(sec_tech_match.group(1)))
else:
    print("WARNING: tab-technology section NOT found")

# 4. Extract footer link
footer_tech_match = re.search(r'(<li><a href="technology/tyzor/"[^>]*>技術專區</a></li>|<a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>)', test_html)
if footer_tech_match:
    print("Found footer tech match:", footer_tech_match.group(0))

