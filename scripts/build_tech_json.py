# -*- coding: utf-8 -*-
"""
Generate complete structured tech_database.json from techdatadb/技術文件摘要與重點.md
Extracted and curated strictly from techdatadb files: rich, specific data, professional parameters,
zero hallucination, following the ATTech 5-dimension standard.
"""

import os
import sys
import re
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TECH_ROOT = os.path.join(ROOT_DIR, 'techdatadb')
MD_FILE = os.path.join(TECH_ROOT, '技術文件摘要與重點.md')

CATEGORIES_META = {
    "tyzor": {
        "slug": "tyzor",
        "hasData": True,
        "brand": "Dorf Ketal",
        "name": "Organic Titanates and Zirconates",
        "sub": "鈦酸酯與鋯酸酯, Tyzor",
        "productLink": "products/dorfketal/tyzor/",
        "titleZh": "鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®)"
    },
    "carbon-black": {
        "slug": "carbon-black",
        "hasData": True,
        "brand": "Orion",
        "name": "Special Carbon Black",
        "sub": "特級碳黑 / 導電碳黑",
        "productLink": "products/orion/coating/",
        "titleZh": "特級碳黑技術應用 (Carbon Black)"
    },
    "maleic": {
        "slug": "maleic",
        "hasData": False,
        "brand": "其他特化",
        "name": "Maleic Resin / 馬林酸樹脂",
        "sub": "松香改性馬林酸樹脂",
        "productLink": "products/others/maleic_acid_resin/",
        "titleZh": "馬林酸樹脂技術應用 (Maleic Resin)"
    },
    "px": {
        "slug": "px",
        "hasData": False,
        "brand": "Dorf Ketal",
        "name": "PX Lubricant Additives",
        "sub": "潤滑油添加劑 (原 ExxonMobil)",
        "productLink": "products/dorfketal/px/",
        "titleZh": "PX 潤滑油添加劑技術應用 (PX Lubricants)"
    },
    "silane": {
        "slug": "silane",
        "hasData": False,
        "brand": "Evonik / 特化",
        "name": "Silane / 矽烷偶合劑",
        "sub": "Dynasylan / hydrosil 系列",
        "productLink": "products/others/silane/",
        "titleZh": "矽烷偶合劑系列技術應用 (Silane)"
    },
    "wax": {
        "slug": "wax",
        "hasData": True,
        "brand": "Micro Powders",
        "name": "Micronized Wax / 微粉蠟",
        "sub": "PTFE 取代 / 耐磨耐刮助劑",
        "productLink": "products/mpi/ptfe/",
        "titleZh": "微粉化蠟技術應用 (Micronized Wax)"
    },
    "adhesion": {
        "slug": "adhesion",
        "hasData": False,
        "brand": "其他特化",
        "name": "Adhesion Resin / 密著樹脂",
        "sub": "氯化聚烯烴 (CPO) & 非氯系",
        "productLink": "products/others/adhesion_promoter/",
        "titleZh": "密著樹脂技術應用 (Adhesion Resin)"
    },
    "polyester": {
        "slug": "polyester",
        "hasData": False,
        "brand": "其他特化",
        "name": "Polyester Resin / 飽和聚酯樹脂",
        "sub": "卷材 / 烤漆 / 防腐樹脂",
        "productLink": "products/others/polyester_resin/",
        "titleZh": "飽和聚酯樹脂技術應用 (Polyester Resin)"
    },
    "chain": {
        "slug": "chain",
        "hasData": True,
        "brand": "Dorf Ketal",
        "name": "Chain Extender / 擴鏈劑",
        "sub": "Unilink & Clearlink 系列",
        "productLink": "products/dorfketal/chain/",
        "titleZh": "擴鏈劑技術應用 (Chain Extender)"
    },
    "matting": {
        "slug": "matting",
        "hasData": True,
        "brand": "其他特化",
        "name": "Matting Agent / 消光粉",
        "sub": "二氧化矽 / 表面處理消光",
        "productLink": "products/others/matting_agent/",
        "titleZh": "消光粉技術應用 (Matting Agent)"
    },
    "powder": {
        "slug": "powder",
        "hasData": False,
        "brand": "其他特化",
        "name": "Powder Coating Additive",
        "sub": "粉體塗料專用功能性助劑",
        "productLink": "products/others/coating_additive/",
        "titleZh": "粉體塗料專用助劑技術應用 (Powder Additives)"
    }
}

