import os
import markdown
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

md_path = r'd:\Jay\vscode\attech0824\analysis report\宏威應用材料_9月與10月數據分析完整報告.md'
html_path = r'd:\Jay\vscode\attech0824\analysis report\宏威應用材料_9月與10月數據分析完整報告.html'

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML with tables extension
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏威應用材料 9月 vs 10月 全方位數位營運與搜尋表現完整數據分析報告</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
        }});
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
        }}
        .report-content h1 {{
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            border-bottom: 3px solid #1e3a8a;
            padding-bottom: 0.75rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        .report-content h2 {{
            font-size: 1.5rem;
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
        }}
        .report-content h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #334155;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        .report-content h4 {{
            font-size: 1.05rem;
            font-weight: 600;
            color: #475569;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }}
        .report-content p {{
            line-height: 1.75;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}
        .report-content ul, .report-content ol {{
            margin-bottom: 1rem;
            padding-left: 1.5rem;
            line-height: 1.75;
            font-size: 0.95rem;
        }}
        .report-content ul {{
            list-style-type: disc;
        }}
        .report-content ol {{
            list-style-type: decimal;
        }}
        .report-content blockquote {{
            border-left: 4px solid #3b82f6;
            background-color: #eff6ff;
            padding: 0.75rem 1rem;
            border-radius: 0 0.5rem 0.5rem 0;
            margin-bottom: 1.25rem;
            font-size: 0.9rem;
            color: #1e40af;
        }}
        .report-content table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            font-size: 0.875rem;
            background-color: #ffffff;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            border-radius: 0.5rem;
            overflow: hidden;
        }}
        .report-content th {{
            background-color: #1e3a8a;
            color: #ffffff;
            font-weight: 600;
            padding: 0.65rem 0.75rem;
            text-align: left;
            border: 1px solid #cbd5e1;
        }}
        .report-content td {{
            padding: 0.6rem 0.75rem;
            border: 1px solid #e2e8f0;
            vertical-align: middle;
        }}
        .report-content tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        .report-content tr:hover {{
            background-color: #f1f5f9;
        }}
        .report-content strong {{
            color: #0f172a;
        }}
        .report-content code {{
            background-color: #e2e8f0;
            color: #b91c1c;
            padding: 0.15rem 0.35rem;
            border-radius: 0.25rem;
            font-size: 0.85em;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}
        .mermaid {{
            margin: 1.5rem 0;
            text-align: center;
            background: #ffffff;
            padding: 1.25rem;
            border-radius: 0.5rem;
            border: 1px solid #e2e8f0;
        }}
        @media print {{
            body {{
                background-color: #ffffff;
            }}
            .no-print {{
                display: none !important;
            }}
            .report-container {{
                max-width: 100% !important;
                box-shadow: none !important;
                padding: 0 !important;
            }}
            .report-content h2 {{
                break-before: page;
            }}
        }}
    </style>
</head>
<body class="py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto bg-white p-6 sm:p-10 rounded-2xl shadow-md border border-slate-200 report-container">
        <!-- 頂部按鈕列 -->
        <div class="flex items-center justify-between pb-4 border-b border-slate-200 mb-6 no-print">
            <div class="flex items-center gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                    ATTech Materials Official Analytics
                </span>
                <span class="text-xs text-slate-500">2026年9月 vs 10月營運分析</span>
            </div>
            <div class="flex gap-2">
                <button onclick="window.print()" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-medium rounded-lg shadow-sm transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                    列印 / 另存為 PDF
                </button>
            </div>
        </div>

        <!-- 報告主體內容 -->
        <div class="report-content">
            {html_body}
        </div>

        <!-- 頁尾宣告 -->
        <div class="mt-12 pt-6 border-t border-slate-200 text-center text-xs text-slate-500">
            <p>宏威應用材料股份有限公司 • 數位營運與市場分析團隊編製 • 資料來源：GA4 & Google Search Console</p>
            <p class="mt-1">Copyright © 2026 ATTech Materials Co., Ltd. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# Replace mermaid code blocks with <div class="mermaid">
import re
full_html = re.sub(r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>', r'<div class="mermaid">\1</div>', full_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("HTML report successfully written to:", html_path)

