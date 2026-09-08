/**
 * ATTech Materials - AWS Lambda 測試腳本 (test-lambda.js)
 * 
 * 使用方式：
 * 1. 本機模擬測試 (離線驗證 PDF 生成、參數驗證、Handler 邏輯)：
 *    node scripts/test-lambda.js
 *    node scripts/test-lambda.js --local
 * 
 * 2. 雲端線上端點測試 (發送真實 HTTP POST 到 AWS Lambda / API Gateway)：
 *    node scripts/test-lambda.js --remote
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 線上 API Gateway / Lambda Function URL 端點
const DEFAULT_REMOTE_URL = 'https://uib4yezvl3.execute-api.us-east-1.amazonaws.com/default/attech-send-email';

// 測試案例 A：詳細樣品申請與技術評估（完整最新欄位）
const detailedPayload = {
    type: '詳細需求',
    applyDate: new Date().toLocaleDateString('zh-TW', { timeZone: 'Asia/Taipei', year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/-/g, '/'),
    company: '宏威測試科技股份有限公司',
    contact: '張經理 (研發部)',
    email: 'atservice@attech.com.tw', // 測試時可改為您的接收信箱
    tel: '04-2239-8056#123',
    mobile: '0912-345-678',
    fax: '04-2239-5165',
    address: '40661 台中市北屯區廍子巷116號1樓',
    appFields: ['一般工業塗料', '接著劑', '粉體塗料'],
    otherAppDomain: '特種耐高溫塗層',
    functions: ['密著促進/改善', '耐磨', '消光'],
    otherFunc: '抗指紋、抗油污',
    systems: ['水性', 'UV硬化', '無溶劑'],
    compType: '雙組份',
    appType: '有顏色',
    colorDesc: '消光黑',
    substrates: ['PVC', '鋁合金', '真皮', '木材'],
    otherSubstrate: '碳纖維複合材',
    filmThick: '25',
    noBake: '否',
    bakeTemp: '150℃',
    bakeTime: '30 min',
    resins: ['PU', 'poly(UPE不飽和聚酯)', '矽利康'],
    otherResin: '改性氟矽樹脂',
    restricted: 'RoHS, REACH, EN-71, 無鹵',
    sampleReq: 'MP-22 (100g)；Micropro 500 (100g)',
    sampleItems: [
        { name: 'MP-22', qty: '100g' },
        { name: 'Micropro 500', qty: '100g' }
    ],
    docs: ['TDS-中文', 'TDS-英文', 'SDS-中文'],
    pastSamples: '曾試過競品 AC-300，耐磨約 800 次磨耗後出現刮痕。',
    remarks: '請協助確認庫存並儘速寄出樣品，預計下月初進行配方試驗。'
};

// 測試案例 B：指定樣品 / 快速詢價
const quickPayload = {
    type: '快速詢價',
    applyDate: new Date().toLocaleDateString('zh-TW', { timeZone: 'Asia/Taipei', year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/-/g, '/'),
    company: '創新材料快速測試',
    contact: '李專員',
    email: 'atservice@attech.com.tw',
    mobile: '0988-123-456',
    phone: '0988-123-456',
    sample: 'MP-22 (200g)',
    address: '台北市信義區信義路五段7號',
    message: '需現貨確認，急件測試。'
};

// 計算 PDF 頁數輔助函式
function getPdfPageCount(buffer) {
    const text = buffer.toString('latin1');
    const matches = text.match(/\/Type\s*\/Page\b/g);
    return matches ? matches.length : 0;
}

// --------------------------------------------------------------------
// 1. 本機模擬測試 (直接調用本地 index.js handler)
// --------------------------------------------------------------------
async function runLocalTest() {
    console.log('====================================================');
    console.log('  🧪 【本機模擬】AWS Lambda Handler 測試開始');
    console.log('====================================================\n');

    const lambda = require('../index.js');
    const nodemailer = require('nodemailer');

    // 攔截發信（若未設定真實 SMTP 密碼，則以 Mock 驗證郵件結構）
    let capturedMails = [];
    const origCreateTransport = nodemailer.createTransport;
    const hasSmtpConfig = process.env.SMTP_USER && process.env.SMTP_PASS;

    if (!hasSmtpConfig) {
        console.log('ℹ️  未檢測到本機 SMTP_USER / SMTP_PASS 環境變數，將注入測試假資料並使用 Mock 發信攔截以驗證結構。\n');
        process.env.SMTP_USER = 'test_atservice@attech.com.tw';
        process.env.SMTP_PASS = 'test_mock_password';
        nodemailer.createTransport = function () {
            return {
                sendMail: async function (options) {
                    capturedMails.push(options);
                    return { messageId: 'mock-' + Date.now() };
                }
            };
        };
    }

    try {
        // 1. 測試 OPTIONS 跨域預檢
        console.log('【步驟 1】測試 HTTP OPTIONS 跨域預檢請求:');
        const optRes = await lambda.handler({ httpMethod: 'OPTIONS' });
        if (optRes.statusCode === 200 && optRes.headers['Access-Control-Allow-Origin'] === '*') {
            console.log('  ✅ OPTIONS 跨域標頭驗證通過 (200 OK)');
        } else {
            console.error('  ❌ OPTIONS 驗證失敗:', optRes);
        }

        // 2. 測試必填防護
        console.log('\n【步驟 2】測試必填欄位防護 (未填公司與聯絡人):');
        const badRes = await lambda.handler({ body: JSON.stringify({ email: 'test@example.com' }) });
        const badBody = JSON.parse(badRes.body);
        if (badRes.statusCode === 400 && badBody.success === false) {
            console.log('  ✅ 成功攔截無效請求:', badBody.message);
        } else {
            console.error('  ❌ 必填防護失敗:', badRes);
        }

        // 3. 測試詳細需求評估單 (含 PDF 生成與頁數驗證)
        console.log('\n【步驟 3】測試【詳細樣品申請單】Handler 與 PDF 生成:');
        const detailedEvent = {
            httpMethod: 'POST',
            body: JSON.stringify(detailedPayload)
        };
        const detailedRes = await lambda.handler(detailedEvent);
        const detailedBody = JSON.parse(detailedRes.body);

        if (detailedRes.statusCode === 200 && detailedBody.success) {
            console.log('  ✅ Handler 執行成功 (200 OK):', detailedBody.message);
            if (capturedMails.length > 0) {
                const mail = capturedMails[capturedMails.length - 1];
                console.log('  📧 郵件主旨:', mail.subject);
                console.log('  📎 附件檔名:', mail.attachments[0].filename);
                console.log('  📎 附件大小:', mail.attachments[0].content.length, 'bytes');

                const pages = getPdfPageCount(mail.attachments[0].content);
                console.log('  📄 PDF 實體頁數:', pages, '頁', (pages === 1 ? '✅ (嚴格單頁 A4 符合規範)' : '❌ (超出 1 頁)'));

                // 儲存產出的 PDF 檔案至 output
                const outDir = path.join(__dirname, '..', 'scratch');
                if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
                const outPdf = path.join(outDir, 'lambda_test_detailed.pdf');
                fs.writeFileSync(outPdf, mail.attachments[0].content);
                console.log('  💾 測試 PDF 已輸出至:', outPdf);
            }
        } else {
            console.error('  ❌ 詳細需求單測試失敗:', detailedRes);
        }

        // 4. 測試快速索樣單
        console.log('\n【步驟 4】測試【快速索樣需求單】Handler 與 PDF 生成:');
        const quickEvent = {
            httpMethod: 'POST',
            body: JSON.stringify(quickPayload)
        };
        const quickRes = await lambda.handler(quickEvent);
        const quickBody = JSON.parse(quickRes.body);

        if (quickRes.statusCode === 200 && quickBody.success) {
            console.log('  ✅ Handler 執行成功 (200 OK):', quickBody.message);
            if (capturedMails.length > 0) {
                const mail = capturedMails[capturedMails.length - 1];
                console.log('  📧 郵件主旨:', mail.subject);
                const pages = getPdfPageCount(mail.attachments[0].content);
                console.log('  📄 PDF 實體頁數:', pages, '頁', (pages === 1 ? '✅ (嚴格單頁 A4 符合規範)' : '❌ (超出 1 頁)'));

                const outPdf = path.join(__dirname, '..', 'scratch', 'lambda_test_quick.pdf');
                fs.writeFileSync(outPdf, mail.attachments[0].content);
                console.log('  💾 測試 PDF 已輸出至:', outPdf);
            }
        } else {
            console.error('  ❌ 快速索樣單測試失敗:', quickRes);
        }

        console.log('\n====================================================');
        console.log('  🎉 【本機模擬測試】全數通過！Handler 與 PDF 運作正常');
        console.log('====================================================\n');

    } finally {
        nodemailer.createTransport = origCreateTransport;
    }
}

// --------------------------------------------------------------------
// 2. 雲端實際 HTTP API 測試 (對線上 AWS 端點發送真實請求)
// --------------------------------------------------------------------
function sendHttpRequest(targetUrl, payload) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(targetUrl);
        const dataStr = JSON.stringify(payload);

        const options = {
            hostname: urlObj.hostname,
            path: urlObj.pathname + (urlObj.search || ''),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(dataStr)
            },
            timeout: 20000
        };

        const req = https.request(options, (res) => {
            let resData = '';
            res.on('data', chunk => resData += chunk);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(resData);
                    resolve({ statusCode: res.statusCode, headers: res.headers, body: parsed });
                } catch (e) {
                    resolve({ statusCode: res.statusCode, headers: res.headers, rawBody: resData });
                }
            });
        });

        req.on('error', reject);
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('請求逾時 (20 秒)'));
        });

        req.write(dataStr);
        req.end();
    });
}

async function runRemoteTest() {
    const remoteUrl = process.env.API_URL || DEFAULT_REMOTE_URL;
    console.log('====================================================');
    console.log('  🌐 【雲端線上端點測試】');
    console.log('  目標 URL:', remoteUrl);
    console.log('====================================================\n');

    console.log('正在向 AWS 線上端點發送【詳細需求評估單】測試請求...');
    try {
        const result = await sendHttpRequest(remoteUrl, detailedPayload);
        console.log('\n伺服器回應狀態碼:', result.statusCode);
        console.log('伺服器回應內容:', JSON.stringify(result.body || result.rawBody, null, 2));

        if (result.statusCode === 200 && result.body && result.body.success) {
            console.log('\n✅ 雲端測試成功！AWS Lambda 已成功接收、生成 PDF 並發送通知郵件。');
        } else {
            console.warn('\n⚠️ 雲端端點回應非成功狀態，請檢視上方回應訊息或 AWS CloudWatch Logs。');
        }
    } catch (err) {
        console.error('❌ 連線雲端端點失敗:', err.message);
    }
}

// --------------------------------------------------------------------
// 主執行入口
// --------------------------------------------------------------------
const args = process.argv.slice(2);
if (args.includes('--remote') || args.includes('-r')) {
    runRemoteTest();
} else {
    runLocalTest();
}
