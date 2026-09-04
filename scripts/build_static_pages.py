# -*- coding: utf-8 -*-
"""
Python 版靜態頁面生成器 (SSG)
與 scripts/build-static-pages.js 同步：
- 依各品牌規則精確解析適合應用領域 (MPI看 mpiall.json application_title_zh、Dorf Ketal看 featured_categories、Orion看 featured_categories、Others看 config.json 分類)
- 豐富完整的產品描述與代表性物性表
- 畫面不使用任何漸層底色 (純白/極簡現代風格)
- 移除獨立產品頁的全域搜尋框
- 引導使用者至官網比較其他產品、查看 TDS 與索樣
"""

import os
import sys
import re
import json
import urllib.parse
import html

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(ROOT_DIR, 'index.html')
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
DOMAIN = 'https://www.attech.com.tw'

def escape_html(s):
    if s is None:
        return ''
    return html.escape(str(s), quote=True)

def load_data():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_html = f.read()

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)

    all_products_cache = {}
    for brand_key, brand_obj in config.items():
        if 'masterPath' in brand_obj:
            master_file_path = os.path.join(ROOT_DIR, brand_obj['masterPath'].lstrip('./').replace('/', os.sep))
            if os.path.exists(master_file_path):
                with open(master_file_path, 'r', encoding='utf-8') as mf:
                    master_data = json.load(mf)
                all_products_cache['mpi_master'] = master_data
                for f_info in brand_obj.get('files', []):
                    key = f_info['key']
                    all_products_cache[key] = [p for p in master_data if p.get('applications_data', {}).get(key)]
        elif 'files' in brand_obj:
            for f_info in brand_obj['files']:
                if 'jsonPath' in f_info:
                    j_path = os.path.join(ROOT_DIR, f_info['jsonPath'].lstrip('./').replace('/', os.sep))
                    if os.path.exists(j_path):
                        try:
                            with open(j_path, 'r', encoding='utf-8') as jf:
                                data = json.load(jf)
                            key = f_info['key']
                            all_products_cache[key] = data if isinstance(data, list) else data.get('products', [])
                        except Exception:
                            all_products_cache[f_info['key']] = []
    return template_html, config, all_products_cache

def get_product_applications(p, partner_key, line_key, config_data):
    apps = []
    p_lower = (partner_key or '').lower()
    p_name = p.get('product_name') or p.get('name') or ''
    safe_name = urllib.parse.quote(p_name)

    if p_lower == 'mpi':
        # MPI: 依據 json/mpi/mpiall.json 中的 application_title_zh
        apps_data = p.get('applications_data', {})
        if isinstance(apps_data, dict):
            for app_key, app_obj in apps_data.items():
                if isinstance(app_obj, dict) and app_obj.get('application_title_zh'):
                    title = str(app_obj['application_title_zh']).strip()
                    if title and not any(a['title'] == title for a in apps):
                        apps.append({
                            'title': title,
                            'key': app_key,
                            'url': f'/products/mpi/{app_key}/',
                            'product_url': f'/products/mpi/{app_key}/?product={safe_name}#{safe_name}',
                            'is_current': (app_key == line_key)
                        })
    elif p_lower == 'dorfketal':
        cats = p.get('featured_categories', [])
        if isinstance(cats, list):
            for cat in cats:
                title = str(cat).strip()
                if title and not any(a['title'] == title for a in apps):
                    apps.append({
                        'title': title,
                        'key': line_key,
                        'url': f'/products/dorfketal/{line_key}/?category={urllib.parse.quote(title)}',
                        'product_url': f'/products/dorfketal/{line_key}/?product={safe_name}#{safe_name}',
                        'is_current': True
                    })
    elif p_lower == 'orion':
        cats = p.get('featured_categories', [])
        if isinstance(cats, list):
            for cat in cats:
                title = str(cat).strip()
                if title and not any(a['title'] == title for a in apps):
                    apps.append({
                        'title': title,
                        'key': line_key,
                        'url': f'/products/orion/{line_key}/?category={urllib.parse.quote(title)}',
                        'product_url': f'/products/orion/{line_key}/?product={safe_name}#{safe_name}',
                        'is_current': True
                    })
    else:
        cats = p.get('featured_categories', [])
        if isinstance(cats, list) and len(cats) > 0:
            for cat in cats:
                title = str(cat).strip()
                if title and not any(a['title'] == title for a in apps):
                    apps.append({
                        'title': title,
                        'key': line_key,
                        'url': f'/products/others/{line_key}/?category={urllib.parse.quote(title)}',
                        'product_url': f'/products/others/{line_key}/?product={safe_name}#{safe_name}',
                        'is_current': True
                    })
        if len(apps) == 0:
            others_conf = config_data.get('others', {})
            files_conf = others_conf.get('files', [])
            f_found = next((f for f in files_conf if f.get('key') == line_key), None)
            line_name = f_found.get('titleZh') if f_found else '特化材料助劑'
            apps.append({
                'title': line_name,
                'key': line_key,
                'url': f'/products/others/{line_key}/',
                'product_url': f'/products/others/{line_key}/?product={safe_name}#{safe_name}',
                'is_current': True
            })
    return apps

