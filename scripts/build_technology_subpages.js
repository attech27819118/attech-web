/**
 * ATTech Web - Technology Subpages & Index Static Generator (Node.js)
 * 
 * 核心架構：以 js/technology.js 為唯一真實來源 (Single Source of Truth)
 * 1. 直接讀取 js/technology.js 的資料庫與 HTML 渲染函式，保證 100% 相同，絕不發生落差或語法 Bug。
 * 2. 絕不反向覆蓋或修改 js/technology.js，保障開發者手動修改的完整性。
 * 3. 一鍵生成 11 大獨立技術頁面、轉向頁、更新首頁 tab-technology、Sitemap，並備份最新 JSON。
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT_DIR = path.resolve(__dirname, '..');
const DOMAIN = 'https://www.attech.com.tw';
const CACHE_VERSION = '20261103_v1';

console.log('==================================================');
console.log('🚀 ATTech 技術專區 - 依據 js/technology.js 一鍵建置靜態頁面');
console.log('==================================================');

// 1. 讀取並執行 js/technology.js
const jsPath = path.join(ROOT_DIR, 'js', 'technology.js');
let jsCode = fs.readFileSync(jsPath, 'utf8');
jsCode += '\nglobalThis.__EXPORT__ = { TECH_CATEGORIES, TECH_DATABASE, buildCategoryContentHtml, buildSingleDocLayoutHtml, getBestSubTabForCategory, TechState };';

const globalScope = {
    window: { APP_BASE_HREF: '/', APP_VERSION: CACHE_VERSION, addEventListener: () => { } },
    document: { readyState: 'complete', addEventListener: () => { }, getElementById: () => null, querySelectorAll: () => [] }
};
const context = vm.createContext(globalScope);
vm.runInContext(jsCode, context);
const exp = context.__EXPORT__;

const categories = exp.TECH_CATEGORIES;
const database = exp.TECH_DATABASE;

console.log(`📦 成功載入前端資料庫：共 ${categories.length} 大分類、${Object.keys(database).length} 條專題資料`);

// 2. 備份最新資料至 json/tech_database.json (保持同步備份)
try {
    const jsonPath = path.join(ROOT_DIR, 'json', 'tech_database.json');
    fs.writeFileSync(jsonPath, JSON.stringify(database, null, 2), 'utf8');
    console.log('💾 已自動同步備份資料庫至 json/tech_database.json');
} catch (e) {
    console.warn('⚠️ 備份 JSON 失敗:', e.message);
}

// 3. 讀取 index.html 樣板
const templateShell = fs.readFileSync(path.join(ROOT_DIR, 'index.html'), 'utf8');

// 安全替換 tab-technology 區塊 (精準比對至 tab-partners 前，絕不殘留多餘標籤)
function replaceTechSectionInHtml(html, newSectionContent) {
    const startIdx = html.indexOf('id="tab-technology"');
    if (startIdx === -1) return html;
    const commentMarker = '<!-- Tab: 技術專區';
    let replaceStart = html.lastIndexOf(commentMarker, startIdx);
    if (replaceStart !== -1) {
        while (true) {
            const prev = html.lastIndexOf(commentMarker, replaceStart - 1);
            if (prev !== -1 && html.slice(prev, replaceStart).trim().startsWith('<!-- Tab: 技術專區')) {
                replaceStart = prev;
            } else {
                break;
            }
        }
    } else {
        replaceStart = html.lastIndexOf('<section', startIdx);
    }
    const nextSec = html.indexOf('id="tab-partners"');
    if (nextSec === -1) return html;
    let replaceEnd = html.lastIndexOf('<!-- Tab 3: 合作夥伴', nextSec);
    if (replaceEnd === -1) {
        replaceEnd = html.lastIndexOf('<section', nextSec);
    }
    return html.slice(0, replaceStart) + newSectionContent + '\n\n        ' + html.slice(replaceEnd);
}

// 側邊欄 HTML 產生器
function buildSidebarHtml(currentSlug) {
    const cards = categories.map(item => {
        const isActive = (item.slug === currentSlug);
        const url = `technology/${item.slug}/`;
        if (isActive) {
            return `                        <a href="${url}" onclick="if(event.button===0&&!event.ctrlKey&&!event.metaKey){event.preventDefault();switchTechCategory('${item.slug}');}" data-tech-slug="${item.slug}"
                           class="tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-blue-50/90 border-2 border-blue-600/80 text-blue-950 no-underline shadow-xs transition-all">
                            <div class="flex items-center gap-2 min-w-0 w-full">
                                <span class="tech-num-badge w-5 h-5 rounded-md bg-blue-900 text-white text-xs font-black flex items-center justify-center shrink-0 shadow-2xs">
                                    ${item.itemNo}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="tech-btn-title text-sm font-bold text-blue-950 truncate leading-snug">
                                        ${item.name}
                                    </div>
                                    <div class="tech-btn-sub text-xs font-medium text-blue-800/80 truncate">
                                        ${item.sub}
                                    </div>
                                </div>
                            </div>
                        </a>`;
        } else {
            return `                        <a href="${url}" onclick="if(event.button===0&&!event.ctrlKey&&!event.metaKey){event.preventDefault();switchTechCategory('${item.slug}');}" data-tech-slug="${item.slug}"
                           class="tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-blue-400 text-slate-800 hover:text-blue-950 no-underline transition-all">
                            <div class="flex items-center gap-2 min-w-0 w-full">
                                <span class="tech-num-badge w-5 h-5 rounded-md bg-slate-100 group-hover:bg-blue-50 text-slate-500 group-hover:text-blue-700 text-xs font-bold flex items-center justify-center shrink-0 transition-colors">
                                    ${item.itemNo}
                                </span>
                                <div class="min-w-0 flex-1">
                                    <div class="tech-btn-title text-sm font-bold text-slate-800 group-hover:text-blue-950 truncate leading-snug">
                                        ${item.name}
                                    </div>
                                    <div class="tech-btn-sub text-xs font-normal text-slate-500 group-hover:text-slate-600 truncate">
                                        ${item.sub}
                                    </div>
                                </div>
                            </div>
                        </a>`;
        }
    }).join('\n');

    return `                <!-- 左側：技術專題產品分類 (緊湊精緻條列) -->
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
${cards}
                    </nav>
                </aside>`;
}

// 組裝完整 subpage
function buildFullPage(cat) {
    const slug = cat.slug;
    const titleZh = cat.titleZh || `${cat.name} 技術應用`;
    const metaDesc = `宏威應用材料 ${cat.name} 技術專題，原廠技術資料與配方評估諮詢。`;
    const canonicalUrl = `${DOMAIN}/technology/${slug}/`;

    // 取得該專題最佳分頁，並設定狀態以便渲染
    const bestTab = exp.getBestSubTabForCategory(slug);
    exp.TechState.activeCategory = slug;
    exp.TechState.activeSubTab = bestTab;

    // 核心內容 HTML (直接由 js/technology.js 生成)
    const contentHtml = exp.buildCategoryContentHtml(cat);
    const switcherHtml = buildSidebarHtml(slug);

    const techSection = `    <!-- Tab: 技術專區 (Technology) - 獨立分頁一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->
    <section id="tab-technology" class="tab-content active" role="tabpanel" aria-labelledby="nav-technology">
        <style>
        .tech-layout-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
            width: 100%;
        }
        .tech-sidebar {
            width: 100%;
            flex-shrink: 0;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        }
        .tech-sidebar-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.375rem !important;
            width: 100% !important;
        }
        .tech-sidebar-btn {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .tech-sidebar-btn .min-w-0.flex-1 {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-width: 0 !important;
        }
        .tech-btn-title {
            display: block !important;
            width: 100% !important;
        }
        .tech-btn-sub {
            display: block !important;
            width: 100% !important;
        }
        .tech-content-main {
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
        }
        @media (min-width: 900px) {
            .tech-layout-container {
                flex-direction: row;
                gap: 1.25rem;
                align-items: flex-start;
            }
            .tech-sidebar {
                width: 310px;
                position: sticky;
                top: 5rem;
                max-height: calc(100vh - 5.5rem);
                display: flex;
                flex-direction: column;
                overflow-y: auto;
            }
            .tech-sidebar::-webkit-scrollbar {
                width: 4px;
            }
            .tech-sidebar::-webkit-scrollbar-track {
                background: #f8fafc;
            }
            .tech-sidebar::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
            }
        }
        /* 瀏覽器書籤風格容器與標籤列 */
        .tech-bookmark-wrapper {
            width: 100%;
            margin-top: 0.5rem;
            position: relative;
        }
        .tech-subtab-strip {
            display: flex;
            align-items: flex-end;
            gap: 0.375rem;
            padding-left: 0.5rem;
            margin-bottom: -1px;
            position: relative;
            z-index: 10;
        }
        @media (max-width: 640px) {
            .tech-subtab-strip {
                overflow-x: auto;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 1px;
            }
            .tech-subtab-strip::-webkit-scrollbar {
                display: none;
            }
        }
        .tech-subtab-btn {
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
        }
        .tech-subtab-btn:hover {
            background: #e2e8f0 !important;
            color: #0f172a !important;
        }
        .tech-subtab-btn.active {
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
        }
        .tech-bookmark-body {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 0 0.75rem 0.75rem 0.75rem;
            padding: 1rem;
            position: relative;
            z-index: 1;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }
        @media (max-width: 640px) {
            .tech-bookmark-body {
                border-radius: 0 0 0.75rem 0.75rem;
                padding: 0.75rem;
            }
        }
        /* 原理維度專用：一塊一塊技術文件切換按鈕 */
        .tech-doc-block-btn {
            font-weight: 600;
            transition: all 0.15s ease;
        }
        .tech-doc-block-btn.active {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border-color: #1e3a8a !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        .tech-principles-grid {
            display: grid;
            grid-template-columns: 50% 50%;
            gap: 0.875rem;
            align-items: start;
        }
        @media (max-width: 900px) {
            .tech-principles-grid {
                grid-template-columns: 1fr;
            }
        }
        #tech-pdf-fullscreen-modal {
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
        }
        #tech-pdf-fullscreen-modal.hidden {
            display: none !important;
        }
        #tech-pdf-fullscreen-modal .tech-modal-inner {
            position: relative !important;
            z-index: 100000 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
        }
        </style>

        <div class="optimized-container px-3 sm:px-4 py-4 sm:py-6">
            <!-- 頂部技術專區導覽列 -->
            <div class="mb-4 pb-3 border-b border-gray-200">
                <div class="flex flex-wrap items-center gap-1.5 text-xs font-semibold text-slate-500 mb-1.5">
                    <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <span id="tech-breadcrumb-current" class="text-blue-950 font-bold">${cat.name}</span>
                </div>
                
            </div>

            <!-- 主佈局架構：左側分類條列 + 右側主內容 -->
            <div class="tech-layout-container">
