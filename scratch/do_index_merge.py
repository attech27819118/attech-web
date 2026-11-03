import re, sys

with open(r'D:\Jay\vscode\attech0824\index.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

with open(r'D:\Jay\vscode\attech0824 - test\index.html', 'r', encoding='utf-8') as f:
    test_html = f.read()

# 1. Nav technology block from test
nav_tech_match = re.search(r'(\s*<!-- 導覽列技術項目 \(包含 Mega Menu\) -->[\s\S]*?</div>\s*</div>)', test_html)
assert nav_tech_match, "Nav technology block not found"
nav_tech_block = nav_tech_match.group(1)

# 2. Mobile nav technology button from test
mobile_tech_match = re.search(r'(\s*<a href="technology/tyzor/" id="mobile-nav-technology"[\s\S]*?</a>)', test_html)
assert mobile_tech_match, "Mobile nav button not found"
mobile_tech_btn = mobile_tech_match.group(1)

# 3. tab-technology section from test (cleaned)
clean_test = re.sub(r'(\s*<!-- Tab: 技術專區[^\n]*-->)+', '\n    <!-- Tab: 技術專區 (Technology) - 獨立分頁一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->', test_html)
sec_tech_match = re.search(r'(<!-- Tab: 技術專區[\s\S]*?<section id="tab-technology"[\s\S]*?</section>)', clean_test)
assert sec_tech_match, "Tab technology section not found"
sec_tech_block = sec_tech_match.group(1)

# Ensure #tab-technology in index.html is inactive
sec_tech_block = sec_tech_block.replace('class="tab-content active"', 'class="tab-content"')

# Start modifying orig_html
html = orig_html

# A. Insert cache headers in head if not present
if '<meta http-equiv="Cache-Control"' not in html:
    cache_meta = '\n    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n    <meta http-equiv="Pragma" content="no-cache">\n    <meta http-equiv="Expires" content="0">'
    html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">', '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + cache_meta)

# B. Insert desktop nav-technology after products mega menu
# Find where products dropdown ends: the closing tag of "導覽列產品項目"
# In orig_html, look for the closing div of products container before "nav-partners"
prod_end_marker = 'id="nav-partners"'
idx_partners = html.find(prod_end_marker)
assert idx_partners != -1, "nav-partners not found"

# Insert nav_tech_block right before nav-partners
# Find the start of the <a> for nav-partners
idx_nav_partners_a = html.rfind('<a href="partners/"', 0, idx_partners)
assert idx_nav_partners_a != -1, "nav-partners <a> not found"
html = html[:idx_nav_partners_a] + nav_tech_block + '\n\n                    ' + html[idx_nav_partners_a:]

# C. Insert mobile nav button after mobile-nav-products
idx_mobile_prod = html.find('id="mobile-nav-products"')
assert idx_mobile_prod != -1, "mobile-nav-products not found"
idx_mobile_prod_close = html.find('</a>', idx_mobile_prod) + 4
html = html[:idx_mobile_prod_close] + mobile_tech_btn + html[idx_mobile_prod_close:]

# D. Insert tab-technology section before tab-partners
# Look for '<!-- Tab 3: 合作夥伴' or '<section id="tab-partners"'
idx_partners_sec = html.find('id="tab-partners"')
assert idx_partners_sec != -1, "tab-partners section not found"
idx_partners_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, idx_partners_sec)
if idx_partners_comment == -1:
    idx_partners_comment = html.rfind('<section id="tab-partners"', 0, idx_partners_sec)
html = html[:idx_partners_comment] + sec_tech_block + '\n\n        ' + html[idx_partners_comment:]

# E. Add footer link
# Look for footer links list
footer_partners_idx = html.find('href="partners/" class="hover:text-blue-900 hover:underline">')
if footer_partners_idx != -1:
    # find closing </a> or </li>
    close_a = html.find('</a>', footer_partners_idx) + 4
    tech_footer_link = ' | <a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>'
    html = html[:close_a] + tech_footer_link + html[close_a:]

# F. Add script tags before app.js
if 'js/technology.js' not in html:
    app_script_idx = html.find('<script src="js/app.js')
    assert app_script_idx != -1, "app.js script tag not found"
    tech_scripts = '<script src="js/vendor/pdf.min.js"></script>\n<script src="js/technology.js?v=20261103_v1"></script>\n'
    html = html[:app_script_idx] + tech_scripts + html[app_script_idx:]

# Update CSS & JS version tags
html = re.sub(r'css/output\.css\?v=[^"]*', 'css/output.css?v=20261103_v1', html)
html = re.sub(r'css/style\.css\?v=[^"]*', 'css/style.css?v=20261103_v1', html)
html = re.sub(r'js/([^"]+?\.js)\?v=[^"]*', r'js/\1?v=20261103_v1', html)

# Verify key elements
print("=== VERIFICATION ===")
print("Has contact-success-state:", "contact-success-state" in html)
print("Has nav-technology:", "nav-technology" in html)
print("Has mobile-nav-technology:", "mobile-nav-technology" in html)
print("Has tab-technology:", "tab-technology" in html)
print("Has pdf.min.js:", "pdf.min.js" in html)
print("Has technology.js:", "technology.js" in html)
print("Tab technology comment count:", html.count("Tab: 技術專區"))

with open(r'D:\Jay\vscode\attech0824\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated!")

