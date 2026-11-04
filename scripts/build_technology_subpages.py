# -*- coding: utf-8 -*-
"""
Build Technology Subpages & Technology Index
為 11 大特用化學品產品線建立獨立技術專頁 (Independent Subpages)，
三大核心維度一覽卡片 (1.原理、2.目錄、3.單一產品技術)，
依據 techdatadb 原廠資料庫，比照原理排版架構，線上預覽不開放下載。
實事求是：無公開資料之分頁誠實告知，絕不憑空杜撰！
"""

import os
import sys
import re
import json
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.attech.com.tw"
CACHE_VERSION = "20261103_v1"

# 載入原廠技術資料庫 (由 build_tech_json.py 產生)
JSON_PATH = os.path.join(ROOT_DIR, "json", "tech_database.json")
TECH_DATABASE = {}
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        TECH_DATABASE = json.load(f)

# 11 大特用化學品專題，嚴格依據圖示順序排列
TECH_ITEMS = [
    {
        "slug": "tyzor",
        "item_no": "01",
        "menu_name": "Organic Titanates and Zirconates",
        "menu_sub": "鈦酸酯與鋯酸酯, Tyzor",
        "title_zh": "鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®)",
        "title_en": "Organic Titanates & Zirconates",
        "category_name": "鈦酸酯與鋯酸酯 (Tyzor®)",
        "brand_name": "Dorf Ketal 原廠專用技術",
        "brand_tag": "Dorf Ketal",
        "product_link": "products/dorfketal/tyzor/",
        "product_link_text": "瀏覽 Tyzor 產品",
        "description": "Tyzor® 有機鈦（鋯）化合物具備高反應性與特殊配位多重功能，針對高分子合成催化、三維網絡交聯、異質基材介面結合力提升及 Sol-Gel 表面改性，提供全面工業化解決方案。",
        "has_data": True,
        "inquiry_param": "Tyzor",
        "meta_desc": "宏威應用材料 Dorf Ketal Tyzor® 有機鈦酸酯與鋯酸酯四大核心技術應用，涵蓋酯化催化劑、油墨塗料交聯劑、玻璃金屬密著促進劑與表面改性方案。"
    },
    {
        "slug": "carbon-black",
        "item_no": "02",
        "menu_name": "Special Carbon Black",
        "menu_sub": "特級碳黑 / 導電碳黑",
        "title_zh": "特級碳黑技術應用 (Carbon Black)",
        "title_en": "Special Carbon Black / 特級碳黑",
        "category_name": "特級碳黑 (Carbon Black)",
        "brand_name": "Orion Engineered Carbons 原廠技術",
        "brand_tag": "Orion",
        "product_link": "products/orion/coating/",
        "product_link_text": "瀏覽 40+ 款 Orion 碳黑",
        "description": "Orion Engineered Carbons 為全球特級碳黑領導品牌，提供卓越黑度、分散流變性與耐候堅牢度，廣泛應用於高階塗料、油墨與塑料。",
        "has_data": True,
        "inquiry_param": "CarbonBlack-Tech",
        "meta_desc": "宏威應用材料 Orion 特級碳黑技術專題，特級碳黑與導電碳黑原廠技術資料與配方評估諮詢。"
    },
    {
        "slug": "maleic",
        "item_no": "03",
        "menu_name": "Maleic Resin / 馬林酸樹脂",
        "menu_sub": "松香改性馬林酸樹脂",
        "title_zh": "馬林酸樹脂技術應用 (Maleic Resin)",
        "title_en": "Maleic Resin / 馬林酸樹脂",
        "category_name": "馬林酸樹脂 (Maleic Resin)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/maleic_acid_resin/",
        "product_link_text": "瀏覽馬林酸樹脂規格",
        "description": "松香改性馬林酸樹脂系列，提供優異之硬度、光澤度、快乾性與耐黃變特性。",
        "has_data": False,
        "inquiry_param": "Maleic-Resin-Tech",
        "meta_desc": "宏威應用材料松香改性馬林酸樹脂技術專題，原廠技術資料與配方諮詢。"
    },
    {
        "slug": "px",
        "item_no": "04",
        "menu_name": "PX Lubricant Additives",
        "menu_sub": "潤滑油添加劑 (原 ExxonMobil)",
        "title_zh": "PX 潤滑油添加劑技術應用 (PX Lubricants)",
        "title_en": "PX Lubricants / 潤滑油添加劑",
        "category_name": "PX 潤滑油添加劑",
        "brand_name": "Dorf Ketal (原 ExxonMobil) 原廠技術",
        "brand_tag": "Dorf Ketal",
        "product_link": "products/dorfketal/px/",
        "product_link_text": "瀏覽 PX 潤滑油添加劑",
        "description": "Dorf Ketal (原 ExxonMobil 產品線) 特種潤滑油合成酯添加劑技術專題。",
        "has_data": False,
        "inquiry_param": "PX-Lubricant-Tech",
        "meta_desc": "宏威應用材料 PX 潤滑油添加劑技術專題 (原 ExxonMobil 產品線)，原廠技術資料與配方諮詢。"
    },
    {
        "slug": "silane",
        "item_no": "05",
        "menu_name": "Silane / 矽烷偶合劑",
        "menu_sub": "Dynasylan / hydrosil 系列",
        "title_zh": "矽烷偶合劑系列技術應用 (Silane)",
        "title_en": "Silane / 矽烷偶合劑",
        "category_name": "矽烷偶合劑 (Silane)",
        "brand_name": "Evonik 原廠專用技術",
        "brand_tag": "Evonik / 特化",
        "product_link": "products/others/silane/",
        "product_link_text": "瀏覽 24 款矽烷規格",
        "description": "矽烷偶合劑技術專題，涵蓋水性與溶劑型有機官能基矽烷於複合材料與表面改性應用。",
        "has_data": False,
        "inquiry_param": "Silane-Technology",
        "meta_desc": "宏威應用材料矽烷偶合劑系列技術專題，包含 Dynasylan 與 Hydrosil 水性及溶劑型矽烷技術諮詢。"
    },
    {
        "slug": "wax",
        "item_no": "06",
        "menu_name": "Micronized Wax / 微粉蠟",
        "menu_sub": "PTFE 取代 / 耐磨耐刮助劑",
        "title_zh": "微粉化蠟技術應用 (Micronized Wax)",
        "title_en": "Micronized Wax / 微粉蠟",
        "category_name": "微粉蠟 (Micronized Wax)",
        "brand_name": "Micro Powders (MPI) 原廠技術",
        "brand_tag": "Micro Powders",
        "product_link": "products/mpi/ptfe/",
        "product_link_text": "瀏覽微粉蠟與 PTFE 替代方案",
        "description": "Micro Powders (MPI) 全球微粉化蠟技術權威，提供合規無氟 PFAS-Free PTFE 替代方案、耐磨耐刮、消光爽滑及觸感改性劑。",
        "has_data": True,
        "inquiry_param": "MPI-Wax-Tech",
        "meta_desc": "宏威應用材料 Micro Powders (MPI) 微粉蠟技術專題，合規無氟 PTFE 取代系列技術諮詢。"
    },
    {
        "slug": "adhesion",
        "item_no": "07",
        "menu_name": "Adhesion Resin / 密著樹脂",
        "menu_sub": "氯化聚烯烴 (CPO) & 非氯系",
        "title_zh": "密著樹脂技術應用 (Adhesion Resin)",
        "title_en": "Adhesion Resin / 密著樹脂",
        "category_name": "密著促進劑 (Adhesion)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/adhesion_promoter/",
        "product_link_text": "瀏覽密著促進劑規格",
        "description": "氯化聚烯烴 (CPO) 與非氯系特種密著樹脂技術應用。",
        "has_data": False,
        "inquiry_param": "Adhesion-Promoter-Tech",
        "meta_desc": "宏威應用材料密著促進劑技術專題，涵蓋氯化聚烯烴 CPO 與非氯系架橋樹脂技術諮詢。"
    },
    {
        "slug": "polyester",
        "item_no": "08",
        "menu_name": "Polyester Resin / 聚酯樹脂",
        "menu_sub": "聚酯樹脂 (DYNAPOL/DYNACOLL替代品)",
        "title_zh": "聚酯樹脂技術應用 (Polyester Resin)",
        "title_en": "Polyester Resin / 聚酯樹脂",
        "category_name": "聚酯樹脂 (Polyester Resin)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/polyester_resin/",
        "product_link_text": "瀏覽 37 款聚酯規格",
        "description": "飽和共聚聚酯樹脂技術專題，提供高附著、柔韌性與優異耐化學品塗料樹脂。",
        "has_data": False,
        "inquiry_param": "Polyester-Resin-Tech",
        "meta_desc": "宏威應用材料飽和共聚聚酯樹脂技術專題，DYNAPOL® 與 DYNACOLL® 替代方案技術諮詢。"
    },
    {
        "slug": "chain",
        "item_no": "09",
        "menu_name": "Chain Extender / 擴鏈劑",
        "menu_sub": "Unilink & Clearlink 系列",
        "title_zh": "擴鏈劑技術應用 (Chain Extender)",
        "title_en": "Chain Extender / 擴鏈劑",
        "category_name": "擴鏈劑 (Chain Extender)",
        "brand_name": "Dorf Ketal 原廠專用技術",
        "brand_tag": "Dorf Ketal",
        "product_link": "products/dorfketal/chain/",
        "product_link_text": "瀏覽擴鏈劑規格",
        "description": "Dorf Ketal Unilink® 與 Clearlink® 受阻二級二胺擴鏈劑技術，專用於聚脲 (Polyurea) 與高性能聚氨酯彈性體體系。",
        "has_data": True,
        "inquiry_param": "Chain-Extender",
        "meta_desc": "宏威應用材料 Dorf Ketal Unilink & Clearlink 系列受阻二胺擴鏈劑技術專題與諮詢。"
    },
    {
        "slug": "matting",
        "item_no": "10",
        "menu_name": "Matting Agent / 消光粉",
        "menu_sub": "二氧化矽 / 表面處理消光",
        "title_zh": "消光粉技術應用 (Matting Agent)",
        "title_en": "Matting Agent / 消光粉",
        "category_name": "消光粉 (Matting Agent)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/matting_agent/",
        "product_link_text": "瀏覽消光粉規格",
        "description": "特種沉澱與氣相二氧化矽消光粉技術專題，包含消光原理、粒徑分佈、孔隙率、膜厚影響與各樹脂體系之分散工藝指引。",
        "has_data": True,
        "inquiry_param": "Matting-Agent-Tech",
        "meta_desc": "宏威應用材料二氧化矽消光粉技術專題與技術諮詢。"
    },
    {
        "slug": "powder",
        "item_no": "11",
        "menu_name": "Powder Coating Additive",
        "menu_sub": "粉體塗料專用功能性助劑",
        "title_zh": "粉體塗料專用助劑技術應用 (Powder Additives)",
        "title_en": "Powder Additives / 粉體助劑",
        "category_name": "粉體塗料助劑 (Powder Additives)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/coating_additive/",
        "product_link_text": "瀏覽粉體塗料助劑規格",
        "description": "熱固性粉體塗料專用功能性助劑技術專區。",
        "has_data": False,
        "inquiry_param": "Powder-Additive-Tech",
        "meta_desc": "宏威應用材料粉體塗料功能性助劑技術專題與技術諮詢。"
    }
]

