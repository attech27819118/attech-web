/**
 * ====================================================================
 * ATTech Web - State Management & Global Constants (state.js)
 * ====================================================================
 */

const SVG_PLACEHOLDER = "data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='40' viewBox='0 0 120 40'%3E%3Crect width='100%25' height='100%25' fill='%23f1f5f9'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='16' font-weight='bold' fill='%2394a3b8'%3ENo Image%3C/text%3E%3C/svg%3E";

function handleImageFallback(img, localSrc) {
    if (!img.dataset.fallbackStep) {
        img.dataset.fallbackStep = "1";
        if (localSrc) {
            img.src = localSrc;
            return;
        }
    }
    img.onerror = null;
    img.src = SVG_PLACEHOLDER;
    img.classList.add('opacity-70');
}

const partnerConfigMap = {
    'MPI': 'mpi',
    'DorfKetal': 'dorfketal',
    'Orion': 'orion',
    'Others': 'others'
};

const featureCategories = {
    "ptfe_alternative": "ptfe",
    "scratch_resistance": "scratch_and_abrasion",
    "abrasion_resistance": "scratch_and_abrasion",
    "burnish_resistance": "scratch_and_abrasion",
    "rub_resistance": "scratch_and_abrasion",
    "slip_lubricity": "scratch_and_abrasion",
    "anti_slip": "scratch_and_abrasion",
    "increased_cof": "scratch_and_abrasion",
    "matting_gloss_control": "scratch_and_abrasion",
    "gloss_retention": "scratch_and_abrasion",
    "clarity": "scratch_and_abrasion",
    "soft_touch": "scratch_and_abrasion",
    "texture_structure": "texture",
    "corrosion_resistance": "special",
    "block_resistance": "special",
    "improved_extrusion_flow": "special",
    "anti_gassing": "special",
    "metal_mark_resistance": "special",
    "apparent_hardness": "special",
    "water_beading": "special",
    "water_repellency": "special",
    "heat_resistance": "special",
    "soil_resistance": "special",
    "no_silica_dust": "special",
    "cleanability": "special",
};

const featureConfig = {
    "zh": {
        "ptfe_alternative": "PTFE取代", "scratch_resistance": "耐刮", "abrasion_resistance": "耐磨",
        "burnish_resistance": "耐拋光", "rub_resistance": "耐摩擦",
        "slip_lubricity": "滑爽", "slip": "滑爽", "anti_slip": "防滑", "increased_cof": "高摩擦",
        "matting_gloss_control": "消光","v_matting_gloss_control": "更消光","gloss_retention": "保持光澤", "clarity": "透明","v_clarity": "更透明",
        "soft_touch": "柔感", "texture_structure": "織紋", "corrosion_resistance": "防腐蝕",
        "block_resistance": "抗黏性", "improved_extrusion_flow": "改善流動", "anti_gassing": "防氣泡",
        "metal_mark_resistance": "抗金屬劃痕", "apparent_hardness": "提升表面硬度", "water_beading": "撥水",
        "water_repellency": "撥水", "heat_resistance": "耐高溫", "soil_resistance": "防污性",
        "cleanability": "易潔性", "no_silica_dust": "無矽塵",
        "lubricity_smooth_feel": "滑爽/滑度", "lubricity": "滑爽/潤滑", "flow_leveling": "流平性",
        "recoatability": "重塗性", "weather_resistance": "耐候性", "chemical_resistance": "耐化學性","high_dispersibility":"易分散"
    },
    "en": {
        "ptfe_alternative": "PTFE Alt.",
        "scratch_resistance": "Scratch Res.",
        "abrasion_resistance": "Abrasion Res.",
        "burnish_resistance": "Burnish Res.",
        "rub_resistance": "Rub Res.",
        "slip_lubricity": "Slip / Lubricity",
        "slip": "Slip",
        "anti_slip": "Anti-Slip",
        "increased_cof": "High COF",
        "matting_gloss_control": "Matting / Gloss",
        "gloss_retention": "Gloss Retention",
        "clarity": "High Clarity",
        "soft_touch": "Soft Touch",
        "texture_structure": "Texture / Structure",
        "corrosion_resistance": "Corrosion Res.",
        "block_resistance": "Block Res.",
        "improved_extrusion_flow": "Extrusion Flow",
        "anti_gassing": "Anti-Gassing",
        "metal_mark_resistance": "Metal Mark Res.",
        "apparent_hardness": "Apparent Hardness",
        "water_beading": "Water Beading",
        "water_repellency": "Water Repellency",
        "heat_resistance": "Heat Res.",
        "soil_resistance": "Soil Res.",
        "cleanability": "Cleanability",
        "no_silica_dust": "No Silica Dust",
        "lubricity_smooth_feel": "Lubricity / Smooth Feel",
        "lubricity": "Lubricity",
        "flow_leveling": "Flow & Leveling",
        "recoatability": "Recoatability",
        "weather_resistance": "Weather Res.",
        "chemical_resistance": "Chemical Res.",
        "high_dispersibility":"High dispersibility"
    }
};

