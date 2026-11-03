import os
import re

ROOT_DIR = r"d:\Jay\vscode\attech0824 - test"
SUBPAGES_PY = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")
JS_PATH = os.path.join(ROOT_DIR, "js", "technology.js")

print("=== 1. Updating scripts/build_technology_subpages.py ===")
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_code = f.read()

# A. 在 build_category_content_section 中加入類別簡介說明 (item["description"])
old_sec_pattern = re.compile(
    r'(<div class="flex items-center justify-between gap-3 pb-2 border-b border-slate-100">.*?</div>\s*</div>\s*)(<!-- 瀏覽器書籤風格容器 -->)',
    re.DOTALL
)

desc_snippet = '''
                <!-- 專題核心技術簡介說明 -->
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                    {item.get("description", "")}
                </p>

                '''

if old_sec_pattern.search(py_code):
    py_code = old_sec_pattern.sub(r'\1' + desc_snippet + r'\2', py_code)
    print("Added item['description'] to build_category_content_section in python script.")
else:
    print("Could not match section header pattern in python script, checking...")

# B. 在 build_single_doc_layout_html 中確保讀取 doc.get("desc") or doc.get("summary")
old_desc_code = '{doc.get("desc")}'
new_desc_code = '{doc.get("desc") or doc.get("summary") or ""}'
if old_desc_code in py_code:
    py_code = py_code.replace(old_desc_code, new_desc_code)
    print("Updated doc.get('desc') fallback in build_single_doc_layout_html.")

# C. 修正 get_best_subtab_for_category 的搜尋優先順序 (1.原理 -> 2.目錄 -> 3.應用技術 -> 4.單一產品技術)
old_best_subtab = '''def get_best_subtab_for_category(slug):
    """取得特定產品線最佳的預設子分頁 (優先選擇有實際原廠文件的分頁，避免首屏顯示空白)"""
    cat_data = TECH_DATABASE.get(slug, {"tabs": {}})
    tabs = cat_data.get("tabs", {})
    
    # 優先順序：principles (若有) -> applications (若有) -> catalog (若有) -> single (若有) -> formulation
    if tabs.get("principles") and len(tabs["principles"]) > 0:
        return "principles"
    elif tabs.get("applications") and len(tabs["applications"]) > 0:
        return "applications"
    elif tabs.get("catalog") and len(tabs["catalog"]) > 0:
        return "catalog"
    elif tabs.get("single") and len(tabs["single"]) > 0:
        return "single"
    elif tabs.get("formulation") and len(tabs["formulation"]) > 0:
        return "formulation"
    return "principles"'''

new_best_subtab = '''def get_best_subtab_for_category(slug):
    """取得特定產品線最佳的預設子分頁 (按 1.原理 -> 2.目錄 -> 3.應用技術 -> 4.單一產品技術 自然順序)"""
    cat_data = TECH_DATABASE.get(slug, {"tabs": {}})
    tabs = cat_data.get("tabs", {})
    
    order = ["principles", "catalog", "applications", "single", "formulation"]
    for tab_key in order:
        if tabs.get(tab_key) and len(tabs[tab_key]) > 0:
            return tab_key
    return "principles"'''

if old_best_subtab in py_code:
    py_code = py_code.replace(old_best_subtab, new_best_subtab)
    print("Updated get_best_subtab_for_category to natural order in python script.")

# D. 快取版本號更新至 20261007_fix1
py_code = re.sub(r'js/technology\.js\?v=[^"\'`]*', 'js/technology.js?v=20261007_fix1', py_code)

with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
    f.write(py_code)
print("Saved scripts/build_technology_subpages.py successfully!")


print("\n=== 2. Updating js/technology.js ===")
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_code = f.read()