def get_encoded_pdf_url(rel_path):
    if not rel_path:
        return ""
    clean = rel_path.lstrip("./")
    segments = clean.split("/")
    encoded = "/".join(urllib.parse.quote(s) for s in segments)
    return f"{encoded}#toolbar=0&navpanes=0"

def build_category_switcher(current_slug, is_index=False):
    """建立 11 個產品系列分類切換列"""
    cards_html = []
    for item in TECH_ITEMS:
        slug = item["slug"]
        is_active = (slug == current_slug)
        url = f"technology/{slug}/"
        item_no = item.get("item_no", "01")
        menu_name = item.get("menu_name", item["category_name"])
        menu_sub = item.get("menu_sub", item["brand_tag"])

        if is_active:
            card = f'''                        <a href="{url}" onclick="if(event.button===0&&!event.ctrlKey&&!event.metaKey){{event.preventDefault();switchTechCategory('{slug}');}}" data-tech-slug="{slug}"
                           class="tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-blue-50/90 border-2 border-blue-600/80 text-blue-950 no-underline shadow-xs transition-all">
                            <div class="flex items-center gap-2 min-w-0 w-full">
                                <span class="tech-num-badge w-5 h-5 rounded-md bg-blue-900 text-white text-xs font-black flex items-center justify-center shrink-0 shadow-2xs">
                                    {item_no}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="tech-btn-title text-sm font-bold text-blue-950 truncate leading-snug">
                                        {menu_name}
                                    </div>
                                    <div class="tech-btn-sub text-xs font-medium text-blue-800/80 truncate">
                                        {menu_sub}
                                    </div>
                                </div>
                            </div>
                        </a>'''
        else:
            card = f'''                        <a href="{url}" onclick="if(event.button===0&&!event.ctrlKey&&!event.metaKey){{event.preventDefault();switchTechCategory('{slug}');}}" data-tech-slug="{slug}"
                           class="tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-blue-400 text-slate-800 hover:text-blue-950 no-underline transition-all">
                            <div class="flex items-center gap-2 min-w-0 w-full">
                                <span class="tech-num-badge w-5 h-5 rounded-md bg-slate-100 group-hover:bg-blue-50 text-slate-500 group-hover:text-blue-700 text-xs font-bold flex items-center justify-center shrink-0 transition-colors">
                                    {item_no}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="tech-btn-title text-sm font-bold text-slate-800 group-hover:text-blue-950 truncate leading-snug">
                                        {menu_name}
                                    </div>
                                    <div class="tech-btn-sub text-xs font-normal text-slate-500 group-hover:text-slate-600 truncate">
                                        {menu_sub}
                                    </div>
                                </div>
                            </div>
                        </a>'''
        cards_html.append(card)

    return f'''                <!-- 左側：技術專題產品分類 (緊湊精緻條列) -->
                <aside class="tech-sidebar bg-white rounded-2xl border border-slate-200 p-3.5 sm:p-4 shadow-xs shrink-0">
                    <div class="flex items-center justify-between pb-2.5 mb-2 border-b border-slate-100">
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-5 bg-blue-900 rounded-full inline-block shrink-0"></span>
                            <div>
                                <h2 class="text-sm sm:text-base font-bold text-blue-950 leading-tight">
                                    技術分類
                                </h2>
                            </div>
                        </div>
                        <span class="text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">11 產品線</span>
                    </div>
                    <!-- 條列式導覽清單 -->
                    <nav class="tech-sidebar-list" aria-label="11大技術專題產品分類導覽">
{chr(10).join(cards_html)}
                    </nav>
                </aside>'''

def build_subtab_nav(has_data=True, active_key="principles"):
    """三大核心維度純單行標籤列"""
    tabs = [
        ("principles", "1. 原理", "fa-atom"),
        ("catalog", "2. 目錄", "fa-list-check"),
        ("single", "3. 單一產品技術", "fa-flask-vial")
    ]

    buttons = []
    for key, label, icon in tabs:
        is_active = (key == active_key)
        active_cls = "active" if is_active else ""
        btn = f'''                    <button type="button" onclick="switchTechSubTab('{key}')" id="tech-subtab-{key}"
                            class="tech-subtab-btn {active_cls}">
                        <i class="fa-solid {icon} text-xs"></i>
                        <span>{label}</span>
                    </button>'''
        buttons.append(btn)

    return f'''                <!-- 瀏覽器書籤樣式：四大核心維度標籤列 -->
                <div class="tech-subtab-strip" role="tablist" aria-label="技術專題四大核心維度導覽">
{chr(10).join(buttons)}
                </div>'''

