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

/**
 * 依各品牌規則解析產品適合的應用領域 (Suitable Applications)
 * 1. MPI: 看 json/mpi/mpiall.json 中的 application_title_zh
 * 2. dorfketal: 看 json/dorfketal 中的 featured_categories
 * 3. orion: 看 json/orion 中的 featured_categories
 * 4. others: 看 config.json 怎麼分類與各 JSON 的 featured_categories
 */
function getProductApplications(p, partnerKey, lineKey, configData) {
    const apps = [];
    const pLower = (partnerKey || '').toLowerCase();
    const pName = p.product_name || p.name || '';
    const safeName = encodeURIComponent(pName);

    if (pLower === 'mpi') {
        // MPI: 依據 json/mpi/mpiall.json 中的 application_title_zh
        if (p.applications_data && typeof p.applications_data === 'object') {
            for (const [appKey, appObj] of Object.entries(p.applications_data)) {
                if (appObj && appObj.application_title_zh) {
                    const title = String(appObj.application_title_zh).trim();
                    if (title && !apps.some(a => a.title === title)) {
                        apps.push({
                            title: title,
                            key: appKey,
                            url: `/products/mpi/${appKey}/`,
                            productUrl: `/products/mpi/${appKey}/?product=${safeName}#${safeName}`,
                            isCurrent: (appKey === lineKey)
                        });
                    }
                }
            }
        }
    } else if (pLower === 'dorfketal') {
        // dorfketal: 依據 json/dorfketal 中的 featured_categories
        const cats = Array.isArray(p.featured_categories) ? p.featured_categories : [];
        for (const cat of cats) {
            const title = String(cat).trim();
            if (title && !apps.some(a => a.title === title)) {
                apps.push({
                    title: title,
                    key: lineKey,
                    url: `/products/dorfketal/${lineKey}/?category=${encodeURIComponent(title)}`,
                    productUrl: `/products/dorfketal/${lineKey}/?product=${safeName}#${safeName}`,
                    isCurrent: true
                });
            }
        }
    } else if (pLower === 'orion') {
        // orion: 依據 json/orion 中的 featured_categories
        const cats = Array.isArray(p.featured_categories) ? p.featured_categories : [];
        for (const cat of cats) {
            const title = String(cat).trim();
            if (title && !apps.some(a => a.title === title)) {
                apps.push({
                    title: title,
                    key: lineKey,
                    url: `/products/orion/${lineKey}/?category=${encodeURIComponent(title)}`,
                    productUrl: `/products/orion/${lineKey}/?product=${safeName}#${safeName}`,
                    isCurrent: true
                });
            }
        }
    } else {
        // others: 依據 config.json 怎麼分類與各 JSON featured_categories
        const cats = Array.isArray(p.featured_categories) ? p.featured_categories : [];
        if (cats.length > 0) {
            for (const cat of cats) {
                const title = String(cat).trim();
                if (title && !apps.some(a => a.title === title)) {
                    apps.push({
                        title: title,
                        key: lineKey,
                        url: `/products/others/${lineKey}/?category=${encodeURIComponent(title)}`,
                        productUrl: `/products/others/${lineKey}/?product=${safeName}#${safeName}`,
                        isCurrent: true
                    });
                }
            }
        }
        // 若無明確 featured_categories，採用 config.json 該系列之 titleZh 分類名稱
        if (apps.length === 0) {
            const othersConfig = configData?.others;
            const fileConf = (othersConfig?.files || []).find(f => f.key === lineKey);
            const lineName = fileConf?.titleZh || fileConf?.titleEn || '特化材料助劑';
            apps.push({
                title: lineName,
                key: lineKey,
                url: `/products/others/${lineKey}/`,
                productUrl: `/products/others/${lineKey}/?product=${safeName}#${safeName}`,
                isCurrent: true
            });
        }
    }

    return apps;
}

/**
 * 提取各品牌產品的詳細描述與特點性能
 */
