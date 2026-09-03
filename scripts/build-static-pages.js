const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const templatePath = path.join(rootDir, 'index.html');
const configPath = path.join(rootDir, 'config.json');
const DOMAIN = 'https://www.attech.com.tw';

if (!fs.existsSync(templatePath) || !fs.existsSync(configPath)) {
    console.error('Missing index.html or config.json');
    process.exit(1);
}

const templateHtml = fs.readFileSync(templatePath, 'utf8');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Helper to escape HTML
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// 讀取所有品牌產品庫
const allProductsCache = {};
for (const [brandKey, brandObj] of Object.entries(config)) {
    if (brandObj.masterPath) {
        const masterFilePath = path.join(rootDir, brandObj.masterPath.replace(/^\.?\//, ''));
        if (fs.existsSync(masterFilePath)) {
            const masterData = JSON.parse(fs.readFileSync(masterFilePath, 'utf8'));
            allProductsCache['mpi_master'] = masterData;
            for (const file of brandObj.files) {
                allProductsCache[file.key] = masterData.filter(p => p.applications_data && p.applications_data[file.key]);
            }
        }
    } else if (brandObj.files) {
        for (const file of brandObj.files) {
            if (file.jsonPath) {
                const jsonFilePath = path.join(rootDir, file.jsonPath.replace(/^\.?\//, ''));
                if (fs.existsSync(jsonFilePath)) {
                    try {
                        const data = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
                        allProductsCache[file.key] = Array.isArray(data) ? data : (data.products || []);
                    } catch (e) {
                        allProductsCache[file.key] = [];
                    }
                }
            }
        }
    }
}

// 產生單一產品規格表格 HTML
function renderProductDetailTableHtml(product, partnerKey, lineKey, brandName) {
    const p = product;
    const name = p.product_name || p.name || '';
    const comp = p.composition_zh || p.chemical_component || p.composition_en || p.chemistry || '—';
    const props = p.properties || p.performance || '—';
    const usage = p.main_usage || p.application_fields_zh || (p.featured_categories || []).join(', ') || '—';
    const density = p.typical_properties?.density_g_cc_25c || p.density || '—';
    const meltPoint = p.typical_properties?.melt_point_c || p.softening_point || '—';
    const particleSize = p.typical_properties?.mean_particle_size_um || p.particle_size || '—';
    const acidValue = p.typical_properties?.acid_value || p.acid_value || '—';
    const flashPoint = p.typical_properties?.flash_point || p.flash_point || '—';

    let extraRows = '';
    if (meltPoint !== '—') extraRows += `<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">熔點 / 軟化點</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(meltPoint)}</td></tr>`;
    if (particleSize !== '—') extraRows += `<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">平均粒徑 (µm)</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(particleSize)}</td></tr>`;
    if (density !== '—') extraRows += `<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">密度 (g/cm³)</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(density)}</td></tr>`;
    if (acidValue !== '—') extraRows += `<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">酸價</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(acidValue)}</td></tr>`;
    if (flashPoint !== '—') extraRows += `<tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">閃點 (°C)</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(flashPoint)}</td></tr>`;

    const tdsLink = p.website && p.website !== 'N/A' 
        ? `<a href="${p.website}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-md text-xs font-bold shadow-xs transition-all"><i class="fa-solid fa-file-pdf"></i> 下載原廠技術資料表 (TDS)</a>`
        : '';

    return `
    <div class="product-seo-detail bg-white rounded-xl border border-blue-200 shadow-sm p-6 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-gray-200">
            <div>
                <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-900 mb-1.5">${escapeHtml(brandName)}</span>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-blue-950">${escapeHtml(name)}</h1>
            </div>
            <div class="flex items-center gap-2">
                ${tdsLink}
                <a href="/contact" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-950 hover:bg-blue-900 text-white rounded-md text-xs font-bold shadow-xs transition-all">
                    <i class="fa-solid fa-envelope"></i> 索取樣品與技術諮詢
                </a>
            </div>
        </div>
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="border border-gray-200 rounded-lg overflow-hidden">
                <table class="w-full text-left text-sm">
                    <tbody>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">主要化學成分</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(comp)}</td></tr>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">主要用途 / 應用領域</td><td class="py-2.5 px-4 text-slate-900">${escapeHtml(usage)}</td></tr>
                        <tr class="border-b border-gray-100"><td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50 w-1/3">性質與特點</td><td class="py-2.5 px-4 text-slate-900 whitespace-pre-line">${escapeHtml(props)}</td></tr>
                        ${extraRows}
                    </tbody>
                </table>
            </div>
            <div class="bg-slate-50 rounded-lg p-4 border border-slate-200 flex flex-col justify-between">
                <div>
                    <h3 class="text-sm font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-check text-emerald-600"></i> 原廠供應與品質保證
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        宏威應用材料為 ${escapeHtml(brandName)} 專業特用化學品代理經銷商，提供 ${escapeHtml(name)} 之完整技術資料、原廠物性規格與配方建議。歡迎研發技術人員與採購經理線上申請樣品評估。
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
                    <span>供應狀態：現貨供應 / 樣品齊全</span>
                    <a href="/products/${partnerKey}/${lineKey}" class="text-blue-700 hover:underline font-bold">查看此系列所有產品 →</a>
                </div>
            </div>
        </div>
    </div>`;
}

// 產生分類列表產品表格 HTML
function renderProductListTableHtml(products, partnerKey, lineKey, brandName) {
    if (!products || products.length === 0) return '';
    const rows = products.map((p, idx) => {
        const name = p.product_name || p.name || '';
        const comp = p.composition_zh || p.chemical_component || p.composition_en || p.chemistry || '—';
        const props = p.properties || p.performance || '—';
        const usage = p.main_usage || p.application_fields_zh || (p.featured_categories || []).join(', ') || '—';
        const safeUrl = `/products/${partnerKey}/${lineKey}/${encodeURIComponent(name)}`;
        const isFdaLine = (partnerKey.toLowerCase() === 'mpi' && (lineKey === 'industrial' || lineKey === 'ink'));
        const fdaBadge = (isFdaLine && p.fda_compliant)
            ? `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 align-middle shrink-0 ml-1.5 shadow-xs select-none" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-[9px] text-emerald-600"></i> FDA</span>`
            : '';

        return `
        <tr class="hover:bg-blue-50/50 border-b border-gray-200 text-sm transition-colors" data-product-name="${escapeHtml(name)}" data-index="${idx}">
            <td class="py-3 px-3.5 font-bold text-slate-900 align-top w-[25%]">
                <div class="flex items-center flex-wrap gap-y-0.5">
                    <a href="${safeUrl}" class="text-blue-950 font-extrabold text-sm hover:underline inline leading-snug">
                        ${escapeHtml(name)}
                    </a>
                    ${fdaBadge}
                </div>
                <div class="text-xs text-slate-500 font-normal mt-0.5">${escapeHtml(comp)}</div>
            </td>
            <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[40%]">${escapeHtml(props)}</td>
            <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[25%]">${escapeHtml(usage)}</td>
            <td class="py-3 px-3.5 text-center align-top w-[10%]">
                <a href="${safeUrl}" class="px-2.5 py-1 bg-white hover:bg-blue-50 border border-blue-300 text-blue-950 rounded font-bold text-xs shadow-xs inline-flex items-center gap-1 transition-all">
                    <span>規格詳情</span>
                    <i class="fa-solid fa-chevron-right text-[10px]"></i>
                </a>
            </td>
        </tr>`;
    }).join('');

    return `
    <table class="w-full text-left border-collapse text-sm table-auto min-w-full">
        <thead>
            <tr class="bg-slate-100 border-b border-slate-300 text-slate-900 font-bold text-sm">
                <th class="py-3 px-3.5 w-[25%]">產品名稱 / 成分</th>
                <th class="py-3 px-3.5 w-[40%]">性質與特點描述</th>
                <th class="py-3 px-3.5 w-[25%]">主要用途 / 應用領域</th>
                <th class="py-3 px-3.5 w-[10%] text-center">操作</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 text-slate-800 font-normal">
            ${rows}
        </tbody>
    </table>`;
}

// 產生完整 HTML 頁面
function buildPageHtml({
    title,
    description,
    canonicalPath,
    activeTab = 'about',
    preRenderedContent = '',
    schemaJson = null,
    breadcrumbs = []
}) {
    let html = templateHtml;

    // 1. 替換 Title
    html = html.replace(/<title id="web-title">.*?<\/title>/, `<title id="web-title">${escapeHtml(title)}</title>`);

    // 2. 替換 Meta Description
    html = html.replace(/<meta name="description"\s+content=".*?">/s, `<meta name="description" content="${escapeHtml(description)}">`);

    // 3. 替換 Canonical
    const fullCanonical = `${DOMAIN}${canonicalPath === '/' ? '' : canonicalPath}`;
    html = html.replace(/<link rel="canonical"\s+href=".*?">/, `<link rel="canonical" href="${fullCanonical}">`);

    // 4. 替換 OpenGraph & Twitter
    html = html.replace(/<meta property="og:title"\s+content=".*?">/, `<meta property="og:title" content="${escapeHtml(title)}">`);
    html = html.replace(/<meta property="og:description"\s+content=".*?">/, `<meta property="og:description" content="${escapeHtml(description)}">`);
    html = html.replace(/<meta property="og:url"\s+content=".*?">/, `<meta property="og:url" content="${fullCanonical}">`);
    html = html.replace(/<meta name="twitter:title"\s+content=".*?">/, `<meta name="twitter:title" content="${escapeHtml(title)}">`);
    html = html.replace(/<meta name="twitter:description"\s+content=".*?">/, `<meta name="twitter:description" content="${escapeHtml(description)}">`);
    html = html.replace(/<meta name="twitter:url"\s+content=".*?">/, `<meta name="twitter:url" content="${fullCanonical}">`);

    // 5. 設定 Active Tab
    const tabs = ['about', 'products', 'partners', 'contact'];
    tabs.forEach(t => {
        if (t === activeTab) {
            html = html.replace(new RegExp(`id="tab-${t}" class="tab-content.*?"`), `id="tab-${t}" class="tab-content active"`);
            html = html.replace(new RegExp(`id="nav-${t}".*?aria-selected=".*?"`), `id="nav-${t}" role="tab" aria-selected="true"`);
            html = html.replace(new RegExp(`id="mobile-nav-${t}".*?aria-selected=".*?"`), `id="mobile-nav-${t}" role="tab" aria-selected="true"`);
        } else {
            html = html.replace(new RegExp(`id="tab-${t}" class="tab-content active"`), `id="tab-${t}" class="tab-content"`);
            html = html.replace(new RegExp(`id="nav-${t}".*?aria-selected="true"`), `id="nav-${t}" role="tab" aria-selected="false"`);
            html = html.replace(new RegExp(`id="mobile-nav-${t}".*?aria-selected="true"`), `id="mobile-nav-${t}" role="tab" aria-selected="false"`);
        }
    });

    // 6. 注入預渲染內容 (如果有的話)
    if (preRenderedContent) {
        // 替換或注入至 table container
        html = html.replace(
            /<tbody id="directory-matrix-body"[\s\S]*?<\/tbody>/,
            `<tbody id="directory-matrix-body" class="divide-y divide-gray-200 text-slate-800 f-weight-normal">${preRenderedContent}</tbody>`
        );
    }

    // 7. 注入專屬 Schema.org JSON-LD
    if (schemaJson) {
        const schemaString = `\n    <script type="application/ld+json">\n${JSON.stringify(schemaJson, null, 2)}\n    </script>`;
        html = html.replace('</head>', `${schemaString}\n</head>`);
    }

    return html;
}

// 建立資料夾並寫入 index.html
function writeStaticHtmlFile(relativePath, htmlContent) {
    const targetDir = path.join(rootDir, relativePath.replace(/^\//, ''));
    if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
    }
    const filePath = path.join(targetDir, 'index.html');
    fs.writeFileSync(filePath, htmlContent, 'utf8');
}

console.log('🚀 開始建置靜態預渲染 (SSG) 頁面...');
let generatedCount = 0;

// 1. 核心頁面
const corePages = [
    {
        path: '/about/',
        title: '宏威應用材料 Discover The Link To Life | 專業特用化學品供應商',
        description: '宏威應用材料 Discover The Link To Life - 專業特用化學品供應商，提供PTFE取代方案、Micro Powders微粉蠟、Dorf Ketal鈦鋯酸酯、Orion特級碳黑等高性能材料與免費索樣服務。',
        tab: 'about'
    },
    {
        path: '/products/',
        title: '特用化學品目錄 | 宏威應用材料 ATTech Materials',
        description: '宏威應用材料特用化學品完整產品目錄，涵蓋微粉蠟、PTFE取代、鈦酸酯/鋯酸酯、特級碳黑、矽烷偶合劑與塗料助劑，支援線上多維度篩選與規格比對。',
        tab: 'products'
    },
    {
        path: '/partners/',
        title: '合作夥伴品牌 | 宏威應用材料 Discover The Link To Life',
        description: '宏威應用材料代理銷售 Micro Powders、Dorf Ketal、Orion 等國際領導化學品牌，提供正品保證與原廠技術支援。',
        tab: 'partners'
    },
    {
        path: '/contact/',
        title: '樣品索取與技術諮詢 | 宏威應用材料 Discover The Link To Life',
        description: '線上索取特用化學品樣品與配方技術諮詢，提供快速詢價與詳細應用需求評估雙模式表單，自動產製正式 PDF 需求單。',
        tab: 'contact'
    }
];

corePages.forEach(page => {
    const html = buildPageHtml({
        title: page.title,
        description: page.description,
        canonicalPath: page.path,
        activeTab: page.tab
    });
    writeStaticHtmlFile(page.path, html);
    generatedCount++;
});

// 2. 品牌與產品線頁面
for (const [brandKey, brandObj] of Object.entries(config)) {
    const partnerSlug = brandKey.toLowerCase();
    const brandName = brandObj.brandName || brandKey;

    // 品牌首頁
    const partnerPath = `/products/${partnerSlug}/`;
    const partnerHtml = buildPageHtml({
        title: `${brandName} 特用化學品系列 | 宏威應用材料 ATTech Materials`,
        description: `宏威應用材料代理銷售 ${brandName} 全系列特用化學品，提供規格對比、TDS技術資料下載與免費樣品申請服務。`,
        canonicalPath: partnerPath,
        activeTab: 'products'
    });
    writeStaticHtmlFile(partnerPath, partnerHtml);
    generatedCount++;

    // 產品線頁面
    for (const file of (brandObj.files || [])) {
        const lineSlug = file.key;
        const lineTitle = file.titleZh || file.titleEn || lineSlug;
        const linePath = `/products/${partnerSlug}/${lineSlug}/`;
        const products = allProductsCache[lineSlug] || [];

        const tableContentHtml = products.map((p, idx) => {
            const name = p.product_name || p.name || '';
            const comp = p.composition_zh || p.chemical_component || p.composition_en || p.chemistry || '—';
            const props = p.properties || p.performance || '—';
            const usage = p.main_usage || p.application_fields_zh || (p.featured_categories || []).join(', ') || '—';
            const safeUrl = `/products/${partnerSlug}/${lineSlug}/${encodeURIComponent(name)}/`;
            const isFdaLine = (partnerSlug === 'mpi' && (lineSlug === 'industrial' || lineSlug === 'ink'));
            const fdaBadge = (isFdaLine && p.fda_compliant)
                ? `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 align-middle shrink-0 ml-1.5 shadow-xs select-none" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-[9px] text-emerald-600"></i> FDA</span>`
                : '';

            return `
            <tr class="hover:bg-blue-50/50 border-b border-gray-200 text-sm transition-colors">
                <td class="py-3 px-3.5 font-bold text-slate-900 align-top w-[25%]">
                    <div class="flex items-center flex-wrap gap-y-0.5">
                        <a href="${safeUrl}" class="text-blue-950 font-extrabold text-sm hover:underline inline leading-snug">
                            ${escapeHtml(name)}
                        </a>
                        ${fdaBadge}
                    </div>
                    <div class="text-xs text-slate-500 font-normal mt-0.5">${escapeHtml(comp)}</div>
                </td>
                <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[40%]">${escapeHtml(props)}</td>
                <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[25%]">${escapeHtml(usage)}</td>
                <td class="py-3 px-3.5 text-center align-top w-[10%]">
                    <a href="${safeUrl}" class="px-2.5 py-1 bg-white hover:bg-blue-50 border border-blue-300 text-blue-950 rounded font-bold text-xs shadow-xs inline-flex items-center gap-1 transition-all">
                        <span>規格詳情</span>
                        <i class="fa-solid fa-chevron-right text-[10px]"></i>
                    </a>
                </td>
            </tr>`;
        }).join('');

        const itemListSchema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": `${brandName} ${lineTitle} 產品目錄`,
            "description": `${brandName} ${lineTitle} 特用化學品規格表，共 ${products.length} 項品項。`,
            "url": `${DOMAIN}${linePath}`,
            "numberOfItems": products.length,
            "itemListElement": products.map((p, idx) => ({
                "@type": "ListItem",
                "position": idx + 1,
                "name": p.product_name || p.name,
                "url": `${DOMAIN}${linePath}${encodeURIComponent((p.product_name || p.name || '').trim())}/`
            }))
        };

        const lineHtml = buildPageHtml({
            title: `${lineTitle} (${brandName}) | 宏威應用材料 ATTech Materials`,
            description: `宏威應用材料精選 ${brandName} ${lineTitle} 特用化學品，提供 ${products.map(p => p.product_name || p.name).slice(0, 8).join(', ')} 等品項之物性參數與免費索樣。`,
            canonicalPath: linePath,
            activeTab: 'products',
            preRenderedContent: tableContentHtml,
            schemaJson: itemListSchema
        });
        writeStaticHtmlFile(linePath, lineHtml);
        generatedCount++;

        // 3. 單一產品獨立頁面 (Product Detail Pages)
        for (const p of products) {
            const pName = (p.product_name || p.name || '').trim();
            if (!pName) continue;

            const productPath = `/products/${partnerSlug}/${lineSlug}/${encodeURIComponent(pName)}/`;
            const comp = p.composition_zh || p.chemical_component || p.composition_en || p.chemistry || '';
            const props = p.properties || p.performance || '';
            const usage = p.main_usage || p.application_fields_zh || (p.featured_categories || []).join(', ') || '';

            const productDetailHtml = renderProductDetailTableHtml(p, partnerSlug, lineSlug, brandName);

            const productSchema = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "BreadcrumbList",
                        "itemListElement": [
                            { "@type": "ListItem", "position": 1, "name": "首頁", "item": `${DOMAIN}/` },
                            { "@type": "ListItem", "position": 2, "name": "產品", "item": `${DOMAIN}/products/` },
                            { "@type": "ListItem", "position": 3, "name": brandName, "item": `${DOMAIN}/products/${partnerSlug}/` },
                            { "@type": "ListItem", "position": 4, "name": lineTitle, "item": `${DOMAIN}/products/${partnerSlug}/${lineSlug}/` },
                            { "@type": "ListItem", "position": 5, "name": pName, "item": `${DOMAIN}${productPath}` }
                        ]
                    },
                    {
                        "@type": "Product",
                        "name": pName,
                        "image": `${DOMAIN}/img/MCP-Logo.png`,
                        "description": `${brandName} ${pName} - 主要成分：${comp || '特用化學材料'}。用途：${usage || lineTitle}。特性：${props}`,
                        "category": lineTitle,
                        "brand": {
                            "@type": "Brand",
                            "name": brandName
                        },
                        "offers": {
                            "@type": "Offer",
                            "url": `${DOMAIN}${productPath}`,
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
            };

            const prodPageHtml = buildPageHtml({
                title: `${pName} (${brandName}) | 宏威應用材料 ATTech Materials`,
                description: `${brandName} ${pName} 特用化學品：${comp ? comp + '，' : ''}${props ? props + '。' : ''}適用於 ${usage || lineTitle}，提供 TDS 技術資料與樣品索取。`,
                canonicalPath: productPath,
                activeTab: 'products',
                preRenderedContent: `<tr><td colspan="4" class="p-0">${productDetailHtml}</td></tr>`,
                schemaJson: productSchema
            });

            // Windows 與 Linux 檔案路徑：以 decodeURIComponent 之安全名稱作為資料夾名
            writeStaticHtmlFile(`/products/${partnerSlug}/${lineSlug}/${pName}`, prodPageHtml);
            generatedCount++;
        }
    }
}

console.log(`✅ 靜態預渲染完成！共產出 ${generatedCount} 個實體 index.html 頁面。`);
