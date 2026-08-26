const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const jsonDir = path.join(rootDir, 'json');

function scanDir(dir) {
    let files = [];
    for (const f of fs.readdirSync(dir)) {
        const full = path.join(dir, f);
        if (fs.statSync(full).isDirectory()) files.push(...scanDir(full));
        else if (f.endsWith('.json')) files.push(full);
    }
    return files;
}

const allJson = scanDir(jsonDir);

console.log('=== Checking Fields across all JSONs ===');
for (const jf of allJson) {
    const rel = path.relative(rootDir, jf);
    const content = JSON.parse(fs.readFileSync(jf, 'utf8'));
    const items = Array.isArray(content) ? content : (content.products || content.data || []);
    
    let withWebsite = 0;
    let withTechData = 0;
    let withPdfField = 0;
    let total = items.length;
    let sampleKeys = new Set();

    items.forEach(p => {
        Object.keys(p).forEach(k => sampleKeys.add(k));
        if (p.website && p.website !== 'N/A' && p.website !== '') withWebsite++;
        if (p.tech_data_url && p.tech_data_url !== 'N/A' && p.tech_data_url !== '') withTechData++;
        if (p.pdf || p.tds || p.document) withPdfField++;
    });

    console.log(`${rel} (${total} items):`);
    console.log(`  website: ${withWebsite}, tech_data_url: ${withTechData}, other doc fields: ${withPdfField}`);
}