function getProductDescription(p, partnerKey, lineKey) {
    const pLower = (partnerKey || '').toLowerCase();
    let desc = p.properties || p.performance || '';

    if (!desc && pLower === 'mpi') {
        // MPI: 若 properties 為空，由 applications_data 中提取性能描述
        const lines = [];
        if (p.applications_data && typeof p.applications_data === 'object') {
            const currentAppData = p.applications_data[lineKey] || Object.values(p.applications_data)[0];
            if (currentAppData && currentAppData.performance_descriptions_zh) {
                for (const [, val] of Object.entries(currentAppData.performance_descriptions_zh)) {
                    if (val && typeof val === 'string' && !lines.includes(val.trim())) {
                        lines.push(val.trim());
                    }
                }
            }
        }
        if (lines.length > 0) {
            desc = lines.join('\n');
        } else if (p.application_fields_zh) {
            desc = `主要應用領域：${p.application_fields_zh}`;
        }
    } else if (!desc && pLower === 'orion') {
        // Orion 碳黑：依製程方式、黑度、粒徑與應用組合出完整規格描述
        const methodMap = {
            'HCF': '高色素爐黑 (High Color Furnace Black)',
            'MCF': '中色素爐黑 (Medium Color Furnace Black)',
            'RCF': '標準色素爐黑 (Regular Color Furnace Black)',
            'Gas Black': '特級氣黑 (Gas Black)',
            'Lamp Black': '燈黑 (Lamp Black)',
            'Furnace Black': '爐法碳黑 (Furnace Black)'
        };
        const method = methodMap[p.production_method] || p.production_method || '特級碳黑製程';
        const cats = Array.isArray(p.featured_categories) ? p.featured_categories.join('、') : '';
        const typical = p.typical_properties || {};
        const pName = p.product_name || p.name || '';
        desc = `${pName} 為 Orion Engineered Carbons 頂級碳黑材料，採用 ${method}。具備優良著色力與分散穩定性，黑度值 (My) 達 ${typical.blackness_my || '—'}，原生平均粒徑約 ${typical.average_primary_particle_size_nm || '—'} nm。廣泛應用於 ${cats || '工業塗料與油墨'} 等高性能著色體系。`;
    } else if (!desc && pLower === 'others') {
        if (lineKey === 'silane') {
            desc = `高性能矽烷偶合劑（${p.composition_zh || '有機矽烷'}），能顯著改善無機填料與有機基體間之相容性，提升界面附著力、耐水性與力學機械強度。`;
        }
    }

    return desc || '提供卓越的加工相容性、表面改質效果與穩定物性，完整配方諮詢與規格建議請洽宏威應用材料技術團隊。';
}

/**
 * 提取代表性物性表格數據 (Typical Properties)
 */
function getTypicalPropertiesRows(p) {
    const t = p.typical_properties || {};
    const rows = [];

    const addRow = (label, val) => {
        if (val !== undefined && val !== null && String(val).trim() !== '' && String(val).trim() !== '—' && String(val).trim() !== 'N/A') {
            rows.push({ label, val: String(val).trim() });
        }
    };

    // 微粉蠟、樹脂與化學品通用物性
    addRow('熔點 / 軟化點 (°C)', t.melt_point_c || p.softening_point);
    addRow('平均粒徑 (µm)', t.mean_particle_size_um || p.particle_size);
    addRow('最大粒徑 (µm)', t.max_particle_size_um);
    addRow('密度 / 比重 (g/cm³)', t.density_g_cc_25c || p.density || p.specific_gravity);
    addRow('酸價 (mg KOH/g)', t.acid_value || p.acid_value);
    addRow('閃點 (°C)', t.flash_point || p.flash_point);
    addRow('分子量 (Mw)', t.molecular_weight);
    addRow('外觀 / 狀態', p.appearance);
    addRow('固成份 / 活性物含量 (%)', t.solid_content || t.active_content || p.active_content);
    addRow('黏度 (mPa·s / cSt)', t.viscosity || p.viscosity);

    // 碳黑專用物性指標
    addRow('黑度值 (My)', t.blackness_my);
    addRow('著色力 (% vs. IRB 3)', t.tinting_strength);
    addRow('吸油量 (OAN, ml/100g)', t.oil_absorption_number);
    addRow('pH 值', t.ph_value);
    addRow('灰分含量 (%)', t.ash_content);
    addRow('BET 比表面積 (m²/g)', t.bet_surface_area);
    addRow('原生粒徑 (nm)', t.average_primary_particle_size_nm);
    addRow('揮發份 950°C (%)', t.volatile_matter_950c);

    return rows;
}