def classify_doc(path, fn):
    """
    依據檔案路徑與檔名判定 slug 與所屬維度 tab_key
    """
    clean_p = path.replace(chr(96), '').strip().replace(chr(92), '/')
    parts = clean_p.split('/')
    top = parts[0]
    sub = parts[1] if len(parts) > 1 else ''

    slug_map = {
        '2.Tyzor': 'tyzor',
        '3.unilink': 'chain',
        '4.Orion': 'carbon-black',
        '5. MPI': 'wax',
        '7.Matting Agent': 'matting'
    }
    slug = slug_map.get(top, 'unknown')

    if 'Formulation Guide' in fn or 'Formulation' in sub:
        tab = 'formulation'
    elif '1.原理' in sub:
        tab = 'principles'
    elif '2.' in sub or 'Brochure' in sub or '目錄' in sub:
        tab = 'catalog'
    elif '3.' in sub or 'Application Note' in sub:
        tab = 'applications'
    elif '4.' in sub or '單一產品' in sub:
        tab = 'single'
    else:
        tab = 'applications'

    return slug, tab, clean_p

def determine_labels_and_meta(slug, tab, fn, title, origin, clean_p=""):
    """
    生成短標籤 (shortLabel)、語言、版本、群組 (productGroup) 等中繼資訊
    """
    lang = "EN (英文)"
    if " CN" in f" {fn} " or fn.endswith(" CN") or fn.endswith("(中)") or "（中文版）" in title:
        lang = "CN (簡體中文)"
    elif " TW" in f" {fn} " or fn.endswith(" TW") or "(繁)" in title or "（繁體中文）" in title:
        lang = "TW (繁體中文)"
    elif any('\u4e00' <= c <= '\u9fff' for c in fn):
        lang = "TW (繁體中文)"

    version = "原廠發行版"
    for yr in ["202608", "202607", "202602", "202512", "202504", "202412", "202407", "202208", "201707", "2026", "2025", "2024", "2022", "2020"]:
        if yr in fn or yr in origin:
            version = yr
            break

    doc_type_map = {
        "principles": "原理機制",
        "catalog": "Brochure 總覽型錄",
        "applications": "Application Note 應用技術手冊",
        "single": "I 單一產品技術資料",
        "formulation": "Formulation 配方指南"
    }

    short_label = title
    product_group = "其他產品技術"
    mech_img = None

    # ==========================
    # 1. TYZOR
    # ==========================
    if slug == "tyzor":
        if tab == "principles":
            if "交聯劑" in fn or "交聯劑" in title:
                short_label = "作為交聯劑"
                mech_img = "techdatadb/2.Tyzor/1.原理/crosslinker.webp"
            elif "催化劑" in fn or "催化劑" in title:
                short_label = "作為催化劑"
                mech_img = "techdatadb/2.Tyzor/1.原理/catalyst.webp"
            elif "表面改性" in fn or "表面改性" in title:
                short_label = "作為表面改性"
                mech_img = "techdatadb/2.Tyzor/1.原理/surface_treatment.webp"
            elif "附著力" in fn or "附著力" in title:
                short_label = "作為附著力促進劑"
                mech_img = "techdatadb/2.Tyzor/1.原理/adhesion.webp"
        elif tab == "catalog":
            if "Adhesive Plus Coatings" in fn:
                short_label = "膠黏劑與密封膠"
            elif "Polyols Polymers" in fn:
                short_label = "多元醇聚合物"
            elif "General CN" in fn:
                short_label = "綜合手冊 (中)"
            elif "Plus Coatings" in fn:
                short_label = "塗料專用型錄"
        elif tab == "applications":
            app_short_map = {
                "Adhesives Sealants": "膠黏與密封膠",
                "Bulk Handling": "大宗儲運規範",
                "Catalyst Plasticizer": "可塑劑生產催化",
                "Crosslinking for Paper": "紙張塗佈交聯",
                "Direct Esterification": "直接酯化反應",
                "Ferrous and Nonferrous": "金屬表面前處理",
                "Glass Surface Coatings": "玻璃表面塗層",
                "Inorganic Filler": "無機填料改質",
                "Surface Primers": "底塗促進劑",
                "Thawing Frozen": "TPT 解凍操作",
                "Transesterification": "酯交換反應",
                "Vapor Pressure": "蒸氣壓曲線手冊"
            }
            for k, sl in app_short_map.items():
                if k in fn:
                    short_label = sl
                    break
        elif tab == "single":
            if "Activate 422 Plastic Packaging" in fn:
                short_label = "Activate 422 食品接觸"
                product_group = "Activate 專利耐水解系列"
            elif "Activate 422 for PET" in fn:
                short_label = "Activate 422 瓶級聚酯"
                product_group = "Activate 專利耐水解系列"
            elif "IAM for Ink" in fn:
                short_label = "IAM 印刷油墨"
                product_group = "IAM 油墨無黃變系列"
            elif "IAM for Solvent-Based" in fn:
                short_label = "IAM 溶劑型油墨"
                product_group = "IAM 油墨無黃變系列"

    # ==========================
    # 2. CHAIN (UNILINK / CLEARLINK)
    # ==========================
    elif slug == "chain":
        if tab == "catalog":
            short_label = "Unilink & Clearlink 型錄"
        elif tab == "single":
            if "Clearlink 1000" in fn:
                short_label = "Clearlink 1000 聚脲塗層"
                product_group = "Clearlink 耐候脂肪族系列"
            elif "Unilink 1030" in fn:
                short_label = "Unilink 1030 澆注彈性體"
                product_group = "Unilink 催化系統"
            elif "Foams" in fn:
                short_label = "Unilink 4200 軟質泡棉"
                product_group = "Unilink 芳香族擴鏈劑系列"
            elif "Elastomeric Coatings" in fn:
                short_label = "Unilink 4200 彈性體塗層"
                product_group = "Unilink 芳香族擴鏈劑系列"

    # ==========================
    # 3. CARBON BLACK (ORION)
    # ==========================
    elif slug == "carbon-black":
        if tab == "principles":
            if "平均原生粒徑" in title or "平均原生粒徑" in origin:
                short_label = "平均原生粒徑"
                mech_img = "techdatadb/4.Orion/1.原理/particle size.png"
            elif "結構" in title or "結構" in origin:
                short_label = "結構"
                mech_img = "techdatadb/4.Orion/1.原理/property comparison chart.png"
            elif "表面處理" in title or "表面處理" in origin:
                short_label = "表面處理"
                mech_img = "techdatadb/4.Orion/1.原理/processes_comparison.png"
            elif "製程差異" in title or "製程差異" in origin:
                short_label = "製程差異"
                mech_img = "techdatadb/4.Orion/1.原理/processes_comparison.png"
        elif tab == "catalog":
            if "CN" in fn:
                short_label = "特種碳黑型錄 (中)"
            else:
                short_label = "特種碳黑型錄 (英)"
        elif tab == "applications":
            cb_app_map = {
                "Fastness": "碳黑堅牢度 (TI 1460)",
                "Handling": "碳黑安全裝卸 (TI 1451)",
                "Modern Coatings": "現代塗料系統 (0402)",
                "Fibers": "纖維紡絲碳黑 (TI 1377)",
                "Disperse Guideline": "潤濕分散指引 (TI 1375)",
                "Industrial Coatings": "工業防護塗料 (TI 1458)",
                "Inkjet": "數位噴墨油墨 (TI 1482)",
                "Powder Coatings": "粉體塗料碳黑 (TI 1456)",
                "Printing Inks": "包裝印刷油墨 (TI 1452)",
                "Tinting Coating": "調色塗料碳黑 (TI 1459)",
                "Food Package": "食品包裝油墨 (TI 1453)",
                "Low PAHS": "低 PAHs 環保碳黑 (TI 1483)"
            }
            for k, sl in cb_app_map.items():
                if k in fn:
                    short_label = sl
                    break
        elif tab == "single":
            if "CN" in fn:
                short_label = "FW 310 超高黑度碳黑在水性及油性塗料中應用(中文版)"
            else:
                short_label = "FW 310 超高黑度碳黑在水性及油性塗料中應用(英文版)"
            product_group = "Colour Black 超高色素氣黑系列"

    # ==========================
    # 4. WAX (MICRO POWDERS)
    # ==========================
    elif slug == "wax":
        if tab == "principles":
            if "作用原理" in title:
                short_label = "作用原理"
                mech_img = "techdatadb/5. MPI/1.原理/作用原理.png"
            elif "品種及功能" in title:
                short_label = "微粉蠟品種及功能"
                mech_img = "techdatadb/5. MPI/1.原理/指標.png"
            elif "粒徑" in title:
                short_label = "粒徑及粒徑分布"
            elif "分散性" in title:
                short_label = "分散性及應用方便性"
            elif "熔點" in title:
                short_label = "熔點對其表面性能的影響"
            elif "極性" in title:
                short_label = "極性對其表面性能的影響"
        elif tab == "catalog":
            if "PTFE Alternatives" in fn:
                short_label = "PTFE 無氟替代指南"
            elif "Specialty Wax Additives" in fn:
                short_label = "微粉蠟產品目錄總覽"
        elif tab == "applications":
            wax_app_map = {
                "Advanced Composite": "先進複合材料 (PFAS-Free)",
                "How to Disperse": "微粉蠟高效分散指引",
                "MicroTouch": "MicroTouch 觸感助劑",
                "Can Container": "罐頭金屬塗層選用",
                "Energy Curable": "UV/EB 固化塗料油墨",
                "Industrial Coatings": "工業塗料選用指南",
                "Industrial Flooring": "工業地坪耐磨塗料",
                "Powder Coatings": "粉體塗料選用指南",
                "Printing Inks": "印刷油墨抗耐磨",
                "WoodCoatings": "木器傢俱塗料",
                "Architectural Coatings": "建築裝飾塗料"
            }
            for k, sl in wax_app_map.items():
                if k in fn:
                    short_label = sl
                    break
        elif tab == "formulation":
            short_label = "MicroTouch 觸感起始配方"
        elif tab == "single":
            if "PolyGlide" in fn:
                short_label = "PolyGlide 1226XF"
                product_group = "PolyGlide 超滑無氟系列"
            elif "PropylMatte 31 HD" in fn:
                short_label = "PropylMatte 31 HD"
                product_group = "PropylMatte / AquaMatte 啞光系列"
            elif "MicroKlear" in fn:
                short_label = "MicroKlear 418AL"
                product_group = "MicroKlear 棕櫚蠟複合系列"
            elif "MicroMatte 1415-EZ" in fn:
                short_label = "MicroMatte 1415-EZ"
                product_group = "MicroMatte 易分散消光系列"
            elif "MPP-611AL" in fn:
                short_label = "MPP-611AL 氧化鋁耐磨"
                product_group = "MPP 聚乙烯氧化鋁複合系列"
            elif "PolyTuf" in fn:
                short_label = "PolyTuf 1229 耐磨衝擊"
                product_group = "PolyTuf 抗衝擊高韌性系列"
            elif "AquaMatte and PropylMatte" in fn:
                short_label = "AquaMatte 水性消光"
                product_group = "PropylMatte / AquaMatte 啞光系列"
            elif "Superslip" in fn:
                short_label = "Superslip 6515AL 超滑爽"
                product_group = "Superslip 超滑爽耐磨系列"
            elif "Polyfluo 190" in fn:
                short_label = "Polyfluo 190 / Fluo 300"
                product_group = "Polyfluo / Fluo 微粉系列"
            elif "MicroTex" in fn:
                short_label = "MicroTex 950 紋理防滑"
                product_group = "MicroTex 砂紋紋理助劑系列"
            elif "MP 22 MP 620F MP 635F" in fn:
                if "MP 22 VF" in clean_p:
                    short_label = "MP-22 VF 油墨耐磨"
                    product_group = "MP-22 合成費托微粉系列"
                elif "MP-22XF" in clean_p:
                    short_label = "MP-22XF 薄膜耐磨"
                    product_group = "MP-22 合成費托微粉系列"
                elif "MPP-620F" in clean_p:
                    short_label = "MPP-620F 油墨耐磨"
                    product_group = "MPP 高耐磨聚乙烯系列"
                elif "MPP-620XF" in clean_p:
                    short_label = "MPP-620XF 超細耐磨"
                    product_group = "MPP 高耐磨聚乙烯系列"
                elif "MPP-635VF" in clean_p:
                    short_label = "MPP-635VF 高分子量耐磨"
                    product_group = "MPP 高耐磨聚乙烯系列"
                else:
                    short_label = "MPP 耐摩擦試驗研究"
                    product_group = "MPP 高耐磨聚乙烯系列"

    # ==========================
    # 5. MATTING (二氧化矽消光粉)
    # ==========================
    elif slug == "matting":
        if tab == "principles":
            if "消光原理" in title:
                short_label = "消光原理"
                mech_img = "techdatadb/7.Matting Agent/1.原理/消光原理.png"
            elif "平均粒徑" in title:
                short_label = "平均粒徑"
                mech_img = "techdatadb/7.Matting Agent/1.原理/Average Particle Size.png"
            elif "表面處理" in title:
                short_label = "表面處理"
                mech_img = "techdatadb/7.Matting Agent/1.原理/表面處理.png"
            elif "孔隙率" in title:
                short_label = "孔隙率"
                mech_img = "techdatadb/7.Matting Agent/1.原理/孔隙率.png"
            elif "膜厚" in title:
                short_label = "膜厚"
                mech_img = "techdatadb/7.Matting Agent/1.原理/膜厚.png"
            elif "樹脂系統" in title:
                short_label = "樹脂系統"

    return {
        "lang": lang,
        "version": version,
        "docType": doc_type_map.get(tab, "技術資料"),
        "shortLabel": short_label,
        "productGroup": product_group,
        "mechImg": mech_img
    }

