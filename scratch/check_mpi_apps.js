const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const mpiAppDir = path.join(rootDir, 'MPI applications');
const tdsDir = path.join(rootDir, 'tds');
const coatingsDir = path.join(rootDir, 'coatingsdata');

function scanDir(dir) {
    let files = [];
    if (!fs.existsSync(dir)) return files;
    for (const f of fs.readdirSync(dir)) {
        const full = path.join(dir, f);
        if (fs.statSync(full).isDirectory()) files.push(...scanDir(full));
        else if (f.endsWith('.pdf') || f.endsWith('.pptx')) files.push({ name: f, fullPath: full, size: fs.statSync(full).size });
    }
    return files;
}

const allMpiAppFiles = scanDir(mpiAppDir);
const tdsFiles = fs.readdirSync(tdsDir);
const coatingsFiles = fs.readdirSync(coatingsDir);

console.log(`Found ${allMpiAppFiles.length} files in MPI applications/`);

const missingInTds = [];
for (const f of allMpiAppFiles) {
    if (f.name.endsWith('.pdf')) {
        if (!tdsFiles.includes(f.name) && !coatingsFiles.includes(f.name)) {
            missingInTds.push(f);
        }
    }
}

console.log('\n=== Files in MPI applications/ that are NOT in ./tds/ or ./coatingsdata/ ===');
console.log(missingInTds);
