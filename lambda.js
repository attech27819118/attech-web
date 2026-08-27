/**
 * ====================================================================
 * ATTech Materials - AWS Lambda 專用郵件與 PDF 生成 Handler (lambda.js)
 * ====================================================================
 */

const nodemailer = require('nodemailer');
const PDFDocument = require('pdfkit');
const path = require('path');
const fs = require('fs');

// 輔助函式：陣列轉換字串
function formatList(val) {
    if (Array.isArray(val)) {
        return val.length > 0 ? val.join('、') : '無';
    }
    return val || '無';
}

// 動態生成單頁 PDF 附件
function createStyledPDF(title, sections, companyName) {
    return new Promise((resolve, reject) => {
        const doc = new PDFDocument({
            size: 'A4',
            margins: { top: 25, bottom: 25, left: 28, right: 28 },
            bufferPages: true
        });

        let buffers = [];
        doc.on('data', buffers.push.bind(buffers));
        doc.on('end', () => resolve(Buffer.concat(buffers)));
        doc.on('error', reject);

        // 字型路徑 (支援 Lambda 環境)
        const regularFontPath = path.join(__dirname, 'fonts', 'NotoSansTC-Regular.ttf');
        const boldFontPath = path.join(__dirname, 'fonts', 'NotoSansTC-Bold.ttf');

        if (fs.existsSync(regularFontPath)) {
            doc.registerFont('ChineseRegular', regularFontPath);
        }
        if (fs.existsSync(boldFontPath)) {
            doc.registerFont('ChineseBold', boldFontPath);
        } else if (fs.existsSync(regularFontPath)) {
            doc.registerFont('ChineseBold', regularFontPath);
        }

        const fontRegular = doc._fontFamilies && doc._fontFamilies['ChineseRegular'] ? 'ChineseRegular' : 'Helvetica';
        const fontBold = doc._fontFamilies && doc._fontFamilies['ChineseBold'] ? 'ChineseBold' : 'Helvetica-Bold';

        const pageWidth = doc.page.width - 56;
        const startX = 28;

        // Header 公司抬頭
        doc.font(fontBold).fontSize(14).fillColor('#0F2C59').text('宏威應用材料 ATTech Materials', startX, 22, { align: 'left' });
        doc.font(fontRegular).fontSize(8).fillColor('#475569').text('Discover The Link To Life | 40661 台中市北屯區廍子巷116號1樓 | TEL: +886-4-2239-8056', startX, 38, { align: 'left' });
        doc.moveTo(startX, 50).lineTo(startX + pageWidth, 50).strokeColor('#1E3A8A').lineWidth(1.5).stroke();

        // 表單大標題
        doc.y = 56;
        doc.font(fontBold).fontSize(12).fillColor('#1E3A8A').text(title, { align: 'center' });
        doc.moveDown(0.25);

        let totalRows = 0;
        sections.forEach(sec => {
            totalRows += (sec.rows ? sec.rows.length : 0);
        });

        const isCompact = totalRows > 12;
        const rowHeight = isCompact ? 16 : 20;
        const fontSize = isCompact ? 8 : 8.5;
        const sectionHeaderHeight = isCompact ? 16 : 18;

        sections.forEach(section => {
            const secHeaderY = doc.y;
            doc.rect(startX, secHeaderY, pageWidth, sectionHeaderHeight).fill('#E2E8F0');
            doc.font(fontBold).fontSize(8.5).fillColor('#0F2C59').text(`  ${section.title}`, startX + 4, secHeaderY + 3.5);
            doc.y = secHeaderY + sectionHeaderHeight;

            section.rows.forEach(row => {
                const currentY = doc.y;
                const labelWidth = isCompact ? 120 : 130;
                const valueWidth = pageWidth - labelWidth;

                doc.rect(startX, currentY, labelWidth, rowHeight).fillAndStroke('#F8FAFC', '#CBD5E1');
                doc.rect(startX + labelWidth, currentY, valueWidth, rowHeight).fillAndStroke('#FFFFFF', '#CBD5E1');

                doc.font(fontBold).fontSize(fontSize).fillColor('#1E293B').text(row.label, startX + 6, currentY + (isCompact ? 3.5 : 4.5), {
                    width: labelWidth - 10,
                    ellipsis: true
                });

                doc.font(fontRegular).fontSize(fontSize).fillColor('#334155').text(row.value || '無', startX + labelWidth + 6, currentY + (isCompact ? 3.5 : 4.5), {
                    width: valueWidth - 10,
                    ellipsis: true
                });

                doc.y = currentY + rowHeight;
            });

            doc.y += 4;
        });

        const currentDate = new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
        const footerY = doc.page.height - 24;

        doc.moveTo(startX, footerY - 4).lineTo(startX + pageWidth, footerY - 4).strokeColor('#CBD5E1').lineWidth(0.5).stroke();
        doc.font(fontRegular).fontSize(7.5).fillColor('#64748B').text(`列印時間：${currentDate} | 宏威應用材料 Discover The Link To Life`, startX, footerY, { align: 'left' });
        doc.font(fontRegular).fontSize(7.5).fillColor('#64748B').text(`第 1 頁 / 共 1 頁`, startX, footerY, { align: 'right' });

        doc.end();
    });
}