// 產生單一產品規格詳細卡片 HTML (無漸層底色、純白/極簡現代風格、無全域搜尋、引導至官網比較)
function renderProductDetailTableHtml(product, partnerKey, lineKey, brandName, lineTitle = '', configData) {
    const p = product;
    const name = (p.product_name || p.name || '').trim();
    const safeName = encodeURIComponent(name);
    const comp = p.composition_zh || p.chemical_component || p.composition_en || p.chemistry || '特用化學品材料';
    const props = getProductDescription(p, partnerKey, lineKey);
    const applications = getProductApplications(p, partnerKey, lineKey, configData);

    const isFdaLine = (partnerKey.toLowerCase() === 'mpi' && (lineKey === 'industrial' || lineKey === 'ink'));
    const fdaBadge = (isFdaLine && p.fda_compliant)
        ? `<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-300" title="符合 FDA 食品接觸規範 (21 CFR 175.300 / 176.170)"><i class="fa-solid fa-shield-halved text-emerald-600"></i> FDA 食品接觸合規</span>`
        : '';

    // 適合應用標籤 HTML
    const usageTagsHtml = applications.map(app => `
        <a href="${app.url}" 
           title="至官網檢視 ${escapeHtml(app.title)} 應用領域之所有規格與比較表"
           class="inline-flex items-center gap-1.5 px-3.5 py-1.5 ${app.isCurrent ? 'bg-blue-900 text-white font-bold' : 'bg-white hover:bg-blue-50 text-slate-800 hover:text-blue-950 font-semibold border border-slate-300'} rounded-lg text-xs transition-colors shadow-xs">
            <i class="fa-solid fa-tag text-[10px] ${app.isCurrent ? 'text-blue-200' : 'text-blue-600'}"></i>
            <span>${escapeHtml(app.title)}</span>
            ${app.isCurrent ? '<span class="text-[10px] opacity-75 font-normal">(當前系列)</span>' : ''}
        </a>
    `).join('');

    // 物性參數表行
    const propRows = getTypicalPropertiesRows(p);
    const extraRowsHtml = propRows.map(r => `
        <tr class="border-b border-slate-100">
            <td class="py-2.5 px-4 font-bold text-slate-700 bg-slate-50/80 w-2/5">${escapeHtml(r.label)}</td>
            <td class="py-2.5 px-4 text-slate-900 font-semibold">${escapeHtml(r.val)}</td>
        </tr>
    `).join('');

    return `
    <div class="product-seo-detail bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 mb-8 text-slate-900">
        <!-- 頂部產品基本資訊與快速操作 (純白卡片無漸層) -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5 pb-6 border-b border-slate-200">
            <div>
                <div class="flex flex-wrap items-center gap-2 mb-2.5">
                    <span class="inline-block px-3 py-1 rounded-md text-xs font-bold bg-slate-100 text-slate-800 border border-slate-200">${escapeHtml(brandName)}</span>
                    ${lineTitle ? `<span class="inline-block px-3 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">${escapeHtml(lineTitle)}</span>` : ''}
                    ${fdaBadge}
                </div>
                <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">${escapeHtml(name)}</h1>
                <p class="text-sm text-slate-600 mt-2 font-medium">
                    主要化學成分：<span class="text-slate-900 font-semibold">${escapeHtml(comp)}</span>
                </p>
            </div>
            <div class="flex flex-wrap items-center gap-2.5 shrink-0">
                <a href="/contact?product=${safeName}" 
                   class="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-sm font-bold shadow-xs transition-colors active:scale-95">
                    <i class="fa-solid fa-envelope"></i>
                    <span>索取樣品與技術諮詢</span>
                </a>
                <a href="/products/${partnerKey}/${lineKey}/" 
                   class="inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300 rounded-xl text-sm font-bold transition-colors">
                    <i class="fa-solid fa-scale-balanced text-slate-700"></i>
                    <span>比較同系列其他產品</span>
                </a>
                <a href="/products/${partnerKey}/${lineKey}/?product=${safeName}#${safeName}" 
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
                        ${usageTagsHtml || `<span class="text-sm text-slate-700">${escapeHtml(lineTitle || '特用化學品工業應用')}</span>`}
                    </div>

                    ${(p.application_fields_zh || p.recommended_system_type_zh || p.suggested_use_level_zh) ? `
                    <div class="mt-4 pt-3 border-t border-slate-200 text-xs text-slate-700 space-y-2 leading-relaxed">
                        ${p.application_fields_zh ? `<div><span class="font-bold text-slate-900">詳細應用範疇：</span>${escapeHtml(p.application_fields_zh)}</div>` : ''}
                        ${p.recommended_system_type_zh ? `<div><span class="font-bold text-slate-900">建議適用系統：</span>${escapeHtml(p.recommended_system_type_zh)}</div>` : ''}
                        ${p.suggested_use_level_zh ? `<div><span class="font-bold text-slate-900">建議添加量：</span>${escapeHtml(p.suggested_use_level_zh)}</div>` : ''}
                    </div>` : ''}

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
                    <p class="text-sm text-slate-800 leading-relaxed whitespace-pre-line">${escapeHtml(props)}</p>
                </div>

                <!-- 代表性物性摘要表格 (若有) -->
                ${extraRowsHtml ? `
                <div class="border border-slate-200 rounded-xl overflow-hidden shadow-xs">
                    <div class="bg-slate-100 px-4 py-2.5 border-b border-slate-200 font-bold text-xs text-slate-700 uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-chart-simple text-blue-900"></i> 代表性物性摘要 (Typical Properties)
                    </div>
                    <table class="w-full text-left text-sm">
                        <tbody>
                            ${extraRowsHtml}
                        </tbody>
                    </table>
                </div>` : ''}
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
                        宏威應用材料官網提供完整的特用化學品物性規格，您可同時比較 ${escapeHtml(brandName)} ${escapeHtml(lineTitle)} 各產品的物性規格與適用系統。
                    </p>
                    <a href="/products/${partnerKey}/${lineKey}/" 
                       class="inline-flex items-center justify-center gap-1.5 w-full px-4 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold transition-colors">
                        <span>進入 ${escapeHtml(lineTitle || '此系列')} 完整規格比較表</span>
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
                        宏威應用材料為 ${escapeHtml(brandName)} 在台灣之專業特用化學代理商，備有原廠技術規格書 (TDS)、樣品庫存與應用技術諮詢服務。
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
                        原廠技術資料表（TDS）與全品項多規格比較矩陣已完整收錄於官網系統。點擊下方按鈕可前往官網產品專區，系統將自動定位並展開 ${escapeHtml(name)} 之完整技術檔案。
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-2.5 shrink-0 w-full lg:w-auto">
                    <a href="/products/${partnerKey}/${lineKey}/" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-bold border border-slate-700 transition-colors">
                        <i class="fa-solid fa-scale-balanced"></i>
                        <span>比較同系列其他產品</span>
                    </a>
                    <a href="/products/${partnerKey}/${lineKey}/?product=${safeName}#${safeName}" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold shadow-sm transition-colors active:scale-95">
                        <i class="fa-solid fa-file-lines"></i>
                        <span>直達官網看 TDS 與完整規格</span>
                    </a>
                    <a href="/contact?product=${safeName}" 
                       class="flex-1 lg:flex-initial inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-100 text-slate-900 rounded-xl text-sm font-bold transition-colors">
                        <i class="fa-solid fa-envelope"></i>
                        <span>索取免費樣品</span>
                    </a>
                </div>
            </div>
        </div>
    </div>`;
}

