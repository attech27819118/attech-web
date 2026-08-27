const fs = require('fs');
const cfg = JSON.parse(fs.readFileSync('config.json', 'utf8'));
let mismatches = 0;
const normalize = s => (s || '').trim().replace(/[\r\n\s]+/g, ' ').toLowerCase();

for (const [k, brand] of Object.entries(cfg)) {
    for (const f of brand.files) {
        const filePath = k === 'mpi' ? 'json/mpi/master_database_clear.json' : f.jsonPath;
        if (filePath && fs.existsSync(filePath)) {
            const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            for (const p of data) {
                const rawName = p.product_name || '—';
                const safeProductName = (p.product_name || '').replace(/"/g, '&quot;');
                if (normalize(rawName) !== normalize(safeProductName) && rawName !== safeProductName) {
                    console.log('Mismatch:', rawName, 'vs', safeProductName);
                    mismatches++;
                }
            }
        }
    }
}
console.log('Total mismatches:', mismatches);
