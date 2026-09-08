const fs = require('fs');
const path = require('path');
const lambda = require('../index.js');
const nodemailer = require('nodemailer');

function getPdfPageCount(buffer) {
    const text = buffer.toString('latin1');
    const matches = text.match(/\/Type\s*\/Page\b/g);
    return matches ? matches.length : 0;
}

async function runTests() {
    console.log('==============================================');
    console.log('  開始全面測試 Lambda 郵件與 PDF 生成腳本');
    console.log('==============================================\n');

    // 測試 1: 缺少必填欄位
    console.log('【測試 1】必填欄位校驗測試:');
    const badRes = await lambda.handler({
        body: JSON.stringify({ company: '測試公司' })
    });
    const badBody = JSON.parse(badRes.body);
    if (badRes.statusCode === 400 && badBody.success === false) {
        console.log('  ✅ 成功攔截未填聯絡人與信箱，返回 400:', badBody.message);
    } else {
        console.error('  ❌ 必填校驗失敗:', badRes);
        process.exit(1);
    }

    // 測試 2: OPTIONS 預檢請求
    console.log('\n【測試 2】CORS OPTIONS 預檢請求測試:');
    const optionsRes = await lambda.handler({
        httpMethod: 'OPTIONS'
    });
    if (optionsRes.statusCode === 200 && optionsRes.headers['Access-Control-Allow-Origin'] === '*') {
        console.log('  ✅ OPTIONS 預檢請求通過，返回 200 及跨域標頭');
    } else {
        console.error('  ❌ OPTIONS 失敗:', optionsRes);
        process.exit(1);
    }

    // 測試 3: 詳細需求評估單 PDF 生成測試 (使用最新欄位規範)
    console.log('\n【測試 3】詳細需求評估單 PDF 生成測試 (含所有新欄位):');
    const detailedSections = [
        {
            title: 'A. 基本聯絡資訊',
            rows: [
                { label: '填表日期', value: '2026/09/08' },
                { label: '公司名稱', value: '宏威科技股份有限公司' },
                { label: '聯絡人（職稱）', value: '張經理 (研發部)' },
                { label: '電子信箱', value: 'test@example.com' },
                { label: '電話及分機', value: '04-2239-8056#123' },
                { label: '手機號碼', value: '0912-345-678' },
                { label: '傳真號碼', value: '04-2239-5165' },
                { label: '樣品寄送地址', value: '40661 台中市北屯區廍子巷116號1樓' }
            ]
        },
        {
            title: 'B. 應用需求',
            rows: [
                { label: '應用領域', value: '一般工業塗料、粉體塗料、接著劑（其他: 特種耐高溫塗層）' },
                { label: '功能需求', value: '密著促進/改善、耐磨、消光（其他: 抗指紋、抗油污）' },
                { label: '系統型態', value: '水性、UV硬化、無溶劑' },
                { label: '組份 / 外觀', value: '雙組份 / 有顏色 (消光黑)' }
            ]
        },
        {
            title: 'C. 基本資訊與規格',
            rows: [
                { label: '底材類型', value: 'PVC、鋁合金、真皮、木材（其它: 碳纖維複合材）' },
                { label: '乾膜厚度', value: '25 µm' },
                { label: '乾燥固化條件', value: '不烘烤: 否 | 溫度: 150℃ | 時間: 30 min' },
                { label: '樹脂系統', value: 'PU、poly(UPE不飽和聚酯)、矽利康（其他: 改性氟矽樹脂）' },
                { label: '其他資訊(限用物質)', value: '八大重金屬、EN-71、RoHS、REACH、無鹵、FDA等規範' },
                { label: '索樣產品資訊', value: 'MP-22（數量: 100g）；Micropro 500（數量: 100g）' },
                { label: '需求文件', value: 'TDS-中文、TDS-英文、SDS-中文' }
            ]
        },
        {
            title: 'D & E. 曾測試紀錄與備註',
            rows: [
                { label: '曾試過的相關樣品', value: '曾試過競品 AC-300，耐磨測試約 800 次磨耗後出現刮痕，希望尋求更佳耐磨產品。' },
                { label: '備註 / 其他說明', value: '希望能儘速提供樣品進行配方評估測試，預計下個月進行產線中試。' }
            ]
        }
    ];

    const detailedPdfBuffer = await lambda.createStyledPDF(
        '宏威科技股份有限公司 - 詳細樣品申請與技術評估單',
        detailedSections,
        '宏威科技股份有限公司'
    );
    const detailedPdfPath = path.join(__dirname, 'test_detailed_result.pdf');
    fs.writeFileSync(detailedPdfPath, detailedPdfBuffer);
    const detailedPages = getPdfPageCount(detailedPdfBuffer);
    if (detailedPages !== 1) {
        throw new Error(`詳細評估單 PDF 頁數不符！預期 1 頁，實際為 ${detailedPages} 頁`);
    }
    console.log(`  ✅ 詳細評估單 PDF 生成成功且為嚴格 1 頁！檔案大小: ${detailedPdfBuffer.length} bytes -> ${detailedPdfPath}`);

    // 測試 4: 快速索樣單 PDF 生成測試
    console.log('\n【測試 4】快速索樣單 PDF 生成測試:');
    const quickSections = [
        {
            title: '基本聯絡與索樣資訊',
            rows: [
                { label: '填表日期', value: '2026/09/08' },
                { label: '公司名稱', value: '創新材料研發中心' },
                { label: '聯絡人（職稱）', value: '李專員' },
                { label: '電子信箱', value: 'lee@example.com' },
                { label: '聯絡電話 / 手機', value: '0988-123-456' },
                { label: '指定索樣產品與數量', value: 'MP-22 (200g)' },
                { label: '樣品寄送地址', value: '台北市信義區信義路五段7號' },
                { label: '備註 / 詢問內容', value: '需現貨確認，急件測試。' }
            ]
        }
    ];

    const quickPdfBuffer = await lambda.createStyledPDF(
        '創新材料研發中心 - 快速樣品申請單',
        quickSections,
        '創新材料研發中心'
    );
    const quickPdfPath = path.join(__dirname, 'test_quick_result.pdf');
    fs.writeFileSync(quickPdfPath, quickPdfBuffer);
    const quickPages = getPdfPageCount(quickPdfBuffer);
    if (quickPages !== 1) {
        throw new Error(`快速索樣單 PDF 頁數不符！預期 1 頁，實際為 ${quickPages} 頁`);
    }
    console.log(`  ✅ 快速索樣單 PDF 生成成功且為嚴格 1 頁！檔案大小: ${quickPdfBuffer.length} bytes -> ${quickPdfPath}`);

    // 測試 5: 模擬完整 Lambda 發信流程 (以 Mock Transporter 測試 Handler 完整邏輯)
    console.log('\n【測試 5】模擬完整 Lambda 發信 Handler 邏輯:');
    
    // 設定測試用環境變數
    process.env.SMTP_USER = 'test_user';
    process.env.SMTP_PASS = 'test_pass';
    process.env.FROM_EMAIL = 'atservice@attech.com.tw';
    process.env.TO_EMAIL = 'atservice@attech.com.tw';

    let capturedMailOptions = null;
    // Mock nodemailer.createTransport
    const origCreateTransport = nodemailer.createTransport;
    nodemailer.createTransport = function (config) {
        return {
            sendMail: async function (options) {
                capturedMailOptions = options;
                return { messageId: 'mock-test-123' };
            }
        };
    };

    const mockEvent = {
        body: JSON.stringify({
            type: '詳細需求',
            applyDate: '2026/09/08',
            company: '宏威測試工業',
            contact: '王工程師',
            email: 'wang@test.com',
            tel: '04-2239-8056',
            mobile: '0900-111-222',
            address: '台中市北屯區',
            appFields: ['一般工業塗料', '接著劑'],
            otherAppDomain: '光學光電塗佈',
            functions: ['密著促進/改善', 'PTFE取代'],
            otherFunc: '超低表面張力',
            systems: ['水性', '無溶劑'],
            compType: '單組份',
            appType: '透明',
            substrates: ['PET', '薄膜', '木材'],
            otherSubstrate: '特種防黏紙',
            filmThick: '15',
            noBake: '否',
            bakeTemp: '120℃',
            bakeTime: '20 min',
            resins: ['PU', 'poly(UPE不飽和聚酯)'],
            otherResin: '高固含醇酸樹脂',
            restricted: 'RoHS, REACH',
            sampleItems: [
                { name: 'MP-22', qty: '100g' },
                { name: 'Micropro 500', qty: '50g' }
            ],
            docs: ['TDS-中文', 'SDS-中文'],
            pastSamples: '無',
            remarks: '請附樣品檢驗規格說明。'
        })
    };

    const handlerRes = await lambda.handler(mockEvent);
    nodemailer.createTransport = origCreateTransport; // 還原

    const resBody = JSON.parse(handlerRes.body);
    if (handlerRes.statusCode === 200 && resBody.success === true) {
        console.log('  ✅ Lambda Handler 成功執行並返回 200:', resBody.message);
        console.log('  📧 郵件標題:', capturedMailOptions.subject);
        console.log('  📎 附件數量:', capturedMailOptions.attachments.length);
        console.log('  📎 附件檔名:', capturedMailOptions.attachments[0].filename);
        console.log('  📎 附件內容大小:', capturedMailOptions.attachments[0].content.length, 'bytes');
        const attachPages = getPdfPageCount(capturedMailOptions.attachments[0].content);
        if (attachPages !== 1) {
            throw new Error(`Handler 附件 PDF 頁數不符！預期 1 頁，實際為 ${attachPages} 頁`);
        }
        console.log('  📄 附件 PDF 頁數驗證通過: 嚴格 1 頁');
    } else {
        console.error('  ❌ Lambda Handler 測試失敗:', handlerRes);
        process.exit(1);
    }

    console.log('\n==============================================');
    console.log('  🎉 所有送信與 PDF 生成測試全部 PASS 通過！');
    console.log('==============================================');
}

runTests().catch(err => {
    console.error('測試發生未預期錯誤:', err);
    process.exit(1);
});
