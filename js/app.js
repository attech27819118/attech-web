/**
 * ====================================================================
 * ATTech Web - Main Application Logic & Initialization (app.js)
 * ====================================================================
 */

let searchDebounceTimer = null;

function debouncedSearch(val) {
    document.querySelectorAll('.global-search-input').forEach(input => {
        if (input.value !== val) input.value = val;
    });

    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(async () => {
        const query = val.trim();
        AppState.searchQuery = query;

        if (query !== '') {
            switchTab('products', false);
            await loadAllBrandsData();
            renderGroupedSearchResults(query);
            updateHashRoute(false);
        } else {
            renderProducts();
            updateHashRoute(false);
        }
    }, 200);
}

function removeSearchToken(tokenToRemove) {
    const tokens = SearchEngine.parseTokens(AppState.searchQuery);
    const newTokens = tokens.filter(t => t.toLowerCase() !== tokenToRemove.toLowerCase());
    const newQuery = newTokens.join(' ');
    AppState.searchQuery = newQuery;
    document.querySelectorAll('.global-search-input').forEach(input => input.value = newQuery);

    if (newQuery !== '') {
        renderGroupedSearchResults(newQuery);
        updateHashRoute(false);
    } else {
        renderProducts();
        updateHashRoute(false);
    }
}

