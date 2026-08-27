const https = require('https');

const data = JSON.stringify({
    company: '宏威測試公司',
    contact: '陳專員',
    email: 'atservice@attech.com.tw',
    type: '快速詢價',
    mobile: '0912-345-678',
    sample: 'MPI-600 x 1KG',
    address: '台中市北屯區廍子巷116號',
    message: '這是一封來自網頁的測試需求單'
});

const options = {
    hostname: 'uib4yezvl3.execute-api.us-east-1.amazonaws.com',
    port: 443,
    path: '/default/attech-send-email',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
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
req.write(data);
req.end();
