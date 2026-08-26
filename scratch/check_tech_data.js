const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const jsonDir = path.join(rootDir, 'json', 'mpi');

const files = fs.readdirSync(jsonDir).filter(f => f.endsWith('.json'));

for (const f of files) {
    const data = JSON.parse(fs.readFileSync(path.join(jsonDir, f), 'utf8'));
    const items = Array.isArray(data) ? data : (data.products || data.data || []);
    const withData = items.filter(p => p.tech_data_url && p.tech_data_url !== 'N/A' && p.tech_data_url !== '');
    if (withData.length > 0) {
        console.log(`\nFile: ${f} (${withData.length} items with tech_data_url)`);
        withData.forEach(p => {
            console.log(`  - Product: "${p.product_name}", tech_data_url: "${p.tech_data_url}"`);
        });
    }
}