const uiText = {
    zh: {
        unselected_path: '未選取分類',
        select_catalog_tips: '請選擇左側目錄',
        no_match_title: '查無符合條件之產品',
        no_match_sub: '請嘗試清除篩選條件',
        btn_clear_filters: '清除篩選',
        cat_all: '全系列產品',
        official_doc: 'TDS',
        tech_data: '技術資料',
        density: '密度',
        max_size: '最大粒徑 D100',
        mean_size: '平均粒徑 D50',
        suggested_use_level_title: '建議添加量',
        system_type_title: '推薦系統',
        app_fields_title: '應用行業',
        example: '實際案例應用',
        unspecified_tag: '未指定細分標籤',
        perf_descriptions: '核心性能與特點描述 (Performance Descriptions)',
        no_specific_desc: '尚無詳細描述',
        compare: '比較',
        compared: '已加入',
        max_compare_limit: '最多僅能同時比較 4 個產品',
        compare_dock_title: '產品規格對比',
        compare_dock_sub: '最多可選擇 4 款產品進行規格比對',
        btn_start_compare: '開始比較',
        btn_clear_compare: '清空',
        compare_empty_slot: '+ 選擇產品',
        compare_modal_title: '產品規格比較表',
        compare_modal_sub: '橫向並列對比所選產品之物理特性、體系相容性與性能指標',
        compare_mode_label: '比較模式：',
        filter_all_valid: '全部規格',
        filter_diff: '標示差異',
        compare_filter_info_all: '顯示所選產品之完整規格對比',
        compare_filter_info_diff: '已標示所選產品數值或評分不同之項目',
        spec_attribute: '產品規格與性能項目',
        sec_basic_info: '基本資料與成分',
        sec_physical_props: '典型物理特性',
        sec_applications: '適用體系與應用領域',
        spec_perf_ratings: '核心性能評分',
        spec_perf_desc: '性能特點詳細說明',
        spec_actions: '文件與索樣諮詢',
        spec_comp: '主要化學成分',
        spec_melt_point: '熔點 (°C)',
        spec_mean_size: '平均粒徑 D50 (µm)',
        spec_max_size: '最大粒徑 D100 (µm)',
        spec_density: '密度 (g/cm³)',
        spec_sys_type: '推薦適用體系',
        spec_app_fields: '主要應用領域',
        spec_use_level: '建議添加量',
        btn_req_sample: '索樣 / 詢價',
        btn_remove_compare: '移除',
        no_compare_items: '目前尚未選取比較產品',
        sample_prefill_msg: '已將產品「{name}」帶入索樣諮詢欄位',
        rating_guide_text: '評分提示：+++ 卓越　++ 良好　+ 有效',
        global_search_results: '全域搜尋結果：'
    },
    en: {
        unselected_path: 'No Category Selected',
        select_catalog_tips: 'Please select a catalog from left menu',
        no_match_title: 'No Products Found',
        no_match_sub: 'Try clearing your search query',
        btn_clear_filters: 'Clear Filters',
        cat_all: 'All Products',
        official_doc: 'TDS',
        tech_data: 'Tech Data',
        density: 'Density',
        max_size: 'Max Size D100',
        mean_size: 'Mean Size D50',
        suggested_use_level_title: 'Suggested Use Level',
        system_type_title: 'Recommended System',
        app_fields_title: 'Application Fields',
        example: 'Application Examples',
        unspecified_tag: 'Unspecified Tags',
        perf_descriptions: 'Performance Descriptions',
        no_specific_desc: 'No specific description available',
        compare: 'Compare',
        compared: 'Added',
        max_compare_limit: 'Maximum 4 products can be compared at once',
        compare_dock_title: 'Product Comparison',
        compare_dock_sub: 'Select up to 4 products to compare specifications',
        btn_start_compare: 'Compare Now',
        btn_clear_compare: 'Clear All',
        compare_empty_slot: '+ Add Product',
        compare_modal_title: 'Product Comparison Matrix',
        compare_modal_sub: 'Side-by-side comparison of specifications, systems and performance ratings',
        compare_mode_label: 'Compare Mode:',
        filter_all_valid: 'All Specs',
        filter_diff: 'Highlight Diff',
        compare_filter_info_all: 'Showing complete specifications for selected products',
        compare_filter_info_diff: 'Highlighting attributes with differing values or ratings',
        spec_attribute: 'Specifications & Features',
        sec_basic_info: 'Basic Info & Chemistry',
        sec_physical_props: 'Physical Properties',
        sec_applications: 'Systems & Applications',
        spec_perf_ratings: 'Performance Ratings',
        spec_perf_desc: 'Performance Descriptions',
        spec_actions: 'Docs & Inquiries',
        spec_comp: 'Chemical Composition',
        spec_melt_point: 'Melt Point (°C)',
        spec_mean_size: 'Mean Size D50 (µm)',
        spec_max_size: 'Max Size D100 (µm)',
        spec_density: 'Density (g/cm³)',
        spec_sys_type: 'Recommended Systems',
        spec_app_fields: 'Application Fields',
        spec_use_level: 'Suggested Use Level',
        btn_req_sample: 'Request Sample',
        btn_remove_compare: 'Remove',
        no_compare_items: 'No products selected for comparison',
        sample_prefill_msg: 'Added "{name}" to sample request form',
        rating_guide_text: 'Rating Guide: +++ Outstanding  ++ Recommended  + Effective',
        global_search_results: 'Global Search Results: '
    }
};

