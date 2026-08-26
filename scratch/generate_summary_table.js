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

console.log(`| # | Product Name | Has Website (TDS) | TDS File in ./tds/ | Has Tech Data | Tech Data in ./coatingsdata/ | Status |`);
console.log(`|---|---|---|---|---|---|---|`);

let i = 1;
for (const [name, info] of Array.from(productsMap.entries()).sort((a,b) => a[0].localeCompare(b[0]))) {
    const expectedTds = `${name} TDS.pdf`;
    const expectedData = `${name} data.pdf`;

    const tdsExact = tdsFiles.includes(expectedTds);
    const tdsCase = tdsFiles.find(f => f.toLowerCase() === expectedTds.toLowerCase());

    const dataExact = coatingsFiles.includes(expectedData);
    const dataCase = coatingsFiles.find(f => f.toLowerCase() === expectedData.toLowerCase());

    let tdsStatus = 'None';
    if (info.website && info.website !== 'N/A') {
        if (tdsExact) tdsStatus = 'OK (Exact)';
        else if (tdsCase) tdsStatus = `Case mismatch (${tdsCase})`;
        else tdsStatus = 'MISSING (404)';
    }

    let dataStatus = 'None';
    if (info.tech_data_url && info.tech_data_url !== 'N/A') {
        if (dataExact) dataStatus = 'OK (Exact)';
        else if (dataCase) dataStatus = `Case mismatch (${dataCase})`;
        else dataStatus = 'MISSING (404)';
    }

    let overall = 'Normal';
    if (tdsStatus.includes('MISSING') || tdsStatus.includes('mismatch') || dataStatus.includes('MISSING') || dataStatus.includes('mismatch')) {
        overall = 'ISSUE';
    }

    console.log(`| ${i++} | ${name} | ${info.website ? 'Yes' : 'No'} | ${tdsStatus} | ${info.tech_data_url ? 'Yes' : 'No'} | ${dataStatus} | ${overall} |`);
}
