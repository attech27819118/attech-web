/**
 * ====================================================================
 * ATTech Web - Navigation, Clean URL Router, Modals & Toast (router.js)
 * ====================================================================
 */

function switchTab(tabId, updateUrl = true, shouldUpdatePartnerUI = true) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    const target = document.getElementById(`tab-${tabId}`);
    if (target) target.classList.add('active');

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('text-blue-950', 'border-blue-900', 'f-weight-bold');
        btn.classList.add('text-slate-700', 'border-transparent', 'f-weight-medium');
        btn.setAttribute('aria-selected', 'false');
    });
    const activeNavBtn = document.getElementById(`nav-${tabId}`);
    if (activeNavBtn) {
        activeNavBtn.classList.remove('text-slate-700', 'border-transparent', 'f-weight-medium');
        activeNavBtn.classList.add('text-blue-950', 'border-blue-900', 'f-weight-bold');
        activeNavBtn.setAttribute('aria-selected', 'true');
    }

    document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
        btn.classList.remove('bg-blue-900', 'text-white', 'font-bold', 'shadow-xs');
        btn.classList.add('text-slate-700', 'font-medium');
        btn.setAttribute('aria-selected', 'false');
    });
    const activeMobileNavBtn = document.getElementById(`mobile-nav-${tabId}`);
    if (activeMobileNavBtn) {
        activeMobileNavBtn.classList.remove('text-slate-700', 'font-medium');
        activeMobileNavBtn.classList.add('bg-blue-900', 'text-white', 'font-bold', 'shadow-xs');
        activeMobileNavBtn.setAttribute('aria-selected', 'true');
    }

    if (tabId === 'products') {
        AppState.expandedMenus = [];
        if (typeof updateSearchLayout === 'function' && !AppState.searchQuery) {
            updateSearchLayout(false);
        }
        if (updateUrl && !window.location.search.includes('q=')) {
            if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
        }
        if (shouldUpdatePartnerUI && typeof updatePartnerUI === 'function') {
            updatePartnerUI();
        }
    } else if (tabId === 'contact') {
        if (typeof prewarmBackendServer === 'function') prewarmBackendServer();
    }
    if (typeof updateCompareUI === 'function') updateCompareUI();
    if (updateUrl) updateUrlRoute(true);
}

window.addEventListener('popstate', parseUrlRoute);

// 全域內部連結攔截器：確保點擊 <a> 標籤時維持平滑 SPA 切換，避免整頁重新整理
document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href) return;

    // 排除外部連結、錨點、電話與郵件協定
    if (
        href.startsWith('http://') ||
        href.startsWith('https://') ||
        href.startsWith('mailto:') ||
        href.startsWith('tel:') ||
        href.startsWith('#') ||
        link.target === '_blank' ||
        link.hasAttribute('download')
    ) {
        return;
    }

    e.preventDefault();
    const cleanHref = href.startsWith('/') ? href : ('/' + href);
    const basePath = getAppBasePath();
    let fullPath = cleanHref;
    if (basePath) {
        fullPath = '/' + basePath + (cleanHref === '/' ? '' : cleanHref);
    }

    if (window.location.pathname + window.location.search !== fullPath) {
        history.pushState(null, '', fullPath);
        parseUrlRoute();
    }
});

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' || e.key === 'Esc') {
        if (typeof toggleTdsModal === 'function') toggleTdsModal(false);
        if (typeof closeCompareModal === 'function') closeCompareModal();
    }
});

function switchLanguage(lang) {
    AppState.set('lang', lang);
}

