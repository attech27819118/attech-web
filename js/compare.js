/**
 * ====================================================================
 * ATTech Web - Product Comparison Dock & Modal Matrix (compare.js)
 * ====================================================================
 */

let compareFilterMode = 'all_valid'; // 'all_valid' | 'diff'

function setCompareFilterMode(mode) {
    compareFilterMode = mode;
    ['all_valid', 'diff'].forEach(m => {
        const btn = document.getElementById(`btn-filter-${m}`);
        if (btn) {
            if (m === mode) {
                btn.className = "px-3.5 py-1 text-xs font-bold rounded-md transition-all bg-blue-900 text-white shadow-xs";
            } else {
                btn.className = "px-3.5 py-1 text-xs font-medium text-slate-700 hover:text-blue-900 rounded-md transition-all";
            }
        }
    });
    const infoEl = document.getElementById('compare-filter-info');
    if (infoEl) {
        const tMap = {
            'all_valid': uiText[AppState.lang].compare_filter_info_all,
            'diff': uiText[AppState.lang].compare_filter_info_diff
        };
        infoEl.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-blue-600 inline-block mr-1"></span><span>${tMap[mode] || tMap['all_valid']}</span>`;
    }
    renderCompareMatrix();
}

function findProductByName(productName) {
    if (!productName) return null;
    if (AppState.allProductsCache['mpi_master']) {
        const found = AppState.allProductsCache['mpi_master'].find(p => p.product_name === productName);
        if (found) return found;
    }
    for (const key in AppState.allProductsCache) {
        const list = AppState.allProductsCache[key];
        if (Array.isArray(list)) {
            const found = list.find(p => p && p.product_name === productName);
            if (found) return found;
        }
    }
    return null;
}

function toggleCompareProduct(productName, partnerKey = null, lineKey = null, productObj = null) {
    if (!productName) return;
    const index = AppState.compareList.findIndex(item => item.product_name === productName);
    const t = uiText[AppState.lang];

    if (index > -1) {
        AppState.compareList.splice(index, 1);
        showToast(AppState.lang === 'zh' ? `已從比較清單移除「${productName}」` : `Removed "${productName}" from comparison`, 'info');
    } else {
        if (AppState.compareList.length >= 4) {
            showToast(t.max_compare_limit, 'warning');
            return;
        }
        const p = (productObj && Object.keys(productObj).length > 2) ? productObj : (findProductByName(productName) || {product_name: productName});
        let finalPartner = partnerKey;
        if (!finalPartner || finalPartner === 'MPI') {
            if (p.brand_code === 'dorfketal' || p.brand === 'dorfketal') finalPartner = 'DorfKetal';
            else if (p.brand_code === 'orion' || p.brand === 'orion') finalPartner = 'Orion';
            else if (p.brand_code === 'others' || p.brand === 'others') finalPartner = 'Others';
            else if (p.applications_data) finalPartner = 'MPI';
            else finalPartner = partnerKey || AppState.partner;
        }
        AppState.compareList.push({
            product_name: productName,
            partnerKey: finalPartner,
            lineKey: lineKey || AppState.productLine,
            product: p
        });
        showToast(AppState.lang === 'zh' ? `已將「${productName}」加入比較清單 (${AppState.compareList.length}/4)` : `Added "${productName}" to comparison (${AppState.compareList.length}/4)`, 'success');
    }

    updateCompareUI();
    if (!document.getElementById('compare-modal')?.classList.contains('hidden')) {
        renderCompareMatrix();
    }
}

function removeCompareProduct(productName) {
    AppState.compareList = AppState.compareList.filter(item => item.product_name !== productName);
    updateCompareUI();
    if (!document.getElementById('compare-modal')?.classList.contains('hidden')) {
        if (AppState.compareList.length === 0) {
            closeCompareModal();
        } else {
            renderCompareMatrix();
        }
    }
}

function clearCompare() {
    AppState.compareList = [];
    updateCompareUI();
    closeCompareModal();
    showToast(AppState.lang === 'zh' ? '已清空比較清單' : 'Comparison list cleared', 'info');
}