function renderGroupedSearchResults(query) {
    updateRatingLegend();
    const tokens = SearchEngine.parseTokens(query);
    const tbody = document.getElementById('directory-matrix-body');
    const thead = document.querySelector('table thead');
    const t = uiText[AppState.lang];

    const pathElem = document.getElementById('dir-current-path');
    if (tokens.length > 0) {
        const chipsHtml = tokens.map(tok => `
            <span class="inline-flex items-center gap-1 bg-blue-100 text-blue-950 border border-blue-200 px-2.5 py-0.5 rounded-full text-xs font-semibold shadow-2xs transition-all">
                <i class="fa-solid fa-tag text-[10px] text-blue-600"></i>
                <span>${tok.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>
                <button type="button" onclick="removeSearchToken('${tok.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}')" class="ml-0.5 text-blue-500 hover:text-red-600 rounded-full w-3.5 h-3.5 flex items-center justify-center transition-colors" title="移除關鍵字 ${tok}" aria-label="移除關鍵字 ${tok}">
                    <i class="fa-solid fa-xmark text-[10px]"></i>
                </button>
            </span>
        `).join('');

        pathElem.innerHTML = `
            <div class="flex flex-wrap items-center gap-1.5 py-0.5">
                <span class="text-blue-950 f-weight-bold shrink-0">${t.global_search_results || '全域搜尋結果：'}</span>
                <div class="flex flex-wrap items-center gap-1.5">${chipsHtml}</div>
                ${tokens.length > 1 ? `
                    <button type="button" onclick="resetFilters()" class="text-xs text-slate-500 hover:text-red-600 underline font-medium ml-1 transition-colors">
                        清除全部
                    </button>
                ` : ''}
            </div>
        `;
    } else {
        pathElem.innerHTML = `<span class="text-blue-950 f-weight-bold">${t.global_search_results || '全域搜尋結果：'}</span> "${query}"`;
    }

    let totalMatchCount = 0;
    let groupedHTML = '';

    if (thead) {
        thead.innerHTML = `
    <tr class="bg-slate-100 border-b border-slate-300 text-slate-900 f-weight-bold select-none f-size-sm">
        <th class="py-3 px-3.5 w-[25%]">產品名稱 / 成分</th>
        <th class="py-3 px-3.5 w-[33%]">主要特性 / 說明</th>
        <th class="py-3 px-3.5 w-[27%]">主要用途 / 應用領域</th>
        <th class="py-3 px-3.5 w-[15%] text-center">所屬品牌與操作</th>
    </tr>`;
    }

    for (const [configKey, brand] of Object.entries(AppState.configs)) {
        const reversePartnerMap = Object.fromEntries(
            Object.entries(partnerConfigMap).map(([k, v]) => [v, k])
        );
        const partnerName = reversePartnerMap[configKey] || configKey;

        for (const file of (brand.files || [])) {
            const products = AppState.allProductsCache[file.key] || [];

            const matchedProducts = products.filter(p => {
                return SearchEngine.matchProduct(p, tokens, file.key, brand.brandName);
            });

            if (matchedProducts.length > 0) {
                totalMatchCount += matchedProducts.length;
                const sectionTitle = AppState.lang === 'zh' ? file.titleZh : file.titleEn;

                groupedHTML += `
            <tr class="bg-slate-200 border-y-2 border-blue-600 text-slate-900 f-size-sm">
                <td colspan="4" class="py-2.5 px-4 tracking-wide">
                    <div class="flex items-center justify-between">
                        <span class="flex items-center gap-2 f-size-sm f-weight-bold text-slate-900">
                            <i class="fa-solid fa-folder-open text-blue-700"></i>
                            【${brand.brandName}】 ${sectionTitle}
                            <span class="f-size-xs f-weight-normal text-slate-700">(${matchedProducts.length} 項結果)</span>
                        </span>
                        <button onclick="navigateToCategory('${partnerName}', '${file.key}', 'all')"
                                title="前往【${brand.brandName}】${sectionTitle}分類專區"
                                aria-label="前往【${brand.brandName}】${sectionTitle}分類專區"
                                class="px-3 py-1 bg-blue-700 hover:bg-blue-800 text-white rounded f-size-xs f-weight-bold flex items-center gap-1.5 transition-all active:scale-95 shadow-sm">
                            <span>前往該分類專區</span>
                            <i class="fa-solid fa-arrow-right f-size-xs" aria-hidden="true"></i>
                        </button>
                    </div>
                </td>
            </tr>`;

                matchedProducts.forEach((p) => {
                    const appData = getAppSpecificData(p, file.key);
                    const rawName = p.product_name || '—';
                    const rawComp = p.composition_zh || p.chemical_component || p.composition_en || '—';
                    const rawProps = p.properties || p.performance || '—';
                    const rawUsage = p.main_usage || p.application_fields_zh || (appData.featured_categories || []).join(', ') || (p.featured_categories || []).join(', ') || '—';

                    const highlightedName = SearchEngine.highlight(rawName, tokens);
                    const highlightedComp = SearchEngine.highlight(rawComp, tokens);
                    const highlightedProps = SearchEngine.highlight(rawProps, tokens);
                    const highlightedUsage = SearchEngine.highlight(rawUsage, tokens);
                    const safeTitleName = rawName.replace(/"/g, '&quot;');

                    groupedHTML += `
                <tr class="hover:bg-blue-50/50 border-b border-gray-200 f-size-sm transition-colors">
                    <td class="py-3 px-3.5 f-weight-bold text-slate-900 align-top">
                        <div class="flex flex-col items-start gap-1 w-full">
                            <div class="min-w-0 w-full">
                                <div class="text-blue-950 f-weight-extrabold f-size-sm break-words leading-snug">${highlightedName}</div>
                                <div class="f-size-xs text-slate-600 f-weight-normal mt-0.5 break-words">${highlightedComp}</div>
                            </div>
                            ${renderCompareIcon(p, partnerName, file.key)}
                        </div>
                    </td>
                    <td class="py-3 px-3.5 text-slate-800 f-weight-normal align-top leading-relaxed whitespace-pre-line">${highlightedProps}</td>
                    <td class="py-3 px-3.5 text-slate-800 f-weight-normal align-top leading-relaxed whitespace-pre-line">${highlightedUsage}</td>
                    <td class="py-3 px-3.5 text-slate-600 align-top text-center">
                        <div class="flex flex-col items-center gap-1.5">
                            <span class="f-size-xs text-slate-600 f-weight-bold">${partnerName}</span>
                            <button onclick="navigateToCategory('${partnerName}', '${file.key}', 'all', decodeURIComponent('${encodeURIComponent(rawName).replace(/'/g, '%27')}'))"
                                    title="查看 ${safeTitleName} 詳細資訊"
                                    aria-label="查看 ${safeTitleName} 詳細資訊"
                                    class="px-2.5 py-1 bg-white hover:bg-blue-50 border border-blue-300 text-blue-950 rounded f-weight-bold f-size-xs shadow-sm flex items-center gap-1 transition-all active:scale-95">
                                <i class="fa-solid fa-circle-info f-size-xs text-blue-700" aria-hidden="true"></i>
                                <span>詳細資訊</span>
                            </button>
                        </div>
                    </td>
                </tr>`;
                });
            }
        }
    }

    document.getElementById('dir-match-count').innerText = totalMatchCount;

    if (totalMatchCount === 0) {
        const hasMultipleTokens = tokens.length > 1;
        tbody.innerHTML = `
    <tr>
        <td colspan="4" class="text-center py-12 text-slate-500">
            <i class="fa-solid fa-filter-circle-xmark f-size-4xl mb-3 text-slate-400"></i>
            <p class="f-weight-bold f-size-base text-slate-800 mb-1">
                ${hasMultipleTokens ? `找不到同時符合「${tokens.join(' + ')}」的產品` : t.no_match_title}
            </p>
            <p class="f-size-sm text-slate-600 f-weight-normal mb-4">
                ${hasMultipleTokens ? '建議您嘗試減少關鍵字數量、改用更通用的詞彙，或點擊上方標籤移除特定關鍵字以擴大搜尋範圍。' : t.no_match_sub}
            </p>
            <div class="flex items-center justify-center gap-2">
                <button onclick="resetFilters()" class="px-4 py-2 bg-blue-950 text-white rounded-lg f-size-sm f-weight-bold hover:bg-blue-900 shadow transition-all">
                    ${t.btn_clear_filters}
                </button>
            </div>
        </td>
    </tr>`;
        return;
    }

    tbody.innerHTML = groupedHTML;
}

function resetSearchInputFields() {
    if (typeof searchDebounceTimer !== 'undefined' && searchDebounceTimer) {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = null;
    }
    AppState.searchQuery = '';
    document.querySelectorAll('.global-search-input').forEach(input => input.value = '');
}

function resetFilters() {
    AppState.filters = {};
    resetSearchInputFields();
    initFilters();
    renderProducts();
    updateHashRoute(false);
}

function switchPartner(partnerKey) {
    resetSearchInputFields();
    AppState.partner = partnerKey;
    const configKey = partnerConfigMap[partnerKey] || 'mpi';
    const brandConfig = AppState.configs[configKey];
    if (brandConfig && brandConfig.files && brandConfig.files[0]) {
        AppState.productLine = brandConfig.files[0].key;
    }
    AppState.category = 'all';
    AppState.filters = {};
    switchTab('products', false, false);
    updatePartnerUI();
    updateHashRoute(true);
}

function selectPartnerAndSwitch(partnerKey) {
    switchPartner(partnerKey);
}

function updatePartnerUI(onRenderComplete = null, preserveExpanded = false) {
    if (!preserveExpanded) {
        AppState.expandedDetails = [];
    }
    const partner = AppState.partner;

    ['MPI', 'DorfKetal', 'Orion', 'Others'].forEach(p => {
        const btn = document.getElementById(`btn-partner-${p}`);
        if (!btn) return;
        btn.classList.remove('ring-4', 'ring-blue-400', 'scale-[1.02]', 'shadow-lg', 'opacity-50');
        if (p === partner) btn.classList.add('ring-4', 'ring-blue-400', 'scale-[1.02]', 'shadow-lg');
        else btn.classList.add('opacity-50');
    });

    const finderSection = document.getElementById('section-directory-finder');
    const comingSoon = document.getElementById('section-coming-soon');
    const configKey = partnerConfigMap[partner] || 'mpi';
    const brandConfig = AppState.configs[configKey];

    updateRatingLegend();
    updateCompareUI();

    if (brandConfig && brandConfig.files && brandConfig.files.length > 0) {
        comingSoon.classList.add('hidden');
        finderSection.classList.remove('hidden');

        ProductRepository.loadBrandData(partner).then(() => {
            const isLineInBrand = brandConfig.files.some(f => f.key === AppState.productLine);
            if (!AppState.productLine || !isLineInBrand) {
                AppState.productLine = brandConfig.files[0].key;
            }

            renderDirectoryTree();
            initFilters();

            if (AppState.searchQuery) {
                renderGroupedSearchResults(AppState.searchQuery);
            } else {
                selectDirectoryNode(AppState.productLine, AppState.category || 'all', preserveExpanded);
            }

            if (typeof onRenderComplete === 'function') {
                onRenderComplete();
            }
        });
    } else {
        finderSection.classList.add('hidden');
        comingSoon.classList.remove('hidden');
    }
}

function renderDirectoryTree() {
    const treeMenu = document.getElementById('directory-tree-menu');
    const configKey = partnerConfigMap[AppState.partner] || 'mpi';
    const brandConfig = AppState.configs[configKey];
    if (!treeMenu || !brandConfig) return;

    const iconMap = {
        'ptfe': 'fa-leaf',
        'powder': 'fa-cubes',
        'industrial': 'fa-industry',
        'ink': 'fa-palette',
        'ink_impact': 'fa-stamp',
        'industrial_floor': 'fa-border-all',
        'leather': 'fa-shoe-prints',
        'wood': 'fa-tree',
        'automotive_polishes': 'fa-car',
        'tyzor': 'fa-vial',
        'px': 'fa-oil-can',
        'chain': 'fa-circle-nodes',
        'silane': 'fa-atom',
        'coating': 'fa-spray-can',
        'carbon_black': 'fa-gem',
        'coating_additive': 'fa-flask-vial',
        'matting_agent': 'fa-cloud',
        'cpo_adhesion_promoter': 'fa-link',
        'adhesion_promoter': 'fa-magnet',
        'maleic_acid_resin': 'fa-dna'
    };

    treeMenu.innerHTML = brandConfig.files.map(file => {
        const lineKey = file.key;
        const lineTitle = AppState.lang === 'zh' ? file.titleZh : file.titleEn;
        const cachedProducts = AppState.allProductsCache[lineKey] || [];

        const categorySet = new Set();
        cachedProducts.forEach(p => {
            const appData = getAppSpecificData(p, lineKey);
            const cats = appData.featured_categories || p.featured_categories;
            if (cats && Array.isArray(cats)) {
                cats.forEach(c => c && categorySet.add(c));
            }
        });

        const definedOrder = file.categoryMap ? Object.keys(file.categoryMap) : [];

        const sortedCategories = Array.from(categorySet).sort((a, b) => {
            const indexA = definedOrder.indexOf(a);
            const indexB = definedOrder.indexOf(b);

            if (indexA !== -1 && indexB !== -1) return indexA - indexB;
            if (indexA !== -1) return -1;
            if (indexB !== -1) return 1;
            return a.localeCompare(b, 'zh-TW');
        });

        const subCategoriesHTML = sortedCategories.map(subCat => {
            const count = cachedProducts.filter(p => ProductFilterEngine.matchCategory(p, subCat, configKey, lineKey)).length;
            return `
<button onclick="selectDirectoryNode('${lineKey}', '${subCat}')"
        data-line="${lineKey}" data-cat="${subCat}"
        title="${lineTitle} - ${subCat}"
        aria-label="${lineTitle} - ${subCat}"
        class="dir-node-btn w-full text-left pl-7 pr-2 py-1.5 rounded f-size-sm text-slate-700 f-weight-bold hover:bg-blue-50 hover:text-blue-900 flex justify-between items-center group">
    <span class="transform group-hover:translate-x-0.5">• ${subCat}</span>
    <span class="f-size-xs bg-slate-200 text-slate-800 px-1.5 py-0.5 rounded-full f-weight-bold">${count}</span>
</button>`;
        }).join('');

        const isExpanded = AppState.expandedMenus.includes(lineKey);

        return `
    <div class="mb-1 border-b border-gray-100 last:border-0 pb-1">
        <button onclick="handleMainDirectoryClick('${lineKey}')"
                id="node-${lineKey}-all"
                aria-expanded="${isExpanded ? 'true' : 'false'}"
                aria-controls="submenu-${lineKey}"
                title="${lineTitle}"
                aria-label="${lineTitle}"
                class="dir-node-btn w-full text-left px-2.5 py-2 rounded f-size-sm f-weight-bold text-slate-900 hover:bg-slate-100 flex items-center justify-between group">
            <div class="flex items-center gap-2 pointer-events-none">
                <i class="fa-solid ${iconMap[lineKey] || 'fa-folder'} text-slate-500 f-size-xs" aria-hidden="true"></i>
                <span>${lineTitle}</span>
            </div>
            <div class="text-slate-500 group-hover:text-blue-900 ${isExpanded ? 'rotate-180' : ''} pointer-events-none" id="chevron-${lineKey}">
                <i class="fa-solid fa-chevron-down f-size-xs" aria-hidden="true"></i>
            </div>
        </button>
        <div id="submenu-${lineKey}" class="mt-0.5 space-y-0.5 border-l-2 border-slate-200 ml-3.5 ${isExpanded ? '' : 'hidden'}">
            ${subCategoriesHTML}
        </div>
    </div>`;
    }).join('');

    if (AppState.productLine) {
        updateNodeActiveStyles(AppState.productLine, AppState.category);
    }
}

function updateBreadcrumbPath() {
    const pathElem = document.getElementById('dir-current-path');
    if (!pathElem) return;

    if (!AppState.productLine) {
        pathElem.innerText = uiText[AppState.lang].unselected_path;
        return;
    }

    const configKey = partnerConfigMap[AppState.partner] || 'mpi';
    const brandConfig = AppState.configs[configKey];

    const currentFile = brandConfig?.files?.find(f => f.key === AppState.productLine);
    const lineTitle = currentFile
        ? (AppState.lang === 'zh' ? currentFile.titleZh : currentFile.titleEn)
        : AppState.productLine;

    if (AppState.category && AppState.category !== 'all') {
        pathElem.innerHTML = `${lineTitle} <i class="fa-solid fa-chevron-right f-size-xs mx-1 text-slate-500"></i> <span class="f-weight-bold text-blue-950">${AppState.category}</span>`;
    } else {
        pathElem.innerHTML = `${lineTitle} <i class="fa-solid fa-chevron-right f-size-xs mx-1 text-slate-500"></i> <span class="f-weight-bold text-blue-950">${uiText[AppState.lang].cat_all}</span>`;
    }
}

function renderProducts() {
    updateRatingLegend();
    const currentPartnerKey = partnerConfigMap[AppState.partner] || 'mpi';
    const tbody = document.getElementById('directory-matrix-body');
    const thead = document.querySelector('table thead');
    const t = uiText[AppState.lang];

    if (!AppState.productLine) {
        document.getElementById('dir-match-count').innerText = 0;
        document.getElementById('dir-current-path').innerText = t.unselected_path;
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-12 text-slate-500 f-weight-bold f-size-sm"><i class="fa-solid fa-arrow-left mr-1"></i> ${t.select_catalog_tips}</td></tr>`;
        return;
    }

    updateBreadcrumbPath();

    let allProducts = AppState.allProductsCache[AppState.productLine] || [];
    let filtered = ProductFilterEngine.filter(allProducts, {
        partner: AppState.partner,
        category: AppState.category,
        searchQuery: AppState.searchQuery,
        filters: AppState.filters
    });

    if (AppState.sortColumn) {
        filtered.sort((a, b) => {
            const valA = a[AppState.sortColumn] !== undefined ? a[AppState.sortColumn] : a.typical_properties?.[AppState.sortColumn];
            const valB = b[AppState.sortColumn] !== undefined ? b[AppState.sortColumn] : b.typical_properties?.[AppState.sortColumn];
            return compareSortValues(valA, valB, AppState.sortOrder);
        });
    }

    document.getElementById('dir-match-count').innerText = filtered.length;

    const activeFields = DynamicTableRenderer.getActiveFields(currentPartnerKey, filtered);
    if (thead) thead.innerHTML = DynamicTableRenderer.getHeaderHTML(activeFields);

    const colCount = activeFields.columns ? activeFields.columns.length : activeFields.length;

    if (filtered.length === 0) {
        tbody.innerHTML = `
    <tr>
        <td colspan="${colCount}" class="text-center py-10 text-slate-500">
            <i class="fa-solid fa-filter-circle-xmark f-size-3xl mb-2 text-slate-400"></i>
            <p class="f-weight-bold f-size-base text-slate-800 mb-0.5">${t.no_match_title}</p>
            <p class="f-size-sm text-slate-600 f-weight-normal mb-3">${t.no_match_sub}</p>
            <button onclick="resetFilters()" class="px-3.5 py-1.5 bg-blue-100 text-blue-950 rounded-lg f-size-sm f-weight-bold hover:bg-blue-200 border border-blue-200">
                ${t.btn_clear_filters}
            </button>
        </td>
    </tr>`;
        return;
    }

    tbody.innerHTML = filtered.map((p, idx) => DynamicTableRenderer.getRowHTML(p, idx, activeFields, currentPartnerKey)).join('');
}

function toggleProductDetail(index, productName) {
    const currentPartnerKey = partnerConfigMap[AppState.partner] || 'mpi';
    if (currentPartnerKey !== 'mpi') return;

    const detailRow = document.getElementById(`detail-${index}`);
    const arrowIcon = document.getElementById(`arrow-${index}`);
    const parentRow = detailRow ? detailRow.previousElementSibling : null;

    if (!detailRow) return;

    if (detailRow.classList.contains('hidden')) {
        detailRow.classList.remove('hidden');
        if (arrowIcon) arrowIcon.classList.add('rotate-90', 'text-blue-900');
        if (parentRow) parentRow.classList.add('row-expanded');
        if (!AppState.expandedDetails.includes(productName)) AppState.expandedDetails.push(productName);
    } else {
        detailRow.classList.add('hidden');
        if (arrowIcon) arrowIcon.classList.remove('rotate-90', 'text-blue-900');
        if (parentRow) parentRow.classList.remove('row-expanded');
        AppState.expandedDetails = AppState.expandedDetails.filter(name => name !== productName);
    }
}

function initFilters() {
    const filterSection = document.getElementById('performance-filter-section');
    const checkboxContainer = document.getElementById('performance-checkboxes');
    if (!checkboxContainer) return;
    checkboxContainer.innerHTML = '';

    const currentPartnerKey = partnerConfigMap[AppState.partner] || 'mpi';

    if (currentPartnerKey !== 'mpi') {
        if (filterSection) filterSection.classList.add('hidden');
        return;
    } else {
        if (filterSection) filterSection.classList.remove('hidden');
    }

    Object.entries(featureConfig[AppState.lang]).forEach(([key, label]) => {
        const isChecked = AppState.filters[key] === true;
        const checkboxItem = document.createElement('label');
        checkboxItem.className = `cursor-pointer inline-flex items-center gap-1 px-3 py-1 rounded-lg f-size-xs f-weight-bold border select-none ${
            isChecked
                ? 'bg-blue-950 text-white border-blue-950 shadow-sm'
                : 'bg-white text-slate-800 border-slate-300 hover:border-blue-400 hover:bg-blue-50'
        }`;
        checkboxItem.innerHTML = `
    <input type="checkbox" value="${key}" ${isChecked ? 'checked' : ''} onchange="toggleFilterCheckbox('${key}', this.checked)" class="sr-only" aria-label="${label}">
    <span>${label}</span>`;
        checkboxContainer.appendChild(checkboxItem);
    });
}

function toggleFilterCheckbox(key, isChecked) {
    if (isChecked) AppState.filters[key] = true;
    else delete AppState.filters[key];
    initFilters();
    renderProducts();
}

function selectDirectoryNode(lineKey, categoryKey = 'all', preserveExpanded = false) {
    if (!preserveExpanded) {
        AppState.expandedDetails = [];
    }
    AppState.productLine = lineKey;
    AppState.category = categoryKey;
    resetSearchInputFields();
    renderDirectoryTree();
    renderProducts();
    updateHashRoute(true);

    if (window.innerWidth < 1024 && categoryKey !== 'all') {
        const menu = document.getElementById('directory-tree-menu');
        const chevron = document.getElementById('mobile-sidebar-chevron');
        if (menu && !menu.classList.contains('hidden')) {
            menu.classList.add('hidden');
            if (chevron) chevron.classList.remove('rotate-180');
        }
    }
}

function handleMainDirectoryClick(lineKey) {
    if (AppState.expandedMenus.includes(lineKey)) {
        AppState.expandedMenus = AppState.expandedMenus.filter(k => k !== lineKey);
    } else {
        AppState.expandedMenus.push(lineKey);
    }
    selectDirectoryNode(lineKey, 'all');
}

function updateNodeActiveStyles(lineKey, categoryKey) {
    document.querySelectorAll('.dir-node-btn').forEach(btn => {
        btn.classList.remove('dir-node-active', 'bg-blue-100', 'text-blue-950', 'f-weight-bold');
    });

    const activeBtn = document.querySelector(`button[data-line="${lineKey}"][data-cat="${categoryKey}"]`);
    if (activeBtn) {
        activeBtn.classList.add('dir-node-active');
        const sidebar = activeBtn.closest('aside');
        if (sidebar) {
            const sidebarRect = sidebar.getBoundingClientRect();
            const btnRect = activeBtn.getBoundingClientRect();
            if (btnRect.top < sidebarRect.top || btnRect.bottom > sidebarRect.bottom) {
                sidebar.scrollTop += (btnRect.top - sidebarRect.top) - 20;
            }
        }
    } else {
        const parentBtn = document.getElementById(`node-${lineKey}-all`);
        if (parentBtn) {
            parentBtn.classList.add('dir-node-active');
        }
    }
}

// DOM Ready & Bootstrap
document.addEventListener("DOMContentLoaded", () => {
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.innerText = new Date().getFullYear();

    const matrixBody = document.getElementById('directory-matrix-body');
    if (matrixBody) {
        matrixBody.addEventListener('click', (e) => {
            const targetBtn = e.target.closest('button[data-action]');
            if (targetBtn) {
                e.stopPropagation();
                if (targetBtn.dataset.action === 'toggle-compare') {
                    toggleCompareProduct(targetBtn.dataset.product, targetBtn.dataset.partner, targetBtn.dataset.line);
                    return;
                }
                if (targetBtn.dataset.action === 'request-sample') {
                    requestProductSample(targetBtn.dataset.product);
                    return;
                }
                openModal(targetBtn.dataset.product, targetBtn.dataset.action);
                return;
            }

            const row = e.target.closest('tr[data-product-name]');
            if (row) {
                toggleProductDetail(row.dataset.index, row.dataset.productName);
            }
        });
    }

    fetch('config.json')
        .then(res => res.ok ? res.json() : AppState.configs)
        .then(configData => {
            AppState.configs = configData;
            parseHashRoute();
            if (!window.location.hash) updatePartnerUI();
            prewarmBackendServer();
        })
        .catch(() => {
            parseHashRoute();
            if (!window.location.hash) updatePartnerUI();
            prewarmBackendServer();
        });
});