# A. 修正 getBestSubTabForCategory 的自然搜尋順序
old_js_best = '''function getBestSubTabForCategory(slug) {
    const catData = TECH_DATABASE[slug];
    if (!catData || !catData.tabs) return 'principles';

    // 若當前選取的 subTab 在目標類別中有文件，維持當前選取
    if (TechState.activeSubTab && catData.tabs[TechState.activeSubTab] && catData.tabs[TechState.activeSubTab].length > 0) {
        return TechState.activeSubTab;
    }

    // 依序搜尋首個有資料的維度分頁
    const candidates = ['principles', 'applications', 'catalog', 'single', 'formulation'];
    for (const tabKey of candidates) {
        if (catData.tabs[tabKey] && catData.tabs[tabKey].length > 0) {
            return tabKey;
        }
    }
    return 'principles';
}'''

new_js_best = '''function getBestSubTabForCategory(slug) {
    const catData = TECH_DATABASE[slug];
    if (!catData || !catData.tabs) return 'principles';

    // 若當前選取的 subTab 在目標類別中有文件，維持當前選取
    if (TechState.activeSubTab && catData.tabs[TechState.activeSubTab] && catData.tabs[TechState.activeSubTab].length > 0) {
        return TechState.activeSubTab;
    }

    // 依自然順序 (1.原理 -> 2.目錄 -> 3.應用技術 -> 4.單一產品技術 -> 5.配方) 搜尋首個有資料的維度分頁
    const candidates = ['principles', 'catalog', 'applications', 'single', 'formulation'];
    for (const tabKey of candidates) {
        if (catData.tabs[tabKey] && catData.tabs[tabKey].length > 0) {
            return tabKey;
        }
    }
    return 'principles';
}'''

if old_js_best in js_code:
    js_code = js_code.replace(old_js_best, new_js_best)
    print("Updated getBestSubTabForCategory in js/technology.js.")

# B. 定義 buildEmptyTabHtml 函數 (修復重要 BUG：先前缺失導致點擊無資料分頁時 JS 拋出 ReferenceError 崩潰)
build_empty_js = '''/**
 * 建立無公開資料提示區塊 HTML (實事求是、誠實告知、不杜撰)
 */
function buildEmptyTabHtml(cat, tabKey) {
    const tabNames = {
        principles: '原理機制',
        catalog: '總覽目錄',
        applications: '應用技術資料',
        single: '單一產品技術資料',
        formulation: '配方指南'
    };
    const name = tabNames[tabKey] || '技術資料';
    const catName = cat.name || '特用化學品';
    const inquiryParam = encodeURIComponent(catName);
    const productLink = cat.productLink || 'products/';

    return `
        <div class="rounded-xl border border-slate-200 bg-slate-50/70 p-4 sm:p-6 text-center space-y-2.5">
            <div class="flex items-center justify-center gap-2">
                <i class="fa-solid fa-folder-open text-slate-400 text-base"></i>
                <span class="px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 text-xs font-bold">資料整備中</span>
                <span class="text-sm sm:text-base font-bold text-blue-950">原廠技術資料整理中，暫無公開${name}</span>
            </div>
            <p class="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                目前原廠未提供此項之公開資料，我們秉持實事求是原則不進行臆測杜撰。若您需要特定規格手冊或評估樣品，歡迎直接聯繫宏威業務團隊為您服務。
            </p>
            <div class="pt-1 flex items-center justify-center gap-2.5">
                <a href="contact/?mode=detailed&inquiry=${inquiryParam}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                    <i class="fa-solid fa-paper-plane text-xs"></i>
                    <span>聯繫業務索取資料</span>
                </a>
                <a href="${productLink}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                    <i class="fa-solid fa-table-list text-xs"></i>
                    <span>瀏覽相關產品專區</span>
                </a>
            </div>
        </div>
    `;
}'''

# 將 buildEmptyTabHtml 插入至 buildCategoryContentHtml 上方
if 'function buildEmptyTabHtml(' not in js_code:
    target_marker = 'function buildCategoryContentHtml(cat) {'
    if target_marker in js_code:
        js_code = js_code.replace(target_marker, build_empty_js + '\n\n' + target_marker)
        print("Inserted buildEmptyTabHtml into js/technology.js.")

