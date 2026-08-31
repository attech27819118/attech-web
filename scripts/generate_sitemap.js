const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://www.attech.com.tw';
const TODAY = new Date().toISOString().split('T')[0]; // e.g. '2026-08-31'

const rootDir = path.resolve(__dirname, '..');
const configPath = path.join(rootDir, 'config.json');
const sitemapPath = path.join(rootDir, 'sitemap.xml');

if (!fs.existsSync(configPath)) {
    console.error('config.json not found!');
    process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Helper to escape XML
function escapeXml(unsafe) {
    return unsafe.replace(/[<>&'"]/g, c => {
        switch (c) {
            case '<': return '&lt;';
            case '>': return '&gt;';
            case '&': return '&amp;';
            case '\'': return '&apos;';
            case '"': return '&quot;';
        }
    });
}

function formatUrlEntry(loc, lastmod = TODAY, changefreq = 'weekly', priority = '0.8') {
    const safeLoc = escapeXml(loc);
    return `    <url>
        <loc>${safeLoc}</loc>
        <lastmod>${lastmod}</lastmod>
        <changefreq>${changefreq}</changefreq>
        <priority>${priority}</priority>
    </url>`;
}

const urlEntries = [];
const seenUrls = new Set();

function addUrl(loc, changefreq = 'weekly', priority = '0.8') {
    if (seenUrls.has(loc)) return;
    seenUrls.add(loc);
    urlEntries.push(formatUrlEntry(loc, TODAY, changefreq, priority));
}

// 1. Core Static Pages
addUrl(`${DOMAIN}/`, 'daily', '1.0');
addUrl(`${DOMAIN}/about`, 'weekly', '0.9');
addUrl(`${DOMAIN}/products`, 'daily', '0.95');
addUrl(`${DOMAIN}/partners`, 'monthly', '0.8');
addUrl(`${DOMAIN}/contact`, 'monthly', '0.9');

// 2. Partner Brand and Product Line Pages
for (const [brandKey, brandObj] of Object.entries(config)) {
    const partnerSlug = brandKey.toLowerCase();
    
    // Add partner main page
    addUrl(`${DOMAIN}/products/${partnerSlug}`, 'weekly', '0.9');

    if (brandObj.masterPath) {
        const masterFilePath = path.join(rootDir, brandObj.masterPath.replace(/^\.?\//, ''));
        if (fs.existsSync(masterFilePath)) {
            const masterData = JSON.parse(fs.readFileSync(masterFilePath, 'utf8'));
            for (const file of brandObj.files) {
                const lineSlug = file.key;
                const lineUrl = `${DOMAIN}/products/${partnerSlug}/${lineSlug}`;
                addUrl(lineUrl, 'weekly', '0.85');

                const products = masterData.filter(p => p.applications_data && p.applications_data[lineSlug]);
                for (const p of products) {
                    const pName = p.product_name || p.name;
                    if (pName) {
                        const productUrl = `${DOMAIN}/products/${partnerSlug}/${lineSlug}/${encodeURIComponent(pName.trim())}`;
                        addUrl(productUrl, 'weekly', '0.8');
                    }
                }
            }
        }
    } else {
        for (const file of brandObj.files) {
            const lineSlug = file.key;
            const lineUrl = `${DOMAIN}/products/${partnerSlug}/${lineSlug}`;
            addUrl(lineUrl, 'weekly', '0.85');

            if (file.jsonPath) {
                const jsonFilePath = path.join(rootDir, file.jsonPath.replace(/^\.?\//, ''));
                if (fs.existsSync(jsonFilePath)) {
                    try {
                        const data = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
                        const items = Array.isArray(data) ? data : (data.products || []);
                        
                        for (const p of items) {
                            const pName = p.product_name || p.name;
                            if (pName) {
                                const productUrl = `${DOMAIN}/products/${partnerSlug}/${lineSlug}/${encodeURIComponent(pName.trim())}`;
                                addUrl(productUrl, 'weekly', '0.8');
                            }
                        }
                    } catch (err) {
                        console.error(`Error reading ${jsonFilePath}:`, err.message);
                    }
                } else {
                    console.warn(`File not found: ${jsonFilePath}`);
                }
            }
        }
    }
}

const xmlOutput = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

${urlEntries.join('\n')}

</urlset>
`;

fs.writeFileSync(sitemapPath, xmlOutput, 'utf8');

console.log(`Successfully generated sitemap.xml!`);
console.log(`Total URLs: ${urlEntries.length}`);
console.log(`Saved to: ${sitemapPath}`);
