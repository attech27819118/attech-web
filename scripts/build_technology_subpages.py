# -*- coding: utf-8 -*-
"""
Build Technology Subpages & Technology Index
為 11 大特用化學品產品線建立獨立技術專頁 (Independent Subpages)，
無資料者呈現高質感「暫無資料」看板與專屬諮詢通道。
完全移除 URL Hash，符合 Google Search Console 索引需求。
畫面與彈窗依視窗大小自動最適化。
"""

import os
import sys
import re
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.attech.com.tw"

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
        "meta_desc": "宏威應用材料 Dorf Ketal Tyzor® 有機鈦酸酯與鋯酸酯四大核心技術應用，涵蓋酯化催化劑、油墨塗料交聯劑、玻璃金屬密著促進劑與表面改性方案。",
        "placeholder_subtitle": "",
        "placeholder_text": ""
    },
    {
        "slug": "silane",
        "item_no": "02",
        "menu_name": "Silane / 矽烷偶合劑",
        "menu_sub": "Dynasylan / hydrosil 系列",
        "title_zh": "矽烷偶合劑系列技術應用 (Silane)",
        "title_en": "Silane / 矽烷偶合劑",
        "category_name": "矽烷偶合劑 (Silane)",
        "brand_name": "Evonik 原廠專用技術",
        "brand_tag": "Evonik / 特化",
        "product_link": "products/others/silane/",
        "product_link_text": "瀏覽 24 款矽烷規格",
        "description": "矽烷分子具備有機與無機雙重反應性端基，扮演「分子橋樑」角色，廣泛應用於水性塗料改性、玻璃/金屬/填料表面處理、防腐底漆及密封膠交聯。",
        "has_data": False,
        "inquiry_param": "Silane-Technology",
        "meta_desc": "宏威應用材料矽烷偶合劑系列技術專題，包含 Dynasylan 與 Hydrosil 水性及溶劑型矽烷之無機/有機介面架橋、玻璃金屬表面處理與水解縮合應用指引。",
        "placeholder_subtitle": "矽烷水解縮合機理與各底材配方比較表整理中",
        "placeholder_text": "本專題之原廠技術資料、水解工藝說明與填料表面處理數據目前正在編整中，暫無公開資料。如需特定樹脂（如水性 PU、環氧重防腐）之添加比例與催化指引，歡迎直接聯繫技術團隊。"
    },
    {
        "slug": "chain",
        "item_no": "03",
        "menu_name": "Chain Extender / 擴鏈劑",
        "menu_sub": "Unilink & Clearlink 系列",
        "title_zh": "擴鏈劑高性能彈性體改性技術 (Chain Extender)",
        "title_en": "Chain Extender / 擴鏈劑",
        "category_name": "擴鏈劑 (Chain Extender)",
        "brand_name": "Dorf Ketal 原廠專用技術",
        "brand_tag": "Dorf Ketal",
        "product_link": "products/dorfketal/chain/",
        "product_link_text": "瀏覽擴鏈劑規格",
        "description": "專為聚脲 (Polyurea)、聚氨酯 (Polyurethane) 與環氧樹脂體系開發之受阻二胺擴鏈劑，精準調控凝膠固化速度，賦予彈性體優異的機械強度與耐黃變性能。",
        "has_data": False,
        "inquiry_param": "Chain-Extender",
        "meta_desc": "宏威應用材料 Dorf Ketal Unilink & Clearlink 系列受阻二胺擴鏈劑技術專題，適用於噴塗聚脲、彈性體改性與聚氨酯固化速度調控。",
        "placeholder_subtitle": "聚脲/聚氨酯擴鏈配方動力學曲線與比較指引整理中",
        "placeholder_text": "本專題之原廠動力學反應曲線、凝膠時間對照表與高低溫拉伸強度測試資料整理中，暫無公開資料。如需特定受阻胺反應速率、配比或固化試樣，歡迎聯繫宏威工程師。"
    },
    {
        "slug": "carbon-black",
        "item_no": "04",
        "menu_name": "Special Carbon Black",
        "menu_sub": "特級碳黑 / 導電碳黑",
        "title_zh": "特級碳黑高黑度與色相調控技術 (Carbon Black)",
        "title_en": "Special Carbon Black / 特級碳黑",
        "category_name": "特級碳黑 (Carbon Black)",
        "brand_name": "Orion Engineered Carbons 原廠技術",
        "brand_tag": "Orion",
        "product_link": "products/orion/coating/",
        "product_link_text": "瀏覽 40+ 款 Orion 碳黑",
        "description": "全球領先特級碳黑，藉由精密原生粒徑、聚集體結構及化學氧化表面改性，在塗料與油墨中實現極致黑度 (Jetness)、純藍底色相 (Bluish Undertone) 及超低研磨黏度。",
        "has_data": False,
        "inquiry_param": "CarbonBlack-Tech",
        "meta_desc": "宏威應用材料 Orion 特級碳黑技術專題，解析原生粒徑、表面化學改性對塗料油墨黑度 (Jetness)、純藍底相與流變黏度之影響機理。",
        "placeholder_subtitle": "特級碳黑黑度 (My) 與色相 (dM) 分佈及分散機理圖整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。如需特級碳黑原生粒徑分佈、研磨分散設備推薦、高色素碳黑藍底相調校或導電碳黑配方指引，歡迎洽詢宏威技術諮詢。"
    },
    {
        "slug": "wax",
        "item_no": "05",
        "menu_name": "Micronized Wax / 微粉蠟",
        "menu_sub": "PTFE 取代 / 耐磨耐刮助劑",
        "title_zh": "微粉化蠟極致耐磨耐刮與抗擦傷技術 (Micronized Wax)",
        "title_en": "Micronized Wax / 微粉蠟",
        "category_name": "微粉蠟 (Micronized Wax)",
        "brand_name": "Micro Powders (MPI) 原廠技術",
        "brand_tag": "Micro Powders",
        "product_link": "products/mpi/ptfe/",
        "product_link_text": "瀏覽微粉蠟與 PTFE 替代方案",
        "description": "美國 Micro Powders 微米級表面改性助劑，針對木器漆、卷材塗料、油墨及工業塗料，提供卓越的耐刮擦性、平滑爽滑感及抗黏連性，具備完整無氟 PTFE-Free 解決方案。",
        "has_data": False,
        "inquiry_param": "MPI-Wax-Tech",
        "meta_desc": "宏威應用材料 Micro Powders (MPI) 微粉蠟技術專題，涵蓋高滑爽抗刮性、消光手感調控及合規無氟 PTFE 取代 (PTFE-Free) 系列完整解決方案。",
        "placeholder_subtitle": "微粉蠟耐刮耐磨機理與各塗層體系添加對比整理中",
        "placeholder_text": "原廠微粉蠟滑爽度測試數據、Taber 耐磨對比圖及無氟 PTFE 替代樣品評估資料正在整理中，暫無公開資料。如需索取測試樣品或配方諮詢，請與我們聯繫。"
    },
    {
        "slug": "matting",
        "item_no": "06",
        "menu_name": "Matting Agent / 消光粉",
        "menu_sub": "二氧化矽 / 表面處理消光",
        "title_zh": "二氧化矽精密消光與表面紋理調控 (Matting Agent)",
        "title_en": "Matting Agent / 消光粉",
        "category_name": "消光粉 (Matting Agent)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/matting_agent/",
        "product_link_text": "瀏覽消光粉規格",
        "description": "沉澱法與凝膠法精密二氧化矽消光粉，嚴格控制孔隙率與粒徑分佈，兼顧極致消光效率、高透明度與漆膜平滑手感，廣泛適用於皮革漆、木器漆與工業烤漆。",
        "has_data": False,
        "inquiry_param": "Matting-Agent-Tech",
        "meta_desc": "宏威應用材料二氧化矽消光粉技術專題，包含有機表面處理與無處理消光粉之吸油量、孔隙率、重塗附著力及防沉降流變技術指南。",
        "placeholder_subtitle": "二氧化矽消光機理、孔容吸油量與手感評估圖整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。如需比較德固賽 Acematt 系列、孔容與吸油量檢驗報告或薄塗高透消光粉樣品，歡迎向宏威團隊索取。"
    },
    {
        "slug": "maleic",
        "item_no": "07",
        "menu_name": "Maleic Resin / 馬林酸樹脂",
        "menu_sub": "松香改性馬林酸樹脂",
        "title_zh": "馬林酸樹脂快乾高光與環保醇溶改性技術 (Maleic Resin)",
        "title_en": "Maleic Resin / 馬林酸樹脂",
        "category_name": "馬林酸樹脂 (Maleic Resin)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/maleic_acid_resin/",
        "product_link_text": "瀏覽馬林酸樹脂規格",
        "description": "精選松香改性馬林酸樹脂，具備優異的醇溶性、快乾性、高硬度與高光澤度，特別適用於凹版印刷油墨、水基光油、硝基木器漆及熱熔膠改性體系。",
        "has_data": False,
        "inquiry_param": "Maleic-Resin-Tech",
        "meta_desc": "宏威應用材料松香改性馬林酸樹脂技術專題，提供醇溶型與酯溶型馬林酸樹脂之酸價、軟化點、快乾高光澤與油墨顏料潤濕技術方案。",
        "placeholder_subtitle": "馬林酸樹脂酸價、軟化點與溶劑釋放性圖譜整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。如需了解各型號馬林酸樹脂在乙醇/醋酸乙酯體系中之溶解度、黏度穩定性或索取樣品，歡迎洽詢。"
    },
    {
        "slug": "adhesion",
        "item_no": "08",
        "menu_name": "Adhesion Resin / 密著樹脂",
        "menu_sub": "氯化聚烯烴 (CPO) & 非氯系",
        "title_zh": "密著促進劑與難附著非極性底材架橋技術 (Adhesion Promoters)",
        "title_en": "Adhesion Resin / 密著樹脂",
        "category_name": "密著促進劑 (Adhesion)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/adhesion_promoter/",
        "product_link_text": "瀏覽密著促進劑規格",
        "description": "提供氯化聚烯烴 (CPO) 與環保非氯系密著促進樹脂，專為 PP、BOPP、TPO 等難附著塑膠與金屬底材設計，大幅提升塗層耐水煮、耐刮耐磨與熱封附著強度。",
        "has_data": False,
        "inquiry_param": "Adhesion-Promoter-Tech",
        "meta_desc": "宏威應用材料密著促進劑技術專題，涵蓋氯化聚烯烴 CPO 與非氯系架橋樹脂，解決 PP、BOPP、鋁箔與複合膜之難附著、耐水煮與百格測試脫落問題。",
        "placeholder_subtitle": "非極性塑膠底材 (PP/PE) 介面結合與附著促進機理圖整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。若您面臨汽車保險桿改性、PP 免底漆直塗、油墨耐水煮剝離等附著力瓶頸，歡迎直接預約配方評估。"
    },
    {
        "slug": "powder",
        "item_no": "09",
        "menu_name": "Powder Coating Additive",
        "menu_sub": "粉體塗料專用功能性助劑",
        "title_zh": "粉體塗料專用功能性紋理與消光助劑技術 (Powder Additives)",
        "title_en": "Powder Additives / 粉體助劑",
        "category_name": "粉體塗料助劑 (Powder Additives)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/coating_additive/",
        "product_link_text": "瀏覽粉體塗料助劑規格",
        "description": "專為戶外與工業粉體塗料開發之多功能助劑，涵蓋砂紋劑、戶外物理/化學消光劑、附著力增進劑與表面流平增硬劑，在高溫烘烤下維持優異重現性與耐候性。",
        "has_data": False,
        "inquiry_param": "Powder-Additive-Tech",
        "meta_desc": "宏威應用材料粉體塗料功能性助劑技術專題，包含戶外純聚酯消光劑、高重現性砂紋紋理劑、流平劑與基材附著力改進技術方案。",
        "placeholder_subtitle": "粉體塗料烘烤固化紋理形成機理與消光配方建議整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。如需聚酯/TGIC、聚酯/HAA 或環氧體系之戶外耐候消光數據或砂紋紋理調配手冊，歡迎洽詢宏威工程師。"
    },
    {
        "slug": "px",
        "item_no": "10",
        "menu_name": "PX Lubricant Additives",
        "menu_sub": "潤滑油添加劑 (原 ExxonMobil)",
        "title_zh": "PX 潤滑油特用抗磨與熱氧化穩定添加劑 (PX Lubricants)",
        "title_en": "PX Lubricants / 潤滑油添加劑",
        "category_name": "PX 潤滑油添加劑",
        "brand_name": "Dorf Ketal (原 ExxonMobil) 原廠技術",
        "brand_tag": "Dorf Ketal",
        "product_link": "products/dorfketal/px/",
        "product_link_text": "瀏覽 PX 潤滑油添加劑",
        "description": "承襲原 ExxonMobil 核心化學配方，PX 系列專用添加劑提供優異的極壓抗磨、清淨分散與高溫抗氧化性，滿足車用引擎、工業齒輪及高精度金屬加工液嚴苛規範。",
        "has_data": False,
        "inquiry_param": "PX-Lubricant-Tech",
        "meta_desc": "宏威應用材料 PX 潤滑油添加劑技術專題 (原 ExxonMobil 產品線)，涵蓋極壓抗磨劑、高溫抗氧劑、金屬鈍化劑與工業齒輪油複合配方手冊。",
        "placeholder_subtitle": "潤滑添加劑高溫高壓抗磨 (Four-Ball / Timken) 機理評估表整理中",
        "placeholder_text": "原廠高溫四球極壓測試 (Four-Ball EP)、Timken 抗磨負載曲線與金屬加工液相容性資料整理中，暫無公開資料。如需索取特定牌號潤滑添加劑規格，請隨時聯絡。"
    },
    {
        "slug": "polyester",
        "item_no": "11",
        "menu_name": "Polyester Resin / 聚酯樹脂",
        "menu_sub": "聚酯樹脂 (DYNAPOL/DYNACOLL替代品)",
        "title_zh": "飽和共聚聚酯樹脂與多元醇技術應用 (Polyester Resin)",
        "title_en": "Polyester Resin / 聚酯樹脂",
        "category_name": "聚酯樹脂 (Polyester Resin)",
        "brand_name": "特用化學品技術專區",
        "brand_tag": "其他特化",
        "product_link": "products/others/polyester_resin/",
        "product_link_text": "瀏覽 37 款聚酯規格",
        "description": "高分子量共聚聚酯與特用多元醇，專為卷材塗料、罐頭塗料、軟包裝複合膠與 PUR 熱熔膠開發，具備與 DYNAPOL® / DYNACOLL® 同級之抗深衝延伸率、耐熱性與 FDA 食品接觸符合性。",
        "has_data": False,
        "inquiry_param": "Polyester-Resin-Tech",
        "meta_desc": "宏威應用材料飽和共聚聚酯樹脂技術專題，同級 DYNAPOL® 與 DYNACOLL® 替代方案，適用於金屬卷材烤漆、食品罐內外塗料、軟包裝複合膠與 PUR 熱熔膠。",
        "placeholder_subtitle": "共聚聚酯玻璃化轉變溫度 (Tg) 與柔韌深衝性能關聯圖整理中",
        "placeholder_text": "原廠技術資料整理中，暫無公開資料。如需 DYNAPOL / DYNACOLL 替代型號比較表、FDA 食品接觸認證或 PUR 熱熔膠初黏力曲線，歡迎洽詢宏威技術團隊。"
    }
]

