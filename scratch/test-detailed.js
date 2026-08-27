const https = require('https');

const detailedPayload = JSON.stringify({
    type: '詳細需求',
    company: '宏威詳細需求測試公司',
    contact: '李工程師',
    email: 'atservice@attech.com.tw',
    mobile: '0912-345-678',
    phone: '04-2239-8056',
    fax: '04-2239-8057',
    address: '台中市北屯區廍子巷116號',
    appFields: ['車用電子', '航太工業'],
    functions: ['耐高溫', '絕緣耐壓'],
    otherFunc: '無',
    systems: ['溶劑型'],
    compType: '單液型',
    appType: '透明液體',
    substrates: ['鋁合金', '不鏽鋼'],
    otherSubstrate: '無',
    filmThick: '25',
    noBake: '否',
    bakeTemp: '150°C',
    bakeTime: '30分鐘',
    resins: ['環氧樹脂 Epoxy'],
    restricted: 'RoHS 2.0 合規',
    sampleReq: 'MPI-500 x 500g',
    docs: ['TDS', 'SDS', 'COA'],
    pastSamples: '曾試過他牌但耐熱性不足',
    remarks: '急需樣品評估耐溫性'
});

const options = {
    hostname: 'uib4yezvl3.execute-api.us-east-1.amazonaws.com',
    port: 443,
    path: '/default/attech-send-email',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(detailedPayload)
    }
};

const req = https.request(options, (res) => {
    let body = '';
    res.on('data', (d) => body += d);
    res.on('end', () => {
        console.log('Status:', res.statusCode);
        console.log('Response:', body);
    });
});

req.on('error', (e) => console.error('Request error:', e));
req.write(detailedPayload);
req.end();