// 產生完整 HTML 頁面
function buildPageHtml({
    title,
    description,
    canonicalPath,
    activeTab = 'about',
    preRenderedContent = '',
    schemaJson = null,
    isProductDetailPage = false,
    productMeta = null
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

    // 6. 實體產品專屬頁面 (Product Detail Pages)：
    // - 移除桌面與行動版全域搜尋框 (使用者需求：不需要全域搜尋)
    // - 移除 1.請選擇品牌、資料建置中提示與樹狀側邊欄
    // - 頂部替換為麵包屑與返回系列產品比較表按鈕
    // - 注入完整的產品詳情卡片
    if (isProductDetailPage) {
        html = html.replace('<body class="', '<body class="is-product-detail bg-slate-50 ');

        // 移除桌面版與行動版全域搜尋容器
        html = html.replace(/<div class="flex-1 max-w-sm mx-2 hidden sm:block">[\s\S]*?<\/form>\s*<\/div>/, '<!-- 全域搜尋已在獨立產品頁移除 -->');
        html = html.replace(/<div class="block sm:hidden pb-2\.5">[\s\S]*?<\/form>\s*<\/div>/, '<!-- 行動版全域搜尋已在獨立產品頁移除 -->');

        // 移除 1. 請選擇品牌 與 資料建置提示
        html = html.replace(/<section[^>]*id="section-partner"[\s\S]*?<\/section>/, '');
        html = html.replace(/<section[^>]*id="section-coming-soon"[\s\S]*?<\/section>/, '');

        let breadcrumbBarHtml = '';
        if (productMeta) {
            breadcrumbBarHtml = `
            <div class="flex flex-wrap items-center justify-between gap-3 mb-5 pb-3 border-b border-slate-200">
                <a href="${productMeta.backUrl}" class="inline-flex items-center gap-2 text-sm font-bold text-slate-800 hover:text-blue-900 transition-colors">
                    <i class="fa-solid fa-arrow-left"></i> 返回 ${escapeHtml(productMeta.brandName)} ${escapeHtml(productMeta.lineTitle)} 產品列表與規格比較
                </a>
                <nav class="flex items-center gap-1.5 text-xs text-slate-500 font-medium" aria-label="麵包屑導航">
                    <a href="/" class="hover:underline">首頁</a>
                    <span>/</span>
                    <a href="/products/" class="hover:underline">產品</a>
                    <span>/</span>
                    <a href="/products/${productMeta.partnerSlug}/" class="hover:underline">${escapeHtml(productMeta.brandName)}</a>
                    <span>/</span>
                    <a href="${productMeta.backUrl}" class="hover:underline">${escapeHtml(productMeta.lineTitle)}</a>
                    <span>/</span>
                    <span class="text-slate-900 font-bold">${escapeHtml(productMeta.name)}</span>
                </nav>
            </div>`;
        }

        // 將整個目錄與表格工作區 (section-directory-finder) 乾淨替換為獨立產品詳細區塊
        html = html.replace(
            /<div id="section-directory-finder"[\s\S]*?<\/main>\s*<\/div>/,
            `<div id="section-product-detail" class="w-full">${breadcrumbBarHtml}${preRenderedContent}</div>`
        );
    } else if (preRenderedContent) {
        // 列表頁預渲染注入
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
            const props = getProductDescription(p, partnerSlug, lineSlug);
            const appList = getProductApplications(p, partnerSlug, lineSlug, config);
            const usageText = appList.map(a => a.title).join('、') || p.main_usage || p.application_fields_zh || '—';
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
                <td class="py-3 px-3.5 text-slate-800 font-normal align-top leading-relaxed whitespace-pre-line w-[25%]">${escapeHtml(usageText)}</td>
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
            const props = getProductDescription(p, partnerSlug, lineSlug);
            const appList = getProductApplications(p, partnerSlug, lineSlug, config);
            const usageText = appList.map(a => a.title).join('、') || lineTitle;

            const productDetailHtml = renderProductDetailTableHtml(p, partnerSlug, lineSlug, brandName, lineTitle, config);

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
                        "description": `${brandName} ${pName} - 主要成分：${comp || '特用化學材料'}。適合應用：${usageText}。特性：${props.replace(/\n/g, ' ')}`,
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
                title: `${pName} (${brandName}) ${lineTitle} | 宏威應用材料 ATTech Materials`,
                description: `${brandName} ${pName} 特用化學品：${comp ? comp + '，' : ''}${props ? props.replace(/\n/g, ' ').slice(0, 100) + '... ' : ''}適合應用：${usageText}。提供官網線上規格比較、TDS技術資料與樣品索取。`,
                canonicalPath: productPath,
                activeTab: 'products',
                preRenderedContent: productDetailHtml,
                schemaJson: productSchema,
                isProductDetailPage: true,
                productMeta: {
                    name: pName,
                    brandName,
                    lineTitle,
                    partnerSlug,
                    lineSlug,
                    backUrl: `/products/${partnerSlug}/${lineSlug}/`
                }
            });

            // Windows 與 Linux 檔案路徑：以安全名稱作為資料夾名
            writeStaticHtmlFile(`/products/${partnerSlug}/${lineSlug}/${pName}`, prodPageHtml);
            generatedCount++;
        }
    }
}

console.log(`✅ 靜態預渲染完成！共產出 ${generatedCount} 個實體 index.html 頁面。`);
