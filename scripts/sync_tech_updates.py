# -*- coding: utf-8 -*-
"""
ATTech 技術專區 - 一鍵全自動同步與建置腳本 (One-Click Master Sync & Build)

【一鍵全流程同步】
1. [萃取] 讀取 techdatadb/技術文件摘要與重點.md 生成最新 json/tech_database.json
2. [同步] 自動同步更新資料庫至前端 js/technology.js（只增不減，智慧保留圖表與設定）
3. [編譯] 生成 11 大獨立技術靜態網頁 (technology/{slug}/index.html)
4. [入口] 同步更新根目錄首頁 index.html 與 sitemap.xml

★ 修改完 techdatadb/技術文件摘要與重點.md，直接執行本腳本即可全站同步！
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

def sync_and_build():
    md_file = os.path.join(ROOT_DIR, 'techdatadb', '技術文件摘要與重點.md')
    
    # 步驟 1：若存在技術文件 Markdown，自動萃取並同步至 JS 與 JSON
    if os.path.exists(md_file) and "--skip-md" not in sys.argv:
        print("📦 [1/2] 從 techdatadb/技術文件摘要與重點.md 萃取最新資料庫並同步至 JS...", flush=True)
        from build_tech_json import build_database_from_md
        build_database_from_md()
        sys.stdout.flush()

    # 步驟 2：執行靜態子頁面與首頁編譯
    print("🚀 [2/2] 開始編譯 11 大獨立技術靜態網頁與首頁...", flush=True)
    js_builder = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.js")
    if os.path.exists(js_builder):
        res = subprocess.run(["node", js_builder], cwd=ROOT_DIR)
        if res.returncode != 0:
            print(f"❌ 建置失敗 (Node.js 結束代碼: {res.returncode})", file=sys.stderr)
            sys.exit(res.returncode)
    else:
        from build_technology_subpages import build_all
        build_all()

if __name__ == '__main__':
    sync_and_build()