${switcherHtml}
                <!-- 右側主要展示區 (純白底色，無任何破版) -->
                <main class="tech-content-main min-w-0" id="tech-content-display">
${contentHtml}
                </main>
            </div>
        </div>
    </section>`;

    // 替換樣板
    let pageHtml = templateShell;

    // 將所有非 tab-technology 的 section class 設為 tab-content (移除 active)
    pageHtml = pageHtml.replace(/<section id="tab-about" class="tab-content active"/g, '<section id="tab-about" class="tab-content"');

    // 替換 tab-technology 區塊 (安全精準替換)
    pageHtml = replaceTechSectionInHtml(pageHtml, techSection);

    // 確保導覽列連結正確
    pageHtml = pageHtml.replace(/href="technology\/" id="nav-technology"/g, 'href="technology/tyzor/" id="nav-technology"');
    pageHtml = pageHtml.replace(/href="technology\/" id="mobile-nav-technology"/g, 'href="technology/tyzor/" id="mobile-nav-technology"');

    // 導覽列 Active 樣式
    pageHtml = pageHtml.replace(/id="nav-about" role="tab" aria-selected="false"\s+class="nav-btn [^"]*"/, 'id="nav-about" role="tab" aria-selected="false"\n                   class="nav-btn text-slate-700 hover:text-blue-900 border-b-2 border-transparent hover:border-gray-400 px-1 pt-1 h-16 inline-flex items-center"');
    pageHtml = pageHtml.replace(/id="nav-technology" role="tab" aria-selected="true" aria-controls="tab-technology"\s+class="nav-btn [^"]*"/, 'id="nav-technology" role="tab" aria-selected="true" aria-controls="tab-technology"\n                   class="nav-btn text-blue-950 f-weight-bold border-b-2 border-blue-900 px-1 pt-1 h-16 inline-flex items-center"');
    pageHtml = pageHtml.replace(/id="mobile-nav-about" role="tab" aria-selected="false"\s+class="mobile-nav-btn [^"]*"/, 'id="mobile-nav-about" role="tab" aria-selected="false"\n               class="mobile-nav-btn flex-1 py-1.5 px-2 text-center rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-100 transition-all"');
    pageHtml = pageHtml.replace(/id="mobile-nav-technology" role="tab" aria-selected="true"\s+class="mobile-nav-btn [^"]*"/, 'id="mobile-nav-technology" role="tab" aria-selected="true"\n               class="mobile-nav-btn flex-1 py-1.5 px-2 text-center rounded-lg text-xs font-bold transition-all bg-blue-900 text-white shadow-xs"');

    // 快取版本號更新
    pageHtml = pageHtml.replace(/css\/output\.css\?v=[^"]*/g, `css/output.css?v=${CACHE_VERSION}`);
    pageHtml = pageHtml.replace(/css\/style\.css\?v=[^"]*/g, `css/style.css?v=${CACHE_VERSION}`);
    pageHtml = pageHtml.replace(/js\/([^"]+?\.js)\?v=[^"]*/g, `js/$1?v=${CACHE_VERSION}`);

    // PDF.js 確保載入
    if (!pageHtml.includes('js/vendor/pdf.min.js')) {
        pageHtml = pageHtml.replace('<script src="js/technology.js', '<script src="js/vendor/pdf.min.js"></script>\n    <script src="js/technology.js');
    }

    // Title & Meta SEO
    const pageTitle = `${cat.name} | 宏威應用材料 ATTech Materials`;
    pageHtml = pageHtml.replace(/<title[^>]*>.*?<\/title>/, `<title id="web-title">${pageTitle}</title>`);
    pageHtml = pageHtml.replace(/<meta\s+name="description"\s+content="[^"]*"/, `<meta name="description" content="${metaDesc}"`);
    pageHtml = pageHtml.replace(/<link\s+rel="canonical"\s+href="[^"]*"/, `<link rel="canonical" href="${canonicalUrl}"`);
    pageHtml = pageHtml.replace(/<meta\s+property="og:title"\s+content="[^"]*"/, `<meta property="og:title" content="${pageTitle}"`);
    pageHtml = pageHtml.replace(/<meta\s+property="og:url"\s+content="[^"]*"/, `<meta property="og:url" content="${canonicalUrl}"`);
    pageHtml = pageHtml.replace(/<meta\s+property="og:description"\s+content="[^"]*"/, `<meta property="og:description" content="${metaDesc}"`);

    // Body 屬性
    pageHtml = pageHtml.replace('<body class="', `<body data-tech-slug="${slug}" class="`);

    return pageHtml;
}

