const fs = require('fs');
const vm = require('vm');

console.log('====================================================');
console.log('🧪 正在執行語言切換關閉與搜尋詳細資訊導向測試...');
console.log('====================================================');

// 1. Verify index.html does not contain language switcher
const indexHTML = fs.readFileSync('index.html', 'utf8');
if (indexHTML.includes('id="lang-zh-btn"') || indexHTML.includes('id="lang-en-btn"')) {
    throw new Error('❌ index.html 仍包含語言切換按鈕');
}
console.log('✅ 1. index.html 中英文切換按鈕已成功移除');

// 2. Setup mock DOM & Browser global environment
let scrollIntoViewCalled = false;
let scrollToCalled = false;
let scrollY = 0;

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
                    classes: [],
                    add: function(...classes) { this.classes = this.classes || []; this.classes.push(...classes); },
                    remove: function(...classes) { this.classes = (this.classes || []).filter(c => !classes.includes(c)); },
                    contains: function(c) { return (this.classes || []).includes(c); },
                    replace: function(o, n) { this.remove(o); this.add(n); }
                },
                setAttribute: function(k, v) { this[k] = v; },
                getAttribute: function(k) { return this[k] || null; },
                addEventListener: () => {},
                appendChild: () => {},
                querySelector: () => null,
                querySelectorAll: () => [],
                closest: () => ({ scrollLeft: 0, scrollTo: () => {} }),
                scrollIntoView: () => { scrollIntoViewCalled = true; },
                getBoundingClientRect: () => ({ top: 300, bottom: 350, left: 0, right: 800, width: 800, height: 50 })
            };
        }
        return this.elements[id];
    },
    createElement(tag) {
        return {
            tagName: tag.toUpperCase(),
            className: '',
            innerHTML: '',
            appendChild: () => {},
            setAttribute: () => {},
            getAttribute: () => null
        };
    },
    querySelectorAll(selector) {
        if (selector === 'tr[data-product-name]') {
            return this.productRows || [];
        }
        return [];
    },
    querySelector() { return null; },
    addEventListener() {}
};

global.document = mockDOM;
global.window = {
    location: { hash: '', hostname: 'localhost' },
    addEventListener: () => {},
    scrollTo: (opts) => { scrollToCalled = true; scrollY = opts?.top || 0; },
    pageYOffset: 100,
    innerWidth: 1200,
    requestAnimationFrame: (cb) => cb(),
    setTimeout: (cb, ms) => cb()
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

modules.forEach(modPath => {
    const code = fs.readFileSync(modPath, 'utf8');
    vm.runInThisContext(code, { filename: modPath });
});

// Load config
const configs = JSON.parse(fs.readFileSync('config.json', 'utf8'));
AppState.configs = configs;

// Load all products cache
const mpiMaster = JSON.parse(fs.readFileSync('json/mpi/master_database_clear.json', 'utf8'));
AppState.allProductsCache['mpi_master'] = mpiMaster;
configs.mpi.files.forEach(file => {
    AppState.allProductsCache[file.key] = mpiMaster.filter(p => p.applications_data && p.applications_data[file.key]);
});

for (const [brandKey, brand] of Object.entries(configs)) {
    if (brandKey === 'mpi') continue;
    for (const file of brand.files) {
        if (file.jsonPath && fs.existsSync(file.jsonPath)) {
            AppState.allProductsCache[file.key] = JSON.parse(fs.readFileSync(file.jsonPath, 'utf8'));
        }
    }
}

console.log('\n[測試 2: 搜尋與詳細資訊引導至大表]');

// Test searching Tyzor and navigating to Tyzor 436
const testProducts = [
    { brand: 'DorfKetal', line: 'tyzor', name: 'Tyzor 436' },
    { brand: 'MPI', line: 'ptfe', name: 'MP-28AL' },
    { brand: 'Orion', line: 'coating', name: 'PRINTEX® 95' },
    { brand: 'Others', line: 'matting_agent', name: 'Acematt OK 412' }
];

(async () => {
    for (const item of testProducts) {
        scrollIntoViewCalled = false;
        scrollToCalled = false;

        // Simulate search
        AppState.searchQuery = item.name.split(' ')[0];

        // Mock product rows for table
        const productsInLine = AppState.allProductsCache[item.line] || [];

        mockDOM.productRows = productsInLine.map((p, idx) => {
            const safeName = (p.product_name || '').replace(/"/g, '&quot;');
            const el = mockDOM.getElementById(`mock-row-${idx}`);
            el.setAttribute('data-product-name', safeName);
            el.setAttribute('data-index', String(idx));
            el.scrollIntoView = () => { scrollIntoViewCalled = true; };
            return el;
        });

        navigateToCategory(item.brand, item.line, 'all', item.name);

        // Wait for Promise.then and setTimeout
        await new Promise(r => setTimeout(r, 300));

        if (AppState.partner === item.brand && AppState.productLine === item.line) {
            console.log(`✅ 成功導向至 ${item.brand} -> ${item.line} (產品: ${item.name})`);
        } else {
            throw new Error(`❌ 導向失敗: ${item.brand} -> ${item.line}`);
        }

        if (scrollIntoViewCalled || scrollToCalled) {
            console.log(`✅ 成功觸發產品列捲動置中 (${item.name})`);
        } else {
            throw new Error(`❌ 未觸發產品列捲動: ${item.name}`);
        }
    }

    console.log('\n====================================================');
    console.log('🎉 所有測試全部通過！');
    console.log('====================================================');
})();