def get_product_description(p, partner_key, line_key):
    p_lower = (partner_key or '').lower()
    desc = p.get('properties') or p.get('performance') or ''

    if not desc and p_lower == 'mpi':
        lines = []
        apps_data = p.get('applications_data', {})
        if isinstance(apps_data, dict):
            curr_data = apps_data.get(line_key) or next(iter(apps_data.values()), None)
            if isinstance(curr_data, dict) and curr_data.get('performance_descriptions_zh'):
                for _, val in curr_data['performance_descriptions_zh'].items():
                    if val and isinstance(val, str) and val.strip() not in lines:
                        lines.append(val.strip())
        if lines:
            desc = '\n'.join(lines)
        elif p.get('application_fields_zh'):
            desc = f"主要應用領域：{p['application_fields_zh']}"
    elif not desc and p_lower == 'orion':
        method_map = {
            'HCF': '高色素爐黑 (High Color Furnace Black)',
            'MCF': '中色素爐黑 (Medium Color Furnace Black)',
            'RCF': '標準色素爐黑 (Regular Color Furnace Black)',
            'Gas Black': '特級氣黑 (Gas Black)',
            'Lamp Black': '燈黑 (Lamp Black)',
            'Furnace Black': '爐法碳黑 (Furnace Black)'
        }
        method = method_map.get(p.get('production_method'), p.get('production_method') or '特級碳黑製程')
        cats = '、'.join(p.get('featured_categories', [])) if isinstance(p.get('featured_categories'), list) else ''
        typical = p.get('typical_properties', {})
        p_name = p.get('product_name') or p.get('name') or ''
        desc = f"{p_name} 為 Orion Engineered Carbons 頂級碳黑材料，採用 {method}。具備優良著色力與分散穩定性，黑度值 (My) 達 {typical.get('blackness_my') or '—'}，原生平均粒徑約 {typical.get('average_primary_particle_size_nm') or '—'} nm。廣泛應用於 {cats or '工業塗料與油墨'} 等高性能著色體系。"
    elif not desc and p_lower == 'others':
        if line_key == 'silane':
            desc = f"高性能矽烷偶合劑（{p.get('composition_zh') or '有機矽烷'}），能顯著改善無機填料與有機基體間之相容性，提升界面附著力、耐水性與力學機械強度。"

    return desc or '提供卓越的加工相容性、表面改質效果與穩定物性，完整配方諮詢與規格建議請洽宏威應用材料業務。'

def get_typical_properties_rows(p):
    t = p.get('typical_properties', {})
    rows = []
    def add_row(label, val):
        if val is not None and str(val).strip() not in ('', '—', 'N/A'):
            rows.append({'label': label, 'val': str(val).strip()})

    add_row('熔點 / 軟化點 (°C)', t.get('melt_point_c') or p.get('softening_point'))
    add_row('平均粒徑 (µm)', t.get('mean_particle_size_um') or p.get('particle_size'))
    add_row('最大粒徑 (µm)', t.get('max_particle_size_um'))
    add_row('密度 / 比重 (g/cm³)', t.get('density_g_cc_25c') or p.get('density') or p.get('specific_gravity'))
    add_row('酸價 (mg KOH/g)', t.get('acid_value') or p.get('acid_value'))
    add_row('閃點 (°C)', t.get('flash_point') or p.get('flash_point'))
    add_row('分子量 (Mw)', t.get('molecular_weight'))
    add_row('外觀 / 狀態', p.get('appearance'))
    add_row('固成份 / 活性物含量 (%)', t.get('solid_content') or t.get('active_content') or p.get('active_content'))
    add_row('黏度 (mPa·s / cSt)', t.get('viscosity') or p.get('viscosity'))

    add_row('黑度值 (My)', t.get('blackness_my'))
    add_row('著色力 (% vs. IRB 3)', t.get('tinting_strength'))
    add_row('吸油量 (OAN, ml/100g)', t.get('oil_absorption_number'))
    add_row('pH 值', t.get('ph_value'))
    add_row('灰分含量 (%)', t.get('ash_content'))
    add_row('BET 比表面積 (m²/g)', t.get('bet_surface_area'))
    add_row('原生粒徑 (nm)', t.get('average_primary_particle_size_nm'))
    add_row('揮發份 950°C (%)', t.get('volatile_matter_950c'))

    return rows

