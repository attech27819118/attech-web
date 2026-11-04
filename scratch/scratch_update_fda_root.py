# -*- coding: utf-8 -*-
"""
腳本名稱: scratch_update_fda_root.py
功能說明:
1. 依據 FDA COMPLIANCE 文件判定各產品是否符合 21 CFR 175.300 與 21 CFR 176.170。
2. 於 mpiall.json 產品根層級寫入:
   - "fda_compliant": True / False
   - "fda_regulations": ["21 CFR 175.300", "21 CFR 176.170"] (符合者) 或 [] (不符合者)
3. 確保 applications_data 內的 featured_categories 保持純淨功能分類（若有殘留 FDA 標籤一併清理）。
"""

import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), 'json', 'mpi', 'mpiall.json')

# 不符合 FDA 21 CFR 175.300 與 176.170 之產品清單 (原廠表列 No)
NON_COMPLIANT_PRODUCTS = {
    'Micropro 440W',
    'MicroTex 950',
    'MicroTex 975'
}

STANDARD_FDA_REGS = [
    "21 CFR 175.300",
    "21 CFR 176.170"
]

def update_fda_status():
    if not os.path.exists(FILE_PATH):
        print(f"錯誤: 找不到檔案 {FILE_PATH}")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    compliant_count = 0
    non_compliant_count = 0
    cleaned_tags_count = 0

    for p in products:
        name = p.get('product_name', '')
        
        # 1. 設定根層級 FDA 狀態
        if name in NON_COMPLIANT_PRODUCTS:
            p['fda_compliant'] = False
            p['fda_regulations'] = []
            non_compliant_count += 1
        else:
            p['fda_compliant'] = True
            p['fda_regulations'] = list(STANDARD_FDA_REGS)
            compliant_count += 1

        # 2. 清理 applications_data 中的 featured_categories，避免重複標籤
        apps_data = p.get('applications_data', {})
        for app_key, app_obj in apps_data.items():
            if isinstance(app_obj, dict) and 'featured_categories' in app_obj:
                fc = app_obj['featured_categories']
                if 'FDA' in fc:
                    app_obj['featured_categories'] = [c for c in fc if c != 'FDA']
                    cleaned_tags_count += 1

    # 存檔回 mpiall.json
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print("========================================")
    print("mpiall.json FDA 屬性更新成功！")
    print(f"總產品數: {len(products)}")
    print(f"符合 FDA 產品數: {compliant_count} (已標記 fda_compliant = True)")
    print(f"非符合 FDA 產品數: {non_compliant_count} (已標記 fda_compliant = False)")
    if cleaned_tags_count > 0:
        print(f"清理 featured_categories 內殘留 FDA 標籤: {cleaned_tags_count} 處")
    print("========================================")

if __name__ == '__main__':
    update_fda_status()