def build_single_doc_layout_html(doc, slug, tab_key, item):
    """產生單一文件檢視視圖 (封面式預覽或純文字專題卡片)"""
    pdf_url = get_encoded_pdf_url(doc.get("pdfPath", ""))
    has_mech_img = bool(doc.get("mechImg"))
    is_pdf = bool(doc.get("pdfPath", "").lower().endswith(".pdf"))
    doc_title_clean = doc.get("title", "").replace('"', '&quot;').replace("'", "&#39;")
    inquiry_title = f"{item['menu_name']}-{doc.get('title')}"
    encoded_inquiry = urllib.parse.quote(inquiry_title)
    product_link = item.get("product_link", "products/")

    advantages_items = []
    for idx, adv in enumerate(doc.get("advantages", [])):
        adv_li = f'''                        <li class="flex items-start gap-1.5">
                            <span class="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">{idx + 1}</span>
                            <span>{adv}</span>
                        </li>'''
        advantages_items.append(adv_li)
    advantages_html = "\n".join(advantages_items)

    apps_items = []
    for app in doc.get("applications", []):
        app_span = f'''                            <span class="px-2 py-0.5 rounded bg-white text-slate-700 text-xs font-medium border border-slate-200">{app}</span>'''
        apps_items.append(app_span)
    apps_html = "\n".join(apps_items)

    # 若該技術文件無圖片亦無 PDF 封面（例如純文字手冊章節）：
    # 採滿版對稱佈局，徹底解決畫面左半邊為空卡片、右半邊單邊擠壓之問題
    if not has_mech_img and not is_pdf:
        origin_html = f'''                <div class="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-600 text-xs font-mono shrink-0">
                    <i class="fa-solid fa-book-bookmark text-blue-900 mr-1"></i>
                    <span>{doc.get('origin', '')}</span>
                </div>''' if doc.get('origin') else '''                <span class="px-2 py-0.5 rounded-full bg-blue-50 text-blue-800 text-[11px] font-bold border border-blue-200/60 shrink-0">技術手冊規範</span>'''

        desc_html = f'''            <div class="p-3.5 rounded-xl bg-white border border-slate-200/90 shadow-2xs">
                <div class="text-xs font-bold text-blue-950 mb-1 flex items-center gap-1.5">
                    <i class="fa-solid fa-microscope text-blue-900 text-xs"></i>
                    <span>核心作用原理與機制：</span>
                </div>
                <p class="text-sm text-slate-700 leading-relaxed font-normal">
                    {doc.get('desc') or doc.get('summary') or ''}
                </p>
            </div>''' if (doc.get('desc') or doc.get('summary')) else ''

        apps_block = apps_html if apps_html else '<span class="text-xs text-slate-400">詳見技術手冊各行業應用章節</span>'
        adv_block = f'''                    <ul class="space-y-1.5 text-sm text-slate-700">
{advantages_html}
                    </ul>''' if advantages_html else '<p class="text-xs text-slate-400">詳見技術手冊內文規範</p>'

        return f'''        <div class="bg-slate-50/70 rounded-xl border border-slate-200 p-4 sm:p-5 space-y-3.5">
            <!-- 頂部：專題標題與手冊來源徽章 -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 border-b border-slate-200/80 pb-3">
                <div class="flex items-center gap-2.5">
                    <span class="w-8 h-8 rounded-lg bg-blue-900/10 text-blue-900 flex items-center justify-center font-bold text-sm shrink-0">
                        <i class="fa-solid fa-atom"></i>
                    </span>
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                            {doc_title_clean}
                        </h3>
                        <div class="text-[11px] text-slate-500 font-medium">技術原理與手冊章節規範</div>
                    </div>
                </div>
{origin_html}
            </div>

            <!-- 核心作用原理說明 (滿版清晰舒適) -->
{desc_html}

            <!-- 下半部：左右雙欄平衡展示技術特點與適用範疇 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-0.5">
                <!-- 主要技術特點 -->
                <div class="space-y-2 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-2xs">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
{adv_block}
                </div>

                <!-- 適用範疇與動作 -->
                <div class="space-y-3 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-2xs flex flex-col justify-between">
                    <div class="space-y-2">
                        <div class="flex items-center gap-1.5 text-xs font-bold text-slate-800">
                            <i class="fa-solid fa-layer-group text-blue-900 text-xs"></i>
                            <span>適用範疇 / 相關領域：</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5">
{apps_block}
                        </div>
                    </div>

                    <!-- 諮詢動作列 -->
                    <div class="pt-2 flex flex-wrap items-center gap-2 border-t border-slate-100">
                        <a href="contact/?mode=detailed&inquiry={encoded_inquiry}"
                           class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                            <i class="fa-solid fa-envelope text-xs"></i>
                            <span>索取規格諮詢 / 申請樣品</span>
                        </a>
                        <a href="{product_link}"
                           class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                            <i class="fa-solid fa-table-list text-xs"></i>
                            <span>查看相關產品列表</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>'''

    if has_mech_img:
        # 原廠技術機制圖 (依原圖比例自然排版自適應，不強制固定卡片高度)
        preview_box_html = f'''            <div class="flex flex-col justify-center">
                <div class="bg-white rounded-xl border border-slate-200 p-3 sm:p-4 shadow-2xs flex flex-col items-center justify-center overflow-hidden select-none" oncontextmenu="return false;">
                    <img src="{doc.get("mechImg")}" alt="{doc.get("title")} 反應機制圖"
                         class="max-w-full h-auto max-h-[640px] object-contain rounded select-none pointer-events-none mx-auto"
                         draggable="false">
                </div>
            </div>'''
    elif is_pdf:
        # 文件封面卡片：第一頁作為封面 (等比例不拉伸)，點擊封面直接開啟全螢幕放大閱讀
        viewer_id = f"pdf-canvas-viewer-{slug}-{tab_key}"
        preview_box_html = f'''            <div class="h-full flex flex-col justify-center">
                <div id="{viewer_id}"
                     class="pdf-viewer-container group relative w-full h-[580px] sm:h-[640px] rounded-xl border border-slate-200 bg-white p-3 flex items-center justify-center overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-500 hover:shadow-lg"
                     data-pdf-url="{pdf_url}"
                     data-pdf-title="{doc_title_clean}"
                     onclick="openPdfFullscreenModal('{pdf_url}', '{doc_title_clean}')"
                     title="點擊全螢幕放大閱讀"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">文件封面載入中...</span>
                    </div>
                </div>
            </div>'''
    else:
        preview_box_html = ''

    return f'''        <div class="tech-principles-grid bg-slate-50/70 rounded-xl border border-slate-200 p-3 sm:p-3.5">
            <!-- 左欄：線上文件瀏覽視窗 (視窗拉長補滿空白，無下載按鈕，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
{preview_box_html}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 (依圖 1 指示：移除被劃掉的語言/版本標籤與檔案名字串) -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        {doc.get("title")}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    {doc.get("desc") or doc.get("summary") or ""}
                </p>

                <!-- 主要技術特點 -->
                <div class="space-y-1.5">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
                    <ul class="space-y-1 text-sm text-slate-700">
{advantages_html}
                    </ul>
                </div>

                <!-- 適用範疇標籤 -->
                <div class="space-y-1 pt-0.5">
                    <span class="text-xs font-bold text-slate-700">適用範疇 / 相關領域：</span>
                    <div class="flex flex-wrap gap-1">
{apps_html}
                    </div>
                </div>

                <!-- 諮詢動作列 -->
                <div class="pt-2 flex flex-wrap items-center gap-2 border-t border-slate-100">
                    <a href="contact/?mode=detailed&inquiry={encoded_inquiry}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                        <i class="fa-solid fa-envelope text-xs"></i>
                        <span>索取規格諮詢 / 申請樣品</span>
                    </a>
                    <a href="{product_link}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>查看相關產品列表</span>
                    </a>
                </div>
            </div>
        </div>'''

def build_empty_tab_html(item, tab_key):
    """產生暫無公開資料提示區塊 (實事求是、誠實告知、不杜撰)"""
    tab_names = {
        "principles": "原理機制",
        "catalog": "總覽目錄",
        "single": "單一產品技術資料",
    }
    name = tab_names.get(tab_key, "技術資料")

    return f'''        <div class="rounded-xl border border-slate-200 bg-slate-50/70 p-4 sm:p-6 text-center space-y-2.5">
            <div class="flex items-center justify-center gap-2">
                <i class="fa-solid fa-folder-open text-slate-400 text-base"></i>
                <span class="px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 text-xs font-bold">資料整備中</span>
                <span class="text-sm sm:text-base font-bold text-blue-950">原廠技術資料整理中，暫無公開{name}</span>
            </div>
            <p class="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                目前原廠未提供此項之公開資料，我們秉持實事求是原則不進行臆測杜撰。若您需要特定規格手冊或評估樣品，歡迎直接聯繫宏威業務團隊為您服務。
            </p>
            <div class="pt-1 flex items-center justify-center gap-2.5">
                <a href="contact/?mode=detailed&inquiry={urllib.parse.quote(item["menu_name"])}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                    <i class="fa-solid fa-paper-plane text-xs"></i>
                    <span>聯繫業務索取資料</span>
                </a>
                <a href="{item["product_link"]}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                    <i class="fa-solid fa-table-list text-xs"></i>
                    <span>瀏覽相關產品專區</span>
                </a>
            </div>
        </div>'''

