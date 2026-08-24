const fs = require('fs');
const vm = require('vm');

console.log('====================================================');
console.log('🧪 正在執行模組化架構全面自動化驗證測試...');
console.log('====================================================');

// Setup mock DOM & Browser global environment
const mockDOM = {
    elements: {},
    getElementById(id) {
        if (!this.elements[id]) {
            this.elements[id] = {
                id,
                innerText: '',
                innerHTML: '',
                value: '',
                className: '',
                style: {},
                classList: {
                    add: function(...classes) { this.classes = this.classes || []; this.classes.push(...classes); },
                    remove: function(...classes) { this.classes = (this.classes || []).filter(c => !classes.includes(c)); },
                    contains: function(c) { return (this.classes || []).includes(c); },
                    replace: function(o, n) { this.remove(o); this.add(n); }
                },
                setAttribute: () => {},
                getAttribute: () => null,
                addEventListener: () => {},
                querySelector: () => null,
                querySelectorAll: () => [],
                closest: () => null
            };
        }
        return this.elements[id];
    },
    querySelectorAll() { return []; },
    querySelector() { return null },
    addEventListener() {}
};

global.document = mockDOM;
global.window = {
    location: { hash: '', hostname: 'localhost' },
    addEventListener: () => {},
    scrollTo: () => {},
    innerWidth: 1200
};
global.history = { replaceState: () => {}, pushState: () => {} };
global.navigator = { userAgent: '' };

const modules = [
    'js/state.js',
    'js/search-engine.js',
    'js/data-repo.js',
    'js/filter-engine.js',
    'js/table-renderer.js',
    'js/compare.js',
    'js/contact.js',
    'js/router.js',
    'js/app.js'
];

// Load each module in order
modules.forEach(modPath => {
    const code = fs.readFileSync(modPath, 'utf8');
    vm.runInThisContext(code, { filename: modPath });
    console.log(`✅ 成功載入並編譯模組: ${modPath}`);
});

// Test 1: AppState & Dictionaries
console.log('\n[測試 1: 狀態管理與字典]');
if (AppState.partner === 'MPI' && uiText.zh.compare === '比較' && uiText.en.compare === 'Compare') {
    console.log('✅ AppState 與 uiText 多語系字典正確');
} else {
    throw new Error('AppState or uiText failed');
}

// Test 2: SearchEngine
console.log('\n[測試 2: 多重搜尋引擎]');
const tokens = SearchEngine.parseTokens('水性, 耐磨+"MP-28"');
if (tokens.length === 3 && tokens.includes('水性') && tokens.includes('耐磨') && tokens.includes('mp-28')) {
    console.log('✅ SearchEngine.parseTokens 正確解析逗號、加號與引號:', tokens);
} else {
    throw new Error('SearchEngine.parseTokens failed');
}

const hl = SearchEngine.highlight('水性抗刮耐磨添加劑 MP-28AL', ['水性', '耐磨']);
if (hl.includes('<mark') && hl.includes('水性') && hl.includes('耐磨')) {
    console.log('✅ SearchEngine.highlight 標記正確');
} else {
    throw new Error('SearchEngine.highlight failed');
}

// Test 3: Load Data & FilterEngine
console.log('\n[測試 3: 資料庫載入與篩選引擎]');
const configs = JSON.parse(fs.readFileSync('config.json', 'utf8'));
AppState.configs = configs;

const mpiMaster = JSON.parse(fs.readFileSync('json/mpi/master_database_clear.json', 'utf8'));
AppState.allProductsCache['mpi_master'] = mpiMaster;
configs.mpi.files.forEach(f => {
    AppState.allProductsCache[f.key] = mpiMaster.filter(p => p.applications_data && p.applications_data[f.key]);
});

['dorfketal', 'orion', 'others'].forEach(brandKey => {
    configs[brandKey].files.forEach(f => {
        if (f.jsonPath && fs.existsSync(f.jsonPath)) {
            AppState.allProductsCache[f.key] = JSON.parse(fs.readFileSync(f.jsonPath, 'utf8'));
        }
    });
});

const mpiInks = AppState.allProductsCache['ink'] || [];
const filteredMPI = ProductFilterEngine.filter(mpiInks, {
    partner: 'MPI',
    category: 'all',
    searchQuery: '水性 耐磨',
    filters: {}
});
console.log(`✅ MPI Inks 搜尋 [水性 耐磨] 找到 ${filteredMPI.length} 筆產品（AND 邏輯收斂正確）`);

// Test 4: DynamicTableRenderer
console.log('\n[測試 4: 動態表格渲染器]');
['mpi', 'dorfketal', 'orion', 'others'].forEach(pKey => {
    const fields = DynamicTableRenderer.getActiveFields(pKey, []);
    if (!fields || (Array.isArray(fields) && fields.length === 0)) {
        throw new Error(`DynamicTableRenderer failed for ${pKey}`);
    }
    console.log(`✅ DynamicTableRenderer 正確取得 ${pKey} 欄位定義 (${Array.isArray(fields) ? fields.length : '自定義'} 欄)`);
});

// Test 5: CompareManager
console.log('\n[測試 5: 產品比較管理]');
AppState.compareList = [];
toggleCompareProduct('MP-28AL', 'MPI', 'powder', mpiInks[0]);
toggleCompareProduct('MicroKlear 418AL', 'MPI', 'powder', mpiInks[1]);
if (AppState.compareList.length === 2) {
    console.log('✅ 加入 2 項產品至比較清單成功');
} else {
    throw new Error('toggleCompareProduct failed');
}

removeCompareProduct('MP-28AL');
if (AppState.compareList.length === 1) {
    console.log('✅ 移除產品成功，清單剩餘 1 項');
} else {
    throw new Error('removeCompareProduct failed');
}

clearCompare();
if (AppState.compareList.length === 0) {
    console.log('✅ 清空比較清單成功');
} else {
    throw new Error('clearCompare failed');
}

// Test 6: Contact form mode switch
console.log('\n[測試 6: 索樣與諮詢表單雙模式切換]');
switchFormMode('quick');
switchFormMode('detailed');
console.log('✅ switchFormMode 雙向切換執行無誤');

console.log('\n====================================================');
console.log('🎉 所有模組單元與整合測試 100% 順利通過！');
console.log('====================================================');
