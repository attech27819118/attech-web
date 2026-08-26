const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');

// 1. Read files in tds/ and coatingsdata/
const tdsDir = path.join(rootDir, 'tds');
const coatingsdataDir = path.join(rootDir, 'coatingsdata');

const tdsFiles = fs.existsSync(tdsDir) ? fs.readdirSync(tdsDir) : [];
const coatingsFiles = fs.existsSync(coatingsdataDir) ? fs.readdirSync(coatingsdataDir) : [];

console.log('=== Physical PDF files ===');
console.log(`tds/ count: ${tdsFiles.length}`);
console.log(`coatingsdata/ count: ${coatingsFiles.length}`);

// 2. Read all JSON files
function getJsonFiles(dir) {
    let results = [];
    if (!fs.existsSync(dir)) return results;
    const list = fs.readdirSync(dir);
    for (const file of list) {
        const full = path.join(dir, file);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
            results = results.concat(getJsonFiles(full));
        } else if (file.endsWith('.json')) {
            results.push(full);
        }
    }
    return results;
}

const jsonFiles = getJsonFiles(path.join(rootDir, 'json'));

console.log('\n=== Scanning all JSON files for products and checking PDF matches ===');

let totalProducts = 0;
let productsWithTdsBtn = 0;
let productsWithDataBtn = 0;
let missingTdsFiles = [];
let missingDataFiles = [];
let matchedTdsFiles = [];
let matchedDataFiles = [];

for (const jf of jsonFiles) {
    const relPath = path.relative(rootDir, jf);
    try {
        const content = JSON.parse(fs.readFileSync(jf, 'utf8'));
        let products = [];
        if (Array.isArray(content)) {
            products = content;
        } else if (content.products && Array.isArray(content.products)) {
            products = content.products;
        } else if (content.data && Array.isArray(content.data)) {
            products = content.data;
        }

        for (const p of products) {
            if (!p.product_name) continue;
            totalProducts++;

            const hasWebsite = p.website && p.website !== 'N/A';
            const hasTechData = p.tech_data_url && p.tech_data_url !== 'N/A';

            // Check TDS file
            // router.js expects: `./tds/${productName} TDS.pdf`
            const expectedTdsName = `${p.product_name} TDS.pdf`;
            const tdsExists = tdsFiles.includes(expectedTdsName);

            // Check Data file
            // router.js expects: `./coatingsdata/${productName} data.pdf`
            const expectedDataName = `${p.product_name} data.pdf`;
            const dataExists = coatingsFiles.includes(expectedDataName);

            if (hasWebsite) {
                productsWithTdsBtn++;
                if (tdsExists) {
                    matchedTdsFiles.push({ file: relPath, product: p.product_name, expected: expectedTdsName, website: p.website });
                } else {
                    // Check if there is a case mismatch or slightly different name
                    const similar = tdsFiles.filter(f => f.toLowerCase().includes(p.product_name.toLowerCase()) || p.product_name.toLowerCase().includes(f.toLowerCase().replace(' tds.pdf', '')));
                    missingTdsFiles.push({ file: relPath, product: p.product_name, expected: expectedTdsName, website: p.website, similar });
                }
            }

            if (hasTechData) {
                productsWithDataBtn++;
                if (dataExists) {
                    matchedDataFiles.push({ file: relPath, product: p.product_name, expected: expectedDataName });
                } else {
                    const similar = coatingsFiles.filter(f => f.toLowerCase().includes(p.product_name.toLowerCase()) || p.product_name.toLowerCase().includes(f.toLowerCase().replace(' data.pdf', '')));
                    missingDataFiles.push({ file: relPath, product: p.product_name, expected: expectedDataName, tech_data_url: p.tech_data_url, similar });
                }
            }
        }
    } catch (e) {
        console.error(`Error reading ${relPath}:`, e.message);
    }
}

console.log(`Total Products scanned: ${totalProducts}`);
console.log(`Products with website (TDS button): ${productsWithTdsBtn}`);
console.log(`  -> Matched physical TDS files: ${matchedTdsFiles.length}`);
console.log(`  -> MISSING physical TDS files: ${missingTdsFiles.length}`);
console.log(`Products with tech_data_url (Data button): ${productsWithDataBtn}`);
console.log(`  -> Matched physical Data files: ${matchedDataFiles.length}`);
console.log(`  -> MISSING physical Data files: ${missingDataFiles.length}`);

if (missingTdsFiles.length > 0) {
    console.log('\n--- Missing TDS files (Detail) ---');
    console.log(JSON.stringify(missingTdsFiles, null, 2));
}

if (missingDataFiles.length > 0) {
    console.log('\n--- Missing Data files (Detail) ---');
    console.log(JSON.stringify(missingDataFiles, null, 2));
}

// Check if any TDS files on disk are unused
console.log('\n--- Unused TDS files in ./tds/ ---');
const usedTds = new Set(matchedTdsFiles.map(m => m.expected));
const unusedTds = tdsFiles.filter(f => !usedTds.has(f));
console.log(unusedTds);

console.log('\n--- Unused Data files in ./coatingsdata/ ---');
const usedData = new Set(matchedDataFiles.map(m => m.expected));
const unusedData = coatingsFiles.filter(f => !usedData.has(f));
console.log(unusedData);
