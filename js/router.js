/**
 * ====================================================================
 * ATTech Web - Navigation, Hash Router, Modals & Toast (router.js)
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
        if (updateUrl && !window.location.hash.includes('?q=')) {
            if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
        }
        if (shouldUpdatePartnerUI && typeof updatePartnerUI === 'function') {
            updatePartnerUI();
        }
    } else if (tabId === 'contact') {
        if (typeof prewarmBackendServer === 'function') prewarmBackendServer();
    }
    if (typeof updateCompareUI === 'function') updateCompareUI();
    if (updateUrl) updateHashRoute(true);
}

window.addEventListener('popstate', parseHashRoute);

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
    const headerCompareText = document.getElementById('header-compare-btn-text');
    if (headerCompareText) headerCompareText.innerText = uiText[AppState.lang].compare_modal_title_short || uiText[AppState.lang].compare_dock_title;
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
        localPath = `./tds/${productName} TDS.pdf`;
        title.innerText = `${productName} - TDS`;
        icon.className = "fa-solid fa-file-pdf text-red-600 mr-2 f-size-base";
    } else if (type === 'data') {
        localPath = `./coatingsdata/${productName} data.pdf`;
        title.innerText = `${productName} - Tech Data`;
        icon.className = "fa-solid fa-file-lines text-blue-700 mr-2 f-size-base";
    }

    iframe.src = localPath + "#toolbar=0&navpanes=0";
    if (downloadBtn) {
        downloadBtn.href = localPath;
        downloadBtn.download = `${productName}_${type.toUpperCase()}.pdf`;
    }

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function toggleTdsModal(open) {
    const modal = document.getElementById('tds-modal');
    const iframe = document.getElementById('tds-iframe');
    if (!open) {
        modal.classList.replace('flex', 'hidden');
        iframe.src = "";
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

function parseHashRoute() {
    const hash = window.location.hash.replace(/^#/, '');
    if (!hash) return;

    const [tabPart, queryPart] = hash.split('?');
    const tabId = tabPart || 'about';
    const params = new URLSearchParams(queryPart || '');

    switchTab(tabId, false, false);

    if (tabId === 'products') {
        const q = params.get('q');
        if (q) {
            AppState.searchQuery = q;
            document.querySelectorAll('.global-search-input').forEach(input => input.value = q);
            loadAllBrandsData().then(() => {
                if (typeof renderGroupedSearchResults === 'function') {
                    renderGroupedSearchResults(q);
                }
            });
            return;
        }

        if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
        const partner = params.get('partner');
        const line = params.get('line');
        const category = params.get('category');

        if (partner) AppState.partner = partner;

        const configKey = partnerConfigMap[AppState.partner] || 'mpi';
        const brandConfig = AppState.configs[configKey];

        if (line && brandConfig?.files?.some(f => f.key === line)) {
            AppState.productLine = line;
        } else if (brandConfig?.files?.[0]) {
            AppState.productLine = brandConfig.files[0].key;
        }

        AppState.category = category || 'all';

        if (typeof updatePartnerUI === 'function') updatePartnerUI();
    } else if (tabId === 'contact') {
        const mode = params.get('mode');
        if (mode && typeof switchFormMode === 'function') switchFormMode(mode);
    }
}

function updateHashRoute(usePush = false) {
    const activeTab = document.querySelector('.tab-content.active')?.id.replace('tab-', '') || 'about';
    const params = new URLSearchParams();

    if (activeTab === 'products') {
        if (AppState.searchQuery) {
            params.set('q', AppState.searchQuery);
        } else {
            if (AppState.partner) params.set('partner', AppState.partner);
            if (AppState.productLine) params.set('line', AppState.productLine);
            if (AppState.category && AppState.category !== 'all') params.set('category', AppState.category);
        }
    } else if (activeTab === 'contact') {
        const isDetailed = !document.getElementById('form-mode-detailed')?.classList.contains('hidden');
        params.set('mode', isDetailed ? 'detailed' : 'quick');
    }

    const queryString = params.toString();
    const newHash = `#${activeTab}${queryString ? '?' + queryString : ''}`;

    if (window.location.hash !== newHash) {
        if (usePush) {
            history.pushState(null, '', newHash);
        } else {
            history.replaceState(null, '', newHash);
        }
    }
}

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
    if (typeof resetSearchInputFields === 'function') resetSearchInputFields();

    // 先設定好目標品牌、產品線與分類，確保狀態即時就緒
    AppState.partner = partner;
    AppState.productLine = lineKey;
    AppState.category = categoryKey || 'all';

    if (!AppState.expandedMenus.includes(lineKey)) {
        AppState.expandedMenus.push(lineKey);
    }

    // 切換分頁外觀，但不觸發多餘的非同步渲染
    switchTab('products', false, false);

    if (typeof updatePartnerUI === 'function') {
        updatePartnerUI(() => {
            // 如果有指定產品名稱，確保在表格渲染後加入 expandedDetails 並展開卡片
            if (productName) {
                if (!AppState.expandedDetails.includes(productName)) {
                    AppState.expandedDetails.push(productName);
                }
                if (typeof renderProducts === 'function') renderProducts();
            }

            if (typeof updateNodeActiveStyles === 'function') {
                updateNodeActiveStyles(lineKey, categoryKey || 'all');
            }

            setTimeout(() => {
                if (productName) {
                    document.querySelectorAll('.row-target-highlight').forEach(el => el.classList.remove('row-target-highlight'));

                    // 尋找目標產品列 (使用屬性值比對，避免特殊字元造成 CSS selector 錯誤)
                    const targetRow = Array.from(document.querySelectorAll('tr[data-product-name]'))
                        .find(row => row.getAttribute('data-product-name') === productName);

                    if (targetRow) {
                        const rect = targetRow.getBoundingClientRect();
                        const top = window.pageYOffset + rect.top - 85;
                        window.scrollTo({top: Math.max(0, top), behavior: 'smooth'});
                        targetRow.classList.add('row-target-highlight');
                        return;
                    }
                }

                const targetSection = document.getElementById('section-directory-finder');
                if (targetSection) {
                    const rect = targetSection.getBoundingClientRect();
                    const top = window.pageYOffset + rect.top - 75;
                    window.scrollTo({top: Math.max(0, top), behavior: 'smooth'});
                }
            }, 80);
        });
    }

    updateHashRoute(true);
}