def get_best_subtab_for_category(slug):
    """取得特定產品線最佳的預設子分頁 (按 1.原理 -> 2.目錄 -> 3.單一產品技術 自然順序)"""
    cat_data = TECH_DATABASE.get(slug, {"tabs": {}})
    tabs = cat_data.get("tabs", {})
    
    order = ["principles", "catalog", "single"]
    for tab_key in order:
        if tabs.get(tab_key) and len(tabs[tab_key]) > 0:
            return tab_key
    return "principles"

def build_category_content_section(item, active_subtab="principles"):
    """
    產生特定技術類別的完整 HTML 內容 (四大子分頁，比照原理排版架構，線上預覽不開放下載)
    """
    slug = item["slug"]
    cat_data = TECH_DATABASE.get(slug, {"tabs": {}})
    sub_tabs = ["principles", "catalog", "single"]

    panels_html = []
    for tab_key in sub_tabs:
        docs = cat_data.get("tabs", {}).get(tab_key, [])
        is_hidden = (active_subtab != tab_key)
        hidden_cls = "hidden " if is_hidden else ""

        if not docs:
            empty_html = build_empty_tab_html(item, tab_key)
            panel = f'''                    <div id="tech-panel-{tab_key}" class="{hidden_cls}space-y-2">
{empty_html}
                    </div>'''
            panels_html.append(panel)
        else:
            first_doc = docs[0]
            doc_view_html = build_single_doc_layout_html(first_doc, slug, tab_key, item)

            if len(docs) > 1:
                if tab_key == "principles":
                    # 原理維度：依圖 2 指示改成一塊一塊按鈕切換
                    blocks = []
                    for idx, doc in enumerate(docs):
                        is_selected = (idx == 0)
                        active_cls = "bg-blue-900 text-white font-bold border-blue-900 shadow-2xs ring-2 ring-blue-900/20 active" if is_selected else "bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-950 border-slate-200 hover:border-blue-300 font-semibold"
                        label = doc.get('shortLabel') or doc.get('title')
                        blocks.append(f'''                                <button type="button"
                                        data-doc-idx="{idx}"
                                        onclick="selectTechDoc('{slug}', 'principles', {idx})"
                                        class="tech-doc-block-btn tech-doc-block-btn-{slug}-principles inline-flex items-center justify-center px-2 py-1 rounded-md border text-xs transition-all duration-150 cursor-pointer {active_cls}">
                                    <span>{label}</span>
                                </button>''')
                    blocks_str = "\n".join(blocks)
                    panel = f'''                    <div id="tech-panel-principles" class="{hidden_cls}space-y-3">
                        <!-- 一塊一塊技術文件選擇列 (依圖 2 指示：原理專用區塊按鈕) -->
                        <div class="tech-principles-blocks-bar bg-slate-50 border border-slate-200/90 rounded-lg p-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-2 shadow-2xs">
                            <div class="flex items-center gap-1.5 text-xs font-bold text-slate-800 shrink-0">
                                <i class="fa-solid fa-file-lines text-blue-900 text-sm"></i>
                                <span>選擇技術文件：</span>
                            </div>
                            <div class="flex flex-wrap items-center gap-1.5 flex-1">
{blocks_str}
                            </div>
                        </div>

                        <!-- 100% 滿版雙欄核心展示區 -->
                        <div id="viewer-{slug}-principles" class="w-full">
{doc_view_html}
                        </div>
                    </div>'''
                elif tab_key == "single":
                    # 單一產品依相同產品系列分組排列 optgroup
                    groups = {}
                    group_names = []
                    for idx, doc in enumerate(docs):
                        grp = doc.get("productGroup", "其他")
                        if grp not in groups:
                            groups[grp] = []
                            group_names.append(grp)
                        groups[grp].append((idx, doc))

                    group_opts = []
                    for grp in group_names:
                        opt_lines = []
                        for idx, doc in groups[grp]:
                            selected_attr = ' selected' if idx == 0 else ''
                            label = doc.get('shortLabel') or doc.get('title')
                            opt_lines.append(f'                                    <option value="{idx}"{selected_attr}>{label}</option>')
                        opt_lines_str = "\n".join(opt_lines)
                        group_opts.append(f'                                <optgroup label="── {grp} ({len(groups[grp])} 篇) ──">\n{opt_lines_str}\n                                </optgroup>')
                    options_html = "\n".join(group_opts)

                    panel = f'''                    <div id="tech-panel-{tab_key}" class="{hidden_cls}space-y-3">
                        <!-- 下拉式卷軸選單列 (Munzing 風格：精緻簡潔、完全不佔據兩側版面空間) -->
                        <div class="tech-doc-selector-bar bg-slate-50 border border-slate-200/90 rounded-xl p-2.5 sm:p-3 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 shadow-2xs">
                            <div class="flex items-center gap-2 sm:gap-3 flex-1 min-w-0">
                                <label for="doc-select-{slug}-{tab_key}" class="flex items-center gap-1.5 text-xs font-bold text-slate-800 shrink-0">
                                    <i class="fa-solid fa-file-lines text-blue-900 text-sm"></i>
                                    <span>選擇技術文件：</span>
                                </label>
                                <div class="relative flex-1 min-w-0 max-w-full sm:max-w-xl">
                                    <select id="doc-select-{slug}-{tab_key}" onchange="selectTechDoc('{slug}', '{tab_key}', parseInt(this.value, 10))"
                                            class="w-full bg-white hover:bg-slate-50/50 border border-slate-300 hover:border-blue-500 focus:border-blue-900 focus:ring-2 focus:ring-blue-100 rounded-lg px-3 py-2 text-xs sm:text-sm font-semibold text-slate-800 shadow-2xs cursor-pointer transition-all truncate">
{options_html}
                                    </select>
                                </div>
                            </div>

                            <!-- 篇數統計與上一篇/下一篇快速切換按鈕 -->
                            <div class="flex items-center justify-between sm:justify-end gap-2 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-slate-200/60">
                                <span class="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded-md border border-slate-200 shadow-2xs">
                                    第 <strong id="doc-count-current-{slug}-{tab_key}" class="text-blue-950 font-bold">1</strong> / {len(docs)} 篇
                                </span>
                                <div class="flex items-center gap-1">
                                    <button type="button" id="doc-prev-btn-{slug}-{tab_key}" onclick="navigateTechDoc('{slug}', '{tab_key}', -1)"
                                            disabled
                                            class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                            title="上一篇技術文件">
                                        <i class="fa-solid fa-chevron-left text-xs"></i>
                                    </button>
                                    <button type="button" id="doc-next-btn-{slug}-{tab_key}" onclick="navigateTechDoc('{slug}', '{tab_key}', 1)"
                                            {'disabled' if len(docs) <= 1 else ''}
                                            class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                            title="下一篇技術文件">
                                        <i class="fa-solid fa-chevron-right text-xs"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 100% 滿版雙欄核心展示區 -->
                        <div id="viewer-{slug}-{tab_key}" class="w-full">
{doc_view_html}
                        </div>
                    </div>'''
                else:
                    opt_lines = []
                    for idx, doc in enumerate(docs):
                        selected_attr = ' selected' if idx == 0 else ''
                        label = doc.get('shortLabel') or doc.get('title')
                        opt_lines.append(f'                                <option value="{idx}"{selected_attr}>{label}</option>')
                    options_html = "\n".join(opt_lines)

                    panel = f'''                    <div id="tech-panel-{tab_key}" class="{hidden_cls}space-y-3">
                        <!-- 下拉式卷軸選單列 (Munzing 風格：精緻簡潔、完全不佔據兩側版面空間) -->
                        <div class="tech-doc-selector-bar bg-slate-50 border border-slate-200/90 rounded-xl p-2.5 sm:p-3 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 shadow-2xs">
                            <div class="flex items-center gap-2 sm:gap-3 flex-1 min-w-0">
                                <label for="doc-select-{slug}-{tab_key}" class="flex items-center gap-1.5 text-xs font-bold text-slate-800 shrink-0">
                                    <i class="fa-solid fa-file-lines text-blue-900 text-sm"></i>
                                    <span>選擇技術文件：</span>
                                </label>
                                <div class="relative flex-1 min-w-0 max-w-full sm:max-w-xl">
                                    <select id="doc-select-{slug}-{tab_key}" onchange="selectTechDoc('{slug}', '{tab_key}', parseInt(this.value, 10))"
                                            class="w-full bg-white hover:bg-slate-50/50 border border-slate-300 hover:border-blue-500 focus:border-blue-900 focus:ring-2 focus:ring-blue-100 rounded-lg px-3 py-2 text-xs sm:text-sm font-semibold text-slate-800 shadow-2xs cursor-pointer transition-all truncate">
{options_html}
                                    </select>
                                </div>
                            </div>

                            <!-- 篇數統計與上一篇/下一篇快速切換按鈕 -->
                            <div class="flex items-center justify-between sm:justify-end gap-2 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-slate-200/60">
                                <span class="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded-md border border-slate-200 shadow-2xs">
                                    第 <strong id="doc-count-current-{slug}-{tab_key}" class="text-blue-950 font-bold">1</strong> / {len(docs)} 篇
                                </span>
                                <div class="flex items-center gap-1">
                                    <button type="button" id="doc-prev-btn-{slug}-{tab_key}" onclick="navigateTechDoc('{slug}', '{tab_key}', -1)"
                                            disabled
                                            class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                            title="上一篇技術文件">
                                        <i class="fa-solid fa-chevron-left text-xs"></i>
                                    </button>
                                    <button type="button" id="doc-next-btn-{slug}-{tab_key}" onclick="navigateTechDoc('{slug}', '{tab_key}', 1)"
                                            {'disabled' if len(docs) <= 1 else ''}
                                            class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                            title="下一篇技術文件">
                                        <i class="fa-solid fa-chevron-right text-xs"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 100% 滿版雙欄核心展示區 -->
                        <div id="viewer-{slug}-{tab_key}" class="w-full">
{doc_view_html}
                        </div>
                    </div>'''
            else:
                # 只有 1 篇文件時直接滿版展示
                panel = f'''                    <div id="tech-panel-{tab_key}" class="{hidden_cls}space-y-2">
                        <div id="viewer-{slug}-{tab_key}" class="w-full">
{doc_view_html}
                        </div>
                    </div>'''
            panels_html.append(panel)

    all_panels_html = "\n\n".join(panels_html)
    subtab_nav_html = build_subtab_nav(has_data=item["has_data"], active_key=active_subtab)

    return f'''            <section class="bg-white border border-slate-200 rounded-xl shadow-xs p-3 sm:p-4 space-y-2.5">
                <!-- 專題標題與頂部操作列 (依圖 1 指示：改成產品類別名稱) -->
                <div class="flex items-center justify-between gap-3 pb-2 border-b border-slate-100">
                    <div class="flex items-center gap-2 min-w-0">
                        <span class="w-1.5 h-4 bg-blue-900 rounded-full inline-block shrink-0"></span>
                        <h1 class="text-base sm:text-lg font-bold text-blue-950 tracking-tight truncate">
                            {item["menu_name"]}
                        </h1>
                    </div>
                    
                    <div class="shrink-0 flex items-center">
                        <a href="{item["product_link"]}"
                           class="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-bold transition-colors">
                            <i class="fa-solid fa-table-list text-xs"></i>
                            <span>{item["product_link_text"]}</span>
                        </a>
                    </div>
                </div>

                <!-- 專題核心技術簡介 (實事求是依據技術資料庫精確摘要) -->
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal pt-0.5 pb-0.5">
                    {item["description"]}
                </p>

                <!-- 瀏覽器書籤風格容器 -->
                <div class="tech-bookmark-wrapper mt-1">
{subtab_nav_html}

                    <div class="tech-bookmark-body">
{all_panels_html}
                    </div>
                </div>
            </section>'''

