# -*- coding: utf-8 -*-
"""
Python 版靜態頁面生成器 (SSG)
功能等同 scripts/build-static-pages.js，免依賴 Node.js 環境即可即時生成所有靜態頁面。
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

def render_product_detail_table(p, partner_key, line_key, brand_name):
    name = p.get('product_name') or p.get('name') or ''
    comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or '—'
    props = p.get('properties') or p.get('performance') or '—'
    usage = p.get('main_usage') or p.get('application_fields_zh') or ', '.join(p.get('featured_categories', [])) or '—'

    typical = p.get('typical_properties', {})
    density = typical.get('density_g_cc_25c') or p.get('density') or '—'
    melt_point = typical.get('melt_point_c') or p.get('softening_point') or '—'
    particle_size = typical.get('mean_particle_size_um') or p.get('particle_size') or '—'
    acid_value = typical.get('acid_value') or p.get('acid_value') or '—'
    flash_point = typical.get('flash_point') or p.get('flash_point') or '—'

    extra_rows = ''
    if melt_point != '—':
        extra_rows += f'<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">熔點 / 軟化點</td><td class="py-2.5 px-4 text-slate-900">{escape_html(melt_point)}</td></tr>'
    if particle_size != '—':
        extra_rows += f'<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">平均粒徑 (µm)</td><td class="py-2.5 px-4 text-slate-900">{escape_html(particle_size)}</td></tr>'
    if density != '—':
        extra_rows += f'<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">密度 (g/cm³)</td><td class="py-2.5 px-4 text-slate-900">{escape_html(density)}</td></tr>'
    if acid_value != '—':
        extra_rows += f'<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">酸價</td><td class="py-2.5 px-4 text-slate-900">{escape_html(acid_value)}</td></tr>'
    if flash_point != '—':
        extra_rows += f'<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">閃點 (°C)</td><td class="py-2.5 px-4 text-slate-900">{escape_html(flash_point)}</td></tr>'

    website = p.get('website')
    tds_link = f'<a href="{website}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-md text-xs font-bold shadow-xs transition-all"><i class="fa-solid fa-file-pdf"></i> 下載原廠技術資料表 (TDS)</a>' if (website and website != 'N/A') else ''

    fda_badge_detail = ''
    if partner_key.lower() == 'mpi' and p.get('fda_compliant'):
        fda_badge_detail = '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 align-middle ml-2"><i class="fa-solid fa-shield-halved text-[10px] text-emerald-600"></i> FDA 食品接觸合規</span>'

    return f'''
    <div class="product-seo-detail bg-white rounded-xl border border-blue-200 shadow-sm p-6 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-gray-200">
            <div>
                <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-900 mb-1.5">{escape_html(brand_name)}</span>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-blue-950 flex items-center flex-wrap gap-2">
                    <span>{escape_html(name)}</span>
                    {fda_badge_detail}
                </h1>
            </div>
            <div class="flex items-center gap-2">
                {tds_link}
                <a href="/contact" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-950 hover:bg-blue-900 text-white rounded-md text-xs font-bold shadow-xs transition-all">
                    <i class="fa-solid fa-envelope"></i> 索取樣品與技術諮詢
                </a>
            </div>
        </div>
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="border border-gray-200 rounded-lg overflow-hidden">
                <table class="w-full text-left text-sm">
                    <tbody>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">主要化學成分</td><td class="py-2.5 px-4 text-slate-900">{escape_html(comp)}</td></tr>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">主要用途 / 應用領域</td><td class="py-2.5 px-4 text-slate-900">{escape_html(usage)}</td></tr>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">性質與特點</td><td class="py-2.5 px-4 text-slate-900 whitespace-pre-line">{escape_html(props)}</td></tr>
                        {extra_rows}
                    </tbody>
                </table>
            </div>
            <div class="bg-slate-50 rounded-lg p-4 border border-slate-200 flex flex-col justify-between">
                <div>
                    <h3 class="text-sm font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-check text-emerald-600"></i> 原廠供應與品質保證
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        宏威應用材料為 {escape_html(brand_name)} 專業特用化學品代理經銷商，提供 {escape_html(name)} 之完整技術資料、原廠物性規格與配方建議。歡迎研發技術人員與採購經理線上申請樣品評估。
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
                    <span>供應狀態：現貨供應 / 樣品齊全</span>
                    <a href="/products/{partner_key}/{line_key}" class="text-blue-700 hover:underline font-bold">查看此系列所有產品 →</a>
                </div>
            </div>
        </div>
    </div>'''

def build_page_html(template_html, title, description, canonical_path, active_tab='about', pre_rendered_content='', schema_json=None):
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
            html_out = re.sub(f'id="tab-{t}" class="tab-content.*?"', f'id="tab-{t}" class="tab-content active"', html_out)
            html_out = re.sub(f'id="nav-{t}".*?aria-selected=".*?"', f'id="nav-{t}" role="tab" aria-selected="true"', html_out)
            html_out = re.sub(f'id="mobile-nav-{t}".*?aria-selected=".*?"', f'id="mobile-nav-{t}" role="tab" aria-selected="true"', html_out)
        else:
            html_out = re.sub(f'id="tab-{t}" class="tab-content active"', f'id="tab-{t}" class="tab-content"', html_out)
            html_out = re.sub(f'id="nav-{t}".*?aria-selected="true"', f'id="nav-{t}" role="tab" aria-selected="false"', html_out)
            html_out = re.sub(f'id="mobile-nav-{t}".*?aria-selected="true"', f'id="mobile-nav-{t}" role="tab" aria-selected="false"', html_out)

    if pre_rendered_content:
        html_out = re.sub(
            r'<tbody id="directory-matrix-body"[\s\S]*?</tbody>',
            f'<tbody id="directory-matrix-body" class="divide-y divide-gray-200 text-slate-800 f-weight-normal">{pre_rendered_content}</tbody>',
            html_out
        )

    if schema_json:
        schema_string = f'\n    <script type="application/ld+json">\n{json.dumps(schema_json, ensure_ascii=False, indent=2)}\n    </script>'
        html_out = html_out.replace('</head>', f'{schema_string}\n</head>')

    return html_out

def write_static_file(relative_path, html_content):
    clean_path = relative_path.strip('/')
    target_dir = os.path.join(ROOT_DIR, clean_path.replace('/', os.sep))
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    print("🚀 開始建置靜態預渲染 (SSG) 頁面 (Python 版)...")
    template_html, config, all_products_cache = load_data()
    generated_count = 0

    # 1. 核心頁面
    core_pages = [
        {
            'path': '/about/',
            'title': '宏威應用材料 Discover The Link To Life | 專業特用化學品供應商',
            'description': '宏威應用材料 Discover The Link To Life - 專業特用化學品供應商，提供PTFE取代方案、Micro Powders微粉蠟、Dorf Ketal鈦鋯酸酯、Orion特級碳黑等高性能材料與免費索樣服務。',
            'tab': 'about'
        },
        {
            'path': '/products/',
            'title': '特用化學品目錄 | 宏威應用材料 ATTech Materials',
            'description': '宏威應用材料特用化學品完整產品目錄，涵蓋微粉蠟、PTFE取代、鈦酸酯/鋯酸酯、特級碳黑、矽烷偶合劑與塗料助劑，支援線上多維度篩選與規格比對。',
            'tab': 'products'
        },
        {
            'path': '/partners/',
            'title': '合作夥伴品牌 | 宏威應用材料 Discover The Link To Life',
            'description': '宏威應用材料代理銷售 Micro Powders、Dorf Ketal、Orion 等國際領導化學品牌，提供正品保證與原廠技術支援。',
            'tab': 'partners'
        },
        {
            'path': '/contact/',
            'title': '樣品索取與技術諮詢 | 宏威應用材料 Discover The Link To Life',
            'description': '線上索取特用化學品樣品與配方技術諮詢，提供快速詢價與詳細應用需求評估雙模式表單，自動產製正式 PDF 需求單。',
            'tab': 'contact'
        }
    ]

    for cp in core_pages:
        h = build_page_html(template_html, cp['title'], cp['description'], cp['path'], active_tab=cp['tab'])
        write_static_file(cp['path'], h)
        generated_count += 1

    # 2. 品牌與產品線
    for brand_key, brand_obj in config.items():
        partner_slug = brand_key.lower()
        brand_name = brand_obj.get('brandName') or brand_key

        partner_path = f"/products/{partner_slug}/"
        ph = build_page_html(
            template_html,
            f"{brand_name} 特用化學品系列 | 宏威應用材料 ATTech Materials",
            f"宏威應用材料代理銷售 {brand_name} 全系列特用化學品，提供規格對比、TDS技術資料下載與免費樣品申請服務。",
            partner_path,
            active_tab='products'
        )
        write_static_file(partner_path, ph)
        generated_count += 1

        for f_info in brand_obj.get('files', []):
            line_slug = f_info['key']
            line_title = f_info.get('titleZh') or f_info.get('titleEn') or line_slug
            line_path = f"/products/{partner_slug}/{line_slug}/"
            products = all_products_cache.get(line_slug, [])

            # 表格 HTML
            table_rows = []
            for p in products:
                name = p.get('product_name') or p.get('name') or ''
                comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or '—'
                props = p.get('properties') or p.get('performance') or '—'
                usage = p.get('main_usage') or p.get('application_fields_zh') or ', '.join(p.get('featured_categories', [])) or '—'
                safe_url = f"/products/{partner_slug}/{line_slug}/{urllib.parse.quote(name)}/"

                is_fda_line = (partner_slug == 'mpi' and line_slug in ['industrial', 'ink'])
                fda_badge = ''
                if is_fda_line and p.get('fda_compliant'):
                    fda_badge = '<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 align-middle shrink-0 ml-1.5 shadow-xs select-none" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-[9px] text-emerald-600"></i> FDA</span>'

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
                    <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[25%]">{escape_html(usage)}</td>
                    <td class="py-3 px-3.5 text-center align-top w-[10%]">
                        <a href="{safe_url}" class="px-2.5 py-1 bg-white hover:bg-blue-50 border border-blue-300 text-blue-950 rounded font-bold text-xs shadow-xs inline-flex items-center gap-1 transition-all">
                            <span>規格詳情</span>
                            <i class="fa-solid fa-chevron-right text-[10px]"></i>
                        </a>
                    </td>
                </tr>''')

            table_content_html = ''.join(table_rows)

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
                    } for idx, p in enumerate(products)
                ]
            }

            line_html = build_page_html(
                template_html,
                f"{line_title} ({brand_name}) | 宏威應用材料 ATTech Materials",
                f"宏威應用材料精選 {brand_name} {line_title} 特用化學品，提供 {', '.join([(p.get('product_name') or p.get('name')) for p in products[:8]])} 等品項之物性參數與免費索樣。",
                line_path,
                active_tab='products',
                pre_rendered_content=table_content_html,
                schema_json=item_list_schema
            )
            write_static_file(line_path, line_html)
            generated_count += 1

            # 3. 單一產品詳情頁
            for p in products:
                p_name = (p.get('product_name') or p.get('name') or '').strip()
                if not p_name:
                    continue

                prod_path = f"/products/{partner_slug}/{line_slug}/{urllib.parse.quote(p_name)}/"
                comp = p.get('composition_zh') or p.get('chemical_component') or p.get('composition_en') or p.get('chemistry') or ''
                props = p.get('properties') or p.get('performance') or ''
                usage = p.get('main_usage') or p.get('application_fields_zh') or ', '.join(p.get('featured_categories', [])) or ''

                detail_html = render_product_detail_table(p, partner_slug, line_slug, brand_name)

                prod_schema = {
                    "@context": "https://schema.org",
                    "@graph": [
                        {
                            "@type": "BreadcrumbList",
                            "itemListElement": [
                                { "@type": "ListItem", "position": 1, "name": "首頁", "item": f"{DOMAIN}/" },
                                { "@type": "ListItem", "position": 2, "name": "產品", "item": f"{DOMAIN}/products/" },
                                { "@type": "ListItem", "position": 3, "name": brand_name, "item": f"{DOMAIN}/products/{partner_slug}/" },
                                { "@type": "ListItem", "position": 4, "name": line_title, "item": f"{DOMAIN}/products/{partner_slug}/{line_slug}/" },
                                { "@type": "ListItem", "position": 5, "name": p_name, "item": f"{DOMAIN}{prod_path}" }
                            ]
                        },
                        {
                            "@type": "Product",
                            "name": p_name,
                            "image": f"{DOMAIN}/img/MCP-Logo.png",
                            "description": f"{brand_name} {p_name} - 主要成分：{comp or '特用化學材料'}。用途：{usage or line_title}。特性：{props}",
                            "category": line_title,
                            "brand": {
                                "@type": "Brand",
                                "name": brand_name
                            },
                            "offers": {
                                "@type": "Offer",
                                "url": f"{DOMAIN}{prod_path}",
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
                    f"{p_name} ({brand_name}) | 宏威應用材料 ATTech Materials",
                    f"{brand_name} {p_name} 特用化學品：{comp + '，' if comp else ''}{props + '。' if props else ''}適用於 {usage or line_title}，提供 TDS 技術資料與樣品索取。",
                    prod_path,
                    active_tab='products',
                    pre_rendered_content=f'<tr><td colspan="4" class="p-0">{detail_html}</td></tr>',
                    schema_json=prod_schema
                )

                # 以實際名稱目錄存檔
                write_static_file(f"/products/{partner_slug}/{line_slug}/{p_name}", prod_page_html)
                generated_count += 1

    print(f"✅ 靜態預渲染完成！共產出 {generated_count} 個實體 index.html 頁面。")

if __name__ == '__main__':
    main()