def clean_wrapped_text(text):
    """
    清理因編輯器自動折行 (Line Wrap) 造成的換行與縮排，智能保持單詞間距
    """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return ""
    result = lines[0]
    for nxt in lines[1:]:
        if re.search(r'[a-zA-Z0-9]$', result) and re.search(r'^[a-zA-Z0-9]', nxt):
            result += ' ' + nxt
        else:
            result += nxt
    return result

def load_existing_images():
    """
    從現有 js/technology.js 或 json/tech_database.json 中提取手動設定的 mechImg，
    建立映射表以便在新資料萃取時完整繼承保留，絕不覆蓋手動新增的圖片網址。
    """
    existing_imgs = {}

    # 1. 優先從 js/technology.js 讀取
    js_path = os.path.join(ROOT_DIR, 'js', 'technology.js')
    if os.path.exists(js_path):
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                js_code = f.read()
            start_marker = 'const TECH_DATABASE = {'
            start_idx = js_code.find(start_marker)
            if start_idx != -1:
                end_marker = 'const TechState = {'
                end_idx = js_code.find(end_marker, start_idx)
                if end_idx != -1:
                    raw_json = js_code[start_idx + len('const TECH_DATABASE = '):end_idx].strip().rstrip(';')
                    db = json.loads(raw_json)
                    for slug, v in db.items():
                        for tab, docs in v.get('tabs', {}).items():
                            for d in docs:
                                img = d.get('mechImg')
                                if img:
                                    if d.get('shortLabel'):
                                        existing_imgs[f"{slug}:{tab}:lbl:{d['shortLabel']}"] = img
                                    if d.get('title'):
                                        existing_imgs[f"{slug}:{tab}:title:{d['title']}"] = img
                                    if d.get('docId'):
                                        existing_imgs[f"{slug}:{tab}:id:{d['docId']}"] = img
        except Exception as e:
            print(f"⚠️ 讀取現有 JS 圖片失敗: {e}")

    # 2. 若 JSON 有現存資料也補充載入
    json_path = os.path.join(ROOT_DIR, 'json', 'tech_database.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
            for slug, v in db.items():
                for tab, docs in v.get('tabs', {}).items():
                    for d in docs:
                        img = d.get('mechImg')
                        if img:
                            k_lbl = f"{slug}:{tab}:lbl:{d.get('shortLabel')}"
                            if k_lbl not in existing_imgs and d.get('shortLabel'):
                                existing_imgs[k_lbl] = img
                            k_title = f"{slug}:{tab}:title:{d.get('title')}"
                            if k_title not in existing_imgs and d.get('title'):
                                existing_imgs[k_title] = img
                            k_id = f"{slug}:{tab}:id:{d.get('docId')}"
                            if k_id not in existing_imgs and d.get('docId'):
                                existing_imgs[k_id] = img
        except Exception as e:
            pass

    return existing_imgs

def sync_to_technology_js(database):
    """
    同步更新 js/technology.js 中的 const TECH_DATABASE = { ... };
    確保前後端與備份 JSON 保持完全一致
    """
    js_path = os.path.join(ROOT_DIR, 'js', 'technology.js')
    if not os.path.exists(js_path):
        return

    with open(js_path, 'r', encoding='utf-8') as f:
        js_code = f.read()

    db_json_str = json.dumps(database, ensure_ascii=False, indent=2)
    new_db_decl = f"const TECH_DATABASE = {db_json_str};\n"

    start_marker = "const TECH_DATABASE = {"
    start_idx = js_code.find(start_marker)
    if start_idx != -1:
        end_marker = "const TechState = {"
        end_idx = js_code.find(end_marker, start_idx)
        if end_idx != -1:
            js_code = js_code[:start_idx] + new_db_decl + js_code[end_idx:]
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_code)
            print("  [SYNC] ✅ 已同步更新最新資料庫至 js/technology.js！")