def render_product_detail_table(p, partner_key, line_key, brand_name, line_title='', config_data=None):
    name = (p.get('product_name') or p.get('name') or '').strip()
    safe_name = urllib.parse.quote(name)
    comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or '特用化學品材料'
    props = get_product_description(p, partner_key, line_key)
    applications = get_product_applications(p, partner_key, line_key, config_data or {})

    is_fda_line = (partner_key.lower() == 'mpi' and (line_key == 'industrial' or line_key == 'ink'))
    fda_badge = ('<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-300" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-emerald-600"></i> FDA 食品接觸合規</span>'
                 if (is_fda_line and p.get('fda_compliant')) else '')

    usage_tags_list = []
    for app in applications:
        current_cls = 'bg-blue-900 text-white font-bold' if app['is_current'] else 'bg-white hover:bg-blue-50 text-slate-800 hover:text-blue-950 font-semibold border border-slate-300'
        icon_cls = 'text-blue-200' if app['is_current'] else 'text-blue-600'
        curr_label = '<span class="text-[10px] opacity-75 font-normal">(當前系列)</span>' if app['is_current'] else ''
        usage_tags_list.append(f'<a href="{app["url"]}" title="至官網檢視 {escape_html(app["title"])} 應用領域之所有規格與比較表" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 {current_cls} rounded-lg text-xs transition-colors shadow-xs"><i class="fa-solid fa-tag text-[10px] {icon_cls}"></i><span>{escape_html(app["title"])}</span>{curr_label}</a>')
    usage_tags_html = '\n'.join(usage_tags_list)

    prop_rows = get_typical_properties_rows(p)
    extra_rows = ''.join([f'<tr class="border-b border-slate-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50/80 w-2/5">{escape_html(r["label"])}</td><td class="py-2.5 px-4 text-slate-900 font-semibold">{escape_html(r["val"])}</td></tr>' for r in prop_rows])

    extra_details = []
    if p.get('application_fields_zh'):
        extra_details.append(f'<div><span class="font-bold text-slate-900">詳細應用範疇：</span>{escape_html(p["application_fields_zh"])}</div>')
    if p.get('recommended_system_type_zh'):
        extra_details.append(f'<div><span class="font-bold text-slate-900">建議適用系統：</span>{escape_html(p["recommended_system_type_zh"])}</div>')
    if p.get('suggested_use_level_zh'):
        extra_details.append(f'<div><span class="font-bold text-slate-900">建議添加量：</span>{escape_html(p["suggested_use_level_zh"])}</div>')
    extra_details_html = f'<div class="mt-4 pt-3 border-t border-slate-200 text-xs text-slate-700 space-y-2 leading-relaxed">{"".join(extra_details)}</div>' if extra_details else ''

    extra_rows_block = f'''
                <div class="border border-slate-200 rounded-xl overflow-hidden shadow-xs">
                    <div class="bg-slate-100 px-4 py-2.5 border-b border-slate-200 font-bold text-xs text-slate-700 uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-chart-simple text-blue-900"></i> 代表性物性摘要 (Typical Properties)
                    </div>
                    <table class="w-full text-left text-sm">
                        <tbody>
                            {extra_rows}
                        </tbody>
                    </table>
                </div>''' if extra_rows else ''

    return f'''
    <div class="product-seo-detail bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 mb-8 text-slate-900">
        <!-- 頂部產品基本資訊與快速操作 (純白卡片無漸層) -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5 pb-6 border-b border-slate-200">
            <div>
                <div class="flex flex-wrap items-center gap-2 mb-2.5">
                    <span class="inline-block px-3 py-1 rounded-md text-xs font-bold bg-slate-100 text-slate-800 border border-slate-200">{escape_html(brand_name)}</span>
                    {f'<span class="inline-block px-3 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">{escape_html(line_title)}</span>' if line_title else ''}
                    {fda_badge}
                </div>
                <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">{escape_html(name)}</h1>
                <p class="text-sm text-slate-600 mt-2 font-medium">
                    主要化學成分：<span class="text-slate-900 font-semibold">{escape_html(comp)}</span>
                </p>
            </div>
            <div class="flex flex-wrap items-center gap-2.5 shrink-0">
                <a href="/contact?product={safe_name}" 
                   class="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-sm font-bold shadow-xs transition-colors active:scale-95">
                    <i class="fa-solid fa-envelope"></i>
                    <span>索取樣品與技術諮詢</span>
                </a>
                <a href="/products/{partner_key}/{line_key}/" 
                   class="inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300 rounded-xl text-sm font-bold transition-colors">
                    <i class="fa-solid fa-scale-balanced text-slate-700"></i>
                    <span>比較同系列其他產品</span>
                </a>
                <a href="/products/{partner_key}/{line_key}/?product={safe_name}#{safe_name}" 
                   class="inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 text-blue-900 border border-blue-300 rounded-xl text-sm font-bold transition-colors">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    <span>官網完整規格與 TDS</span>
                </a>
            </div>
        </div>

        <!-- 產品核心內容區塊 -->
        <div class="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 左側 2 欄：應用領域、特點描述與代表物性 -->
            <div class="lg:col-span-2 space-y-6">
                <!-- 適合在哪些應用與主要用途 (純色背景無漸層) -->
                <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <h2 class="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-layer-group text-blue-900"></i> 適合在哪些應用與主要用途
                    </h2>
                    <div class="flex flex-wrap gap-2">
                        {usage_tags_html or f'<span class="text-sm text-slate-700">{escape_html(line_title or "特用化學品工業應用")}</span>'}
                    </div>

                    {extra_details_html}

                    <div class="mt-3 pt-2.5 border-t border-slate-200 text-xs text-slate-500 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-info text-blue-700 shrink-0"></i>
                        <span>提示：點擊任一標籤可直接前往官網檢閱同領域之完整產品系列與線上規格比對。</span>
                    </div>
                </div>

                <!-- 性質與特點描述 (單一色底無漸層) -->
                <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <h2 class="text-sm font-bold text-slate-900 mb-2.5 flex items-center gap-2">
                        <i class="fa-solid fa-star text-amber-500"></i> 產品描述與性能特點
                    </h2>
                    <p class="text-sm text-slate-800 leading-relaxed whitespace-pre-line">{escape_html(props)}</p>
                </div>

                {extra_rows_block}
            </div>

            <!-- 右側 1 欄：官網產品比較導流與原廠支援 (單一色底無漸層，統一風格) -->
            <div class="space-y-6">
                <!-- 導流卡片 1：線上產品比較 -->
                <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <div class="flex items-center gap-2 text-blue-900 text-xs font-bold uppercase tracking-wider mb-2">
                        <i class="fa-solid fa-scale-balanced"></i> 產品線上對比功能
                    </div>
                    <h3 class="text-base font-bold text-slate-900 mb-2">需要比較同系列其他產品？</h3>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        宏威應用材料官網提供完整的特用化學品物性規格，您可同時比較 {escape_html(brand_name)} {escape_html(line_title)} 各產品的物性規格與適用系統。
                    </p>
                    <a href="/products/{partner_key}/{line_key}/" 
                       class="inline-flex items-center justify-center gap-1.5 w-full px-4 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold transition-colors">
                        <span>進入 {escape_html(line_title or '此系列')} 完整規格比較表</span>
                        <i class="fa-solid fa-chevron-right text-[10px]"></i>
                    </a>
                </div>

                <!-- 導流卡片 2：原廠正品技術保證 (單一色底無漸層，統一風格) -->
                <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <div class="flex items-center gap-2 text-blue-900 text-xs font-bold uppercase tracking-wider mb-2">
                        <i class="fa-solid fa-shield-halved text-blue-800"></i> 原廠正品技術支援
                    </div>
                    <h3 class="text-base font-bold text-slate-900 mb-2">宏威應用材料 專業技術</h3>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">
                        宏威應用材料為 {escape_html(brand_name)} 在台灣之專業特用化學代理商，備有原廠技術規格書 (TDS)、樣品庫存與應用技術諮詢服務。
                    </p>
                    <div class="pt-3 border-t border-slate-200 text-xs text-slate-700 space-y-2.5">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-check text-emerald-600"></i> <span>備有原廠正式技術規格書 (TDS)</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-check text-emerald-600"></i> <span>樣品齊全，支援快速索樣</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-check text-emerald-600"></i> <span>提供多品項線上規格橫向比較</span>
                        </div>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-200 text-[11px] text-slate-500 leading-relaxed">
                        電話諮詢：04-2239-8056<br>
                        技術信箱：atservice@attech.com.tw
                    </div>
                </div>
            </div>
        </div>

        <!-- 底部大橫幅：官網深入互動導流 (純深石板灰底色無漸層) -->
        <div class="mt-8 bg-slate-900 text-white rounded-xl p-6 sm:p-8 border border-slate-800 shadow-sm">
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                <div>
                    <div class="flex items-center gap-2 text-blue-400 text-xs font-bold uppercase tracking-wider mb-1">
                        <i class="fa-solid fa-building"></i> 宏威應用材料 官方產品資料庫
                    </div>
                    <h3 class="text-lg sm:text-xl font-bold text-white">
                        需要檢視完整技術數據、TDS 下載或產品規格比較？
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-300 mt-1.5 max-w-2xl leading-relaxed">
                        原廠技術資料表（TDS）與全品項多規格比較矩陣已完整收錄於官網系統。點擊下方按鈕可前往官網產品專區，系統將自動定位並展開 {escape_html(name)} 之完整技術檔案。
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-2.5 shrink-0 w-full lg:w-auto">
                    <a href="/products/{partner_key}/{line_key}/" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-bold border border-slate-700 transition-colors">
                        <i class="fa-solid fa-scale-balanced"></i>
                        <span>比較同系列其他產品</span>
                    </a>
                    <a href="/products/{partner_key}/{line_key}/?product={safe_name}#{safe_name}" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold shadow-sm transition-colors active:scale-95">
                        <i class="fa-solid fa-file-lines"></i>
                        <span>直達官網看 TDS 與完整規格</span>
                    </a>
                    <a href="/contact?product={safe_name}" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-100 text-slate-900 rounded-xl text-sm font-bold transition-colors">
                        <i class="fa-solid fa-envelope"></i>
                        <span>索取免費樣品</span>
                    </a>
                </div>
            </div>
        </div>
    </div>'''