def build_category_switcher(current_slug, is_index=False):
    """
    建立 11 個產品系列分類切換列 (統一純白高雅風格，條列式清晰呈現)。
    """
    cards_html = []
    for item in TECH_ITEMS:
        slug = item["slug"]
        is_active = (slug == current_slug)
        url = f"technology/{slug}/"
        item_no = item.get("item_no", "01")
        menu_name = item.get("menu_name", item["category_name"])
        menu_sub = item.get("menu_sub", item["brand_tag"])

        if is_active:
            card = f'''                        <a href="{url}" class="group flex items-center p-3 rounded-xl bg-blue-50/90 border-2 border-blue-600/80 text-blue-950 no-underline shadow-xs transition-all">
                            <div class="flex items-center gap-2.5 min-w-0 w-full">
                                <span class="w-6 h-6 rounded-md bg-blue-900 text-white text-xs font-black flex items-center justify-center shrink-0 shadow-2xs">
                                    {item_no}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="text-xs sm:text-sm font-extrabold text-blue-950 truncate leading-snug">
                                        {menu_name}
                                    </div>
                                    <div class="text-[11px] font-semibold text-blue-800/80 truncate">
                                        {menu_sub}
                                    </div>
                                </div>
                            </div>
                        </a>'''
        else:
            card = f'''                        <a href="{url}" class="group flex items-center p-3 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-blue-400 text-slate-800 hover:text-blue-950 no-underline transition-all">
                            <div class="flex items-center gap-2.5 min-w-0 w-full">
                                <span class="w-6 h-6 rounded-md bg-slate-100 group-hover:bg-blue-50 text-slate-500 group-hover:text-blue-700 text-xs font-bold flex items-center justify-center shrink-0 transition-colors">
                                    {item_no}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="text-xs sm:text-sm font-bold text-slate-800 group-hover:text-blue-950 truncate leading-snug">
                                        {menu_name}
                                    </div>
                                    <div class="text-[11px] font-normal text-slate-500 group-hover:text-slate-600 truncate">
                                        {menu_sub}
                                    </div>
                                </div>
                            </div>
                        </a>'''
        cards_html.append(card)

    return f'''                <!-- 左側：技術專題產品分類 (統一白色風格，條列式清晰呈現) -->
                <aside class="tech-sidebar bg-white rounded-2xl border border-slate-200 p-4 sm:p-5 shadow-xs shrink-0">
                    <div class="flex items-center justify-between pb-3 mb-2.5 border-b border-slate-100">
                        <div class="flex items-center gap-2">
                            <span class="w-2.5 h-6 bg-blue-900 rounded-full inline-block shrink-0"></span>
                            <div>
                                <h2 class="text-sm sm:text-base font-extrabold text-blue-950 leading-tight">
                                    技術分類
                                </h2>
                            </div>
                        </div>
                        
                    </div>
                    <!-- 條列式導覽清單：純單欄垂直條列，寬度充裕不被壓縮 -->
                    <nav class="tech-sidebar-list" aria-label="11大技術專題產品分類導覽">
{chr(10).join(cards_html)}
                    </nav>
                </aside>'''