function updateLanguageUI() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.className = "lang-btn px-3 py-0.5 f-size-sm f-weight-medium rounded text-slate-600 hover:text-slate-900";
    });
    const activeLangBtn = document.getElementById(`lang-${AppState.lang}-btn`);
    if (activeLangBtn) {
        activeLangBtn.className = "lang-btn px-3 py-0.5 f-size-sm f-weight-bold rounded shadow-sm bg-white text-blue-950";
    }

    if (typeof updateRatingLegend === 'function') updateRatingLegend();

    const modeLabel = document.getElementById('compare-mode-label');
    if (modeLabel) modeLabel.innerHTML = `<i class="fa-solid fa-sliders text-blue-700 mr-1"></i> ${uiText[AppState.lang].compare_mode_label}`;
    const btnAllValid = document.getElementById('btn-filter-all_valid');
    if (btnAllValid) btnAllValid.innerText = uiText[AppState.lang].filter_all_valid;
    const btnDiff = document.getElementById('btn-filter-diff');
    if (btnDiff) btnDiff.innerText = uiText[AppState.lang].filter_diff;

    const infoEl = document.getElementById('compare-filter-info');
    if (infoEl) {
        const tMap = {
            'all_valid': uiText[AppState.lang].compare_filter_info_all,
            'diff': uiText[AppState.lang].compare_filter_info_diff
        };
        infoEl.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-blue-600 inline-block mr-1"></span><span>${tMap[compareFilterMode] || tMap['all_valid']}</span>`;
    }

    const dockTitle = document.getElementById('compare-dock-title');
    if (dockTitle) dockTitle.innerText = uiText[AppState.lang].compare_dock_title;
    const dockSub = document.getElementById('compare-dock-sub');
    if (dockSub) dockSub.innerText = uiText[AppState.lang].compare_dock_sub;
    const clearBtnText = document.getElementById('btn-clear-compare-text');
    if (clearBtnText) clearBtnText.innerText = uiText[AppState.lang].btn_clear_compare;
    const openBtnText = document.getElementById('btn-open-compare-text');
    if (openBtnText) openBtnText.innerText = uiText[AppState.lang].btn_start_compare;
    const modalTitle = document.getElementById('compare-modal-title');
    if (modalTitle) modalTitle.innerText = uiText[AppState.lang].compare_modal_title;
    const modalSub = document.getElementById('compare-modal-sub');
    if (modalSub) modalSub.innerText = uiText[AppState.lang].compare_modal_sub;
    const modalClearBtn = document.getElementById('compare-modal-clear-btn');
    if (modalClearBtn) modalClearBtn.innerHTML = `<i class="fa-solid fa-arrow-rotate-left mr-1"></i> ${uiText[AppState.lang].btn_clear_compare}`;

    if (typeof renderDirectoryTree === 'function') renderDirectoryTree();
    if (typeof initFilters === 'function') initFilters();
    if (AppState.searchQuery) {
        if (typeof renderGroupedSearchResults === 'function') renderGroupedSearchResults(AppState.searchQuery);
    } else {
        if (typeof renderProducts === 'function') renderProducts();
    }
    if (typeof updateCompareUI === 'function') updateCompareUI();

    if (!document.getElementById('compare-modal')?.classList.contains('hidden')) {
        if (typeof renderCompareMatrix === 'function') renderCompareMatrix();
    }
}

function openModal(productName, type) {
    const modal = document.getElementById('tds-modal');
    const iframe = document.getElementById('tds-iframe');
    const title = document.getElementById('tds-modal-title');
    const icon = document.getElementById('modal-title-icon');
    const loading = document.getElementById('tds-loading');
    const downloadBtn = document.getElementById('tds-download-btn');
    let localPath = "";

    if (loading) loading.classList.remove('hidden');

    if (type === 'tds') {
        localPath = resolveAssetUrl(`tds/${productName} TDS.pdf`);
        if (title) title.innerText = `${productName} - TDS`;
        if (icon) icon.className = "fa-solid fa-file-pdf text-red-600 mr-2 f-size-base";
    } else if (type === 'data') {
        localPath = resolveAssetUrl(`coatingsdata/${productName} data.pdf`);
        if (title) title.innerText = `${productName} - Tech Data`;
        if (icon) icon.className = "fa-solid fa-file-lines text-blue-700 mr-2 f-size-base";
    }

    if (iframe) iframe.src = localPath + "#toolbar=0&navpanes=0";
    if (downloadBtn) {
        downloadBtn.href = localPath;
        downloadBtn.download = `${productName}_${type.toUpperCase()}.pdf`;
    }

    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function toggleTdsModal(open) {
    const modal = document.getElementById('tds-modal');
    const iframe = document.getElementById('tds-iframe');
    if (!modal) return;
    if (open) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        if (iframe) iframe.src = "";
    }
}

function showToast(msg, type = 'success') {
    const toast = document.getElementById('toast-container');
    const toastText = document.getElementById('toast-text');
    const toastIcon = toast?.querySelector('i');
    if (!toast) return;

    if (toastText) toastText.innerText = msg;
    if (toastIcon) {
        if (type === 'error') {
            toastIcon.className = 'fa-solid fa-circle-xmark text-rose-400 f-size-lg';
        } else if (type === 'warning') {
            toastIcon.className = 'fa-solid fa-triangle-exclamation text-amber-400 f-size-lg';
        } else {
            toastIcon.className = 'fa-solid fa-circle-check text-emerald-400 f-size-lg';
        }
    }

    toast.classList.remove('hidden');
    clearTimeout(window.__toastTimeout);
    window.__toastTimeout = setTimeout(() => {
        toast.classList.add('hidden');
    }, 4000);
}

