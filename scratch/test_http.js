const http = require('http');

function checkUrl(url) {
    return new Promise((resolve) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                resolve({
                    status: res.statusCode,
                    headers: res.headers,
                    bodyLength: data.length,
                    hasTyzor: data.includes('id="tech-tyzor"'),
                    hasSilane: data.includes('id="tech-silane"'),
                    hasPolyester: data.includes('id="tech-polyester"'),
                    hasCatalystImg: data.includes('catalyst.webp')
                });
            });
        }).on('error', (err) => resolve({ error: err.message }));
    });
}

async function run() {
    const pageRes = await checkUrl('http://localhost:3000/technology/');
    console.log('GET /technology/:', pageRes);

    const imgRes = await checkUrl('http://localhost:3000/techdata/tyzor/catalyst.webp');
    console.log('GET /techdata/tyzor/catalyst.webp: status =', imgRes.status, 'bytes =', imgRes.headers['content-length']);

    const img2Res = await checkUrl('http://localhost:3000/img/techdata/tyzor/catalyst.webp');
    console.log('GET /img/techdata/tyzor/catalyst.webp: status =', img2Res.status, 'bytes =', img2Res.headers['content-length']);
}

run();