// AWS Lambda 核心進入點
exports.handler = async (event, context) => {
    // 跨域 CORS 標頭
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Requested-With',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    };

    // 處理 OPTIONS 預檢請求
    if (event.httpMethod === 'OPTIONS' || event.requestContext?.http?.method === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: corsHeaders,
            body: ''
        };
    }

    try {
        let data = {};
        if (event.body) {
            const bodyStr = event.isBase64Encoded ? Buffer.from(event.body, 'base64').toString('utf-8') : event.body;
            data = typeof bodyStr === 'string' ? JSON.parse(bodyStr) : bodyStr;
        }

        const { company, contact, email, type } = data;

        if (!company || !contact || !email) {
            return {
                statusCode: 400,
                headers: corsHeaders,
                body: JSON.stringify({
                    success: false,
                    message: '請填寫必填欄位（公司名稱、聯絡人、電子信箱）'
                })
            };
        }

        const isQuickMode = (type === '快速詢價' || !data.appFields);
        let subject = `【官網需求單】${company} - ${contact}（${isQuickMode ? '指定樣品/快速詢價' : '詳細應用需求評估'}）`;
        let textContent = '';
        let htmlContent = '';
        let attachments = [];
        let pdfSections = [];

        if (isQuickMode) {
            const mobile = data.mobile || data.phone || '未提供';
            const sample = data.sample || '未提供';
            const address = data.address || '未提供';
            const message = data.message || '無';

            textContent = `
【宏威應用材料 - 指定樣品 / 快速詢價需求單】
--------------------------------------------------
公司名稱：${company}
聯絡人（職稱）：${contact}
電子信箱：${email}
聯絡電話 / 手機：${mobile}
指定索樣產品與數量：${sample}
樣品寄送地址：${address}
備註 / 詢問內容：${message}
--------------------------------------------------
時間：${new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}
            `;

            htmlContent = `
            <div style="font-family: Arial, 'Microsoft JhengHei', sans-serif; max-width: 650px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1e293b; background-color: #ffffff;">
                <div style="border-bottom: 2px solid #1e3a8a; padding-bottom: 12px; margin-bottom: 16px;">
                    <h2 style="color: #0f2c59; margin: 0 0 4px 0; font-size: 20px;">宏威應用材料 ATTech Materials</h2>
                    <p style="color: #1e3a8a; font-weight: bold; margin: 0; font-size: 15px;">指定樣品 / 快速詢價表單 (簡易樣品申請單)</p>
                </div>
                <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 16px;">
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; width: 150px; color: #475569; background-color: #f8fafc;">公司名稱</td><td style="padding: 8px;">${company}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #475569; background-color: #f8fafc;">聯絡人（職稱）</td><td style="padding: 8px;">${contact}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #475569; background-color: #f8fafc;">電子信箱</td><td style="padding: 8px;"><a href="mailto:${email}" style="color: #1e3a8a; text-decoration: none;">${email}</a></td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #475569; background-color: #f8fafc;">聯絡電話 / 手機</td><td style="padding: 8px;">${mobile}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #1e3a8a; background-color: #eff6ff;">索樣產品與數量</td><td style="padding: 8px; font-weight: bold; color: #1e3a8a;">${sample}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #475569; background-color: #f8fafc;">樣品寄送地址</td><td style="padding: 8px;">${address}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; font-weight: bold; color: #475569; background-color: #f8fafc;">備註 / 詢問內容</td><td style="padding: 8px; white-space: pre-wrap;">${message}</td></tr>
                </table>
                <div style="font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 10px;">
                    ※ 此郵件由 ATTech 官網系統自動發出，PDF 正式申請單已作為附件附加。
                </div>
            </div>
            `;

            pdfSections = [
                {
                    title: '基本聯絡與索樣資訊',
                    rows: [
                        { label: '公司名稱', value: company },
                        { label: '聯絡人（職稱）', value: contact },
                        { label: '電子信箱', value: email },
                        { label: '聯絡電話 / 手機', value: mobile },
                        { label: '指定索樣產品與數量', value: sample },
                        { label: '樣品寄送地址', value: address },
                        { label: '備註 / 詢問內容', value: message }
                    ]
                }
            ];
        } else {
            const mobile = data.mobile || data.phone || '未提供';
            const fax = data.fax || '未提供';
            const address = data.address || '未提供';
            const appFields = formatList(data.appFields);
            const functions = formatList(data.functions);
            const otherFunc = data.otherFunc || '無';
            const systems = formatList(data.systems);
            const compType = data.compType || '未指定';
            const appType = data.appType || '未指定';
            const substrates = formatList(data.substrates);
            const otherSubstrate = data.otherSubstrate || '無';
            const filmThick = data.filmThick ? `${data.filmThick} µm` : '未填寫';
            const noBake = data.noBake || '否';
            const bakeTemp = data.bakeTemp || '未填寫';
            const bakeTime = data.bakeTime || '未填寫';
            const resins = formatList(data.resins);
            const restricted = data.restricted || '無';
            const sampleReq = data.sampleReq || '未填寫';
            const docs = formatList(data.docs);
            const pastSamples = data.pastSamples || '無';
            const remarks = data.remarks || '無';

            textContent = `
【宏威應用材料 - 詳細應用需求評估單 (完整申請單)】
--------------------------------------------------
A. 基本聯絡資訊
公司名稱：${company}
聯絡人（職稱）：${contact}
電子信箱：${email}
聯絡電話 / 手機：${mobile}
傳真號碼：${fax}
寄送地址：${address}

B. 應用需求
應用領域：${appFields}
功能需求：${functions} (其他: ${otherFunc})
系統型態：${systems}
組份 / 外觀：${compType} / ${appType}

C. 基本資訊與規格
底材類型：${substrates} (其它: ${otherSubstrate})
乾膜厚度：${filmThick}
乾燥固化條件：不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}
樹脂系統：${resins}
限用物質：${restricted}
索樣產品需求：${sampleReq}
需求文件：${docs}

D. 曾測試紀錄
曾試過的相關樣品：${pastSamples}

E. 備註
${remarks}
--------------------------------------------------
時間：${new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}
            `;

            htmlContent = `
            <div style="font-family: Arial, 'Microsoft JhengHei', sans-serif; max-width: 700px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1e293b; background-color: #ffffff;">
                <div style="border-bottom: 2px solid #1e3a8a; padding-bottom: 12px; margin-bottom: 16px;">
                    <h2 style="color: #0f2c59; margin: 0 0 4px 0; font-size: 20px;">宏威應用材料 ATTech Materials</h2>
                    <p style="color: #1e3a8a; font-weight: bold; margin: 0; font-size: 15px;">詳細應用需求評估單 (完整樣品申請單)</p>
                </div>
                
                <h3 style="color: #1e3a8a; font-size: 14px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 16px;">A. 基本聯絡資訊</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 12px;">
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; width: 140px; color: #475569;">公司名稱：</td><td style="padding: 6px;">${company}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">聯絡人（職稱）：</td><td style="padding: 6px;">${contact}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">電子信箱：</td><td style="padding: 6px;"><a href="mailto:${email}" style="color: #1e3a8a;">${email}</a></td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">電話 / 手機：</td><td style="padding: 6px;">${mobile}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">傳真號碼：</td><td style="padding: 6px;">${fax}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">樣品寄送地址：</td><td style="padding: 6px;">${address}</td></tr>
                </table>

                <h3 style="color: #1e3a8a; font-size: 14px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 16px;">B. 應用需求與系統</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 12px;">
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; width: 140px; color: #475569;">應用領域：</td><td style="padding: 6px;">${appFields}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">功能需求：</td><td style="padding: 6px;">${functions} (其他: ${otherFunc})</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">系統型態：</td><td style="padding: 6px;">${systems}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">組份 / 外觀：</td><td style="padding: 6px;">${compType} / ${appType}</td></tr>
                </table>

                <h3 style="color: #1e3a8a; font-size: 14px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 16px;">C. 基本規格與限制</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 12px;">
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; width: 140px; color: #475569;">底材類型：</td><td style="padding: 6px;">${substrates} (其它: ${otherSubstrate})</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">乾膜厚度：</td><td style="padding: 6px;">${filmThick}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">固化條件：</td><td style="padding: 6px;">不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">樹脂系統：</td><td style="padding: 6px;">${resins}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">限用物質：</td><td style="padding: 6px;">${restricted}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #1e3a8a; background-color: #eff6ff;">索樣產品需求：</td><td style="padding: 6px; font-weight: bold; color: #1e3a8a;">${sampleReq}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">需求文件：</td><td style="padding: 6px;">${docs}</td></tr>
                </table>

                <h3 style="color: #1e3a8a; font-size: 14px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-top: 16px;">D & E. 曾測試紀錄與備註</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 16px;">
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; width: 140px; color: #475569;">曾試過樣品：</td><td style="padding: 6px;">${pastSamples}</td></tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">備註 / 其他說明：</td><td style="padding: 6px; white-space: pre-wrap;">${remarks}</td></tr>
                </table>

                <div style="font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 10px;">
                    ※ 此郵件由 ATTech 官網系統自動發出，PDF 正式申請單已作為附件附加。
                </div>
            </div>
            `;

            pdfSections = [
                {
                    title: 'A. 基本聯絡資訊',
                    rows: [
                        { label: '公司名稱', value: company },
                        { label: '聯絡人（職稱）', value: contact },
                        { label: '電子信箱', value: email },
                        { label: '聯絡電話 / 手機', value: mobile },
                        { label: '傳真號碼', value: fax },
                        { label: '樣品寄送地址', value: address }
                    ]
                },
                {
                    title: 'B. 應用需求',
                    rows: [
                        { label: '應用領域', value: appFields },
                        { label: '功能需求', value: `${functions} (其他: ${otherFunc})` },
                        { label: '系統型態', value: systems },
                        { label: '組份 / 外觀', value: `${compType} / ${appType}` }
                    ]
                },
                {
                    title: 'C. 基本資訊與規格',
                    rows: [
                        { label: '底材類型', value: `${substrates} (其它: ${otherSubstrate})` },
                        { label: '乾膜厚度', value: filmThick },
                        { label: '乾燥固化條件', value: `不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}` },
                        { label: '樹脂系統', value: resins },
                        { label: '限用物質', value: restricted },
                        { label: '索樣產品需求', value: sampleReq },
                        { label: '需求文件', value: docs }
                    ]
                },
                {
                    title: 'D & E. 曾測試紀錄與備註',
                    rows: [
                        { label: '曾試過的相關樣品', value: pastSamples },
                        { label: '備註 / 其他說明', value: remarks }
                    ]
                }
            ];
        }

        // 動態生成單頁 PDF 附件
        try {
            const pdfBuffer = await createStyledPDF(
                isQuickMode ? `${company} - 快速樣品申請單` : `${company} - 詳細應用需求評估單`,
                pdfSections,
                company
            );

            attachments.push({
                filename: isQuickMode ? `${company}_快速樣品申請單.pdf` : `${company}_詳細樣品申請單.pdf`,
                content: pdfBuffer,
                contentType: 'application/pdf'
            });
        } catch (pdfErr) {
            console.error('PDF 生成錯誤:', pdfErr);
        }

        // 郵件傳輸設定（優先支援 SES SMTP 或企業 SMTP）
        const SMTP_HOST = process.env.SES_SMTP_HOST || process.env.SMTP_HOST || 'email-smtp.us-east-1.amazonaws.com';
        const SMTP_PORT = parseInt(process.env.SES_SMTP_PORT || process.env.SMTP_PORT || '465', 10);
        const SMTP_USER = process.env.SES_SMTP_USER || process.env.SMTP_USER;
        const SMTP_PASS = process.env.SES_SMTP_PASS || process.env.SMTP_PASS;
        const FROM_EMAIL = process.env.FROM_EMAIL || 'atservice@attech.com.tw';
        const TO_EMAIL = process.env.TO_EMAIL || 'atservice@attech.com.tw';

        // CC 副本名單 (預設為空，僅在前端傳入 cc 時加入)
        let ccList = [];
        if (data.cc) {
            if (Array.isArray(data.cc)) {
                ccList = ccList.concat(data.cc);
            } else if (typeof data.cc === 'string') {
                ccList.push(data.cc);
            }
        }

        const transporter = nodemailer.createTransport({
            host: SMTP_HOST,
            port: SMTP_PORT,
            secure: SMTP_PORT === 465,
            auth: {
                user: SMTP_USER,
                pass: SMTP_PASS
            },
            tls: {
                rejectUnauthorized: false
            }
        });

        const mailOptions = {
            from: `"ATTech 官網表單" <${FROM_EMAIL}>`,
            to: TO_EMAIL,
            replyTo: email,
            subject: subject,
            text: textContent,
            html: htmlContent,
            attachments: attachments
        };

        if (ccList.length > 0) {
            mailOptions.cc = ccList;
        }

        await transporter.sendMail(mailOptions);
        console.log(`[Lambda SES Sent] ${company} - ${contact} (${type})`);

        return {
            statusCode: 200,
            headers: corsHeaders,
            body: JSON.stringify({
                success: true,
                message: '需求表單及 PDF 申請單已成功寄出！專人將儘速與您聯繫。'
            })
        };

    } catch (error) {
        console.error('Lambda 處理郵件失敗:', error);
        return {
            statusCode: 500,
            headers: corsHeaders,
            body: JSON.stringify({
                success: false,
                message: '伺服器處理郵件發送失敗，請稍後再試或直接聯繫客服。',
                error: error.message
            })
        };
    }
};