def build_full_tech_page_html(item, template_shell, is_index=False):
    """組裝特定特化產品專屬 HTML 頁面"""
    slug = item["slug"]
    title_zh = item["title_zh"]
    meta_desc = item["meta_desc"]
    canonical_url = f"{DOMAIN}/technology/" if is_index else f"{DOMAIN}/technology/{slug}/"

    breadcrumb_item = f'''                    <a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <span id="tech-breadcrumb-current" class="text-blue-950 font-bold">{item["category_name"]}</span>'''

    switcher_html = build_category_switcher(slug, is_index=False)
    best_tab = get_best_subtab_for_category(slug)
    content_html = build_category_content_section(item, active_subtab=best_tab)

    tech_section = f'''    <!-- Tab: 技術專區 (Technology) - 獨立分頁一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->
    <section id="tab-technology" class="tab-content active" role="tabpanel" aria-labelledby="nav-technology">
        <style>
        .tech-layout-container {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
            width: 100%;
        }}
        .tech-sidebar {{
            width: 100%;
            flex-shrink: 0;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        }}
        .tech-sidebar-list {{
            display: flex !important;
            flex-direction: column !important;
            gap: 0.375rem !important;
            width: 100% !important;
        }}
        .tech-sidebar-btn {{
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }}
        .tech-sidebar-btn .min-w-0.flex-1 {{
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-width: 0 !important;
        }}
        .tech-btn-title {{
            display: block !important;
            width: 100% !important;
        }}
        .tech-btn-sub {{
            display: block !important;
            width: 100% !important;
        }}
        .tech-content-main {{
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
        }}
        @media (min-width: 900px) {{
            .tech-layout-container {{
                flex-direction: row;
                gap: 1.25rem;
                align-items: flex-start;
            }}
            .tech-sidebar {{
                width: 310px;
                position: sticky;
                top: 5rem;
                max-height: calc(100vh - 5.5rem);
                display: flex;
                flex-direction: column;
                overflow-y: auto;
            }}
            .tech-sidebar::-webkit-scrollbar {{
                width: 4px;
            }}
            .tech-sidebar::-webkit-scrollbar-track {{
                background: #f8fafc;
            }}
            .tech-sidebar::-webkit-scrollbar-thumb {{
                background: #cbd5e1;
                border-radius: 4px;
            }}
        }}
        /* 瀏覽器書籤風格容器與標籤列 */
                /* 優化快捷標籤列滾動條樣式 */
        .tech-pills-container {{
            scrollbar-width: thin;
            scrollbar-color: #cbd5e1 transparent;
            -webkit-overflow-scrolling: touch;
        }}
        .tech-pills-container::-webkit-scrollbar {{
            height: 4px;
        }}
        .tech-pills-container::-webkit-scrollbar-track {{
            background: transparent;
        }}
        .tech-pills-container::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}
        .tech-pills-container::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
        .tech-bookmark-wrapper {{
            width: 100%;
            margin-top: 0.5rem;
            position: relative;
        }}
        .tech-subtab-strip {{
            display: flex;
            align-items: flex-end;
            gap: 0.375rem;
            padding-left: 0.5rem;
            margin-bottom: -1px;
            position: relative;
            z-index: 10;
        }}
        @media (max-width: 640px) {{
            .tech-subtab-strip {{
                overflow-x: auto;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 1px;
            }}
            .tech-subtab-strip::-webkit-scrollbar {{
                display: none;
            }}
        }}
        .tech-subtab-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.375rem;
            padding: 0.625rem 1.125rem 0.5rem 1.125rem;
            border-top-left-radius: 0.625rem !important;
            border-top-right-radius: 0.625rem !important;
            border-bottom-left-radius: 0 !important;
            border-bottom-right-radius: 0 !important;
            border: 1px solid #cbd5e1 !important;
            border-bottom: 1px solid #cbd5e1 !important;
            background: #f1f5f9 !important;
            color: #475569 !important;
            font-size: 0.8125rem;
            font-weight: 600;
            line-height: 1.2;
            white-space: nowrap;
            cursor: pointer;
            transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
            position: relative;
            z-index: 5;
            margin-bottom: 0;
        }}
        .tech-subtab-btn:hover {{
            background: #e2e8f0 !important;
            color: #0f172a !important;
        }}
        .tech-subtab-btn.active {{
            background: #ffffff !important;
            color: #1e3a8a !important;
            font-weight: 800 !important;
            border: 1px solid #cbd5e1 !important;
            border-top: 3px solid #1e3a8a !important;
            border-bottom: 2px solid #ffffff !important;
            margin-bottom: -1px !important;
            padding-bottom: calc(0.5rem + 2px) !important;
            position: relative;
            z-index: 20 !important;
            box-shadow: 0 -2px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }}
        .tech-bookmark-body {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 0 0.75rem 0.75rem 0.75rem;
            padding: 1rem;
            position: relative;
            z-index: 1;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }}
        @media (max-width: 640px) {{
            .tech-bookmark-body {{
                border-radius: 0 0 0.75rem 0.75rem;
                padding: 0.75rem;
            }}
        }}
        /* 原理維度專用：一塊一塊技術文件切換按鈕 */
        .tech-doc-block-btn {{
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        .tech-doc-block-btn.active {{
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border-color: #1e3a8a !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }}
        /* 核心原理 2-Column Split 左右分欄雙翼佈局 (重要資訊首屏完全可見) */
                /* 全螢幕技術文件預覽模態視窗 (全畫面滿版沉浸式閱讀，絕不被任何元素遮擋) */
        #tech-pdf-fullscreen-modal {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 99999 !important;
            background: #0f172a !important;
            display: flex !important;
            flex-direction: column !important;
            box-sizing: border-box !important;
        }}
        #tech-pdf-fullscreen-modal.hidden {{
            display: none !important;
        }}
        #tech-pdf-fullscreen-modal .tech-modal-inner {{
            position: relative !important;
            z-index: 100000 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            border-radius: 0 !important;
            border: none !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            background: #0f172a !important;
            overflow: hidden !important;
        }}
.tech-principles-grid {{
            display: grid;
            grid-template-columns: 50% 50%;
            gap: 0.875rem;
            align-items: start;
        }}
        @media (max-width: 900px) {{
            .tech-principles-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        </style>
        <div class="optimized-container px-3 sm:px-4 py-2.5 sm:py-3.5">
            <!-- 頂部麵包屑導航 (極簡緊湊) -->
            <div class="mb-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-slate-500">
                <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
{breadcrumb_item}
            </div>

            <!-- 左右兩欄格局：左側技術分類切換導覽 (條列式)，右側資料顯示區 -->
            <div class="tech-layout-container">
{switcher_html}

                <!-- 右側：資料顯示區 (統一白色風格) -->
                <main class="tech-content-main">
                    <div id="tech-content-display">
{content_html}
                    </div>
                </main>
            </div>
        </div>
    </section>'''

    # Replace section in template shell
    html = template_shell
    sec_start = html.find('id="tab-technology"')
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    if prev_comment != -1:
        while True:
            prev = html.rfind(comment_marker, 0, prev_comment)
            if prev != -1 and html[prev:prev_comment].strip().startswith('<!-- Tab: 技術專區'):
                prev_comment = prev
            else:
                break
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)

    next_sec = html.find('id="tab-partners"')
    prev_partner_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, next_sec)
    replace_end = prev_partner_comment if prev_partner_comment != -1 else html.rfind('<section', 0, next_sec)

    page_html = html[:replace_start] + tech_section + "\n    " + html[replace_end:]

    # Set tab-about inactive and tab-technology active
    page_html = page_html.replace('id="tab-about" class="tab-content active"', 'id="tab-about" class="tab-content"')
    page_html = page_html.replace('id="tab-products" class="tab-content active"', 'id="tab-products" class="tab-content"')
    page_html = page_html.replace('id="nav-about" role="tab" aria-selected="true"', 'id="nav-about" role="tab" aria-selected="false"')
    page_html = page_html.replace('id="mobile-nav-about" role="tab" aria-selected="true"', 'id="mobile-nav-about" role="tab" aria-selected="false"')

    page_html = page_html.replace('id="nav-technology" role="tab" aria-selected="false"', 'id="nav-technology" role="tab" aria-selected="true"')
    page_html = page_html.replace('id="mobile-nav-technology" role="tab" aria-selected="false"', 'id="mobile-nav-technology" role="tab" aria-selected="true"')

    # 確保導覽列「技術」連結一律指向 technology/tyzor/
    page_html = page_html.replace('href="technology/" id="nav-technology"', 'href="technology/tyzor/" id="nav-technology"')
    page_html = page_html.replace('href="technology/" id="mobile-nav-technology"', 'href="technology/tyzor/" id="mobile-nav-technology"')

    # 確保 nav-technology 與 mobile-nav-technology 顯示 active 高亮樣式
    page_html = re.sub(
        r'id="nav-about" role="tab" aria-selected="false"\s+class="nav-btn [^"]*"',
        'id="nav-about" role="tab" aria-selected="false"\n                   class="nav-btn text-slate-700 hover:text-blue-900 border-b-2 border-transparent hover:border-gray-400 px-1 pt-1 h-16 inline-flex items-center"',
        page_html
    )
    page_html = re.sub(
        r'id="nav-technology" role="tab" aria-selected="true" aria-controls="tab-technology"\s+class="nav-btn [^"]*"',
        'id="nav-technology" role="tab" aria-selected="true" aria-controls="tab-technology"\n                   class="nav-btn text-blue-950 f-weight-bold border-b-2 border-blue-900 px-1 pt-1 h-16 inline-flex items-center"',
        page_html
    )
    page_html = re.sub(
        r'id="mobile-nav-about" role="tab" aria-selected="false"\s+class="mobile-nav-btn [^"]*"',
        'id="mobile-nav-about" role="tab" aria-selected="false"\n               class="mobile-nav-btn flex-1 py-1.5 px-2 text-center rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-100 transition-all"',
        page_html
    )
    page_html = re.sub(
        r'id="mobile-nav-technology" role="tab" aria-selected="true"\s+class="mobile-nav-btn [^"]*"',
        'id="mobile-nav-technology" role="tab" aria-selected="true"\n               class="mobile-nav-btn flex-1 py-1.5 px-2 text-center rounded-lg text-xs font-bold transition-all bg-blue-900 text-white shadow-xs"',
        page_html
    )

    # 快取版本破壞
    page_html = re.sub(r'css/output\.css\?v=[^"]*', f'css/output.css?v={CACHE_VERSION}', page_html)
    page_html = re.sub(r'css/style\.css\?v=[^"]*', f'css/style.css?v={CACHE_VERSION}', page_html)
    page_html = re.sub(r'js/([^"]+?\.js)\?v=[^"]*', rf'js/\1?v={CACHE_VERSION}', page_html)

    # 確保注入 pdf.min.js
    if 'js/vendor/pdf.min.js' not in page_html:
        page_html = page_html.replace(
            '<script src="js/technology.js',
            '<script src="js/vendor/pdf.min.js"></script>\n    <script src="js/technology.js'
        )

    # Update Title (產品類別名稱), Meta Description & Canonical
    page_title = f"{item['menu_name']} | 宏威應用材料 ATTech Materials"
    page_html = re.sub(r'<title[^>]*>.*?</title>', f'<title id="web-title">{page_title}</title>', page_html)
    page_html = re.sub(r'<meta\s+name="description"\s+content="[^"]*"', f'<meta name="description" content="{meta_desc}"', page_html)
    page_html = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"', f'<link rel="canonical" href="{canonical_url}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"', f'<meta property="og:title" content="{page_title}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:url"\s+content="[^"]*"', f'<meta property="og:url" content="{canonical_url}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"', f'<meta property="og:description" content="{meta_desc}"', page_html)

    # Set data-tech-slug on body
    page_html = page_html.replace('<body class="', f'<body data-tech-slug="{slug}" class="')

    # 完全移除舊版全螢幕燈箱視窗 HTML (若存在)
    if 'id="tech-image-modal"' in page_html:
        m_start = page_html.find('<!-- ==========================================\n         技術專頁：原廠技術圖表全螢幕燈箱')
        if m_start == -1:
            m_start = page_html.find('<div id="tech-image-modal"')
        m_end = page_html.find('</body>', m_start)
        if m_start != -1 and m_end != -1:
            page_html = page_html[:m_start] + page_html[m_end:]

    return page_html

def build_all():
    # 優先調用 Node.js 建置腳本 (以 js/technology.js 為唯一真實來源)
    node_script = os.path.join(ROOT_DIR, 'scripts', 'build_technology_subpages.js')
    if os.path.exists(node_script):
        import subprocess
        subprocess.run(["node", node_script], cwd=ROOT_DIR, check=True)
        return

    global TECH_DATABASE
    print("==================================================")
    print("🚀 ATTech 技術專區 - 一鍵全自動同步與建置流程")
    print("==================================================")

    # 1. 自動檢查並從 techdatadb/技術文件摘要與重點.md 萃取最新資料庫
    md_file = os.path.join(ROOT_DIR, 'techdatadb', '技術文件摘要與重點.md')
    if os.path.exists(md_file):
        try:
            from build_tech_json import build_database_from_md
            print("📦 [1/4] 自動從技術文件摘要提取最新資料庫 (build_tech_json)...")
            TECH_DATABASE = build_database_from_md()
        except Exception as e:
            print(f"⚠️ 解析 markdown 失敗，使用現有 JSON: {e}")
            if os.path.exists(JSON_PATH):
                with open(JSON_PATH, "r", encoding="utf-8") as f:
                    TECH_DATABASE = json.load(f)
    elif os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            TECH_DATABASE = json.load(f)

    print("📄 [2/4] 開始建置 11 大特用化學品獨立技術分頁（五大維度一覽）...")
    with open(os.path.join(ROOT_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        template_shell = f.read()

    # 2. 產生 11 個獨立子頁面資料夾與 index.html
    for item in TECH_ITEMS:
        slug = item["slug"]
        sub_dir = os.path.join(ROOT_DIR, 'technology', slug)
        os.makedirs(sub_dir, exist_ok=True)
        sub_file = os.path.join(sub_dir, 'index.html')

        sub_html = build_full_tech_page_html(item, template_shell, is_index=False)
        with open(sub_file, 'w', encoding='utf-8') as sf:
            sf.write(sub_html)
        print(f"  [SUBPAGE] 建立獨立分頁: technology/{slug}/index.html ({len(sub_html)} bytes, has_data={item['has_data']})")

    # 2. 產生 technology/index.html (自動即時轉向至 technology/tyzor/)
    redirect_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=tyzor/">
    <link rel="canonical" href="https://www.attech.com.tw/technology/tyzor/">
    <title>技術專區 | 宏威應用材料 ATTech Materials</title>
    <script>
        (function () {
            var baseHref = '/';
            if (window.location.hostname.endsWith('github.io')) {
                var repo = window.location.pathname.split('/').filter(Boolean)[0];
                if (repo) baseHref = '/' + repo + '/';
            }
            var target = baseHref + 'technology/tyzor/' + window.location.search + window.location.hash;
            window.location.replace(target);
        })();
    </script>
</head>
<body style="background:#f8fafc;font-family:system-ui,-apple-system,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;padding:20px;box-sizing:border-box;">
    <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:32px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);text-align:center;max-width:420px;width:100%;">
        <div style="width:48px;height:48px;border-radius:12px;background:#eff6ff;color:#1e3a8a;display:flex;align-items:center;justify-content:center;margin:0 auto 16px auto;font-size:24px;font-weight:bold;">AT</div>
        <h2 style="color:#0f172a;font-size:18px;margin:0 0 8px 0;font-weight:700;">前往技術專區</h2>
        <p style="color:#64748b;font-size:14px;margin:0 0 20px 0;line-height:1.6;">頁面正在自動導向至 Tyzor® 鈦酸酯與鋯酸酯技術專頁...</p>
        <a href="tyzor/" style="display:inline-block;background:#1e3a8a;color:#ffffff;text-decoration:none;padding:10px 24px;border-radius:10px;font-size:14px;font-weight:600;">直接點擊前往</a>
    </div>
</body>
</html>
'''
    with open(os.path.join(ROOT_DIR, 'technology', 'index.html'), 'w', encoding='utf-8') as mf:
        mf.write(redirect_html)
    print(f"  [MAIN] 更新技術專區自動轉向頁: technology/index.html")

    # 3. 同步更新根目錄 index.html 的 tab-technology
    sync_root_index_technology()

    # 4. 同步更新 sitemap.xml
    update_sitemap()

    # 5. 自動同步最新版型與資料庫至 js/technology.js (方案 A：單一事實來源)
    sync_to_technology_js()

    print("🎉 11 項技術獨立分頁與前端 JS 已全部同步建置完成！")

def sync_to_technology_js():
    """
    自動同步至 js/technology.js (方案 A：單一事實來源)
    1. 同步 TECH_DATABASE 資料庫 (與 json/tech_database.json 保持完全一致)
    2. 自動提取 build_single_doc_layout_html 的右欄底部自訂區塊 (如諮詢動作列)，同步至 js/technology.js
    3. 自動同步 build_empty_tab_html 的底部動作按鈕
    """
    js_path = os.path.join(ROOT_DIR, "js", "technology.js")
    if not os.path.exists(js_path):
        return

    with open(js_path, "r", encoding="utf-8") as f:
        js_code = f.read()

    # 1. 同步 TECH_DATABASE 資料庫
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            tech_db = json.load(f)
        db_json_str = json.dumps(tech_db, ensure_ascii=False, indent=2)
        new_db_decl = f"const TECH_DATABASE = {db_json_str};\n"

        start_marker = "const TECH_DATABASE = {"
        start_idx = js_code.find(start_marker)
        if start_idx != -1:
            end_marker = "const TechState = {"
            end_idx = js_code.find(end_marker, start_idx)
            if end_idx != -1:
                js_code = js_code[:start_idx] + new_db_decl + js_code[end_idx:]

    # 2. 同步 build_single_doc_layout_html 的右欄底部附加內容 (例如諮詢動作列)
    with open(__file__, "r", encoding="utf-8") as pf:
        py_code = pf.read()

    py_marker_start = '<!-- 適用範疇標籤 -->'
    py_pos = py_code.find(py_marker_start)
    if py_pos != -1:
        div_end = py_code.find('</div>\n                </div>', py_pos)
        if div_end != -1:
            div_end += len('</div>\n                </div>')
            py_col_end = py_code.find("</div>\n        </div>'''", div_end)
            if py_col_end != -1:
                extra_block = py_code[div_end:py_col_end].strip()
                js_extra = ""
                if extra_block:
                    converted = extra_block
                    converted = re.sub(r'\{urllib\.parse\.quote\([^\)]+\)\}', '${inquiryParam}', converted)
                    converted = re.sub(r'\{item\[["\']product_link["\']\]\}', '${productLink}', converted)
                    converted = re.sub(r'\{item\[["\']product_link_text["\']\]\}', '${productLinkText}', converted)
                    converted = re.sub(r'\{item\[["\']menu_name["\']\]\}', '${cat.name}', converted)
                    converted = re.sub(r'\{doc\.get\(["\']title["\']\)\}', '${docTitleClean}', converted)
                    converted = re.sub(r'\{doc\.get\(["\']desc["\'][^\)]*\)\}', '${doc.desc || ""}', converted)
                    js_extra = "\n\n                " + "\n                ".join(converted.split("\n"))

                js_app_marker = '<!-- 適用範疇標籤 -->'
                js_app_pos = js_code.find(js_app_marker)
                if js_app_pos != -1:
                    js_app_end = js_code.find("` : ''}", js_app_pos)
                    if js_app_end != -1:
                        js_app_end += len("` : ''}")
                        js_target_end = js_code.find('</div>\n        </div>\n    `;', js_app_end)
                        if js_target_end != -1:
                            js_code = js_code[:js_app_end] + js_extra + "\n            " + js_code[js_target_end:]

    # 3. 同步 build_empty_tab_html 動作按鈕列
    empty_marker = 'def build_empty_tab_html'
    empty_pos = py_code.find(empty_marker)
    if empty_pos != -1:
        btn_start_marker = '<div class="pt-1 flex items-center justify-center gap-2.5">'
        b_pos = py_code.find(btn_start_marker, empty_pos)
        if b_pos != -1:
            b_end = py_code.find("</div>\n        </div>'''", b_pos)
            if b_end != -1:
                b_block = py_code[b_pos:b_end].strip()
                b_converted = b_block
                b_converted = re.sub(r'\{urllib\.parse\.quote\([^\)]+\)\}', '${inquiryParam}', b_converted)
                b_converted = re.sub(r'\{item\[["\']product_link["\']\]\}', '${productLink}', b_converted)
                b_converted = re.sub(r'\{item\[["\']menu_name["\']\]\}', '${catName}', b_converted)

                js_empty_func = 'function buildEmptyTabHtml'
                j_pos = js_code.find(js_empty_func)
                if j_pos != -1:
                    j_b_start = js_code.find(btn_start_marker, j_pos)
                    if j_b_start != -1:
                        j_b_end = js_code.find('</div>\n        </div>\n    `;', j_b_start)
                        if j_b_end != -1:
                            js_code = js_code[:j_b_start] + b_converted + "\n        " + js_code[j_b_end:]

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_code)
    print("  [SYNC] ✅ 已自動將最新版型與資料庫同步至 js/technology.js！")

def sync_root_index_technology():
    root_index_path = os.path.join(ROOT_DIR, 'index.html')
    with open(root_index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 確保導覽列指至 technology/tyzor/
    html = html.replace('href="technology/" id="nav-technology"', 'href="technology/tyzor/" id="nav-technology"')
    html = html.replace('href="technology/" id="mobile-nav-technology"', 'href="technology/tyzor/" id="mobile-nav-technology"')

    # 確保快取版本破壞
    html = re.sub(r'css/output\.css\?v=[^"]*', f'css/output.css?v={CACHE_VERSION}', html)
    html = re.sub(r'css/style\.css\?v=[^"]*', f'css/style.css?v={CACHE_VERSION}', html)
    html = re.sub(r'js/([^"]+?\.js)\?v=[^"]*', rf'js/\1?v={CACHE_VERSION}', html)

    # 確保引入 pdf.min.js
    if 'js/vendor/pdf.min.js' not in html:
        html = html.replace(
            '<script src="js/technology.js',
            '<script src="js/vendor/pdf.min.js"></script>\n    <script src="js/technology.js'
        )

    # 替換 tab-technology
    tyzor_item = TECH_ITEMS[0]
    tyzor_content = build_category_content_section(tyzor_item, active_subtab="principles")
    switcher_html = build_category_switcher("tyzor", is_index=False)
    breadcrumb_item = '''                    <a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <span id="tech-breadcrumb-current" class="text-blue-950 font-bold">鈦酸酯與鋯酸酯 (Tyzor®)</span>'''

    tech_section_inactive = f'''    <!-- Tab: 技術專區 (Technology) - 一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->
    <section id="tab-technology" class="tab-content" role="tabpanel" aria-labelledby="nav-technology">
        <style>
        .tech-layout-container {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
            width: 100%;
        }}
        .tech-sidebar {{
            width: 100%;
            flex-shrink: 0;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        }}
        .tech-sidebar-list {{
            display: flex !important;
            flex-direction: column !important;
            gap: 0.375rem !important;
            width: 100% !important;
        }}
        .tech-sidebar-btn {{
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }}
        .tech-sidebar-btn .min-w-0.flex-1 {{
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-width: 0 !important;
        }}
        .tech-btn-title {{
            display: block !important;
            width: 100% !important;
        }}
        .tech-btn-sub {{
            display: block !important;
            width: 100% !important;
        }}
        .tech-content-main {{
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
        }}
        @media (min-width: 900px) {{
            .tech-layout-container {{
                flex-direction: row;
                gap: 1.25rem;
                align-items: flex-start;
            }}
            .tech-sidebar {{
                width: 310px;
                position: sticky;
                top: 5rem;
                max-height: calc(100vh - 5.5rem);
                display: flex;
                flex-direction: column;
                overflow-y: auto;
            }}
            .tech-sidebar::-webkit-scrollbar {{
                width: 4px;
            }}
            .tech-sidebar::-webkit-scrollbar-track {{
                background: #f8fafc;
            }}
            .tech-sidebar::-webkit-scrollbar-thumb {{
                background: #cbd5e1;
                border-radius: 4px;
            }}
        }}
        /* 瀏覽器書籤風格容器與標籤列 */
        .tech-bookmark-wrapper {{
            width: 100%;
            margin-top: 0.5rem;
            position: relative;
        }}
        .tech-subtab-strip {{
            display: flex;
            align-items: flex-end;
            gap: 0.375rem;
            padding-left: 0.5rem;
            margin-bottom: -1px;
            position: relative;
            z-index: 10;
        }}
        @media (max-width: 640px) {{
            .tech-subtab-strip {{
                overflow-x: auto;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 1px;
            }}
            .tech-subtab-strip::-webkit-scrollbar {{
                display: none;
            }}
        }}
        .tech-subtab-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.375rem;
            padding: 0.625rem 1.125rem 0.5rem 1.125rem;
            border-top-left-radius: 0.625rem !important;
            border-top-right-radius: 0.625rem !important;
            border-bottom-left-radius: 0 !important;
            border-bottom-right-radius: 0 !important;
            border: 1px solid #cbd5e1 !important;
            border-bottom: 1px solid #cbd5e1 !important;
            background: #f1f5f9 !important;
            color: #475569 !important;
            font-size: 0.8125rem;
            font-weight: 600;
            line-height: 1.2;
            white-space: nowrap;
            cursor: pointer;
            transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
            position: relative;
            z-index: 5;
            margin-bottom: 0;
        }}
        .tech-subtab-btn:hover {{
            background: #e2e8f0 !important;
            color: #0f172a !important;
        }}
        .tech-subtab-btn.active {{
            background: #ffffff !important;
            color: #1e3a8a !important;
            font-weight: 800 !important;
            border: 1px solid #cbd5e1 !important;
            border-top: 3px solid #1e3a8a !important;
            border-bottom: 2px solid #ffffff !important;
            margin-bottom: -1px !important;
            padding-bottom: calc(0.5rem + 2px) !important;
            position: relative;
            z-index: 20 !important;
            box-shadow: 0 -2px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }}
        .tech-bookmark-body {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 0 0.75rem 0.75rem 0.75rem;
            padding: 1rem;
            position: relative;
            z-index: 1;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }}
        @media (max-width: 640px) {{
            .tech-bookmark-body {{
                border-radius: 0 0 0.75rem 0.75rem;
                padding: 0.75rem;
            }}
        }}
        /* 原理維度專用：一塊一塊技術文件切換按鈕 */
        .tech-doc-block-btn {{
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        .tech-doc-block-btn.active {{
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border-color: #1e3a8a !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }}
        /* 核心原理 2-Column Split 左右分欄雙翼佈局 (重要資訊首屏完全可見) */
        .tech-principles-grid {{
            display: grid;
            grid-template-columns: 50% 50%;
            gap: 0.875rem;
            align-items: start;
        }}
        @media (max-width: 900px) {{
            .tech-principles-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        </style>
        <div class="optimized-container px-3 sm:px-4 py-2.5 sm:py-3.5">
            <!-- 頂部麵包屑導航 (極簡緊湊) -->
            <div class="mb-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-slate-500">
                <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
{breadcrumb_item}
            </div>

            <!-- 左右兩欄格局：左側技術分類切換導覽 (條列式)，右側資料顯示區 -->
            <div class="tech-layout-container">
{switcher_html}

                <!-- 右側：資料顯示區 (統一白色風格) -->
                <main class="tech-content-main">
                    <div id="tech-content-display">
{tyzor_content}
                    </div>
                </main>
            </div>
        </div>
    </section>'''

    sec_start = html.find('id="tab-technology"')
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    if prev_comment != -1:
        while True:
            prev = html.rfind(comment_marker, 0, prev_comment)
            if prev != -1 and html[prev:prev_comment].strip().startswith('<!-- Tab: 技術專區'):
                prev_comment = prev
            else:
                break
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)

    next_sec = html.find('id="tab-partners"')
    prev_partner_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, next_sec)
    replace_end = prev_partner_comment if prev_partner_comment != -1 else html.rfind('<section', 0, next_sec)

    if replace_start != -1 and replace_end != -1:
        html = html[:replace_start] + tech_section_inactive + "\n\n        " + html[replace_end:]

    with open(root_index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  [ROOT] 同步更新 root index.html 中的導覽列連結、JS 版本號與 tab-technology 緊湊佈局")

def update_sitemap():
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        return
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        xml = f.read()

    added_urls = []
    main_tech_url = f"{DOMAIN}/technology/"
    if f"<loc>{main_tech_url}</loc>" not in xml:
        added_urls.append(main_tech_url)

    for item in TECH_ITEMS:
        url = f"{DOMAIN}/technology/{item['slug']}/"
        if f"<loc>{url}</loc>" not in xml:
            added_urls.append(url)

    if added_urls:
        about_loc = f"<loc>{DOMAIN}/about/</loc>"
        pos = xml.find(about_loc)
        if pos != -1:
            end_url_pos = xml.find('</url>', pos) + len('</url>')
            new_blocks = []
            for u in added_urls:
                block = f'''
    <url>
        <loc>{u}</loc>
        <lastmod>2026-10-06</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.85</priority>
    </url>'''
                new_blocks.append(block)
            xml = xml[:end_url_pos] + "".join(new_blocks) + xml[end_url_pos:]
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(xml)
            print(f"✅ 已在 sitemap.xml 中加入 {len(added_urls)} 個獨立技術子分頁 URL！")

if __name__ == '__main__':
    build_all()
