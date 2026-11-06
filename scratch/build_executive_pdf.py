import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>宏威應用材料 9月 vs 10月 流量與搜尋表現分析報告</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 0;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, "PingFang TC", "Microsoft JhengHei", "微軟正黑體", sans-serif;
            background-color: #525659;
            color: #1e293b;
        }
        .page {
            width: 210mm;
            height: 297mm;
            margin: 10px auto;
            background: #ffffff;
            padding: 14mm 16mm 12mm 16mm;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            page-break-after: always;
            page-break-inside: avoid;
            overflow: hidden;
        }
        @media print {
            body {
                background: none;
            }
            .page {
                margin: 0;
                box-shadow: none;
                width: 210mm;
                height: 297mm;
            }
            .no-print {
                display: none !important;
            }
        }

        /* 頂部 Header */
        .report-header {
            margin-bottom: 10px;
        }
        .super-title {
            color: #0f766e;
            font-size: 8pt;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 2px;
        }
        .main-title {
            color: #0f172a;
            font-size: 16.5pt;
            font-weight: 800;
            margin: 0 0 6px 0;
            letter-spacing: -0.01em;
        }
        .meta-bar {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 8.5pt;
            color: #475569;
            border-bottom: 1.5px solid #0f766e;
            padding-bottom: 5px;
        }
        .meta-item strong {
            color: #0f172a;
        }

        /* 核心摘要框 */
        .summary-card {
            background-color: #f0fdfa;
            border-left: 3.5px solid #0f766e;
            padding: 7px 10px;
            border-radius: 0 4px 4px 0;
            margin-top: 8px;
            margin-bottom: 11px;
            font-size: 8.6pt;
            line-height: 1.45;
            color: #134e4a;
        }
        .summary-card strong {
            color: #0f766e;
        }

        /* 區塊標題 */
        .section-title {
            font-size: 10.5pt;
            font-weight: 700;
            color: #0f766e;
            border-bottom: 1.5px solid #ccfbf1;
            padding-bottom: 3px;
            margin-top: 10px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* 表格樣式 */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8.2pt;
            margin-bottom: 8px;
            background: #ffffff;
        }
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: left;
        }
        td {
            border: 1px solid #e2e8f0;
            padding: 3.6px 6px;
            color: #334155;
            vertical-align: middle;
            line-height: 1.35;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .t-center { text-align: center; }
        .t-right { text-align: right; }
        .badge-green {
            color: #059669;
            font-weight: 700;
        }
        .badge-red {
            color: #d97706;
            font-weight: 700;
        }
        .badge-new {
            background: #fef3c7;
            color: #92400e;
            font-size: 7.5pt;
            padding: 1px 4px;
            border-radius: 3px;
            font-weight: 700;
        }

        /* 趨勢與策略卡片 */
        .card-list {
            margin-top: 6px;
            margin-bottom: 8px;
        }
        .insight-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3.5px solid #0f766e;
            padding: 6px 9px;
            border-radius: 0 4px 4px 0;
            margin-bottom: 6px;
            font-size: 8.4pt;
            line-height: 1.4;
            color: #334155;
        }
        .insight-card strong {
            color: #0f172a;
        }

        /* 頁尾 */
        .page-footer {
            position: absolute;
            bottom: 9mm;
            left: 16mm;
            right: 16mm;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 7.8pt;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            padding-top: 4px;
        }

        /* 頂部列印按鈕列 */
        .top-action-bar {
            position: fixed;
            top: 12px;
            right: 12px;
            z-index: 9999;
            display: flex;
            gap: 8px;
        }
        .btn-print {
            background: #0f766e;
            color: #ffffff;
            border: none;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 9pt;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .btn-print:hover {
            background: #115e59;
        }
    </style>
</head>
<body>

    <div class="top-action-bar no-print">
        <button class="btn-print" onclick="window.print()">
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
            列印 / 另存為原版高階 PDF
        </button>
    </div>

    <!-- ==================== PAGE 1 ==================== -->
    <div class="page">
        <div class="report-header">
            <div class="super-title">DIGITAL ANALYTICS PERFORMANCE REPORT</div>
            <h1 class="main-title">宏威應用材料 9 月 vs 10 月 流量與搜尋表現分析報告</h1>
            <div class="meta-bar">
                <span class="meta-item">網址：<strong>attech.com.tw</strong></span>
                <span class="meta-item">分析區間：<strong>2026 年 9 月 vs 10 月</strong></span>
                <span class="meta-item">資料源：<strong>Google Analytics 4 / Google Search Console</strong></span>
            </div>
        </div>

        <div class="summary-card">
            <strong>核心摘要：</strong>10 月網站呈現倍數級流量爆發，活躍使用者激增 <strong>+116.2%</strong>（由 136 人提升至 294 人）。<strong>Google 自然搜尋超越直接造訪成為全站第 1 大流量渠道</strong>，且特用化學品專用材料（Orion 塗料碳黑、PTFE 取代蠟粉、Tyzor 鈦酸酯）點閱率與諮詢瀏覽量同步顯著走升。
        </div>

        <div class="section-title">
            <span>一、 全站關鍵營運指標對比 (GA4 & GSC)</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 14%;">指標類別</th>
                    <th style="width: 32%;">指標項目</th>
                    <th style="width: 13%;" class="t-center">9 月數據</th>
                    <th style="width: 13%;" class="t-center">10 月數據</th>
                    <th style="width: 12%;" class="t-center">增減幅度</th>
                    <th style="width: 16%;">表現評估</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>GA4 流量</td>
                    <td><strong>活躍使用者</strong> (Active Users)</td>
                    <td class="t-center">136 人</td>
                    <td class="t-center"><strong>294 人</strong></td>
                    <td class="t-center badge-green">+116.2%</td>
                    <td>新客顯著翻倍擴張</td>
                </tr>
                <tr>
                    <td>GA4 流量</td>
                    <td><strong>新使用者</strong> (New Users)</td>
                    <td class="t-center">136 人</td>
                    <td class="t-center"><strong>279 人</strong></td>
                    <td class="t-center badge-green">+105.1%</td>
                    <td>外部觸及率顯著提升</td>
                </tr>
                <tr>
                    <td>GA4 互動</td>
                    <td><strong>事件總計數</strong> (Event Count)</td>
                    <td class="t-center">2,115 次</td>
                    <td class="t-center"><strong>3,031 次</strong></td>
                    <td class="t-center badge-green">+43.3%</td>
                    <td>站內活動量持續走高</td>
                </tr>
                <tr>
                    <td>GA4 互動</td>
                    <td><strong>平均參與時間</strong> (秒 / 人)</td>
                    <td class="t-center">92.3 秒</td>
                    <td class="t-center">80.8 秒</td>
                    <td class="t-center badge-red">-12.5%</td>
                    <td>大量新客湧入正常微降</td>
                </tr>
                <tr>
                    <td>GSC 搜尋</td>
                    <td><strong>總曝光次數</strong> (Impressions)</td>
                    <td class="t-center">2,294 次</td>
                    <td class="t-center"><strong>2,690 次</strong></td>
                    <td class="t-center badge-green">+17.3%</td>
                    <td>搜尋能見度穩定提升</td>
                </tr>
                <tr>
                    <td>GSC 搜尋</td>
                    <td><strong>總點擊次數</strong> (Clicks)</td>
                    <td class="t-center">135 次</td>
                    <td class="t-center">126 次</td>
                    <td class="t-center badge-red">-6.7%</td>
                    <td>點擊總量維持平穩水準</td>
                </tr>
                <tr>
                    <td>GSC 搜尋</td>
                    <td><strong>平均點閱率</strong> (CTR)</td>
                    <td class="t-center">5.88%</td>
                    <td class="t-center">4.68%</td>
                    <td class="t-center badge-red">-1.20% pt</td>
                    <td>長尾廣泛曝光拉低均值</td>
                </tr>
                <tr>
                    <td>GSC 搜尋</td>
                    <td><strong>平均排名</strong> (Position)</td>
                    <td class="t-center">12.08 名</td>
                    <td class="t-center"><strong>11.71 名</strong></td>
                    <td class="t-center badge-green">提升 0.37 名</td>
                    <td>首頁至第二頁前段穩固</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">
            <span>二、 流量獲取來源結構變化 (Session Source / Medium)</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 32%;">流量來源 / 媒介</th>
                    <th style="width: 17%;" class="t-center">9 月工作階段</th>
                    <th style="width: 17%;" class="t-center">10 月工作階段</th>
                    <th style="width: 14%;" class="t-center">增減變化</th>
                    <th style="width: 20%;">結構特徵與洞察說明</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>google / organic</strong> (Google 自然搜尋)</td>
                    <td class="t-center">84 (38.5%)</td>
                    <td class="t-center"><strong>185 (43.9%)</strong></td>
                    <td class="t-center badge-green"><strong>+120.2%</strong></td>
                    <td><strong>超越直接造訪，躍居第 1 大來源</strong>，SEO 成效顯著</td>
                </tr>
                <tr>
                    <td><strong>(direct) / (none)</strong> (直接流量 / 書籤)</td>
                    <td class="t-center">110 (50.5%)</td>
                    <td class="t-center">178 (42.3%)</td>
                    <td class="t-center badge-green">+61.8%</td>
                    <td>線下客戶回訪與名片直接鍵入量持續增長</td>
                </tr>
                <tr>
                    <td><strong>cn.bing.com / referral</strong> (Bing 搜尋)</td>
                    <td class="t-center">8 (3.7%)</td>
                    <td class="t-center">25 (5.9%)</td>
                    <td class="t-center badge-green">+212.5%</td>
                    <td>Bing 管道擴散快速，來自企業端桌面搜尋比例增加</td>
                </tr>
                <tr>
                    <td><strong>github.com / referral</strong> (外部引薦)</td>
                    <td class="t-center">7 (3.2%)</td>
                    <td class="t-center">19 (4.5%)</td>
                    <td class="t-center badge-green">+171.4%</td>
                    <td>技術開源管道之外部反向連結導流穩定</td>
                </tr>
                <tr>
                    <td><strong>chatgpt.com / ai-assistant</strong> (AI 引擎)</td>
                    <td class="t-center">0 (0.0%)</td>
                    <td class="t-center">5 (1.2%)</td>
                    <td class="t-center badge-new">新增來源</td>
                    <td>AI 助理回答化工材料解決方案時已收錄並推薦本站</td>
                </tr>
            </tbody>
        </table>

        <div class="page-footer">
            <span>宏威應用材料股份有限公司 • 數位營運數據分析報告</span>
            <span>Page 1 of 2</span>
        </div>
    </div>

    <!-- ==================== PAGE 2 ==================== -->
    <div class="page">
        <div class="section-title" style="margin-top: 0;">
            <span>三、 熱門產品專頁與轉換意向表現 (GA4 Top Pages)</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th style="width: 38%;">熱門頁面名稱 (Page Title)</th>
                    <th style="width: 14%;" class="t-center">9 月瀏覽</th>
                    <th style="width: 14%;" class="t-center">10 月瀏覽</th>
                    <th style="width: 15%;" class="t-center">10月不重複訪客</th>
                    <th style="width: 19%;">產品關注度趨勢</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Orion 塗料碳黑</strong> (特化材料)</td>
                    <td class="t-center">57 次</td>
                    <td class="t-center"><strong>132 次</strong></td>
                    <td class="t-center"><strong>71 人</strong></td>
                    <td><strong>躍升 10 月全站產品瀏覽冠軍 (+131.6%)</strong></td>
                </tr>
                <tr>
                    <td><strong>PTFE 取代</strong> (Micro Powders 蠟粉)</td>
                    <td class="t-center">59 次</td>
                    <td class="t-center"><strong>113 次</strong></td>
                    <td class="t-center">45 人</td>
                    <td>跳出率僅 <strong>10.5%</strong>，客戶停留與黏著度極高</td>
                </tr>
                <tr>
                    <td><strong>Tyzor® 鈦/鋯酸酯全系列</strong> (Dorf Ketal)</td>
                    <td class="t-center">49 次</td>
                    <td class="t-center"><strong>108 次</strong></td>
                    <td class="t-center">36 人</td>
                    <td>核心產品支柱，相關技術應用頁合計逾 150 次</td>
                </tr>
                <tr>
                    <td><strong>樣品索取與技術諮詢</strong> (商業轉換指標)</td>
                    <td class="t-center">41 次</td>
                    <td class="t-center"><strong>57 次</strong></td>
                    <td class="t-center"><strong>24 人</strong></td>
                    <td>高意向潛在客戶數成長 <strong>+26.3%</strong>，跳出率僅 <strong>11.1%</strong></td>
                </tr>
                <tr>
                    <td><strong>產品分類專區</strong> (全產品導覽)</td>
                    <td class="t-center">24 次</td>
                    <td class="t-center">44 次</td>
                    <td class="t-center">28 人</td>
                    <td>進站後深度探索整體代理產品線比例攀升</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">
            <span>四、 搜尋表現與行動裝置趨勢 (GSC)</span>
        </div>
        <div class="card-list">
            <div class="insight-card">
                <strong>品牌字霸榜：</strong>「宏威應用材料股份有限公司」維持 Google 搜尋首位（平均排名 1.2 ～ 1.3），點閱率（CTR）高達 <strong>47% ～ 52%</strong>，為品牌核心客群最主要進站門戶。
            </div>
            <div class="insight-card">
                <strong>原廠型號長尾字浮現：</strong>10 月出現更多精準型號的自然搜尋曝光，包含 <code>ok 412 / ok-412</code> (Acematt 消光粉)、<code>unilink 4200</code>、<code>polyglide 1226xf</code>、<code>printex v</code> 等，代表終端配方工程師之採購需求湧入。
            </div>
            <div class="insight-card">
                <strong>行動端點擊勁揚 +68%：</strong>行動裝置（Mobile）點擊數由 9 月的 25 次增加到 10 月的 <strong>42 次</strong>，曝光數增至 848 次，行動端點閱率上升至 <strong>4.95%</strong>，顯示工程師在產線或差旅中透過手機查閱材料規格之習慣增強。
            </div>
        </div>

        <div class="section-title">
            <span>五、 後續營運優化策略建議</span>
        </div>
        <div class="card-list">
            <div class="insight-card">
                <strong>縮短熱門產品轉換路徑：</strong>針對目前流量前二大的「Orion 塗料碳黑」與「PTFE 取代」專頁，於規格表下方增設浮動或突出的「索取樣品 (TDS)」按鈕，加速導流至諮詢表單。
            </div>
            <div class="insight-card">
                <strong>針對精準型號補強應用說明：</strong>依據 GSC 搜尋字詞，針對 Acematt OK 412、Polyglide 1226XF 等高頻查詢型號補充「耐磨塗料」與「消光抗刮」配方實例，強化排名至第 1~3 名以獲取更高點擊。
            </div>
            <div class="insight-card">
                <strong>落實行動端閱覽與表單填寫體驗：</strong>因應手機造訪量提升，持續優化產品規格對照表及 PDF 型錄在手機螢幕上的載入流暢度。
            </div>
        </div>

        <div class="page-footer">
            <span>宏威應用材料股份有限公司 • 數位營運數據分析報告</span>
            <span>Page 2 of 2</span>
        </div>
    </div>

</body>
</html>
"""

html_out_path = r'd:\Jay\vscode\attech0824\analysis report\宏威應用材料_9月與10月數據分析報告_高階精美版.html'
pdf_out_path = r'd:\Jay\vscode\attech0824\analysis report\宏威應用材料_9月與10月數據分析報告_高階精美版.pdf'

with open(html_out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML 已寫入: {html_out_path}")

# 使用 Chrome Headless 編譯為 PDF
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_out_path}',
    f'file:///{html_out_path.replace(os.sep, "/")}'
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome 生成 PDF 結果:", res.returncode)
if os.path.exists(pdf_out_path):
    print(f"✅ 成功生成 100% 精美高階 PDF: {pdf_out_path} 大小: {os.path.getsize(pdf_out_path)} bytes")
else:
    print("❌ 生成 PDF 失敗:", res.stderr)