def build_tyzor_content_section():
    """
    Tyzor 有 4 張高解析原廠技術圖表的完整內容區塊 (含 Lightbox 彈窗)。
    統一白色風格。
    """
    return '''            <!-- Tyzor 鈦酸酯與鋯酸酯四大核心技術應用專題區 (統一白色風格) -->
            <div class="space-y-6">
                <section class="bg-white border border-slate-200 rounded-2xl shadow-xs p-5 sm:p-7 space-y-6">
                    <!-- 專題標題與簡介區 (排版流暢無右側懸空空白) -->
                    <div class="pb-5 border-b border-gray-100 space-y-3">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <div class="space-y-1.5 min-w-0">
                                <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-900 uppercase tracking-wider">
                                    <span class="px-2.5 py-0.5 rounded bg-blue-50 border border-blue-100">Dorf Ketal 原廠專用技術</span>
                                    <span>Tyzor® 系列有機鈦／鋯</span>
                                </div>
                                <h1 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                    <span class="w-2.5 h-6 bg-blue-900 rounded-full inline-block shrink-0"></span>
                                    <span>鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®)</span>
                                </h1>
                            </div>
                            <div class="shrink-0 flex items-center gap-2 sm:gap-3">
                                <a href="products/dorfketal/tyzor/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs sm:text-sm font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 Tyzor 產品</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Tyzor"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs sm:text-sm font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>技術諮詢</span>
                                </a>
                            </div>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 font-normal leading-relaxed pt-0.5 w-full">
                            Tyzor® 有機鈦（鋯）化合物具備高反應性與特殊配位多重功能，針對高分子合成催化、三維網絡交聯、異質基材介面結合力提升及 Sol-Gel 表面改性，提供全面工業化解決方案。
                        </p>
                    </div>
                    <!-- 畫廊縮圖展開區 (Gallery Grid，統一白色卡片) -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5">
                        <!-- 縮圖卡片 1: 催化應用 -->
                        <div class="bg-white border border-slate-200 rounded-xl p-3.5 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <div class="mb-2 pb-2 border-b border-slate-100 flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-bold text-blue-800 tracking-wider">類別一・催化應用</span>
                                    <h3 class="text-sm font-extrabold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為催化劑">鈦（鋯）酸酯作為催化劑</h3>
                                </div>
                            </div>
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-slate-50/50 border border-slate-100 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/catalyst.webp', '鈦（鋯）酸酯作為催化劑 (Tyzor® Catalysts)', 'Tyzor-Catalyst')">
                                <img src="techdata/tyzor/catalyst.webp" alt="鈦（鋯）酸酯作為催化劑"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 2: 交聯改性 -->
                        <div class="bg-white border border-slate-200 rounded-xl p-3.5 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <div class="mb-2 pb-2 border-b border-slate-100 flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-bold text-blue-800 tracking-wider">類別二・交聯改性</span>
                                    <h3 class="text-sm font-extrabold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為交聯劑">鈦（鋯）酸酯作為交聯劑</h3>
                                </div>
                            </div>
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-slate-50/50 border border-slate-100 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/crosslinker.webp', '鈦（鋯）酸酯作為交聯劑 (Tyzor® Crosslinkers)', 'Tyzor-Crosslinker')">
                                <img src="techdata/tyzor/crosslinker.webp" alt="鈦（鋯）酸酯作為交聯劑"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 3: 附著促進 -->
                        <div class="bg-white border border-slate-200 rounded-xl p-3.5 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <div class="mb-2 pb-2 border-b border-slate-100 flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-bold text-blue-800 tracking-wider">類別三・附著促進</span>
                                    <h3 class="text-sm font-extrabold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為密著促進劑">鈦（鋯）酸酯作為密著促進劑</h3>
                                </div>
                            </div>
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-slate-50/50 border border-slate-100 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/adhesion.webp', '鈦（鋯）酸酯作為密著促進劑 (Tyzor® Adhesion Promoters)', 'Tyzor-Adhesion')">
                                <img src="techdata/tyzor/adhesion.webp" alt="鈦（鋯）酸酯作為密著促進劑"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 4: 表面改性 -->
                        <div class="bg-white border border-slate-200 rounded-xl p-3.5 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <div class="mb-2 pb-2 border-b border-slate-100 flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-bold text-blue-800 tracking-wider">類別四・表面改性</span>
                                    <h3 class="text-sm font-extrabold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為表面改性">鈦（鋯）酸酯作為表面改性</h3>
                                </div>
                            </div>
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-slate-50/50 border border-slate-100 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/surface_treatment.webp', '鈦（鋯）酸酯作為表面改性 (Tyzor® Surface Modification)', 'Tyzor-Surface')">
                                <img src="techdata/tyzor/surface_treatment.webp" alt="鈦（鋯）酸酯作為表面改性"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>'''

