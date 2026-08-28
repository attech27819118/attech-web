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
        AppState.expandedMenus = [];
        if (typeof updateSearchLayout === 'function' && !AppState.searchQuery) {
            updateSearchLayout(false);
        }
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
        localPath = `./tds/${productName} TDS.pdf`;
        if (title) title.innerText = `${productName} - TDS`;
        if (icon) icon.className = "fa-solid fa-file-pdf text-red-600 mr-2 f-size-base";
    } else if (type === 'data') {
        localPath = `./coatingsdata/${productName} data.pdf`;
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

function parseHashRoute() {
    const hash = window.location.hash.replace(/^#\/?/, '');
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
            if (typeof updateSearchLayout === 'function') updateSearchLayout(true);
            loadAllBrandsData().then(() => {
                if (typeof renderGroupedSearchResults === 'function') {
                    renderGroupedSearchResults(q);
                }
            });
            return;
        }

        if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
        if (typeof updateSearchLayout === 'function') updateSearchLayout(false);
        const partner = params.get('partner');
        const line = params.get('line');
        const category = params.get('category');
        const productName = params.get('product') || params.get('item');

        if (productName) {
            AppState.selectedProduct = productName;
            if (partner && line) {
                navigateToCategory(partner, line, category || 'all', productName);
                return;
            }

            // 若只有 product 參數，全域比對所屬品牌與系列
            loadAllBrandsData().then(() => {
                const cleanStr = s => (s || '').replace(/&[a-z0-9#]+;/gi, '').replace(/[®™©]/g, '').trim().toLowerCase();
                const targetClean = cleanStr(productName);

                if (AppState.allProductsCache['mpi_master']) {
                    const mpiFound = AppState.allProductsCache['mpi_master'].find(item => cleanStr(item.product_name) === targetClean || cleanStr(item.product_name).includes(targetClean));
                    if (mpiFound) {
                        const appKeys = mpiFound.applications_data ? Object.keys(mpiFound.applications_data) : [];
                        const targetLine = appKeys.length > 0 ? appKeys[0] : 'ptfe';
                        navigateToCategory('MPI', targetLine, 'all', mpiFound.product_name);
                        return;
                    }
                }

                for (const [pKey, brandObj] of Object.entries(AppState.configs)) {
                    if (brandObj.files) {
                        for (const file of brandObj.files) {
                            const cached = AppState.allProductsCache[file.key];
                            if (Array.isArray(cached)) {
                                const found = cached.find(item => cleanStr(item.product_name) === targetClean || (item.product_name && cleanStr(item.product_name).includes(targetClean)));
                                if (found) {
                                    const matchedPartner = Object.keys(partnerConfigMap).find(k => partnerConfigMap[k] === pKey) || 'Others';
                                    navigateToCategory(matchedPartner, file.key, 'all', found.product_name);
                                    return;
                                }
                            }
                        }
                    }
                }

                if (partner) AppState.partner = partner;
                if (typeof updatePartnerUI === 'function') updatePartnerUI();
            });
            return;
        }

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
            if (AppState.selectedProduct) params.set('product', AppState.selectedProduct);
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
    if (typeof searchDebounceTimer !== 'undefined' && searchDebounceTimer) {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = null;
    }
    if (typeof resetSearchInputFields === 'function') resetSearchInputFields();
    if (typeof updateSearchLayout === 'function') updateSearchLayout(false);
    AppState.filters = {};
    if (typeof initFilters === 'function') initFilters();

    // 先設定好目標品牌、產品線與分類，確保狀態即時就緒
    AppState.partner = partner;
    AppState.productLine = lineKey;
    AppState.category = categoryKey || 'all';

    // 從導覽列選取產品時，側邊欄子選單預設收起 (expandedMenus 清空)，明確指引當前位置
    AppState.expandedMenus = [];

    // 若行動版側邊欄處於開啟狀態，自動收合
    const mobileMenu = document.getElementById('directory-tree-menu');
    const mobileChevron = document.getElementById('mobile-sidebar-chevron');
    if (mobileMenu && !mobileMenu.classList.contains('hidden') && window.innerWidth < 768) {
        mobileMenu.classList.add('hidden');
        if (mobileChevron) mobileChevron.classList.remove('rotate-180');
    }

    if (productName) {
        AppState.expandedDetails = [productName];
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

            const scrollToTarget = () => {
                if (productName) {
                    document.querySelectorAll('.row-target-highlight').forEach(el => el.classList.remove('row-target-highlight'));

                    const cleanStr = s => (s || '')
                        .replace(/&[a-z0-9#]+;/gi, '')
                        .replace(/[®™©]/g, '')
                        .trim()
                        .replace(/[\r\n\s]+/g, ' ')
                        .toLowerCase();

                    const targetClean = cleanStr(productName);
                    const rows = Array.from(document.querySelectorAll('tr[data-product-name]'));

                    // 尋找目標產品列 (多層級比對：精確比對 -> 淨化標準化比對 -> 子字串比對)
                    let targetRow = rows.find(row => {
                        const rowName = row.getAttribute('data-product-name') || row.dataset?.productName;
                        return rowName === productName;
                    });

                    if (!targetRow) {
                        targetRow = rows.find(row => {
                            const rowName = row.getAttribute('data-product-name') || row.dataset?.productName;
                            return cleanStr(rowName) === targetClean;
                        });
                    }

                    if (!targetRow) {
                        targetRow = rows.find(row => {
                            const rowClean = cleanStr(row.getAttribute('data-product-name') || row.dataset?.productName);
                            return rowClean.length > 0 && targetClean.length > 0 && (rowClean.includes(targetClean) || targetClean.includes(rowClean));
                        });
                    }

                    if (targetRow) {
                        targetRow.classList.add('row-target-highlight');

                        // 滾動水平容器至最左側
                        const scrollContainer = targetRow.closest('.table-container') || targetRow.closest('.overflow-x-auto');
                        if (scrollContainer && scrollContainer.scrollLeft > 0) {
                            scrollContainer.scrollTo({ left: 0, behavior: 'smooth' });
                        }

                        // 執行平滑滾動並置頂顯示
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

                        // 若該列具備可點擊展開功能 (MPI 產品卡片) 且未展開，自動觸發展開
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

    updateHashRoute(true);
}
