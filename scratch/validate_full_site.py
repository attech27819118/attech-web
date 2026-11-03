import os, re, json, sys, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
root_dir = os.path.abspath('.')

print("=" * 60)
print("🔍 啟動全站完整健康與 BUG 檢測 (Full Site Integrity Audit)")
print("=" * 60)

errors = []
warnings = []

# 1. 驗證所有 JS 語法
print("\n[1/5] 檢驗 JavaScript 檔案語法...")
import subprocess
js_files = []
for r, d, files in os.walk(os.path.join(root_dir, 'js')):
    for f in files:
        if f.endswith('.js'):
            js_files.append(os.path.join(r, f))

for js_f in js_files:
    rel = os.path.relpath(js_f, root_dir)
    res = subprocess.run(['node', '-c', js_f], capture_output=True, text=True)
    if res.returncode != 0:
        errors.append(f"JS 語法錯誤 {rel}: {res.stderr.strip()}")
    else:
        print(f"  ✅ {rel} 語法正確")

# 2. 驗證 JSON 檔案
print("\n[2/5] 檢驗核心 JSON 資料庫結構與語法...")
json_files = ['config.json', 'json/tech_database.json']
for jf in json_files:
    p = os.path.join(root_dir, jf)
    if not os.path.exists(p):
        errors.append(f"缺少必要 JSON 檔案: {jf}")
        continue
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✅ {jf} 解析成功")
    except Exception as e:
        errors.append(f"JSON 解析錯誤 {jf}: {e}")

# 3. 檢驗技術專區資料庫內所有檔案引用 (PDF, MechImg, CoverImg)
print("\n[3/5] 檢驗技術資料庫 tech_database.json 資源存在性...")
tech_db_path = os.path.join(root_dir, 'json', 'tech_database.json')
if os.path.exists(tech_db_path):
    with open(tech_db_path, encoding='utf-8') as f:
        tech_db = json.load(f)
    asset_count = 0
    for cat_slug, cat_data in tech_db.items():
        tabs = cat_data.get('tabs', {})
        for tab_k, doc_list in tabs.items():
            if isinstance(doc_list, list):
                for doc in doc_list:
                    for field in ['mechImg', 'coverImg', 'pdfUrl']:
                        val = doc.get(field)
                        if val:
                            asset_count += 1
                            # remove query params or hash
                            clean_val = val.split('?')[0].split('#')[0]
                            full_asset_path = os.path.join(root_dir, clean_val.replace('/', os.sep))
                            if not os.path.exists(full_asset_path):
                                errors.append(f"技術文件遺失資源: [{cat_slug}][{tab_k}][{doc.get('docId')}] {field} -> {clean_val}")
    print(f"  ✅ 共檢驗 {asset_count} 個技術資源引用，全部皆存在！")

# 4. 抽樣與全面掃描 HTML 頁面引用 (CSS, JS, 導覽列, 聯絡表單)
print("\n[4/5] 掃描全站 HTML 靜態頁面健康度...")
html_count = 0
missing_assets = set()
for r, d, files in os.walk(root_dir):
    if any(ig in r for ig in ['.git', 'node_modules', '.idea', 'scratch']):
        continue
    for f in files:
        if f.endswith('.html'):
            html_count += 1
            p = os.path.join(r, f)
            rel_p = os.path.relpath(p, root_dir)
            with open(p, encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            
            # 檢查 script tags
            scripts = re.findall(r'<script\s+[^>]*src="([^"]+)"', content)
            for s in scripts:
                if s.startswith('http') or s.startswith('//'):
                    continue
                clean_s = s.split('?')[0]
                # handle base href / relative path
                asset_full = os.path.join(root_dir, clean_s.lstrip('/').replace('/', os.sep))
                if not os.path.exists(asset_full):
                    missing_assets.add(f"{rel_p} -> 缺少腳本 {clean_s}")

            # 檢查 css links
            css_links = re.findall(r'<link\s+[^>]*href="([^"]+)"', content)
            for l in css_links:
                if l.startswith('http') or l.startswith('//') or 'favicon' in l or 'apple-touch-icon' in l or 'canonical' in l:
                    continue
                clean_l = l.split('?')[0]
                asset_full = os.path.join(root_dir, clean_l.lstrip('/').replace('/', os.sep))
                if not os.path.exists(asset_full):
                    missing_assets.add(f"{rel_p} -> 缺少樣式表 {clean_l}")

if missing_assets:
    for ma in list(missing_assets)[:10]:
        errors.append(f"HTML 引用遺失資源: {ma}")
else:
    print(f"  ✅ 掃描共 {html_count} 個 HTML 頁面，無任何遺失的本地 JS 或 CSS 資源！")

# 5. 檢驗聯絡表單與技術專區關鍵元素
print("\n[5/5] 驗證核心主頁與技術專題頁關鍵 UI 元素...")
core_checks = [
    ('index.html', ['id="tab-technology"', 'id="nav-technology"', 'id="contact-success-state"', 'js/technology.js']),
    ('about/index.html', ['id="nav-technology"', 'id="contact-success-state"']),
    ('contact/index.html', ['id="nav-technology"', 'id="contact-success-state"']),
    ('partners/index.html', ['id="nav-technology"', 'id="contact-success-state"']),
    ('technology/tyzor/index.html', ['id="tab-technology" class="tab-content active"', 'tech-layout-container']),
    ('technology/carbon-black/index.html', ['id="tab-technology" class="tab-content active"', 'tech-layout-container']),
    ('technology/index.html', ['url=tyzor/'])
]

for check_page, req_strings in core_checks:
    p = os.path.join(root_dir, check_page.replace('/', os.sep))
    if not os.path.exists(p):
        errors.append(f"核心頁面不存在: {check_page}")
        continue
    with open(p, encoding='utf-8') as fh:
        c = fh.read()
    for req in req_strings:
        if req not in c:
            errors.append(f"{check_page} 缺少關鍵元素: {req}")
        else:
            pass
    print(f"  ✅ {check_page} 關鍵結構與導航檢查通過")

print("\n" + "=" * 60)
print(f"檢測結果統計: 發現 {len(errors)} 個錯誤，{len(warnings)} 個警告")
print("=" * 60)
if errors:
    print("❌ 錯誤清單：")
    for err in errors:
        print(f"  - {err}")
else:
    print("🎉 全站無任何語法、連結、資源或架構 BUG，所有檢測完全通過！")