def build_placeholder_content_section(item):
    """
    為未有原廠技術資料的 10 個產品線建立專業「暫無資料」獨立專頁內容 (統一白色風格)。
    """
    subtitle = item["placeholder_subtitle"] if item["placeholder_subtitle"] else f'{item["category_name"]}技術資料與配方比較表整理中'
    desc = item["placeholder_text"] if item["placeholder_text"] else "原廠技術資料整理中，暫無公開資料。如需具體配方、添加比例、試樣或技術諮詢，歡迎隨時聯繫宏威技術團隊。"
    return f'''            <!-- {item["title_zh"]} 專題獨立專頁 (統一白色風格) -->
            <div class="space-y-6">
                <section class="bg-white border border-slate-200 rounded-2xl shadow-xs p-5 sm:p-7 space-y-6">
                    <!-- 標題與簡介區 (排版流暢無右側懸空空白) -->
                    <div class="pb-5 border-b border-gray-100 space-y-3">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <div class="space-y-1.5 min-w-0">
                                <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-900 uppercase tracking-wider">
                                    <span class="px-2.5 py-0.5 rounded bg-blue-50 border border-blue-100">{item["brand_name"]}</span>
                                    <span>{item["title_en"]}</span>
                                </div>
                                <h1 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                    <span class="w-2.5 h-6 bg-blue-900 rounded-full inline-block shrink-0"></span>
                                    <span>{item["title_zh"]}</span>
                                </h1>
                            </div>
                            <div class="shrink-0 flex items-center gap-2 sm:gap-3">
                                <a href="{item["product_link"]}"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs sm:text-sm font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>{item["product_link_text"]}</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry={item["inquiry_param"]}"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs sm:text-sm font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-flask-vial"></i>
                                    <span>技術諮詢</span>
                                </a>
                            </div>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-600 font-normal leading-relaxed pt-0.5 w-full">
                            {item["description"]}
                        </p>
                    </div>

                    <!-- 專業「暫無資料」展位看板 (統一白色淺灰風格) -->
                    <div class="bg-slate-50/60 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-12 text-center">
                        <div class="max-w-xl mx-auto space-y-4">
                            <!-- 圖示與暫無資料標籤 -->
                            <div class="w-14 h-14 rounded-2xl bg-white border border-slate-200 text-slate-400 flex items-center justify-center mx-auto text-xl shadow-2xs">
                                <i class="fa-solid fa-folder-open text-blue-900"></i>
                            </div>
                            <div>
                                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white border border-slate-200 text-slate-600 text-xs font-semibold mb-2 shadow-2xs">
                                    <span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
                                    <span>原廠技術資料整理中・暫無公開資料</span>
                                </div>
                                <h2 class="text-base sm:text-xl font-bold text-blue-950">
                                    原廠技術資料整理中，暫無公開資料
                                </h2>
                                <p class="text-xs sm:text-sm font-semibold text-slate-500 mt-1">
                                    {subtitle}
                                </p>
                            </div>
                            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-lg mx-auto font-normal">
                                原廠技術資料整理中，暫無公開資料。<br class="hidden sm:inline">
                                {desc}
                            </p>

                            <!-- 行動引導按鈕群 -->
                            <div class="pt-4 flex flex-wrap items-center justify-center gap-3">
                                <a href="contact/?mode=detailed&inquiry={item["inquiry_param"]}"
                                   class="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs sm:text-sm font-bold shadow-xs transition-all active:scale-95">
                                    <i class="fa-solid fa-envelope"></i>
                                    <span>諮詢此品類專案配方</span>
                                </a>
                                <a href="{item["product_link"]}"
                                   class="inline-flex items-center gap-2 px-5 py-2.5 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-2xs">
                                    <i class="fa-solid fa-table-list text-blue-900"></i>
                                    <span>{item["product_link_text"]}</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </section>
            </div>'''

