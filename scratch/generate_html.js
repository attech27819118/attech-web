const fs = require('fs');
const path = require('path');

const mdPath = path.join(__dirname, '..', 'analysis report', '宏威應用材料_9月與10月數據分析完整報告.md');
const htmlPath = path.join(__dirname, '..', 'analysis report', '宏威應用材料_9月與10月數據分析完整報告.html');

const mdContent = fs.readFileSync(mdPath, 'utf8');

const htmlContent = `<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏威應用材料 9月 vs 10月 全方位數位營運與搜尋表現完整數據分析報告</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Marked.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Mermaid.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
        }
        #report-rendered h1 {
            font-size: 1.875rem;
            font-weight: 800;
            color: #0f172a;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
        #report-rendered h2 {
            font-size: 1.35rem;
            font-weight: 700;
            color: #1e3a8a;
            border-left: 5px solid #1e3a8a;
            padding-left: 0.75rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            background-color: #f1f5f9;
            padding-top: 0.35rem;
            padding-bottom: 0.35rem;
            border-radius: 0 0.375rem 0.375rem 0;
        }
        #report-rendered h3 {
            font-size: 1.15rem;
            font-weight: 700;
            color: #334155;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        #report-rendered h4 {
            font-size: 1rem;
            font-weight: 600;
            color: #475569;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }
        #report-rendered p {
            line-height: 1.75;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }
        #report-rendered ul, #report-rendered ol {
            margin-bottom: 1rem;
            padding-left: 1.5rem;
            line-height: 1.75;
            font-size: 0.95rem;
        }
        #report-rendered ul {
            list-style-type: disc;
        }
        #report-rendered ol {
            list-style-type: decimal;
        }
        #report-rendered blockquote {
            border-left: 4px solid #3b82f6;
            background-color: #eff6ff;
            padding: 0.75rem 1rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin-bottom: 1.25rem;
            font-size: 0.9rem;
            color: #1e40af;
        }
        #report-rendered table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            font-size: 0.85rem;
            background-color: #ffffff;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            border-radius: 0.5rem;
            overflow: hidden;
        }
        #report-rendered th {
            background-color: #1e3a8a;
            color: #ffffff;
            font-weight: 600;
            padding: 0.65rem 0.75rem;
            text-align: left;
            border: 1px solid #cbd5e1;
        }
        #report-rendered td {
            padding: 0.55rem 0.75rem;
            border: 1px solid #e2e8f0;
            vertical-align: middle;
        }
        #report-rendered tr:nth-child(even) {
            background-color: #f8fafc;
        }
        #report-rendered tr:hover {
            background-color: #f1f5f9;
        }
        #report-rendered strong {
            color: #0f172a;
        }
        #report-rendered code {
            background-color: #e2e8f0;
            color: #b91c1c;
            padding: 0.15rem 0.35rem;
            border-radius: 0.25rem;
            font-size: 0.85em;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }
        .mermaid {
            margin: 1.5rem 0;
            text-align: center;
            background: #ffffff;
            padding: 1.25rem;
            border-radius: 0.5rem;
            border: 1px solid #e2e8f0;
        }
        @media print {
            body {
                background-color: #ffffff;
            }
            .no-print {
                display: none !important;
            }
            .report-card {
                max-width: 100% !important;
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
            }
            #report-rendered h2 {
                break-before: page;
            }
        }
    </style>
</head>
<body class="py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto bg-white p-6 sm:p-10 rounded-2xl shadow-sm border border-slate-200 report-card">
        <!-- 頂部按鈕列 -->
        <div class="flex flex-wrap items-center justify-between pb-4 border-b border-slate-200 mb-6 gap-2 no-print">
            <div class="flex items-center gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-900">
                    宏威應用材料 ATTech Materials
                </span>
                <span class="text-xs text-slate-500 font-medium">9月 vs 10月 數位營運分析</span>
            </div>
            <div class="flex items-center gap-2">
                <a href="./宏威應用材料_9月與10月數據指標彙整表.xlsx" download class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-medium rounded-lg shadow-sm transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    下載 Excel 數據總表
                </a>
                <button onclick="window.print()" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-medium rounded-lg shadow-sm transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                    列印 / 另存為 PDF
                </button>
            </div>
        </div>

        <!-- 報告主體內容 (由 marked 解析渲染) -->
        <div id="report-rendered"></div>

        <!-- 頁尾宣告 -->
        <div class="mt-12 pt-6 border-t border-slate-200 text-center text-xs text-slate-500">
            <p class="font-medium text-slate-700">宏威應用材料股份有限公司 • 數位營運與市場分析團隊編製</p>
            <p class="mt-1 text-slate-400">數據來源：Google Analytics 4 / Google Search Console • 區間：2026/09/01 - 2026/10/31</p>
        </div>
    </div>

    <!-- 原始 Markdown 腳本 (避免轉義困擾) -->
    <script type="text/plain" id="raw-markdown">
${mdContent}
    </script>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const rawMd = document.getElementById("raw-markdown").textContent;
            
            // 自訂渲染器：將 mermaid 代碼區塊轉換為 <div class="mermaid">
            const renderer = new marked.Renderer();
            const originalCodeRenderer = renderer.code.bind(renderer);
            renderer.code = function(code, lang) {
                if (lang === 'mermaid') {
                    return '<div class="mermaid">' + code + '</div>';
                }
                return originalCodeRenderer(code, lang);
            };

            marked.setOptions({
                renderer: renderer,
                gfm: true,
                tables: true,
                breaks: false
            });

            document.getElementById("report-rendered").innerHTML = marked.parse(rawMd);

            // 初始化 Mermaid
            mermaid.initialize({
                startOnLoad: false,
                theme: 'neutral',
                fontFamily: 'Microsoft JhengHei'
            });
            mermaid.run({
                querySelector: '.mermaid'
            });
        });
    </script>
</body>
</html>
`;

fs.writeFileSync(htmlPath, htmlContent, 'utf8');
console.log('HTML report generated successfully at:', htmlPath);