const AppState = {
    lang: 'zh',
    partner: 'MPI',
    productLine: null,
    category: 'all',
    filters: {},
    expandedDetails: [],
    expandedMenus: [],
    configs: {},
    allProductsCache: {},
    allLoaded: false,
    searchQuery: '',
    sortColumn: null,
    sortOrder: 'desc',
    compareList: [],
    selectedProduct: null,

    set(key, value) {
        if (this[key] === value) return;
        this[key] = value;
        this.notify(key);
        if (typeof updateHashRoute === 'function') {
            updateHashRoute(key === 'partner');
        }
    },

    notify(key) {
        if (key === 'partner') {
            if (typeof updatePartnerUI === 'function') updatePartnerUI();
        } else if (key === 'lang') {
            if (typeof updateLanguageUI === 'function') updateLanguageUI();
        }
    }
};

function getAppSpecificData(p, lineKey = AppState.productLine) {
    if (p && p.applications_data) {
        if (lineKey && p.applications_data[lineKey]) {
            return p.applications_data[lineKey];
        }
        if (partnerConfigMap[AppState.partner] === 'mpi' && p.applications_data[AppState.productLine]) {
            return p.applications_data[AppState.productLine];
        }
        const keys = Object.keys(p.applications_data);
        if (keys.length > 0) return p.applications_data[keys[0]];
    }
    return p || {};
}

function hasValidValue(val) {
    return val !== null && val !== undefined && val !== '' && val !== '—' && val !== 'N/A';
}

function isCurrentCategoryKey(key, category, productLine) {
    const cat = (category || '').toLowerCase();
    const pLine = (productLine || '').toLowerCase();

    if ((cat.includes('ptfe') || pLine === 'ptfe') && key === 'ptfe_alternative') return true;
    if ((cat === '耐刮' || cat.includes('scratch')) && key === 'scratch_resistance') return true;
    if ((cat === '耐磨' || cat.includes('abrasion')) && key === 'abrasion_resistance') return true;
    if ((cat === '消光' || cat.includes('matting')) && key === 'matting_gloss_control') return true;
    if ((cat === '織紋' || cat.includes('texture')) && key === 'texture_structure') return true;
    if ((cat === '柔感' || cat.includes('soft')) && key === 'soft_touch') return true;
    if ((cat === '防滑' || cat.includes('anti-slip')) && key === 'anti_slip') return true;
    if ((cat === '滑爽' || cat.includes('slip')) && key === 'slip_lubricity') return true;
    if ((cat === '撥水' || cat.includes('water_repellency')) && key === 'water_repellency') return true;
    if ((cat === '耐高溫' || cat.includes('heat')) && key === 'heat_resistance') return true;
    if ((cat === '防腐蝕' || cat.includes('corrosion')) && key === 'corrosion_resistance') return true;
    if ((cat === '撥水' || cat.includes('water_beading')) && key === 'water_beading') return true;

    return false;
}