function updateCompareUI() {
    const dock = document.getElementById('compare-dock');
    const countBadge = document.getElementById('compare-count-badge');
    const slotsContainer = document.getElementById('compare-slots-container');
    const t = uiText[AppState.lang];

    const count = AppState.compareList.length;
    const activeTab = document.querySelector('.tab-content.active')?.id.replace('tab-', '') || 'about';

    // 懸浮比較欄僅在「產品專區」(products) 且有選取項目時顯示，切換至其他分頁時自動隱藏
    if (dock) {
        if (count > 0 && activeTab === 'products') {
            dock.classList.remove('hidden');
            if (dock.style) dock.style.display = 'block';
        } else {
            dock.classList.add('hidden');
            if (dock.style) dock.style.display = 'none';
        }
    }

    if (countBadge) {
        countBadge.innerText = `${count} / 4`;
    }

    // 更新 4 個槽位
    if (slotsContainer) {
        let slotsHTML = '';
        for (let i = 0; i < 4; i++) {
            const item = AppState.compareList[i];
            if (item) {
                const safeName = (item.product_name || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');
                slotsHTML += `
                <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-800/90 hover:bg-slate-800 border border-slate-700 rounded-lg text-xs font-bold text-white shadow-sm shrink-0 transition-all">
                    <span class="text-blue-400 font-bold text-xs uppercase tracking-wider bg-blue-950/80 px-1.5 py-0.5 rounded border border-blue-800/60">${item.partnerKey || 'MPI'}</span>
                    <span class="max-w-[85px] sm:max-w-[125px] truncate font-medium" title="${item.product_name}">${item.product_name}</span>
                    <button onclick="removeCompareProduct('${safeName}')" class="text-slate-400 hover:text-rose-400 ml-0.5 p-0.5 transition-colors" title="${t.btn_remove_compare}" aria-label="${t.btn_remove_compare}">
                        <i class="fa-solid fa-xmark text-xs"></i>
                    </button>
                </div>`;
            } else {
                slotsHTML += `
                <div class="flex items-center justify-center px-2.5 sm:px-3 py-1 border border-dashed border-slate-700/80 rounded-lg text-xs text-slate-500 shrink-0 select-none">
                    <span>${t.compare_empty_slot}</span>
                </div>`;
            }
        }
        slotsContainer.innerHTML = slotsHTML;
    }

    // 更新目前畫面上所有比較按鈕狀態
    document.querySelectorAll('.compare-icon-btn, .compare-toggle-btn').forEach(btn => {
        const prodName = btn.dataset.product;
        if (!prodName) return;
        const isSelected = AppState.compareList.some(item => item.product_name === prodName);
        if (btn.classList.contains('compare-icon-btn')) {
            if (isSelected) {
                btn.className = "compare-icon-btn inline-flex items-center gap-1 px-2 py-0.5 h-6 rounded-md transition-all bg-blue-900 text-white shadow-xs ring-1 ring-blue-400 border border-blue-900 active:scale-90 text-[11px] font-medium cursor-pointer shrink-0 whitespace-nowrap";
                btn.innerHTML = `<i class="fa-solid fa-check text-[10px] text-emerald-300 shrink-0"></i><span class="shrink-0 whitespace-nowrap">${AppState.lang === 'zh' ? '已比' : 'Added'}</span>`;
                btn.title = AppState.lang === 'zh' ? '從比較清單移除' : 'Remove from compare';
            } else {
                btn.className = "compare-icon-btn inline-flex items-center gap-1 px-2 py-0.5 h-6 rounded-md transition-all text-slate-600 hover:text-blue-900 hover:bg-blue-50 bg-slate-50 border border-slate-200 active:scale-90 text-[11px] font-medium cursor-pointer shrink-0 whitespace-nowrap";
                btn.innerHTML = `<i class="fa-solid fa-scale-balanced text-[10px] shrink-0"></i><span class="shrink-0 whitespace-nowrap">${AppState.lang === 'zh' ? '比較' : 'Compare'}</span>`;
                btn.title = AppState.lang === 'zh' ? '加入比較 (最多4項)' : 'Add to compare (max 4)';
            }
        } else if (btn.classList.contains('compare-toggle-btn')) {
            if (isSelected) {
                btn.className = "compare-toggle-btn px-3.5 py-1.5 rounded-lg border text-xs font-bold transition-all flex items-center gap-1.5 bg-blue-900 text-white border-blue-900 shadow-sm";
                btn.innerHTML = `<i class="fa-solid fa-check"></i><span>${t.compared}</span>`;
            } else {
                btn.className = "compare-toggle-btn px-3.5 py-1.5 rounded-lg border text-xs font-bold transition-all flex items-center gap-1.5 bg-white text-slate-700 border-slate-300 hover:bg-blue-50 hover:border-blue-300";
                btn.innerHTML = `<i class="fa-solid fa-plus"></i><span>${t.compare}</span>`;
            }
        }
    });
}

function openCompareModal() {
    if (AppState.compareList.length === 0) {
        showToast(AppState.lang === 'zh' ? '請先在列表中點擊「比較」選取產品 (最多4項)' : 'Please select products to compare first (up to 4)', 'warning');
        return;
    }
    renderCompareMatrix();
    const modal = document.getElementById('compare-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeCompareModal() {
    const modal = document.getElementById('compare-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

function requestSampleFromCompare(productName) {
    requestProductSample(productName, 'quick');
}

function extractProductSpecs(p, item) {
    const lang = AppState.lang;
    const tp = p.typical_properties || {};

    let partnerKey = item?.partnerKey;
    if (!partnerKey || partnerKey === 'MPI') {
        if (p.brand_code === 'dorfketal' || p.brand === 'dorfketal') partnerKey = 'DorfKetal';
        else if (p.brand_code === 'orion' || p.brand === 'orion') partnerKey = 'Orion';
        else if (p.brand_code === 'others' || p.brand === 'others') partnerKey = 'Others';
        else if (p.applications_data) partnerKey = 'MPI';
        else partnerKey = item?.partnerKey || 'MPI';
    }

    let appData = {};
    let ratings = {};
    let descSource = {};
    let appTitle = '';

    if (p.applications_data) {
        const targetLineKey = item?.lineKey || (p.applications_data[AppState.productLine] ? AppState.productLine : null) || Object.keys(p.applications_data)[0];
        if (targetLineKey && p.applications_data[targetLineKey]) {
            appData = p.applications_data[targetLineKey];
        } else {
            const firstKey = Object.keys(p.applications_data)[0];
            if (firstKey) appData = p.applications_data[firstKey];
        }

        if (appData) {
            if (appData.performance_ratings) {
                ratings = {...appData.performance_ratings};
            } else if (p.performance_ratings) {
                ratings = {...p.performance_ratings};
            }
            const d = appData['performance_descriptions_' + lang] || appData.performance_descriptions_zh || appData['performance_descriptions_' + (lang === 'zh' ? 'en' : 'zh')] || p['performance_descriptions_' + lang] || p.performance_descriptions_zh;
            if (d) {
                descSource = {...d};
            }
            appTitle = appData['application_title_' + lang] || appData.application_title_zh || appData.application_title_en || '';
        }
    } else {
        if (p.performance_ratings) ratings = {...p.performance_ratings};
        const d = p['performance_descriptions_' + lang] || p.performance_descriptions_zh || p.performance_descriptions_en;
        if (d) descSource = {...d};

        if (item?.lineKey) {
            const configKey = partnerConfigMap[partnerKey] || partnerKey.toLowerCase();
            const fileObj = AppState.configs[configKey]?.files?.find(f => f.key === item.lineKey);
            if (fileObj) {
                appTitle = lang === 'zh' ? (fileObj.titleZh || fileObj.title) : (fileObj.titleEn || fileObj.title);
            }
        }
    }

    // 基本化學資訊
    const comp = p['composition_' + lang] || p.composition_zh || p.composition_en || p.chemical_component || p.composition || p.chemistry || '';
    const desc = p['properties_' + lang] || p.properties || p.performance || p.desc || '';
    const usage = p['main_usage_' + lang] || p.main_usage || p.application_fields_zh || p.application_fields || p.usage || '';
    const useLevel = p['suggested_use_level_' + lang] || p.suggested_use_level_zh || p.suggested_use_level || p.dosage || '';
    const sysType = p['recommended_system_type_' + lang] || p.recommended_system_type_zh || p.recommended_system_type || (typeof p.system === 'string' ? p.system : '');
    const surfaceTreatment = p.surface_treatment || p.surface_treatment_zh || '';
    const prodMethod = p.production_method || p.process || '';
    const appearance = p.appearance || p.appearance_zh || '';

    // 體系與應用領域相容性檢查
    const checkApp = (keys) => {
        for (const k of keys) {
            if (p[k] === true || p[k] === 1 || (typeof p[k] === 'string' && p[k] !== '0' && p[k] !== 'false' && p[k] !== '')) return true;
            if (p.applications && (p.applications[k] === true || p.applications[k] === 1 || (typeof p.applications[k] === 'string' && p.applications[k] !== '0' && p.applications[k] !== ''))) return true;
            if (p.system && (p.system[k] === true || p.system[k] === 1 || (typeof p.system[k] === 'string' && p.system[k] !== '0' && p.system[k] !== ''))) return true;
            if (appData[k] || appData.applications?.[k] || appData.system?.[k]) return true;
            if (p.applications_data && p.applications_data[k]) return true;
        }
        return false;
    };

    const hasAnyDesc = Object.keys(descSource).length > 0 || (desc && desc !== '—' && desc !== 'N/A');

    return {
        name: p.product_name || item.product_name,
        partnerKey: partnerKey,
        appTitle: appTitle,
        rawProduct: p,

        comp: comp,
        surface_treatment: surfaceTreatment,
        production_method: prodMethod,
        appearance: appearance,
        desc: desc,
        usage: usage,

        melt_point: tp.melt_point_c || tp.melt_point || p.melt_point_c || p.melt_point || '',
        mean_size: (tp.mean_particle_size_um && tp.mean_particle_size_um !== '—') ? tp.mean_particle_size_um : (p.mean_particle_size_um || p.particle_size || tp.mean_size || ''),
        primary_particle_size: tp.average_primary_particle_size_nm || tp.primary_particle_size || p.average_primary_particle_size_nm || p.primary_particle_size || '',
        max_size: tp.max_particle_size_um ? `${tp.max_particle_size_um} µm` : (p.max_particle_size_um || tp.max_size || ''),
        density: tp.density_g_cc_25c || tp.density || p.density_g_cc_25c || p.density || '',
        softening_point: tp.softening_point || p.softening_point || '',
        acid_value: tp.acid_value || p.acid_value || '',
        oh_value: tp.OH_value || p.OH_value || p.oh_value || tp.oh_value || '',
        chlorine: tp.chlorine_content || p.chlorine_content || p.chlorine || '',
        viscosity: tp.viscosity || p.viscosity || '',
        molecular_weight: tp.molecular_weight || p.molecular_weight || '',
        flash_point: tp.flash_point || p.flash_point || '',
        boiling_point: tp.boiling_point || p.boiling_point || '',
        ph_value: tp.ph_value || p.ph_value || '',
        blackness_my: tp.blackness_my || p.blackness_my || '',
        tinting_strength: tp.tinting_strength || p.tinting_strength || '',
        bet_surface_area: tp.bet_surface_area || p.bet_surface_area || '',
        oil_absorption: tp.oil_absorption_number || tp.oil_absorption || p.oil_absorption_number || p.oil_absorption || '',
        volatile_matter: tp.volatile_matter_950c || tp.volatile_matter || p.volatile_matter_950c || p.volatile_matter || '',
        ash_content: tp.ash_content || p.ash_content || '',

        perf_desc: hasAnyDesc ? 'has_desc' : '',
        sysType: sysType,
        useLevel: useLevel,

        app_wood: checkApp(['wood_coating', 'wood_coatings', 'solvent_base_wood_coating', 'wood']),
        app_baking: checkApp(['enamel_paint', 'solvent_base_powder_coatings', 'powder_coating', 'powder_coatings', 'powder']),
        app_plastic: checkApp(['solvent_base_plastic_coatings', 'plastic_coating', 'plastic_coatings', 'plastic']),
        app_leather: checkApp(['solvent_base_leather_coatings', 'leather_coating', 'leather_coatings', 'leather']),
        app_fabric: checkApp(['solvent_base_nylon_coated_fabric', 'nylon', 'fabric']),
        app_ink: checkApp(['ink', 'inks', 'solvent_base_inks', 'solvent_base_ink', 'liquid_inks_solvent_based', 'screen_inks', 'publication_gravure_inks']),
        app_waterborne: checkApp(['waterborne', 'waterbased', 'liquid_inks_water_based', 'aquous_inkjet_inks']),
        app_uv: checkApp(['uv_coatings_and_inks', 'uv', 'uv_curing_inks', 'uv_curing_inkjet_inks', 'energy curable coatings and inks']),
        app_pu: checkApp(['pu_industrial_coating', 'industrial_coating', 'industrial_coatings', 'general_industrial_coating', 'wet_pu_coloring']),
        app_traffic: checkApp(['traffic_paint']),
        app_sealant: checkApp(['sealant', 'sealants', 'hot_glue', 'adhesive_and_sealant']),
        app_adhesion: checkApp(['adhesion_promoter', 'adhesion_promotion']),
        app_crosslink: checkApp(['crosslinking_agent', 'crosslinking']),
        app_surface_mod: checkApp(['surface_modifier', 'surface_modification']),
        app_casting: checkApp(['casting_elastomers', 'cold_casting_elastomers', 'hot_casting_elastomers']),
        app_foam: checkApp(['pu_foam_soft_and_rigid_foams', 'pu_foam', 'pu_foams']),
        app_composites: checkApp(['composites', 'composite']),

        ratings: ratings,
        descSource: descSource,
        website: p.website,
        techDataUrl: p.tech_data_url
    };
}

const specCategories = [
    {
        categoryId: 'basic',
        categoryTitle: {zh: '基本化學資訊與成分', en: 'Basic Chemical Information & Composition'},
        categoryIcon: 'fa-microscope',
        rows: [
            {key: 'comp', label: {zh: '化學組成 / 主成分', en: 'Chemical Composition'}, type: 'text'},
            {key: 'production_method', label: {zh: '生產方法 / 製程', en: 'Production Method'}, type: 'badge'},
            {key: 'surface_treatment', label: {zh: '表面處理 / 特徵', en: 'Surface Treatment'}, type: 'text'},
            {key: 'appearance', label: {zh: '外觀 / 色澤', en: 'Appearance'}, type: 'text'},
            {key: 'usage', label: {zh: '主要用途 / 應用領域', en: 'Main Usage / Fields'}, type: 'text'}
        ]
    },
    {
        categoryId: 'physical',
        categoryTitle: {zh: '物理、化學特性與性能指標', en: 'Physical & Chemical Properties & Features'},
        categoryIcon: 'fa-gauge-high',
        rows: [
            {key: 'melt_point', label: {zh: '熔點 (°C)', en: 'Melt Point (°C)'}, type: 'value'},
            {key: 'mean_size', label: {zh: '平均粒徑 D50 (µm)', en: 'Mean Size D50 (µm)'}, type: 'value'},
            {
                key: 'primary_particle_size',
                label: {zh: '原生粒徑 (nm)', en: 'Primary Particle Size (nm)'},
                type: 'value'
            },
            {key: 'max_size', label: {zh: '最大粒徑 D100 (µm)', en: 'Max Size D100 (µm)'}, type: 'value'},
            {key: 'density', label: {zh: '密度 (g/cm³)', en: 'Density (g/cm³)'}, type: 'value'},
            {key: 'softening_point', label: {zh: '軟化點 (°C)', en: 'Softening Point (°C)'}, type: 'value'},
            {key: 'acid_value', label: {zh: '酸值 (mgKOH/g)', en: 'Acid Value (mgKOH/g)'}, type: 'value'},
            {key: 'oh_value', label: {zh: '羥值 OH value', en: 'Hydroxyl Value (OH)'}, type: 'value'},
            {key: 'chlorine', label: {zh: '氯含量 (%)', en: 'Chlorine Content (%)'}, type: 'value'},
            {key: 'viscosity', label: {zh: '黏度 (mPa.s)', en: 'Viscosity (mPa.s)'}, type: 'value'},
            {key: 'molecular_weight', label: {zh: '分子量 (g/mol)', en: 'Molecular Weight (g/mol)'}, type: 'value'},
            {key: 'flash_point', label: {zh: '閃點 (°C)', en: 'Flash Point (°C)'}, type: 'value'},
            {key: 'boiling_point', label: {zh: '沸點 (°C)', en: 'Boiling Point (°C)'}, type: 'value'},
            {key: 'ph_value', label: {zh: 'pH 值', en: 'pH Value'}, type: 'value'},
            {key: 'blackness_my', label: {zh: '黑度 (My)', en: 'Blackness (My)'}, type: 'value'},
            {key: 'tinting_strength', label: {zh: '著色力 (%)', en: 'Tinting Strength (%)'}, type: 'value'},
            {
                key: 'bet_surface_area',
                label: {zh: 'BET 比表面積 (m²/g)', en: 'BET Surface Area (m²/g)'},
                type: 'value'
            },
            {key: 'oil_absorption', label: {zh: '吸油量 (g/100g)', en: 'Oil Absorption (g/100g)'}, type: 'value'},
            {key: 'volatile_matter', label: {zh: '揮發分 (%)', en: 'Volatile Matter (%)'}, type: 'value'},
            {key: 'ash_content', label: {zh: '灰分 (%)', en: 'Ash Content (%)'}, type: 'value'},
            {
                key: 'perf_desc',
                label: {zh: '性能特點詳細說明', en: 'Performance Highlights & Descriptions'},
                type: 'perf_desc'
            }
        ]
    },
    {
        categoryId: 'systems',
        categoryTitle: {zh: '適用體系與建議用量', en: 'Recommended Systems & Usage'},
        categoryIcon: 'fa-sliders',
        rows: [
            {key: 'sysType', label: {zh: '適用系統類型', en: 'Recommended Systems'}, type: 'text'},
            {key: 'useLevel', label: {zh: '建議添加比例 / 用法', en: 'Suggested Use Level'}, type: 'text'}
        ]
    },
    {
        categoryId: 'applications_check',
        categoryTitle: {zh: '應用領域適用對照', en: 'Application Field Compatibility'},
        categoryIcon: 'fa-table-cells',
        rows: [
            {key: 'app_wood', label: {zh: '木器漆塗料', en: 'Wood Coating'}, type: 'check'},
            {key: 'app_baking', label: {zh: '烤漆 / 粉體塗料', en: 'Baking / Powder Coating'}, type: 'check'},
            {key: 'app_plastic', label: {zh: '塑膠塗料', en: 'Plastic Coating'}, type: 'check'},
            {key: 'app_leather', label: {zh: '皮革塗料', en: 'Leather Coating'}, type: 'check'},
            {key: 'app_fabric', label: {zh: '尼龍與織物塗層', en: 'Fabric & Nylon Coating'}, type: 'check'},
            {key: 'app_ink', label: {zh: '油墨印刷', en: 'Inks'}, type: 'check'},
            {key: 'app_waterborne', label: {zh: '水性體系適用', en: 'Waterborne System'}, type: 'check'},
            {key: 'app_uv', label: {zh: 'UV 系統', en: 'UV Curable System'}, type: 'check'},
            {key: 'app_pu', label: {zh: 'PU 機械與工業塗料', en: 'PU & Industrial Coatings'}, type: 'check'},
            {key: 'app_traffic', label: {zh: '路標漆', en: 'Traffic Paint'}, type: 'check'},
            {key: 'app_sealant', label: {zh: '黏著劑與密封膠', en: 'Adhesives & Sealants'}, type: 'check'},
            {key: 'app_adhesion', label: {zh: '密著促進作用', en: 'Adhesion Promotion'}, type: 'check'},
            {key: 'app_crosslink', label: {zh: '交聯固化劑', en: 'Crosslinking Agent'}, type: 'check'},
            {key: 'app_surface_mod', label: {zh: '表面改質作用', en: 'Surface Modification'}, type: 'check'},
            {key: 'app_casting', label: {zh: '灌注型彈性體 (冷/熱)', en: 'Casting Elastomers'}, type: 'check'},
            {key: 'app_foam', label: {zh: 'PU 發泡體系', en: 'PU Foams'}, type: 'check'},
            {key: 'app_composites', label: {zh: '複合材料', en: 'Composites'}, type: 'check'}
        ]
    }
];

function renderCompareMatrix() {
    const container = document.getElementById('compare-table-container');
    if (!container) return;

    if (AppState.compareList.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12 text-slate-500">
                <i class="fa-solid fa-scale-balanced text-4xl mb-3 text-slate-400"></i>
                <p class="font-bold text-base text-slate-800 mb-1">${uiText[AppState.lang].no_compare_items}</p>
                <p class="text-xs text-slate-600">${uiText[AppState.lang].compare_dock_sub}</p>
            </div>`;
        return;
    }

    const t = uiText[AppState.lang];
    const lang = AppState.lang;
    const items = AppState.compareList;
    const colCount = items.length;
    const colWidthPct = Math.floor(80 / colCount);

    const productsSpecs = items.map(item => {
        const p = (item.product && Object.keys(item.product).length > 2) ? item.product : (findProductByName(item.product_name) || item.product || {product_name: item.product_name});
        return extractProductSpecs(p, item);
    });

    const hasVal = (v) => v !== null && v !== undefined && v !== '' && v !== '—' && v !== 'N/A' && v !== false;

    const isRowVisible = (rowKey) => {
        return productsSpecs.some(spec => hasVal(spec[rowKey]));
    };

    const isRowDiff = (rowKey) => {
        const vals = productsSpecs.map(s => String(s[rowKey] || '').trim());
        return new Set(vals).size > 1;
    };

    let html = `
    <table class="compare-matrix-table bg-white shadow-sm min-w-full">
        <thead>
            <tr class="border-b-2 border-slate-300">
                <th class="col-prop-label-head text-slate-800 text-left py-2.5 px-3.5 sm:px-4 text-xs font-semibold uppercase tracking-wider bg-slate-100">
                    <div class="flex items-center gap-1.5">
                        <i class="fa-solid fa-table-columns text-blue-700"></i>
                        <span>${t.spec_attribute}</span>
                    </div>
                </th>
                ${productsSpecs.map(pd => {
        const safeName = (pd.name || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');
        return `
                    <th class="col-product-head text-center py-2.5 px-3 sm:px-4 bg-white border-b-2 border-blue-600 align-top" style="width: ${colWidthPct}%">
                        <div class="flex items-center justify-between mb-1.5">
                            <span class="product-brand-tag inline-block px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-900 border border-blue-200">${pd.partnerKey}</span>
                            <button onclick="removeCompareProduct('${safeName}')" class="text-slate-400 hover:text-rose-600 text-xs p-1 transition-colors" title="${t.btn_remove_compare}" aria-label="${t.btn_remove_compare}">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>
                        <div class="product-name-title mb-1 break-words">${pd.name}</div>
                        ${pd.appTitle ? `<div class="text-[11px] font-medium text-blue-800 bg-blue-50/80 rounded px-2 py-0.5 mb-2 inline-block border border-blue-200">${pd.appTitle}</div>` : '<div class="mb-1"></div>'}
                        <div class="flex flex-col gap-1.5 w-full">
                            <button onclick="requestSampleFromCompare('${safeName}')" class="w-full py-1.5 px-2 bg-blue-900 hover:bg-blue-800 active:scale-95 text-white rounded-lg text-xs font-semibold transition-all shadow-xs flex items-center justify-center gap-1.5">
                                <i class="fa-solid fa-paper-plane text-xs"></i>
                                <span>${t.btn_req_sample}</span>
                            </button>
                            <div class="flex items-center justify-center gap-1.5">
                                ${pd.website && pd.website !== 'N/A' ? `<button onclick="openModal('${safeName}', 'tds')" class="flex-1 py-1 px-1.5 bg-red-50 hover:bg-red-100 border border-red-200 text-red-700 rounded-md text-xs font-semibold flex items-center justify-center gap-1 transition-all" title="${pd.name} TDS"><i class="fa-solid fa-file-pdf"></i> TDS</button>` : ''}
                                ${pd.techDataUrl && pd.techDataUrl !== 'N/A' ? `<button onclick="openModal('${safeName}', 'data')" class="flex-1 py-1 px-1.5 bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-700 rounded-md text-xs font-semibold flex items-center justify-center gap-1 transition-all" title="${pd.name} Tech Data"><i class="fa-solid fa-file-lines"></i> Data</button>` : ''}
                            </div>
                        </div>
                    </th>`;
    }).join('')}
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
    `;

    // 逐一渲染規格分類
    specCategories.forEach(cat => {
        const visibleRows = cat.rows.filter(r => isRowVisible(r.key));
        const hasCatRatings = (cat.categoryId === 'physical') && productsSpecs.some(s => Object.keys(s.ratings || {}).length > 0);

        if (visibleRows.length === 0 && !hasCatRatings) return;

        const catTitle = cat.categoryTitle[lang] || cat.categoryTitle.zh;
        html += `
            <tr class="compare-category-row">
                <td colspan="${colCount + 1}" class="compare-category-cell py-2 px-3.5 sm:px-4">
                    <div class="sticky-cat-title inline-flex items-center gap-2">
                        <i class="fa-solid ${cat.categoryIcon} text-blue-700"></i>
                        <span>${catTitle}</span>
                    </div>
                </td>
            </tr>
        `;

        visibleRows.forEach(row => {
            const rowLabel = row.label[lang] || row.label.zh;
            const rowHasDiff = isRowDiff(row.key);
            const highlightRowClass = (compareFilterMode === 'diff' && rowHasDiff) ? 'compare-diff-cell' : '';

            html += `
            <tr>
                <td class="col-prop-label ${highlightRowClass}">${rowLabel}</td>
                ${productsSpecs.map(pd => {
                const val = pd[row.key];
                let cellContent = '—';

                if (row.type === 'check') {
                    cellContent = val ? '<span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 text-blue-800 text-xs font-bold">✓</span>' : '<span class="text-slate-300 font-normal">—</span>';
                } else if (row.type === 'badge') {
                    cellContent = val ? `<span class="inline-block px-2 py-0.5 rounded bg-slate-100 text-slate-800 text-xs font-medium border border-slate-200">${val}</span>` : '<span class="text-slate-300 text-xs">—</span>';
                } else if (row.type === 'value') {
                    cellContent = hasVal(val) ? `<span class="font-semibold text-slate-900 text-xs font-tabular">${val}</span>` : '<span class="text-slate-300 text-xs">—</span>';
                } else if (row.type === 'perf_desc') {
                    const descEntries = Object.entries(pd.descSource || {}).filter(([_, d]) => d && d !== 'N/A' && d !== '—');
                    if (descEntries.length > 0) {
                        const list = descEntries.map(([k, d]) => {
                            const lbl = (featureConfig[lang] && featureConfig[lang][k]) ? featureConfig[lang][k] : (featureConfig['zh'][k] || k);
                            return `<li class="mb-1.5 text-slate-700 text-xs leading-relaxed"><strong class="text-slate-900 font-semibold">${lbl}：</strong>${d}</li>`;
                        }).join('');
                        cellContent = `<ul class="list-disc pl-4 space-y-1 text-left">${list}</ul>`;
                    } else if (pd.desc && pd.desc !== '—' && pd.desc !== 'N/A') {
                        cellContent = `<div class="text-slate-700 text-xs leading-relaxed text-left whitespace-pre-line">${pd.desc}</div>`;
                    } else {
                        cellContent = '<span class="text-slate-300 text-xs">—</span>';
                    }
                } else {
                    cellContent = hasVal(val) ? `<span class="text-slate-700 text-xs leading-relaxed break-words whitespace-pre-line">${val}</span>` : '<span class="text-slate-300 text-xs">—</span>';
                }

                return `<td class="${(row.type === 'check' || row.type === 'value' || row.type === 'badge') ? 'text-center' : 'text-left'} ${highlightRowClass}">${cellContent}</td>`;
            }).join('')}
            </tr>`;
        });

        // 物理與化學特性評分指標
        if (cat.categoryId === 'physical' && hasCatRatings) {
            const ratingKeysToShow = Object.keys(featureConfig[lang]).filter(fKey => {
                return productsSpecs.some(s => (s.ratings[fKey] || 0) > 0);
            });

            if (ratingKeysToShow.length > 0) {
                ratingKeysToShow.forEach(fKey => {
                    const label = featureConfig[lang][fKey] || fKey;
                    const ratingDiff = new Set(productsSpecs.map(s => s.ratings[fKey] || 0)).size > 1;
                    const highlightClass = (compareFilterMode === 'diff' && ratingDiff) ? 'compare-diff-cell' : '';

                    html += `
                    <tr>
                        <td class="col-prop-label ${highlightClass}">
                            <span class="inline-flex items-center gap-1"><i class="fa-solid fa-star text-amber-500 text-[10px]"></i> ${label}</span>
                        </td>
                        ${productsSpecs.map(pd => {
                        const score = pd.ratings[fKey] || 0;
                        if (score <= 0) return `<td class="text-center text-slate-300 text-xs ${highlightClass}">—</td>`;
                        if (score === 3) {
                            return `<td class="text-center ${highlightClass}"><span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs bg-blue-900 text-white font-semibold shadow-xs"><i class="fa-solid fa-star text-xs text-amber-300"></i> +++ ${lang === 'zh' ? '卓越' : 'Outstanding'}</span></td>`;
                        } else if (score === 2) {
                            return `<td class="text-center ${highlightClass}"><span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs bg-blue-700/90 text-white font-medium shadow-xs">++ ${lang === 'zh' ? '良好' : 'Recommended'}</span></td>`;
                        } else {
                            return `<td class="text-center ${highlightClass}"><span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs bg-blue-100 text-blue-950 border border-blue-300 font-medium">+ ${lang === 'zh' ? '有效' : 'Effective'}</span></td>`;
                        }
                    }).join('')}
                    </tr>`;
                });
            }
        }
    });

    html += `
        </tbody>
    </table>`;

    container.innerHTML = html;
}