// 4. 開始建置 11 大獨立技術頁面
console.log('📄 [1/3] 開始生成 11 大特用化學品獨立技術頁面...');
for (const cat of categories) {
    const slug = cat.slug;
    const subDir = path.join(ROOT_DIR, 'technology', slug);
    if (!fs.existsSync(subDir)) {
        fs.mkdirSync(subDir, { recursive: true });
    }
    const subFile = path.join(subDir, 'index.html');
    const html = buildFullPage(cat);
    fs.writeFileSync(subFile, html, 'utf8');
    console.log(`  [SUBPAGE] 建立獨立分頁: technology/${slug}/index.html (${html.length} bytes)`);
}

// 5. 產生 technology/index.html (轉向頁)
const redirectHtml = `<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=tyzor/">
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
</html>`;
fs.writeFileSync(path.join(ROOT_DIR, 'technology', 'index.html'), redirectHtml, 'utf8');
console.log('  [MAIN] 更新技術專區自動轉向頁: technology/index.html');

// 6. 同步更新根目錄 index.html 中的 #tab-technology
console.log('🔄 [2/3] 同步更新根目錄 index.html 與 sitemap.xml...');
try {
    const rootIndexPath = path.join(ROOT_DIR, 'index.html');
    let rootHtml = fs.readFileSync(rootIndexPath, 'utf8');

    // 取得 Tyzor 核心內容
    const tyzorCat = categories[0];
    exp.TechState.activeCategory = tyzorCat.slug;
    exp.TechState.activeSubTab = exp.getBestSubTabForCategory(tyzorCat.slug);
    const tyzorContentHtml = exp.buildCategoryContentHtml(tyzorCat);
    const tyzorSidebarHtml = buildSidebarHtml(tyzorCat.slug);

    const rootTechSection = `    <!-- Tab: 技術專區 (Technology) - 獨立分頁一頁式緊湊呈現 (統一白色風格：左側條列式切換，右側資料顯示) -->
    <section id="tab-technology" class="tab-content" role="tabpanel" aria-labelledby="nav-technology">
        <style>
        .tech-layout-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
            width: 100%;
        }
        .tech-sidebar {
            width: 100%;
            flex-shrink: 0;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        }
        .tech-sidebar-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.375rem !important;
            width: 100% !important;
        }
        .tech-sidebar-btn {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .tech-sidebar-btn .min-w-0.flex-1 {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-width: 0 !important;
        }
        .tech-btn-title {
            display: block !important;
            width: 100% !important;
        }
        .tech-btn-sub {
            display: block !important;
            width: 100% !important;
        }
        .tech-content-main {
            flex: 1 1 0%;
            min-width: 0;
            width: 100%;
        }
        @media (min-width: 900px) {
            .tech-layout-container {
                flex-direction: row;
                gap: 1.25rem;
                align-items: flex-start;
            }
            .tech-sidebar {
                width: 310px;
                position: sticky;
                top: 5rem;
                max-height: calc(100vh - 5.5rem);
                display: flex;
                flex-direction: column;
                overflow-y: auto;
            }
            .tech-sidebar::-webkit-scrollbar {
                width: 4px;
            }
            .tech-sidebar::-webkit-scrollbar-track {
                background: #f8fafc;
            }
            .tech-sidebar::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
            }
        }
        /* 瀏覽器書籤風格容器與標籤列 */
        .tech-bookmark-wrapper {
            width: 100%;
            margin-top: 0.5rem;
            position: relative;
        }
        .tech-subtab-strip {
            display: flex;
            align-items: flex-end;
            gap: 0.375rem;
            padding-left: 0.5rem;
            margin-bottom: -1px;
            position: relative;
            z-index: 10;
        }
        @media (max-width: 640px) {
            .tech-subtab-strip {
                overflow-x: auto;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 1px;
            }
            .tech-subtab-strip::-webkit-scrollbar {
                display: none;
            }
        }
        .tech-subtab-btn {
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
        }
        .tech-subtab-btn:hover {
            background: #e2e8f0 !important;
            color: #0f172a !important;
        }
        .tech-subtab-btn.active {
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
        }
        .tech-bookmark-body {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 0 0.75rem 0.75rem 0.75rem;
            padding: 1rem;
            position: relative;
            z-index: 1;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
        }
        @media (max-width: 640px) {
            .tech-bookmark-body {
                border-radius: 0 0 0.75rem 0.75rem;
                padding: 0.75rem;
            }
        }
        /* 原理維度專用：一塊一塊技術文件切換按鈕 */
        .tech-doc-block-btn {
            font-weight: 600;
            transition: all 0.15s ease;
        }
        .tech-doc-block-btn.active {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border-color: #1e3a8a !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        .tech-principles-grid {
            display: grid;
            grid-template-columns: 50% 50%;
            gap: 0.875rem;
            align-items: start;
        }
        @media (max-width: 900px) {
            .tech-principles-grid {
                grid-template-columns: 1fr;
            }
        }
        #tech-pdf-fullscreen-modal {
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
        }
        #tech-pdf-fullscreen-modal.hidden {
            display: none !important;
        }
        #tech-pdf-fullscreen-modal .tech-modal-inner {
            position: relative !important;
            z-index: 100000 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
        }
        </style>

        <div class="optimized-container px-3 sm:px-4 py-4 sm:py-6">
            <div class="mb-4 pb-3 border-b border-gray-200">
                <div class="flex flex-wrap items-center gap-1.5 text-xs font-semibold text-slate-500 mb-1.5">
                    <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <a href="technology/tyzor/" class="hover:text-blue-900 hover:underline">技術專區</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <span id="tech-breadcrumb-current" class="text-blue-950 font-bold">${tyzorCat.name}</span>
                </div>
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                        <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2">
                            <span class="w-2 h-6 bg-blue-900 rounded-full inline-block"></span>
                            技術專區 (Technology)
                        </h2>
                    </div>
                    
                </div>
            </div>

            <div class="tech-layout-container">
${tyzorSidebarHtml}
                <main class="tech-content-main min-w-0" id="tech-content-display">
${tyzorContentHtml}
                </main>
            </div>
        </div>
    </section>`;

    rootHtml = replaceTechSectionInHtml(rootHtml, rootTechSection);

    rootHtml = rootHtml.replace(/href="technology\/" id="nav-technology"/g, 'href="technology/tyzor/" id="nav-technology"');
    rootHtml = rootHtml.replace(/href="technology\/" id="mobile-nav-technology"/g, 'href="technology/tyzor/" id="mobile-nav-technology"');

    rootHtml = rootHtml.replace(/css\/output\.css\?v=[^"]*/g, `css/output.css?v=${CACHE_VERSION}`);
    rootHtml = rootHtml.replace(/css\/style\.css\?v=[^"]*/g, `css/style.css?v=${CACHE_VERSION}`);
    rootHtml = rootHtml.replace(/js\/([^"]+?\.js)\?v=[^"]*/g, `js/$1?v=${CACHE_VERSION}`);

    fs.writeFileSync(rootIndexPath, rootHtml, 'utf8');
    console.log('  [ROOT] 已同步更新首頁 index.html 中的 #tab-technology');
} catch (e) {
    console.warn('⚠️ 更新首頁失敗:', e.message);
}

// 7. 更新 sitemap.xml
try {
    const sitemapPath = path.join(ROOT_DIR, 'sitemap.xml');
    if (fs.existsSync(sitemapPath)) {
        let xml = fs.readFileSync(sitemapPath, 'utf8');
        const addedUrls = [];

        const mainTechUrl = `${DOMAIN}/technology/`;
        if (!xml.includes(`<loc>${mainTechUrl}</loc>`)) {
            addedUrls.push(mainTechUrl);
        }
        for (const cat of categories) {
            const url = `${DOMAIN}/technology/${cat.slug}/`;
            if (!xml.includes(`<loc>${url}</loc>`)) {
                addedUrls.push(url);
            }
        }
        if (addedUrls.length > 0) {
            let pos = xml.indexOf(`<loc>${DOMAIN}/contact/</loc>`);
            if (pos === -1) pos = xml.indexOf(`<loc>${DOMAIN}/</loc>`);
            if (pos !== -1) {
                const endPos = xml.indexOf('</url>', pos) + '</url>'.length;
                const todayStr = new Date().toISOString().split('T')[0];
                const newBlocks = addedUrls.map(u => `\n    <url>\n        <loc>${u}</loc>\n        <lastmod>${todayStr}</lastmod>\n        <changefreq>weekly</changefreq>\n        <priority>0.85</priority>\n    </url>`).join('');
                xml = xml.slice(0, endPos) + newBlocks + xml.slice(endPos);
                fs.writeFileSync(sitemapPath, xml, 'utf8');
                console.log(`  [SITEMAP] 已在 sitemap.xml 中加入 ${addedUrls.length} 個技術頁面網址`);
            }
        }
    }
} catch (e) {
    console.warn('⚠️ 更新 Sitemap 失敗:', e.message);
}

console.log('==================================================');
console.log('🎉 [3/3] 11 項技術獨立分頁已全數建置完成！');
console.log('🛡️ js/technology.js 保持原汁原味，絕不覆蓋您的程式碼！');
console.log('==================================================');