def build_full_tech_page_html(item, template_shell, is_index=False):
    """
    組裝完整的獨立技術專頁 HTML。
    """
    slug = item["slug"]
    title_zh = item["title_zh"]
    meta_desc = item["meta_desc"]
    canonical_url = f"{DOMAIN}/technology/" if is_index else f"{DOMAIN}/technology/{slug}/"

    # Breadcrumb
    breadcrumb_item = f'''                    <a href="technology/" class="hover:text-blue-900 hover:underline">技術專區</a>
                    <i class="fa-solid fa-chevron-right text-xs text-slate-400"></i>
                    <span class="text-blue-950 font-bold">{item["category_name"]}</span>''' if not is_index else '''                    <span class="text-blue-950 font-bold">技術專區</span>'''

    # Build Category Switcher & Content
    switcher_html = build_category_switcher(slug, is_index=is_index)
    if item["has_data"]:
        content_html = build_tyzor_content_section()
    else:
        content_html = build_placeholder_content_section(item)

    # Technology Section Container
    tech_section = f'''    <!-- Tab: 技術專區 (Technology) - 獨立分頁呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->
    <section id="tab-technology" class="tab-content active" role="tabpanel" aria-labelledby="nav-technology">
        <style>
        .tech-layout-container {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
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
            padding: 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        }}
        .tech-sidebar-list {{
            display: flex !important;
            flex-direction: column !important;
            gap: 0.5rem !important;
            width: 100% !important;
        }}
        .tech-content-main {{
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
        }}
        @media (min-width: 1024px) {{
            .tech-layout-container {{
                flex-direction: row;
                gap: 1.75rem;
                align-items: flex-start;
            }}
            .tech-sidebar {{
                width: 370px;
                position: sticky;
                top: 5.5rem;
                max-height: calc(100vh - 6.5rem);
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
        </style>
        <div class="optimized-container px-4 py-8">
            <!-- 頂部麵包屑導航 (字體適中易讀、簡約高雅) -->
            <div class="mb-5 flex flex-wrap items-center gap-2.5 text-sm font-semibold text-slate-500">
                <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                <i class="fa-solid fa-chevron-right text-xs text-slate-400"></i>
{breadcrumb_item}
            </div>

            <!-- 左右兩欄格局：左側技術分類切換導覽 (條列式)，右側資料顯示區 -->
            <div class="tech-layout-container">
{switcher_html}

                <!-- 右側：資料顯示區 (統一白色風格) -->
                <main class="tech-content-main">
{content_html}
                </main>
            </div>
    </section>

    <!-- 技術圖檔全螢幕 Lightbox 放大檢視彈窗 (配合視窗自動調整 100% 完整畫面大小，無下載、保護原廠機密) -->
    <div id="tech-image-modal"
         class="hidden select-none"
         style="position: fixed; inset: 0; z-index: 99999; background: rgba(2, 6, 23, 0.92); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; padding: 12px; box-sizing: border-box; user-select: none;"
         onclick="closeTechImageModal(event)">
        <div style="position: relative; display: flex; flex-direction: column; width: 100%; max-width: 920px; height: calc(100vh - 24px); max-height: calc(100vh - 24px); background: #0f172a; border-radius: 16px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); overflow: hidden; border: 1px solid rgba(51, 65, 85, 0.8); margin: auto;"
             onclick="event.stopPropagation()">
            <!-- Modal Header (高度 48px) -->
            <div style="height: 48px; min-height: 48px; padding: 0 16px; background: #0f172a; color: white; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e293b; flex-shrink: 0; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
                    <i class="fa-solid fa-file-image" style="color: #60a5fa; font-size: 15px; flex-shrink: 0;"></i>
                    <h3 id="tech-image-modal-title" style="font-size: 13px; font-weight: bold; color: white; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 320px;">原廠技術說明圖表</h3>
                    
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                    <!-- 視窗最適化切換 / 放大閱讀按鈕 -->
                    <button type="button" id="tech-modal-zoom-btn" onclick="toggleTechModalZoom()"
                            style="height: 32px; padding: 0 10px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; color: #93c5fd; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.2s;"
                            title="切換檢視模式">
                        <i id="tech-modal-zoom-icon" class="fa-solid fa-magnifying-glass-plus"></i>
                        <span id="tech-modal-zoom-text" class="hidden sm:inline">放大滾動閱讀</span>
                    </button>
                    <button type="button" onclick="closeTechImageModal()"
                            style="width: 32px; height: 32px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; color: #cbd5e1; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;"
                            title="關閉 (ESC)">
                        <i class="fa-solid fa-xmark" style="font-size: 16px;"></i>
                    </button>
                </div>
            </div>
            <!-- Modal Image Body (依視窗高度 100% 完整貼合顯示全圖) -->
            <div id="tech-image-container"
                 style="flex: 1 1 auto; min-height: 0; min-width: 0; width: 100%; height: calc(100% - 96px); padding: 8px; box-sizing: border-box; background: #020617; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                <img id="tech-image-modal-img" src="" alt="技術說明圖"
                     style="max-width: 100%; max-height: calc(100vh - 120px); width: auto; height: auto; object-fit: contain; display: block; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); pointer-events: auto; user-select: none;"
                     oncontextmenu="return false;" draggable="false">
            </div>
            <!-- Modal Footer (高度 48px) -->
            <div style="height: 48px; min-height: 48px; padding: 0 16px; background: #0f172a; border-top: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 11px; color: #94a3b8; flex-shrink: 0;">
                <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" class="hidden sm:inline">宏威應用材料原廠特化技術資料</span>
                <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0; margin-left: auto;">
                    <a id="tech-image-modal-inquiry-btn" href="contact/?mode=detailed"
                       style="padding: 6px 14px; background: #1e3a8a; color: white; border-radius: 8px; font-weight: bold; font-size: 12px; text-decoration: none; display: flex; align-items: center; gap: 6px; transition: background 0.2s;">
                        <i class="fa-solid fa-envelope" style="font-size: 11px;"></i> 技術諮詢
                    </a>
                    <button type="button" onclick="closeTechImageModal()"
                            style="padding: 6px 14px; background: #1e293b; border: 1px solid #334155; color: #cbd5e1; border-radius: 8px; font-size: 12px; cursor: pointer; transition: all 0.2s;">
                        關閉
                    </button>
                </div>
            </div>
        </div>
    </div>'''

    # Replace section in template
    html = template_shell
    sec_start = html.find('id="tab-technology"')
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)

    next_sec = html.find('id="tab-partners"')
    prev_partner_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, next_sec)
    replace_end = prev_partner_comment if prev_partner_comment != -1 else html.rfind('<section', 0, next_sec)

    page_html = html[:replace_start] + tech_section + "\n    " + html[replace_end:]

    # Update Title, Meta Description & Canonical
    page_title = f"{title_zh} | 宏威應用材料 ATTech Materials" if not is_index else "技術專區與應用方案 | 宏威應用材料 ATTech Materials"
    page_html = re.sub(r'<title[^>]*>.*?</title>', f'<title id="web-title">{page_title}</title>', page_html)
    page_html = re.sub(r'<meta\s+name="description"\s+content="[^"]*"', f'<meta name="description" content="{meta_desc}"', page_html)
    page_html = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"', f'<link rel="canonical" href="{canonical_url}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"', f'<meta property="og:title" content="{page_title}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:url"\s+content="[^"]*"', f'<meta property="og:url" content="{canonical_url}"', page_html)
    page_html = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"', f'<meta property="og:description" content="{meta_desc}"', page_html)

    # Update Mega Menu Links: replace technology/#tech-<slug> with technology/<slug>/
    for ti in TECH_ITEMS:
        old_href = f'href="technology/#tech-{ti["slug"]}"'
        new_href = f'href="technology/{ti["slug"]}/"'
        page_html = page_html.replace(old_href, new_href)

    # Update Lightbox Modal script logic
    old_script_pattern = re.compile(r'function openTechImageModal\(.*?(?=</script>)', re.DOTALL)
    new_script_body = '''var isTechModalZoomed = false;

    function openTechImageModal(src, title, inquiryTag) {
        var modal = document.getElementById('tech-image-modal');
        var img = document.getElementById('tech-image-modal-img');
        var titleEl = document.getElementById('tech-image-modal-title');
        var inqBtn = document.getElementById('tech-image-modal-inquiry-btn');
        if (!modal || !img) return;

        // Reset to full-page fit view by default
        isTechModalZoomed = false;
        applyTechModalZoomState();

        img.src = src;
        if (titleEl && title) titleEl.textContent = title;
        if (inqBtn) {
            inqBtn.href = 'contact/?mode=detailed' + (inquiryTag ? '&inquiry=' + encodeURIComponent(inquiryTag) : '');
        }
        modal.style.display = 'flex';
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeTechImageModal(e) {
        if (e && e.target && e.target.closest && e.target.closest('#tech-image-modal > div')) {
            // Click inside dialog
            return;
        }
        var modal = document.getElementById('tech-image-modal');
        if (!modal) return;
        modal.style.display = 'none';
        modal.classList.add('hidden');
        document.body.style.overflow = '';
        var img = document.getElementById('tech-image-modal-img');
        if (img) img.src = '';
    }

    function toggleTechModalZoom() {
        isTechModalZoomed = !isTechModalZoomed;
        applyTechModalZoomState();
    }

    function applyTechModalZoomState() {
        var container = document.getElementById('tech-image-container');
        var img = document.getElementById('tech-image-modal-img');
        var icon = document.getElementById('tech-modal-zoom-icon');
        var text = document.getElementById('tech-modal-zoom-text');
        if (!container || !img) return;

        if (isTechModalZoomed) {
            // Zoomed mode: allow vertical scrolling to read small text
            container.style.overflowY = 'auto';
            container.style.alignItems = 'flex-start';
            img.style.maxHeight = 'none';
            img.style.maxWidth = '100%';
            img.style.width = '100%';
            img.style.height = 'auto';
            if (icon) icon.className = 'fa-solid fa-compress';
            if (text) text.textContent = '整頁最適化';
        } else {
            // Default Fit mode: 100% fits within screen height, never overflows!
            container.style.overflow = 'hidden';
            container.style.alignItems = 'center';
            img.style.maxHeight = 'calc(100vh - 120px)';
            img.style.maxWidth = '100%';
            img.style.width = 'auto';
            img.style.height = 'auto';
            if (icon) icon.className = 'fa-solid fa-magnifying-glass-plus';
            if (text) text.textContent = '放大滾動閱讀';
        }
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' || e.key === 'Esc') closeTechImageModal();
    });
'''
    if old_script_pattern.search(page_html):
        page_html = old_script_pattern.sub(new_script_body + '\n    ', page_html)
    else:
        page_html = page_html.replace('</body>', f'<script>\n{new_script_body}\n</script>\n</body>')

    return page_html

def update_mega_menu_in_all_files():
    """
    將所有既有 HTML 檔案中導覽列技術 Mega Menu 的 technology/#tech-<slug>
    全面升級為獨立子頁面路徑 technology/<slug>/，確保全站一致且符合 GSC 索引。
    """
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if 'node_modules' in root or '.git' in root or 'amplify' in root or 'scratch' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as hf:
                        content = hf.read()
                    
                    modified = False
                    for ti in TECH_ITEMS:
                        old_href = f'href="technology/#tech-{ti["slug"]}"'
                        new_href = f'href="technology/{ti["slug"]}/"'
                        if old_href in content:
                            content = content.replace(old_href, new_href)
                            modified = True
                    
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as hf:
                            hf.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error updating mega menu in {file_path}: {e}")
    print(f"✅ 已成功更新全站 {count} 個 HTML 檔案中技術 Mega Menu 連結為獨立分頁 URL！")

def build_all():
    print("🚀 開始建置 11 大特用化學品獨立技術分頁...")
    with open(os.path.join(ROOT_DIR, 'technology', 'index.html'), 'r', encoding='utf-8') as f:
        template_shell = f.read()

    # 1. 產生 11 個獨立子頁面資料夾與 index.html
    for item in TECH_ITEMS:
        slug = item["slug"]
        sub_dir = os.path.join(ROOT_DIR, 'technology', slug)
        os.makedirs(sub_dir, exist_ok=True)
        sub_file = os.path.join(sub_dir, 'index.html')

        sub_html = build_full_tech_page_html(item, template_shell, is_index=False)
        with open(sub_file, 'w', encoding='utf-8') as sf:
            sf.write(sub_html)
        print(f"  [SUBPAGE] 建立獨立分頁: technology/{slug}/index.html ({len(sub_html)} bytes, has_data={item['has_data']})")

    # 2. 產生 technology/index.html (預設首個 Tyzor，亦包含全部 11 個獨立分頁切換按鈕)
    main_tech_html = build_full_tech_page_html(TECH_ITEMS[0], template_shell, is_index=True)
    with open(os.path.join(ROOT_DIR, 'technology', 'index.html'), 'w', encoding='utf-8') as mf:
        mf.write(main_tech_html)
    print(f"  [MAIN] 更新技術專區主頁: technology/index.html ({len(main_tech_html)} bytes)")

    # 3. 更新全站 HTML Mega Menu 連結
    update_mega_menu_in_all_files()

    # 4. 同步更新 sitemap.xml
    update_sitemap()
    print("🎉 11 項技術獨立分頁已全部建置完成！")

def update_sitemap():
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        return
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        xml = f.read()

    # Check if technology URLs are already present
    added_urls = []
    for item in TECH_ITEMS:
        url = f"{DOMAIN}/technology/{item['slug']}/"
        if f"<loc>{url}</loc>" not in xml:
            added_urls.append(url)

    if added_urls:
        tech_root_loc = f"<loc>{DOMAIN}/technology/</loc>"
        pos = xml.find(tech_root_loc)
        if pos != -1:
            end_url_pos = xml.find('</url>', pos) + len('</url>')
            new_blocks = []
            for u in added_urls:
                block = f'''
    <url>
        <loc>{u}</loc>
        <lastmod>2026-09-23</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.85</priority>
    </url>'''
                new_blocks.append(block)
            xml = xml[:end_url_pos] + "".join(new_blocks) + xml[end_url_pos:]
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(xml)
            print(f"✅ 已在 sitemap.xml 中加入 {len(added_urls)} 個獨立技術子分頁 URL！")
        else:
            print("Notice: tech root loc not found in sitemap.xml")

if __name__ == '__main__':
    build_all()