def build_page_html(template_html, title, description, canonical_path, active_tab='about', pre_rendered_content='', schema_json=None, is_product_detail_page=False, product_meta=None):
    html_out = template_html

    html_out = re.sub(r'<title id="web-title">.*?</title>', f'<title id="web-title">{escape_html(title)}</title>', html_out)
    html_out = re.sub(r'<meta name="description"\s+content=".*?">', f'<meta name="description" content="{escape_html(description)}">', html_out, flags=re.DOTALL)

    full_canonical = f"{DOMAIN}{'' if canonical_path == '/' else canonical_path}"
    html_out = re.sub(r'<link rel="canonical"\s+href=".*?">', f'<link rel="canonical" href="{full_canonical}">', html_out)

    html_out = re.sub(r'<meta property="og:title"\s+content=".*?">', f'<meta property="og:title" content="{escape_html(title)}">', html_out)
    html_out = re.sub(r'<meta property="og:description"\s+content=".*?">', f'<meta property="og:description" content="{escape_html(description)}">', html_out)
    html_out = re.sub(r'<meta property="og:url"\s+content=".*?">', f'<meta property="og:url" content="{full_canonical}">', html_out)
    html_out = re.sub(r'<meta name="twitter:title"\s+content=".*?">', f'<meta name="twitter:title" content="{escape_html(title)}">', html_out)
    html_out = re.sub(r'<meta name="twitter:description"\s+content=".*?">', f'<meta name="twitter:description" content="{escape_html(description)}">', html_out)
    html_out = re.sub(r'<meta name="twitter:url"\s+content=".*?">', f'<meta name="twitter:url" content="{full_canonical}">', html_out)

    tabs = ['about', 'products', 'partners', 'contact']
    for t in tabs:
        if t == active_tab:
            html_out = re.sub(rf'id="tab-{t}" class="tab-content.*?"', f'id="tab-{t}" class="tab-content active"', html_out)
            html_out = re.sub(rf'id="nav-{t}".*?aria-selected=".*?"', f'id="nav-{t}" role="tab" aria-selected="true"', html_out)
            html_out = re.sub(rf'id="mobile-nav-{t}".*?aria-selected=".*?"', f'id="mobile-nav-{t}" role="tab" aria-selected="true"', html_out)
        else:
            html_out = re.sub(rf'id="tab-{t}" class="tab-content active"', f'id="tab-{t}" class="tab-content"', html_out)
            html_out = re.sub(rf'id="nav-{t}".*?aria-selected="true"', f'id="nav-{t}" role="tab" aria-selected="false"', html_out)
            html_out = re.sub(rf'id="mobile-nav-{t}".*?aria-selected="true"', f'id="mobile-nav-{t}" role="tab" aria-selected="false"', html_out)

    if is_product_detail_page:
        html_out = html_out.replace('<body class="', '<body class="is-product-detail bg-slate-50 ')

        # 移除全域搜尋
        html_out = re.sub(r'<div class="flex-1 max-w-sm mx-2 hidden sm:block">[\s\S]*?</form>\s*</div>', '<!-- 全域搜尋已在獨立產品頁移除 -->', html_out)
        html_out = re.sub(r'<div class="block sm:hidden pb-2\.5">[\s\S]*?</form>\s*</div>', '<!-- 行動版全域搜尋已在獨立產品頁移除 -->', html_out)

        # 移除 1. 請選擇品牌 與 資料建置提示
        html_out = re.sub(r'<section[^>]*id="section-partner"[\s\S]*?</section>', '', html_out)
        html_out = re.sub(r'<section[^>]*id="section-coming-soon"[\s\S]*?</section>', '', html_out)

        breadcrumb_bar = ''
        if product_meta:
            breadcrumb_bar = f'''
            <div class="flex flex-wrap items-center justify-between gap-3 mb-5 pb-3 border-b border-slate-200">
                <a href="{product_meta['backUrl']}" class="inline-flex items-center gap-2 text-sm font-bold text-slate-800 hover:text-blue-900 transition-colors">
                    <i class="fa-solid fa-arrow-left"></i> 返回 {escape_html(product_meta['brandName'])} {escape_html(product_meta['lineTitle'])} 產品列表與規格比較
                </a>
                <nav class="flex items-center gap-1.5 text-xs text-slate-500 font-medium" aria-label="麵包屑導航">
                    <a href="/" class="hover:underline">首頁</a>
                    <span>/</span>
                    <a href="/products/" class="hover:underline">產品</a>
                    <span>/</span>
                    <a href="/products/{product_meta['partnerSlug']}/" class="hover:underline">{escape_html(product_meta['brandName'])}</a>
                    <span>/</span>
                    <a href="{product_meta['backUrl']}" class="hover:underline">{escape_html(product_meta['lineTitle'])}</a>
                    <span>/</span>
                    <span class="text-slate-900 font-bold">{escape_html(product_meta['name'])}</span>
                </nav>
            </div>'''

        # 將整個目錄與表格工作區 (section-directory-finder) 乾淨替換為獨立產品詳細區塊
        html_out = re.sub(
            r'<div id="section-directory-finder"[\s\S]*?</main>\s*</div>',
            f'<div id="section-product-detail" class="w-full">{breadcrumb_bar}{pre_rendered_content}</div>',
            html_out
        )
    elif pre_rendered_content:
        html_out = re.sub(r'<tbody id="directory-matrix-body"[\s\S]*?</tbody>', f'<tbody id="directory-matrix-body" class="divide-y divide-gray-200 text-slate-800 f-weight-normal">{pre_rendered_content}</tbody>', html_out)

    if schema_json:
        schema_str = f'\n    <script type="application/ld+json">\n{json.dumps(schema_json, ensure_ascii=False, indent=2)}\n    </script>'
        html_out = html_out.replace('</head>', f'{schema_str}\n</head>')

    return html_out