def build_database_from_md():
    database = {}
    for slug, meta in CATEGORIES_META.items():
        database[slug] = {
            "slug": slug,
            "hasData": meta["hasData"],
            "tabs": {
                "principles": [],
                "catalog": [],
                "applications": [],
                "single": [],
                "formulation": []
            }
        }

    # 智能保留現有 JS / JSON 中手動設定的圖片網址
    existing_imgs = load_existing_images()

    # 解析 技術文件摘要與重點.md
    if not os.path.exists(MD_FILE):
        raise FileNotFoundError(f"Markdown file not found: {MD_FILE}")

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 切割個別文件區塊 (以 ### 標題且緊隨 - **檔案** 為界)
    doc_chunks = re.split(r'\n(?=###\s+[^\n]+\n+-\s+\*\*檔案\*\*：)', md_text)[1:]

    print(f"📖 Successfully parsed {len(doc_chunks)} document entries directly from {MD_FILE}")

    for idx, chunk in enumerate(doc_chunks, 1):
        # 移除區塊結尾可能附帶的大章節標題 (例如 ### （二）... 或 ---)
        chunk_clean = re.split(r'\n\s*###\s+[（\(][一二三四五六七八九十0-9]+[）\)]', chunk)[0]
        chunk_clean = re.split(r'\n\s*---', chunk_clean)[0]

        # 標題
        m_title = re.search(r'###\s+([^\n]+)', chunk_clean)
        raw_title = m_title.group(1).strip() if m_title else ''

        # 檔案名稱
        m_fn = re.search(r'-\s+\*\*檔案\*\*：[ \t]*([^\n]+)', chunk_clean)
        fn = m_fn.group(1).replace('`', '').strip() if m_fn else ''

        # 檔案路徑 (支援跨行折行)
        m_path = re.search(r'-\s+\*\*路徑\*\*：[ \t]*([\s\S]+?)(?=\n\s*-\s+\*\*原文出處\*\*：)', chunk_clean)
        raw_path = m_path.group(1).replace('`', '').strip() if m_path else ''
        path_lines = [l.strip() for l in raw_path.splitlines() if l.strip()]
        raw_path = ''.join(path_lines)

        # 原文出處
        m_origin = re.search(r'-\s+\*\*原文出處\*\*：[ \t]*([^\n]+)', chunk_clean)
        origin = m_origin.group(1).strip() if m_origin else ''

        # 圖表 / 圖片 (可選，支援在 markdown 直接設定 - **圖表**： 或 - **圖片**：)
        m_img = re.search(r'-\s+\*\*(?:圖表|圖片|附圖)\*\*：[ \t]*`?([^`\n]+)`?', chunk_clean)
        explicit_img = m_img.group(1).strip() if m_img else None

        # 摘要 (支援跨行折行)
        m_summary = re.search(r'-\s+\*\*摘要\*\*：[ \t]*([\s\S]+?)(?=\n\s*-\s+\*\*核心重點\*\*：)', chunk_clean)
        desc_raw = m_summary.group(1).strip() if m_summary else ''
        desc = clean_wrapped_text(desc_raw)

        # 核心重點 (支援編號條列與跨行折行)
        m_core = re.search(r'-\s+\*\*核心重點\*\*：[ \t]*([\s\S]+?)(?=\n\s*-\s+\*\*應用\*\*：|\Z)', chunk_clean)
        points = []
        if m_core:
            core_raw = m_core.group(1).strip()
            items = re.split(r'\n\s*\d+\.\s*', '\n' + core_raw)
            for it in items:
                cleaned = clean_wrapped_text(it)
                if cleaned:
                    cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
                    points.append(cleaned)

        # 應用領域 (支援跨行折行與逗號分隔)
        m_apps = re.search(r'-\s+\*\*應用\*\*：[ \t]*(.*)', chunk_clean, re.DOTALL)
        apps = []
        if m_apps:
            app_raw = clean_wrapped_text(m_apps.group(1).strip())
            if app_raw:
                apps = [a.strip() for a in re.split(r'[,、，]', app_raw) if a.strip()]

        slug, tab, clean_rel_path = classify_doc(raw_path, fn)
        if slug == "unknown":
            print(f"⚠️ Warning: Unrecognized slug for path: {raw_path}")
            continue

        meta_info = determine_labels_and_meta(slug, tab, fn, raw_title, origin, clean_rel_path)
        brand = CATEGORIES_META[slug]["brand"]

        # 設定 web 相對路徑
        web_pdf_path = f"techdatadb/{clean_rel_path}"

        title_zh = raw_title
        title_en = fn

        doc_item = {
            "docId": f"{slug.upper()[:3]}-{tab.upper()[:4]}-{len(database[slug]['tabs'][tab]) + 1:02d}",
            "filename": fn,
            "pdfPath": web_pdf_path,
            "docType": meta_info["docType"],
            "lang": meta_info["lang"],
            "version": meta_info["version"],
            "brand": brand,
            "shortLabel": meta_info["shortLabel"],
            "title": title_zh,
            "titleEn": title_en,
            "origin": origin,
            "desc": desc,
            "advantages": points,
            "applications": apps
        }

        if tab == "single":
            doc_item["productGroup"] = meta_info["productGroup"]

        # 圖片路徑完全以 Markdown 中宣告的 - **圖表**： 或 - **圖片**： 為準
        # 若在 Markdown 中刪除該行，則同步自資料庫與 js/technology.js 中移除
        mech_img = explicit_img

        if mech_img:
            doc_item["mechImg"] = mech_img

        database[slug]["tabs"][tab].append(doc_item)

    # 寫入 json/tech_database.json
    out_path = os.path.join(ROOT_DIR, 'json', 'tech_database.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {out_path} successfully!")
    for slug, data in database.items():
        counts = {k: len(v) for k, v in data["tabs"].items()}
        print(f"  [{slug:14s}] (hasData={data['hasData']}): {counts}")

    # 同步注入 js/technology.js
    sync_to_technology_js(database)

    return database

if __name__ == '__main__':
    build_database_from_md()