# C. 在 buildSingleDocLayoutHtml 中修復 doc.desc 讀取 (修復重要 BUG：原先僅讀取 doc.summary，導致 74 份文件的說明全部空白不見)
old_summary_p = '<p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">\n                    ${doc.summary || \'\'}\n                </p>'
new_summary_p = '<p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">\n                    ${doc.desc || doc.summary || \'\'}\n                </p>'
if old_summary_p in js_code:
    js_code = js_code.replace(old_summary_p, new_summary_p)
    print("Fixed doc.desc in buildSingleDocLayoutHtml.")
else:
    # 彈性替換
    js_code = re.sub(
        r'\$\{doc\.summary\s*\|\|\s*\'\'\}',
        r'${doc.desc || doc.summary || \'\'}',
        js_code
    )
    print("Substituted ${doc.desc || doc.summary || ''} in js/technology.js.")

# D. 在 buildCategoryContentHtml 中加入類別說明段落 (cat.desc)
old_cat_header = '''                <div class="shrink-0 flex items-center">
                    <a href="${cat.productLink}"
                       class="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-bold transition-colors">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>${cat.productLinkText}</span>
                    </a>
                </div>
            </div>

            <!-- 瀏覽器書籤風格容器 -->'''

new_cat_header = '''                <div class="shrink-0 flex items-center">
                    <a href="${cat.productLink}"
                       class="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-bold transition-colors">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>${cat.productLinkText}</span>
                    </a>
                </div>
            </div>

            <!-- 專題核心技術簡介說明 -->
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-200/80">
                ${cat.desc || cat.description || ''}
            </p>

            <!-- 瀏覽器書籤風格容器 -->'''

if old_cat_header in js_code:
    js_code = js_code.replace(old_cat_header, new_cat_header)
    print("Added cat.desc to buildCategoryContentHtml in js/technology.js.")

# E. 優化 initTechnologyModule (保護子頁面既有 DOM 不被清空重置，僅執行 PDF Canvas 就緒渲染)
old_init = '''function initTechnologyModule() {
    const display = document.getElementById('tech-content-display');
    if (!display) return;
    const currentSlug = document.body.getAttribute('data-tech-slug') || 'tyzor';
    switchTechCategory(currentSlug, false);
}'''

new_init = '''function initTechnologyModule() {
    const display = document.getElementById('tech-content-display');
    if (!display) return;
    const currentSlug = document.body.getAttribute('data-tech-slug') || 'tyzor';

    // 若頁面已由伺服器或靜態建置產生完成 (獨立子頁面)，維持既有 DOM 完整性，僅同步狀態與啟動首頁 PDF 封面渲染！
    const visiblePanel = display.querySelector('.tech-bookmark-body > div:not(.hidden)');
    if (visiblePanel) {
        TechState.activeCategory = currentSlug;
        const panelId = visiblePanel.id || '';
        const currentTabKey = panelId.replace('tech-panel-', '');
        if (currentTabKey) {
            TechState.activeSubTab = currentTabKey;
        }
        const activeViewer = visiblePanel.querySelector('.pdf-viewer-container');
        if (activeViewer && !activeViewer.querySelector('canvas')) {
            const pdfUrl = activeViewer.getAttribute('data-pdf-url');
            if (pdfUrl && activeViewer.id) {
                renderPdfDocumentToContainer(activeViewer.id, pdfUrl);
            }
        }
        return;
    }

    // SPA 模式或主頁模式下需要動態渲染
    switchTechCategory(currentSlug, false);
}'''

if old_init in js_code:
    js_code = js_code.replace(old_init, new_init)
    print("Enhanced initTechnologyModule to preserve pre-rendered subpage DOM.")

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_code)
print("Saved js/technology.js successfully!")
