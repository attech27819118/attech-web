import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = sys.argv[1] if len(sys.argv) > 1 else "20261014_v1"

print(f"==================================================")
print(f"🔧 全域快取破壞與版本同步工具 (ATTech Cache Buster)")
print(f"📌 目標版本號: {VERSION}")
print(f"==================================================")

META_TAGS = """    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">"""

# 1. 更新 js/state.js
state_js_path = os.path.join(ROOT_DIR, "js", "state.js")
if os.path.exists(state_js_path):
    with open(state_js_path, "r", encoding="utf-8") as f:
        s_code = f.read()
    s_code = re.sub(r"const APP_VERSION = '[^']*';", f"const APP_VERSION = '{VERSION}';", s_code)
    if "window.APP_VERSION" not in s_code:
        s_code = s_code.replace(f"const APP_VERSION = '{VERSION}';", f"const APP_VERSION = '{VERSION}';\nwindow.APP_VERSION = APP_VERSION;")
    with open(state_js_path, "w", encoding="utf-8") as f:
        f.write(s_code)
    print(f"✅ 已更新 js/state.js 中的 APP_VERSION = '{VERSION}'")

# 2. 更新 build_technology_subpages.py 中的 CACHE_VERSION
subpage_builder = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")
if os.path.exists(subpage_builder):
    with open(subpage_builder, "r", encoding="utf-8") as f:
        b_code = f.read()
    if "CACHE_VERSION =" in b_code:
        b_code = re.sub(r'CACHE_VERSION = "[^"]*"', f'CACHE_VERSION = "{VERSION}"', b_code)
    else:
        b_code = b_code.replace('DOMAIN = "https://www.attech.com.tw"', f'DOMAIN = "https://www.attech.com.tw"\nCACHE_VERSION = "{VERSION}"')
    
    # 確保正規表示式替換所有 js/*.js 與 css/*.css
    b_code = re.sub(r"js/technology\.js\?v=[^'\"]*", f"js/technology.js?v={VERSION}", b_code)
    b_code = re.sub(r"js/router\.js\?v=[^'\"]*", f"js/router.js?v={VERSION}", b_code)
    
    with open(subpage_builder, "w", encoding="utf-8") as f:
        f.write(b_code)
    print(f"✅ 已更新 scripts/build_technology_subpages.py 的版本常數與替換規則")

# 3. 遍歷專案中所有的 HTML 檔案
html_count = 0
meta_added_count = 0
exclude_dirs = {'.git', '.agents', 'node_modules', '__pycache__', 'dist', 'scratch'}

for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.lower().endswith('.html'):
            html_path = os.path.join(root, file)
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False

            # (A) 檢查並注入快取控制 meta tags
            if '<meta http-equiv="Cache-Control"' not in content and '<head>' in content:
                # 嘗試在 <meta name="viewport" ...> 下方插入
                vp_pattern = re.compile(r'(<meta\s+name=["\']viewport["\'][^>]*>)', re.IGNORECASE)
                if vp_pattern.search(content):
                    content = vp_pattern.sub(r'\1\n' + META_TAGS, content, count=1)
                    meta_added_count += 1
                    modified = True
                else:
                    head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
                    if head_pattern.search(content):
                        content = head_pattern.sub(r'\1\n' + META_TAGS, content, count=1)
                        meta_added_count += 1
                        modified = True

            # (B) 更新 CSS 版本號
            new_content = re.sub(r'(css/output\.css)\?v=[^"\'\s>]*', rf'\1?v={VERSION}', content)
            new_content = re.sub(r'(css/style\.css)\?v=[^"\'\s>]*', rf'\1?v={VERSION}', new_content)
            
            # (C) 更新所有 JS 版本號
            new_content = re.sub(r'(js/[a-zA-Z0-9_\-]+\.js)\?v=[^"\'\s>]*', rf'\1?v={VERSION}', new_content)

            if new_content != content:
                content = new_content
                modified = True

            if modified:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(content)
                html_count += 1

print(f"✅ 成功掃描並更新 {html_count} 個 HTML 檔案的資源版本號至 ?v={VERSION}")
print(f"✅ 成功為 {meta_added_count} 個 HTML 檔案注入防快取 HTTP 標頭 Meta Tags")