// 輔助標準化字串 (比對產品名稱與 URL slug)
function normalizeProductSlug(s) {
    return (s || '')
        .replace(/&[a-z0-9#]+;/gi, '')
        .replace(/[®™©]/g, '')
        .replace(/[-_\s]+/g, ' ')
        .trim()
        .toLowerCase();
}

function getAppBasePath() {
    const baseEl = document.querySelector('base');
    if (baseEl && baseEl.getAttribute('href')) {
        const href = baseEl.getAttribute('href');
        if (href.startsWith('http://') || href.startsWith('https://')) {
            try {
                return new URL(href).pathname.replace(/\/$/, '') || '';
            } catch (e) {
                return '';
            }
        }
        return href.replace(/^\/|\/$/g, '');
    }
    return '';
}

function findProductItemBySlug(items, targetClean) {
    if (!Array.isArray(items) || !targetClean) return null;
    let found = items.find(item => normalizeProductSlug(item.product_name || item.name) === targetClean);
    if (found) return found;
    found = items.find(item => {
        const itemClean = normalizeProductSlug(item.product_name || item.name);
        return itemClean.startsWith(targetClean + ' ') || itemClean.endsWith(' ' + targetClean);
    });
    if (found) return found;
    return items.find(item => {
        const itemClean = normalizeProductSlug(item.product_name || item.name);
        return itemClean.includes(targetClean) || targetClean.includes(itemClean);
    });
}

/**
 * 解析目前 URL 路徑（支援 HTML5 Clean URL、Query 參數及舊版 Hash 路由）
 */
function parseUrlRoute() {
    // 1. 檢查並平滑遷移舊版 Hash 路由 (如 /#products?partner=MPI...)
    if (window.location.hash && window.location.hash.length > 1) {
        const legacyHash = window.location.hash.replace(/^#\/?/, '');
        const [hTab, hQuery] = legacyHash.split('?');
        const hParams = new URLSearchParams(hQuery || '');

        let cleanMigratedPath = '/';
        if (hTab === 'products') {
            const hPartner = (hParams.get('partner') || 'mpi').toLowerCase();
            const hLine = hParams.get('line') || 'ptfe';
            const hProduct = hParams.get('product') || hParams.get('item');
            cleanMigratedPath = `/products/${hPartner}/${hLine}`;
            if (hProduct) cleanMigratedPath += `/${encodeURIComponent(hProduct)}`;
            if (hParams.get('category') && hParams.get('category') !== 'all') {
                cleanMigratedPath += `?category=${encodeURIComponent(hParams.get('category'))}`;
            }
            if (hParams.get('q')) {
                cleanMigratedPath = `/products?q=${encodeURIComponent(hParams.get('q'))}`;
            }
        } else if (hTab === 'partners') {
            cleanMigratedPath = '/partners';
        } else if (hTab === 'contact') {
            const mode = hParams.get('mode');
            cleanMigratedPath = mode === 'detailed' ? '/contact?mode=detailed' : '/contact';
        }

        const basePath = getAppBasePath();
        const fullMigratedPath = basePath ? ('/' + basePath + (cleanMigratedPath === '/' ? '' : cleanMigratedPath)) : cleanMigratedPath;
        history.replaceState(null, '', fullMigratedPath);
    }

    // 2. 解析標準路徑與 Query 參數
    let pathname = window.location.pathname;
    const basePath = getAppBasePath();
    if (basePath && (pathname === '/' + basePath || pathname.startsWith('/' + basePath + '/'))) {
        pathname = pathname.slice(basePath.length + 1);
    }
    pathname = pathname.replace(/(^|\/)index\.html$/i, '').replace(/^\/|\/$/g, '');
    const searchParams = new URLSearchParams(window.location.search);
    const segments = pathname.split('/').filter(Boolean);
    const rootSegment = (segments[0] || '').toLowerCase();

    const partnerSlugMap = {
        'mpi': 'MPI',
        'dorfketal': 'DorfKetal',
        'orion': 'Orion',
        'others': 'Others'
    };

    // 首頁 (About)
    if (!rootSegment || rootSegment === 'about' || rootSegment === 'index.html') {
        switchTab('about', false, false);
        updatePageMeta('about');
        return;
    }

    // 合作夥伴 (Partners)
    if (rootSegment === 'partners') {
        switchTab('partners', false, false);
        updatePageMeta('partners');
        return;
    }

    // 索樣與諮詢 (Contact)
    if (rootSegment === 'contact') {
        switchTab('contact', false, false);
        const mode = segments[1] || searchParams.get('mode') || 'quick';
        if (typeof switchFormMode === 'function') {
            switchFormMode(mode === 'detailed' ? 'detailed' : 'quick');
        }
        updatePageMeta('contact');
        return;
    }

    // 產品專區 (Products)
    if (rootSegment === 'products') {
        switchTab('products', false, false);

        // 全域搜尋
        const query = searchParams.get('q');
        if (query) {
            AppState.searchQuery = query;
            document.querySelectorAll('.global-search-input').forEach(input => input.value = query);
            if (typeof updateSearchLayout === 'function') updateSearchLayout(true);
            loadAllBrandsData().then(() => {
                if (typeof renderGroupedSearchResults === 'function') {
                    renderGroupedSearchResults(query);
                }
            });
            updatePageMeta('search', query);
            return;
        }

        if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
        if (typeof updateSearchLayout === 'function') updateSearchLayout(false);

        const rawPartner = segments[1] || searchParams.get('partner');
        const rawLine = segments[2] || searchParams.get('line');
        const rawProduct = segments[3] || searchParams.get('product') || searchParams.get('item');
        const rawCategory = searchParams.get('category');

        const resolvedPartner = rawPartner ? (partnerSlugMap[rawPartner.toLowerCase()] || rawPartner) : 'MPI';
        if (resolvedPartner) AppState.partner = resolvedPartner;

        const configKey = partnerConfigMap[AppState.partner] || 'mpi';
        const brandConfig = AppState.configs[configKey];

        if (rawLine && brandConfig?.files?.some(f => f.key === rawLine)) {
            AppState.productLine = rawLine;
        } else if (brandConfig?.files?.[0]) {
            AppState.productLine = brandConfig.files[0].key;
        }

        AppState.category = rawCategory || 'all';

        if (rawProduct) {
            const decodedProductName = decodeURIComponent(rawProduct);
            AppState.selectedProduct = decodedProductName;

            loadAllBrandsData().then(() => {
                const targetClean = normalizeProductSlug(decodedProductName);
                let matchedItem = null;
                let matchedPartner = AppState.partner;
                let matchedLine = AppState.productLine;

                // 搜尋所有已快取的產品清單
                for (const [pKey, brandObj] of Object.entries(AppState.configs)) {
                    if (brandObj.files) {
                        for (const file of brandObj.files) {
                            const cached = AppState.allProductsCache[file.key];
                            if (Array.isArray(cached)) {
                                const found = findProductItemBySlug(cached, targetClean);
                                if (found) {
                                    matchedItem = found;
                                    matchedLine = file.key;
                                    matchedPartner = Object.keys(partnerConfigMap).find(k => partnerConfigMap[k] === pKey) || 'Others';
                                    break;
                                }
                            }
                        }
                    }
                    if (matchedItem) break;
                }

                const finalName = matchedItem ? matchedItem.product_name : decodedProductName;
                navigateToCategory(matchedPartner, matchedLine, AppState.category, finalName);
            });
            return;
        }

        if (typeof updatePartnerUI === 'function') updatePartnerUI();
        updatePageMeta('products');
    }
}

/**
 * 取得產品所屬之真實原廠品牌名稱
 */
function getProductBrandName(productName) {
    if (!productName) return '';
    const targetClean = normalizeProductSlug(productName);

    // 1. 比對 MPI 產品庫
    if (AppState.allProductsCache && AppState.allProductsCache['mpi_master']) {
        const found = findProductItemBySlug(AppState.allProductsCache['mpi_master'], targetClean);
        if (found) {
            return AppState.configs?.mpi?.brandName || 'Micro Powders';
        }
    }

    // 2. 比對 Dorf Ketal, Orion, Others 等品牌產品庫
    if (AppState.configs) {
        for (const [pKey, brandObj] of Object.entries(AppState.configs)) {
            if (brandObj.files) {
                for (const file of brandObj.files) {
                    const cached = AppState.allProductsCache ? AppState.allProductsCache[file.key] : null;
                    if (Array.isArray(cached)) {
                        const found = findProductItemBySlug(cached, targetClean);
                        if (found) {
                            return brandObj.brandName || pKey;
                        }
                    }
                }
            }
        }
    }

    const configKey = partnerConfigMap[AppState.partner] || 'mpi';
    const brandConfig = AppState.configs ? AppState.configs[configKey] : null;
    return brandConfig?.brandName || AppState.partner;
}

/**
 * 依據當前狀態平滑更新 Clean URL 與頁面 Meta 資訊
 */
function updateUrlRoute(usePush = false) {
    const activeTab = document.querySelector('.tab-content.active')?.id.replace('tab-', '') || 'about';
    let cleanPath = '/';

    if (activeTab === 'about') {
        cleanPath = '/';
        updatePageMeta('about');
    } else if (activeTab === 'partners') {
        cleanPath = '/partners/';
        updatePageMeta('partners');
    } else if (activeTab === 'contact') {
        const isDetailed = !document.getElementById('form-mode-detailed')?.classList.contains('hidden');
        cleanPath = isDetailed ? '/contact/?mode=detailed' : '/contact/';
        updatePageMeta('contact');
    } else if (activeTab === 'products') {
        if (AppState.searchQuery) {
            cleanPath = `/products/?q=${encodeURIComponent(AppState.searchQuery)}`;
            updatePageMeta('search', AppState.searchQuery);
        } else {
            const partnerSlug = (AppState.partner || 'MPI').toLowerCase();
            const lineSlug = AppState.productLine || 'ptfe';
            cleanPath = `/products/${encodeURIComponent(partnerSlug)}/${encodeURIComponent(lineSlug)}/`;

            if (AppState.selectedProduct) {
                const realBrand = getProductBrandName(AppState.selectedProduct);
                const currentConfigKey = partnerConfigMap[AppState.partner] || 'mpi';
                const currentBrandName = AppState.configs?.[currentConfigKey]?.brandName || AppState.partner;

                const isBrandMatch = !realBrand || 
                    realBrand === currentBrandName || 
                    realBrand.toLowerCase() === (AppState.partner || '').toLowerCase() ||
                    (partnerConfigMap[realBrand] && partnerConfigMap[realBrand] === currentConfigKey);

                // 檢查產品真實品牌是否屬於當前選取之 Partner，防止品牌錯置
                if (isBrandMatch) {
                    cleanPath = `/products/${encodeURIComponent(partnerSlug)}/${encodeURIComponent(lineSlug)}/${encodeURIComponent(AppState.selectedProduct)}/`;
                    updatePageMeta('product', AppState.selectedProduct);
                } else {
                    AppState.selectedProduct = null;
                    updatePageMeta('products');
                }
            } else {
                updatePageMeta('products');
            }

            if (AppState.category && AppState.category !== 'all') {
                cleanPath += `?category=${encodeURIComponent(AppState.category)}`;
            }
        }
    }

    const basePath = getAppBasePath();
    let fullPath = cleanPath;
    if (basePath) {
        fullPath = '/' + basePath + (cleanPath === '/' ? '' : cleanPath);
    }

    const currentUrl = window.location.pathname + window.location.search;
    if (currentUrl !== fullPath) {
        if (usePush) {
            history.pushState(null, '', fullPath);
        } else {
            history.replaceState(null, '', fullPath);
        }
    }
}

/**
 * 動態更新頁面標題 (SEO Title) 與標準網址 (Canonical)
 */
function updatePageMeta(type, extra = '') {
    const titleEl = document.getElementById('web-title') || document.querySelector('title');
    const baseTitle = '宏威應用材料 Discover The Link To Life';

    if (!titleEl) return;

    if (type === 'about') {
        titleEl.innerText = `${baseTitle} | 專業特用化學品供應商`;
    } else if (type === 'partners') {
        titleEl.innerText = `合作夥伴品牌 | ${baseTitle}`;
    } else if (type === 'contact') {
        titleEl.innerText = `樣品索取與技術諮詢 | ${baseTitle}`;
    } else if (type === 'search') {
        titleEl.innerText = `「${extra}」搜尋結果 | ${baseTitle}`;
    } else if (type === 'product' && extra) {
        const brandName = getProductBrandName(extra);
        titleEl.innerText = `${extra} (${brandName}) | 宏威應用材料 ATTech Materials`;
    } else if (type === 'products') {
        const configKey = partnerConfigMap[AppState.partner] || 'mpi';
        const brandConfig = AppState.configs ? AppState.configs[configKey] : null;
        const currentFile = brandConfig?.files?.find(f => f.key === AppState.productLine);
        const lineTitle = currentFile ? currentFile.titleZh : '特用化學品目錄';
        titleEl.innerText = `${lineTitle} | 宏威應用材料 ATTech Materials`;
    }
}

// 相容性函式別名
function parseHashRoute() { parseUrlRoute(); }
function updateHashRoute(usePush = false) { updateUrlRoute(usePush); }

function toggleMobileSidebar() {
    const menu = document.getElementById('directory-tree-menu');
    const chevron = document.getElementById('mobile-sidebar-chevron');
    if (!menu) return;
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
    } else {
        menu.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
    }
}

function navigateToCategory(partner, lineKey, categoryKey = 'all', productName = null) {
    if (typeof searchDebounceTimer !== 'undefined' && searchDebounceTimer) {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = null;
    }
    if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
    if (typeof updateSearchLayout === 'function') updateSearchLayout(false);
    AppState.filters = {};
    if (typeof initFilters === 'function') initFilters();

    AppState.partner = partner;
    AppState.productLine = lineKey;
    AppState.category = categoryKey || 'all';

    AppState.expandedMenus = [];

    const mobileMenu = document.getElementById('directory-tree-menu');
    const mobileChevron = document.getElementById('mobile-sidebar-chevron');
    if (mobileMenu && !mobileMenu.classList.contains('hidden') && window.innerWidth < 768) {
        mobileMenu.classList.add('hidden');
        if (mobileChevron) mobileChevron.classList.remove('rotate-180');
    }

    if (productName) {
        AppState.selectedProduct = productName;
        AppState.expandedDetails = [productName];
    } else {
        AppState.selectedProduct = null;
    }

    switchTab('products', false, false);

    if (typeof updatePartnerUI === 'function') {
        updatePartnerUI(() => {
            if (productName) {
                if (!AppState.expandedDetails.includes(productName)) {
                    AppState.expandedDetails.push(productName);
                }
                if (typeof renderProducts === 'function') renderProducts();
            }

            if (typeof updateNodeActiveStyles === 'function') {
                updateNodeActiveStyles(lineKey, categoryKey || 'all');
            }

            const scrollToTarget = () => {
                if (productName) {
                    document.querySelectorAll('.row-target-highlight').forEach(el => el.classList.remove('row-target-highlight'));

                    const targetClean = normalizeProductSlug(productName);
                    const rows = Array.from(document.querySelectorAll('tr[data-product-name]'));

                    let targetRow = rows.find(row => {
                        const rowName = row.getAttribute('data-product-name') || row.dataset?.productName;
                        return rowName === productName;
                    });

                    if (!targetRow) {
                        targetRow = rows.find(row => {
                            const rowName = row.getAttribute('data-product-name') || row.dataset?.productName;
                            return normalizeProductSlug(rowName) === targetClean;
                        });
                    }


                    if (targetRow) {
                        targetRow.classList.add('row-target-highlight');

                        const scrollContainer = targetRow.closest('.table-container') || targetRow.closest('.overflow-x-auto');
                        if (scrollContainer && scrollContainer.scrollLeft > 0) {
                            scrollContainer.scrollTo({ left: 0, behavior: 'smooth' });
                        }

                        try {
                            targetRow.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start',
                                inline: 'nearest'
                            });
                        } catch (e) {
                            const rect = targetRow.getBoundingClientRect();
                            const top = window.pageYOffset + rect.top - 115;
                            window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
                        }

                        const idx = targetRow.getAttribute('data-index');
                        const detailRow = idx !== null ? document.getElementById(`detail-${idx}`) : null;
                        if (detailRow && detailRow.classList.contains('hidden')) {
                            if (typeof toggleProductDetail === 'function') {
                                toggleProductDetail(idx, productName);
                            }
                        }

                        return;
                    }
                }

                const targetSection = document.getElementById('section-directory-finder');
                if (targetSection) {
                    const rect = targetSection.getBoundingClientRect();
                    const top = window.pageYOffset + rect.top - 75;
                    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
                }
            };

            if (typeof requestAnimationFrame === 'function') {
                requestAnimationFrame(scrollToTarget);
            } else {
                setTimeout(scrollToTarget, 16);
            }
            setTimeout(scrollToTarget, 80);
            setTimeout(scrollToTarget, 240);
        }, !!productName);
    }

    updateUrlRoute(true);
}