def write_static_file(rel_path, content):
    target_dir = os.path.join(ROOT_DIR, rel_path.lstrip('/').replace('/', os.sep))
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🚀 [Python] 開始建置靜態預渲染 (SSG) 頁面...")
    template_html, config, all_products_cache = load_data()
    generated_count = 0

    core_pages = [
        ('/about/', '宏威應用材料 Discover The Link To Life | 專業特用化學品供應商', '宏威應用材料 Discover The Link To Life - 專業特用化學品供應商，提供PTFE取代方案、Micro Powders微粉蠟、Dorf Ketal鈦鋯酸酯、Orion特級碳黑等高性能材料與免費索樣服務。', 'about'),
        ('/products/', '特用化學品目錄 | 宏威應用材料 ATTech Materials', '宏威應用材料特用化學品完整產品目錄，涵蓋微粉蠟、PTFE取代、鈦酸酯/鋯酸酯、特級碳黑、矽烷偶合劑與塗料助劑，支援線上多維度篩選與規格比對。', 'products'),
        ('/partners/', '合作夥伴品牌 | 宏威應用材料 Discover The Link To Life', '宏威應用材料代理銷售 Micro Powders、Dorf Ketal、Orion 等國際領導化學品牌，提供正品保證與原廠技術支援。', 'partners'),
        ('/contact/', '樣品索取與技術諮詢 | 宏威應用材料 Discover The Link To Life', '線上索取特用化學品樣品與配方技術諮詢，提供快速詢價與詳細應用需求評估雙模式表單，自動產製正式 PDF 需求單。', 'contact')
    ]

    for p_path, p_title, p_desc, p_tab in core_pages:
        h = build_page_html(template_html, p_title, p_desc, p_path, active_tab=p_tab)
        write_static_file(p_path, h)
        generated_count += 1

    for brand_key, brand_obj in config.items():
        partner_slug = brand_key.lower()
        brand_name = brand_obj.get('brandName', brand_key)

        p_path = f'/products/{partner_slug}/'
        p_html = build_page_html(template_html, f"{brand_name} 特用化學品系列 | 宏威應用材料 ATTech Materials", f"宏威應用材料代理銷售 {brand_name} 全系列特用化學品，提供規格對比、TDS技術資料下載與免費樣品申請服務。", p_path, active_tab='products')
        write_static_file(p_path, p_html)
        generated_count += 1

        for f_info in brand_obj.get('files', []):
            line_slug = f_info['key']
            line_title = f_info.get('titleZh') or f_info.get('titleEn') or line_slug
            line_path = f'/products/{partner_slug}/{line_slug}/'
            products = all_products_cache.get(line_slug, [])

            table_rows = []
            for p in products:
                name = p.get('product_name') or p.get('name') or ''
                comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or '—'
                props = get_product_description(p, partner_slug, line_slug)
                app_list = get_product_applications(p, partner_slug, line_slug, config)
                usage_text = '、'.join(a['title'] for a in app_list) or p.get('main_usage') or p.get('application_fields_zh') or '—'
                safe_url = f'/products/{partner_slug}/{line_slug}/{urllib.parse.quote(name)}/'
                is_fda_line = (partner_slug == 'mpi' and (line_slug == 'industrial' or line_slug == 'ink'))
                fda_badge = '<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 align-middle shrink-0 ml-1.5 shadow-xs select-none" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-[9px] text-emerald-600"></i> FDA</span>' if (is_fda_line and p.get('fda_compliant')) else ''

                table_rows.append(f'''
                <tr class="hover:bg-blue-50/50 border-b border-gray-200 text-sm transition-colors">
                    <td class="py-3 px-3.5 font-bold text-slate-900 align-top w-[25%]">
                        <div class="flex items-center flex-wrap gap-y-0.5">
                            <a href="{safe_url}" class="text-blue-950 font-extrabold text-sm hover:underline inline leading-snug">
                                {escape_html(name)}
                            </a>
                            {fda_badge}
                        </div>
                        <div class="text-xs text-slate-500 font-normal mt-0.5">{escape_html(comp)}</div>
                    </td>
                    <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[40%]">{escape_html(props)}</td>
                    <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[25%]">{escape_html(usage_text)}</td>
                    <td class="py-3 px-3.5 text-center align-top w-[10%]">
                        <a href="{safe_url}" class="px-2.5 py-1 bg-white hover:bg-blue-50 border border-blue-300 text-blue-950 rounded font-bold text-xs shadow-xs inline-flex items-center gap-1 transition-all">
                            <span>規格詳情</span>
                            <i class="fa-solid fa-chevron-right text-[10px]"></i>
                        </a>
                    </td>
                </tr>''')

            item_list_schema = {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": f"{brand_name} {line_title} 產品目錄",
                "description": f"{brand_name} {line_title} 特用化學品規格表，共 {len(products)} 項品項。",
                "url": f"{DOMAIN}{line_path}",
                "numberOfItems": len(products),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": idx + 1,
                        "name": p.get('product_name') or p.get('name'),
                        "url": f"{DOMAIN}{line_path}{urllib.parse.quote((p.get('product_name') or p.get('name') or '').strip())}/"
                    }
                    for idx, p in enumerate(products)
                ]
            }

            line_html = build_page_html(
                template_html,
                f"{line_title} ({brand_name}) | 宏威應用材料 ATTech Materials",
                f"宏威應用材料精選 {brand_name} {line_title} 特用化學品，提供 {', '.join([p.get('product_name') or p.get('name', '') for p in products[:8]])} 等品項之物性參數與免費索樣。",
                line_path,
                active_tab='products',
                pre_rendered_content=''.join(table_rows),
                schema_json=item_list_schema
            )
            write_static_file(line_path, line_html)
            generated_count += 1

            for p in products:
                p_name = (p.get('product_name') or p.get('name') or '').strip()
                if not p_name:
                    continue
                product_path = f"/products/{partner_slug}/{line_slug}/{urllib.parse.quote(p_name)}/"
                comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or ''
                props = get_product_description(p, partner_slug, line_slug)
                app_list = get_product_applications(p, partner_slug, line_slug, config)
                usage_text = '、'.join(a['title'] for a in app_list) or line_title

                product_detail_html = render_product_detail_table(p, partner_slug, line_slug, brand_name, line_title, config)

                product_schema = {
                    "@context": "https://schema.org",
                    "@graph": [
                        {
                            "@type": "BreadcrumbList",
                            "itemListElement": [
                                { "@type": "ListItem", "position": 1, "name": "首頁", "item": f"{DOMAIN}/" },
                                { "@type": "ListItem", "position": 2, "name": "產品", "item": f"{DOMAIN}/products/" },
                                { "@type": "ListItem", "position": 3, "name": brand_name, "item": f"{DOMAIN}/products/{partner_slug}/" },
                                { "@type": "ListItem", "position": 4, "name": line_title, "item": f"{DOMAIN}/products/{partner_slug}/{line_slug}/" },
                                { "@type": "ListItem", "position": 5, "name": p_name, "item": f"{DOMAIN}{product_path}" }
                            ]
                        },
                        {
                            "@type": "Product",
                            "name": p_name,
                            "image": f"{DOMAIN}/img/MCP-Logo.png",
                            "description": f"{brand_name} {p_name} - 主要成分：{comp or '特用化學材料'}。適合應用：{usage_text}。特性：{props.replace(chr(10), ' ')}",
                            "brand": {
                                "@type": "Brand",
                                "name": brand_name
                            },
                            "offers": {
                                "@type": "Offer",
                                "url": f"{DOMAIN}{product_path}",
                                "price": "0",
                                "priceCurrency": "TWD",
                                "availability": "https://schema.org/InStock",
                                "itemCondition": "https://schema.org/NewCondition",
                                "seller": {
                                    "@type": "Organization",
                                    "name": "宏威應用材料 ATTech Materials"
                                }
                            }
                        }
                    ]
                }

                prod_page_html = build_page_html(
                    template_html,
                    f"{p_name} ({brand_name}) {line_title} | 宏威應用材料 ATTech Materials",
                    f"{brand_name} {p_name} 特用化學品：{comp + '，' if comp else ''}{props.replace(chr(10), ' ')[:100] + '... ' if props else ''}適合應用：{usage_text}。提供官網線上規格比較、TDS技術資料與樣品索取。",
                    product_path,
                    active_tab='products',
                    pre_rendered_content=product_detail_html,
                    schema_json=product_schema,
                    is_product_detail_page=True,
                    product_meta={
                        'name': p_name,
                        'brandName': brand_name,
                        'lineTitle': line_title,
                        'partnerSlug': partner_slug,
                        'lineSlug': line_slug,
                        'backUrl': f"/products/{partner_slug}/{line_slug}/"
                    }
                )
                write_static_file(f"/products/{partner_slug}/{line_slug}/{p_name}", prod_page_html)
                generated_count += 1

    print(f"✅ [Python] 靜態預渲染完成！共產出 {generated_count} 個實體 index.html 頁面。")

if __name__ == '__main__':
    main()
