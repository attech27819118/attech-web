const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const mpiDir = path.join(rootDir, 'json', 'mpi');
const tdsDir = path.join(rootDir, 'tds');
const coatingsDir = path.join(rootDir, 'coatingsdata');

const tdsFiles = fs.readdirSync(tdsDir);
const coatingsFiles = fs.readdirSync(coatingsDir);

const mpiFiles = fs.readdirSync(mpiDir).filter(f => f.endsWith('.json'));

let productsMap = new Map();

for (const mf of mpiFiles) {
    const data = JSON.parse(fs.readFileSync(path.join(mpiDir, mf), 'utf8'));
    const items = Array.isArray(data) ? data : (data.products || data.data || []);
    for (const p of items) {
        if (!p.product_name) continue;
        if (!productsMap.has(p.product_name)) {
            productsMap.set(p.product_name, {
                product_name: p.product_name,
                foundInFiles: [],
                website: p.website,
                tech_data_url: p.tech_data_url,
            });
        }
        const entry = productsMap.get(p.product_name);
        entry.foundInFiles.push(mf);
        if (p.website) entry.website = p.website;
        if (p.tech_data_url) entry.tech_data_url = p.tech_data_url;
    }
}

console.log(`Unique MPI products found: ${productsMap.size}`);

const results = [];

for (const [name, info] of productsMap.entries()) {
    const expectedTds = `${name} TDS.pdf`;
    const expectedData = `${name} data.pdf`;

    const tdsExact = tdsFiles.includes(expectedTds);
    const tdsCaseInsensitive = tdsFiles.find(f => f.toLowerCase() === expectedTds.toLowerCase());

    const dataExact = coatingsFiles.includes(expectedData);
    const dataCaseInsensitive = coatingsFiles.find(f => f.toLowerCase() === expectedData.toLowerCase());

    results.push({
        product: name,
        files: info.foundInFiles,
        hasWebsite: !!(info.website && info.website !== 'N/A'),
        websiteVal: info.website,
        tdsExact,
        tdsCaseInsensitive: tdsCaseInsensitive || null,
        hasTechData: !!(info.tech_data_url && info.tech_data_url !== 'N/A'),
        techDataVal: info.tech_data_url,
        dataExact,
        dataCaseInsensitive: dataCaseInsensitive || null,
    });
}

console.log('=== PRODUCTS WITH TDS ISSUES ===');
const tdsIssues = results.filter(r => r.hasWebsite && !r.tdsExact);
console.log(JSON.stringify(tdsIssues, null, 2));

console.log('=== PRODUCTS WITH DATA ISSUES ===');
const dataIssues = results.filter(r => r.hasTechData && !r.dataExact);
console.log(JSON.stringify(dataIssues, null, 2));

console.log('=== PHYSICAL TDS FILES WITHOUT MATCHING PRODUCT IN JSON ===');
const allExpectedTds = results.map(r => `${r.product} TDS.pdf`);
const unreferencedTds = tdsFiles.filter(f => !allExpectedTds.includes(f));
console.log(unreferencedTds);

console.log('=== PHYSICAL DATA FILES WITHOUT MATCHING PRODUCT IN JSON ===');
const allExpectedData = results.map(r => `${r.product} data.pdf`);
const unreferencedData = coatingsFiles.filter(f => !allExpectedData.includes(f));
console.log(unreferencedData);
