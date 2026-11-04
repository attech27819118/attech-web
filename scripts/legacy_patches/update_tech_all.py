# -*- coding: utf-8 -*-
"""
Update Technology Module and Subpages
1. 將 json/tech_database.json 內容注入 js/technology.js
2. 在 js/technology.js 與 build_technology_subpages.py 中新增「全螢幕放大閱讀」按鈕與模態視窗
3. 移除右欄已不需要之 docType 標籤 (比照手動精簡樣式)
4. 優化 Canvas 渲染 DPR (抗模糊)，讓文字清晰銳利
5. 執行 build_technology_subpages.py 重新產生 11 大子頁面與首頁
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT_DIR, "json", "tech_database.json")
JS_PATH = os.path.join(ROOT_DIR, "js", "technology.js")
SUBPAGES_PY = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    tech_db = json.load(f)

# =========================================================================
# 1. 更新 js/technology.js
# =========================================================================
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 替換 const TECH_DATABASE = { ... };
db_json_str = json.dumps(tech_db, ensure_ascii=False, indent=2)
new_db_declaration = f"const TECH_DATABASE = {db_json_str};\n"

start_marker = "const TECH_DATABASE = {"
start_idx = js_content.find(start_marker)
if start_idx == -1:
    print("Cannot find 'const TECH_DATABASE = {' in js/technology.js")
    sys.exit(1)

end_marker = "\n// 技術專區狀態管理"
end_idx = js_content.find(end_marker, start_idx)
if end_idx == -1:
    end_marker = "const TechState = {"
    end_idx = js_content.rfind("const TechState", start_idx)

if end_idx == -1:
    print("Cannot find end marker of TECH_DATABASE in js/technology.js")
    sys.exit(1)

js_updated = js_content[:start_idx] + new_db_declaration + js_content[end_idx:]

# 替換 js/technology.js 中的 buildSingleDocLayoutHtml 與 PDF.js 渲染部分
# 定位 renderPdfDocumentToContainer 到 buildSingleDocLayoutHtml 的範圍
old_render_marker = "// 全域快取 PDF.js 渲染任務與 PDF Document 物件"
old_render_idx = js_updated.find(old_render_marker)

end_layout_marker = "/**\n * 建立暫無公開資料提示區塊 HTML"
end_layout_idx = js_updated.find(end_layout_marker)

if old_render_idx != -1 and end_layout_idx != -1:
    new_render_and_layout = """// 全域快取 PDF.js 渲染任務與 PDF Document 物件
const techPdfRenderTasks = {};
const techPdfDocCache = {};

/**
 * 使用 PDF.js 將 PDF 多頁渲染至 Canvas 容器 (完全防右鍵另存新檔、高解析度抗模糊、流暢滾動)
 */
async function renderPdfDocumentToContainer(containerId, pdfUrl) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (techPdfRenderTasks[containerId]) {
        techPdfRenderTasks[containerId].cancelled = true;
    }
    const currentTask = { cancelled: false };
    techPdfRenderTasks[containerId] = currentTask;

    container.innerHTML = `
        <div class="flex flex-col items-center justify-center h-full min-h-[360px] text-slate-400 gap-2">
            <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
            <span class="text-xs font-semibold text-slate-600">技術文件載入中...</span>
        </div>
    `;

    try {
        if (typeof window.pdfjsLib === 'undefined') {
            console.warn('PDF.js 未就緒，使用保護視窗模式');
            container.innerHTML = `
                <iframe src="${pdfUrl}#toolbar=0&navpanes=0"
                        class="w-full h-full min-h-[600px] border-0 rounded-lg bg-slate-50"
                        title="技術文件預覽"
                        loading="lazy"></iframe>
            `;
            return;
        }

        window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

        let pdf = techPdfDocCache[pdfUrl];
        if (!pdf) {
            const loadingTask = window.pdfjsLib.getDocument(pdfUrl);
            pdf = await loadingTask.promise;
            techPdfDocCache[pdfUrl] = pdf;
        }
        if (currentTask.cancelled) return;

        container.innerHTML = '';

        const containerWidth = container.clientWidth || 520;
        const targetWidth = Math.max(280, containerWidth - 28);
        const dpr = window.devicePixelRatio || 1;

        // 依序逐頁渲染所有頁面 (採用 DPR 高解析度渲染，字體邊緣銳利清晰)
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            if (currentTask.cancelled) break;

            const page = await pdf.getPage(pageNum);
            if (currentTask.cancelled) break;

            const unscaledViewport = page.getViewport({ scale: 1 });
            const scale = targetWidth / unscaledViewport.width;
            const finalScale = Math.max(1.0, Math.min(scale, 2.5));
            const viewport = page.getViewport({ scale: finalScale * dpr });

            const canvasWrapper = document.createElement('div');
            canvasWrapper.className = 'w-full flex justify-center mb-3 select-none';
            canvasWrapper.setAttribute('oncontextmenu', 'return false;');

            const canvas = document.createElement('canvas');
            canvas.className = 'rounded-lg shadow-xs border border-slate-200 bg-white block max-w-full';
            canvas.style.pointerEvents = 'none';
            canvas.style.userSelect = 'none';
            canvas.style.webkitUserSelect = 'none';
            canvas.style.width = Math.floor(unscaledViewport.width * finalScale) + 'px';
            canvas.style.height = Math.floor(unscaledViewport.height * finalScale) + 'px';

            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            await page.render({
                canvasContext: context,
                viewport: viewport
            }).promise;

            if (currentTask.cancelled) break;

            canvasWrapper.appendChild(canvas);
            container.appendChild(canvasWrapper);
        }
    } catch (err) {
        console.error('PDF.js render error:', err);
        if (!currentTask.cancelled) {
            container.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full min-h-[360px] text-slate-400 gap-2">
                    <i class="fa-solid fa-triangle-exclamation text-amber-500 text-xl"></i>
                    <span class="text-xs font-semibold text-slate-600">文件載入中或格式需重新整理</span>
                </div>
            `;
        }
    }
}

/**
 * 全螢幕放大高解析渲染 (寬版視圖、大字體、高清晰度、無下載功能、支援滾輪與頁碼標示)
 */
async function renderPdfFullscreen(container, pdfUrl) {
    try {
        if (typeof window.pdfjsLib === 'undefined') {
            container.innerHTML = `<iframe src="${pdfUrl}#toolbar=0&navpanes=0" class="w-full h-full min-h-[700px] border-0 rounded-lg"></iframe>`;
            return;
        }

        window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

        let pdf = techPdfDocCache[pdfUrl];
        if (!pdf) {
            const loadingTask = window.pdfjsLib.getDocument(pdfUrl);
            pdf = await loadingTask.promise;
            techPdfDocCache[pdfUrl] = pdf;
        }

        container.innerHTML = '';
        const modalWidth = container.clientWidth || 960;
        const targetWidth = Math.min(920, Math.max(600, modalWidth - 48));
        const dpr = window.devicePixelRatio || 1;

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const unscaledViewport = page.getViewport({ scale: 1 });
            const scale = targetWidth / unscaledViewport.width;
            const finalScale = Math.max(1.3, Math.min(scale, 2.5));
            const viewport = page.getViewport({ scale: finalScale * dpr });

            const canvasWrapper = document.createElement('div');
            canvasWrapper.className = 'w-full flex flex-col items-center mb-6 select-none';
            canvasWrapper.setAttribute('oncontextmenu', 'return false;');

            const pageLabel = document.createElement('div');
            pageLabel.className = 'text-[11px] font-bold text-slate-400 mb-1';
            pageLabel.textContent = `第 ${pageNum} 頁 / 共 ${pdf.numPages} 頁`;

            const canvas = document.createElement('canvas');
            canvas.className = 'rounded-xl shadow-lg border border-slate-300 bg-white block max-w-full';
            canvas.style.pointerEvents = 'none';
            canvas.style.userSelect = 'none';
            canvas.style.webkitUserSelect = 'none';
            canvas.style.width = Math.floor(unscaledViewport.width * finalScale) + 'px';
            canvas.style.height = Math.floor(unscaledViewport.height * finalScale) + 'px';

            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            await page.render({
                canvasContext: context,
                viewport: viewport
            }).promise;

            canvasWrapper.appendChild(pageLabel);
            canvasWrapper.appendChild(canvas);
            container.appendChild(canvasWrapper);
        }
    } catch (err) {
        console.error('Fullscreen render error:', err);
        container.innerHTML = `
            <div class="text-center py-12 text-slate-500">
                <p>文件載入失敗，請重試。</p>
            </div>
        `;
    }
}

/**
 * 開啟 PDF 全螢幕放大檢視模態視窗 (解決預覽視窗字體過小問題，且嚴格禁止下載與另存)
 */
function openPdfFullscreenModal(pdfUrl, title) {
    let modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'tech-pdf-fullscreen-modal';
        modal.className = 'fixed inset-0 z-[9999] bg-slate-950/80 backdrop-blur-sm flex flex-col items-center justify-center p-2 sm:p-4 select-none';
        modal.setAttribute('oncontextmenu', 'return false;');
        modal.innerHTML = `
            <div class="relative w-full max-w-5xl h-[94vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-slate-200">
                <div class="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-200 shrink-0">
                    <div class="flex items-center gap-2.5 min-w-0 pr-3">
                        <span class="w-8 h-8 rounded-lg bg-red-50 text-red-600 flex items-center justify-center shrink-0 border border-red-200">
                            <i class="fa-solid fa-file-pdf text-sm"></i>
                        </span>
                        <div class="min-w-0">
                            <h3 id="tech-modal-title" class="text-sm sm:text-base font-bold text-slate-900 truncate">技術文件全螢幕放大檢視</h3>
                            <p class="text-xs text-slate-500 font-normal">原廠技術文件線上清晰預覽 (不開放下載)</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 shrink-0">
                        <button type="button" onclick="closePdfFullscreenModal()"
                                class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-bold rounded-lg transition-colors cursor-pointer">
                            <i class="fa-solid fa-xmark text-sm"></i>
                            <span>關閉 (ESC)</span>
                        </button>
                    </div>
                </div>
                <div id="tech-modal-pdf-container" class="flex-1 overflow-y-auto p-4 sm:p-6 bg-slate-100 flex flex-col items-center select-none" oncontextmenu="return false;">
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-900"></i>
                        <span class="text-sm font-semibold text-slate-600">全螢幕高解析文件載入中...</span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closePdfFullscreenModal();
        });
    }

    modal.classList.remove('hidden');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    const titleEl = document.getElementById('tech-modal-title');
    if (titleEl) titleEl.textContent = title || '原廠技術文件';

    const container = document.getElementById('tech-modal-pdf-container');
    if (container) {
        container.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full py-16 text-slate-400 gap-2">
                <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-900"></i>
                <span class="text-sm font-semibold text-slate-600">正在以高解析度渲染技術文件...</span>
            </div>
        `;
        renderPdfFullscreen(container, pdfUrl);
    }
}

function closePdfFullscreenModal() {
    const modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
    }
    document.body.style.overflow = '';
}

// 全面攔截在 PDF 預覽與技術專區的右鍵選單與快捷鍵另存
document.addEventListener('contextmenu', function (e) {
    if (e.target.closest('.pdf-viewer-container') || e.target.closest('.tech-principles-grid') || e.target.closest('#tech-pdf-fullscreen-modal')) {
        e.preventDefault();
        return false;
    }
}, true);

window.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S' || e.key === 'p' || e.key === 'P')) {
        const viewer = document.querySelector('.pdf-viewer-container') || document.getElementById('tech-pdf-fullscreen-modal');
        if (viewer) {
            e.preventDefault();
            return false;
        }
    }
});

/**
 * 建立單一文件左右雙欄檢視視圖 HTML (比照原理排版架構，線上預覽不開放下載)
 */
function buildSingleDocLayoutHtml(doc, slug, tabKey) {
    const cat = TECH_CATEGORIES.find(c => c.slug === slug) || { name: '特用化學品', productLink: 'products/' };
    const pdfUrl = getEncodedPdfUrl(doc.pdfPath);

    // 判斷是否為 Tyzor 原理 (有機制圖，依圖 2 指示：tyzor原理已經放了WEBP圖，不需要再另外放PDF)
    const isTyzorPrinciple = (slug === 'tyzor' && tabKey === 'principles' && doc.mechImg);

    let previewBoxHtml = '';
    if (isTyzorPrinciple) {
        // 圖 2：只放 WEBP 反應機制圖，移除被劃掉的標題、移除下方 PDF、移除提示字
        previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col items-center justify-center min-h-[460px] sm:min-h-[560px] overflow-hidden select-none" oncontextmenu="return false;">
                    <div class="text-xs font-bold text-slate-500 mb-3 self-start flex items-center gap-1.5">
                        <i class="fa-solid fa-atom text-blue-900"></i>
                        <span>原廠化學反應機制</span>
                    </div>
                    <img src="${resolveAssetUrl(doc.mechImg)}" alt="${doc.title} 反應機制圖"
                         class="w-full max-h-[420px] sm:max-h-[500px] object-contain rounded select-none pointer-events-none"
                         draggable="false">
                </div>
            </div>
        `;
    } else {
        const viewerId = `pdf-canvas-viewer-${slug}-${tabKey}`;
        const escapedTitle = (doc.title || '').replace(/'/g, "\\\\'").replace(/"/g, '&quot;');
        previewBoxHtml = `
            <div class="h-full flex flex-col">
                <!-- 預覽工具列：支援全螢幕放大閱讀，解決視窗字體過小問題 -->
                <div class="flex items-center justify-between pb-1.5 px-0.5 text-xs text-slate-500">
                    <span class="inline-flex items-center gap-1.5 text-slate-600 font-medium">
                        <i class="fa-solid fa-file-pdf text-red-600"></i>
                        <span>原廠技術文件預覽</span>
                    </span>
                    <button type="button" onclick="openPdfFullscreenModal('${pdfUrl}', '${escapedTitle}')"
                            class="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-bold text-blue-900 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-md shadow-2xs transition-all active:scale-95 cursor-pointer">
                        <i class="fa-solid fa-expand text-[10px]"></i>
                        <span>全螢幕放大閱讀</span>
                    </button>
                </div>
                <div id="${viewerId}"
                     class="pdf-viewer-container w-full h-[620px] sm:h-[680px] rounded-xl border border-slate-200 bg-slate-100/70 p-2 sm:p-3 overflow-y-auto select-none"
                     data-pdf-url="${pdfUrl}"
                     data-pdf-title="${escapedTitle}"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">技術文件載入中...</span>
                    </div>
                </div>
            </div>
        `;
    }

    const advantagesHtml = (doc.advantages || []).map((adv, idx) => `
        <li class="flex items-start gap-1.5">
            <span class="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">${idx + 1}</span>
            <span>${adv}</span>
        </li>
    `).join('');

    const appsHtml = (doc.applications || []).map(app => `
        <span class="px-2 py-0.5 rounded bg-white text-slate-700 text-xs font-medium border border-slate-200">${app}</span>
    `).join('');

    return `
        <div class="tech-principles-grid bg-slate-50/70 rounded-xl border border-slate-200 p-3 sm:p-3.5">
            <!-- 左欄：線上文件瀏覽視窗 (視窗拉長補滿空白，無下載按鈕，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
                ${previewBoxHtml}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 (依圖 1 指示：移除被劃掉的語言/版本標籤與檔案名字串) -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        ${doc.title}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    ${doc.desc}
                </p>

                <!-- 主要技術特點 (深度提煉之真實數據與技術重點) -->
                <div class="space-y-1.5">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
                    <ul class="space-y-1 text-sm text-slate-700">
                        ${advantagesHtml}
                    </ul>
                </div>

                <!-- 適用範疇標籤 -->
                <div class="space-y-1 pt-0.5">
                    <span class="text-xs font-bold text-slate-700">原廠適用範疇 / 相關領域：</span>
                    <div class="flex flex-wrap gap-1">
                        ${appsHtml}
                    </div>
                </div>

                <!-- 諮詢動作列 -->
                <div class="pt-2 flex flex-wrap items-center gap-2 border-t border-slate-200">
                    <a href="contact/?mode=detailed&inquiry=${encodeURIComponent(cat.name + '-' + doc.title)}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                        <i class="fa-solid fa-envelope text-xs"></i>
                        <span>索取規格諮詢 / 申請樣品</span>
                    </a>
                    <a href="${cat.productLink}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>查看相關產品列表</span>
                    </a>
                </div>
            </div>
        </div>
    `;
}
\n"""

    js_updated = js_updated[:old_render_idx] + new_render_and_layout + js_updated[end_layout_idx:]

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_updated)
print(f"Updated {JS_PATH} successfully!")

# =========================================================================
# 2. 更新 scripts/build_technology_subpages.py 中的 build_single_doc_layout_html
# =========================================================================
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_content = f.read()

# 替換 build_single_doc_layout_html 函數
target_func_start = "def build_single_doc_layout_html(doc, slug, tab_key, item):"
target_func_end = "def build_empty_tab_html(item, tab_key):"

start_p = py_content.find(target_func_start)
end_p = py_content.find(target_func_end)

if start_p != -1 and end_p != -1:
    new_func = '''def build_single_doc_layout_html(doc, slug, tab_key, item):
    """產生單一文件左右雙欄檢視視圖 (比照原理排版架構，線上預覽不開放下載)"""
    pdf_url = get_encoded_pdf_url(doc.get("pdfPath", ""))
    is_tyzor_principle = (slug == "tyzor" and tab_key == "principles" and doc.get("mechImg"))

    if is_tyzor_principle:
        # 圖 2：只放 WEBP 反應機制圖，移除被劃掉的標題、移除下方 PDF、移除提示字
        preview_box_html = f\'\'\'            <div class="h-full flex flex-col justify-center">
                <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col items-center justify-center min-h-[460px] sm:min-h-[560px] overflow-hidden select-none" oncontextmenu="return false;">
                    <div class="text-xs font-bold text-slate-500 mb-3 self-start flex items-center gap-1.5">
                        <i class="fa-solid fa-atom text-blue-900"></i>
                        <span>原廠化學反應機制</span>
                    </div>
                    <img src="{doc.get("mechImg")}" alt="{doc.get("title")} 反應機制圖"
                         class="w-full max-h-[420px] sm:max-h-[500px] object-contain rounded select-none pointer-events-none"
                         draggable="false">
                </div>
            </div>\'\'\'
    else:
        # 圖 1：PDF 預覽視窗，拉長補足剩下空白 (h-[620px] sm:h-[680px])，增加「全螢幕放大閱讀」按鈕解決字體過小問題
        viewer_id = f"pdf-canvas-viewer-{slug}-{tab_key}"
        doc_title_clean = doc.get("title", "").replace('"', '&quot;').replace("'", "&#39;")
        preview_box_html = f\'\'\'            <div class="h-full flex flex-col">
                <div class="flex items-center justify-between pb-1.5 px-0.5 text-xs text-slate-500">
                    <span class="inline-flex items-center gap-1.5 text-slate-600 font-medium">
                        <i class="fa-solid fa-file-pdf text-red-600"></i>
                        <span>原廠技術文件預覽</span>
                    </span>
                    <button type="button" onclick="openPdfFullscreenModal(\'{pdf_url}\', \'{doc_title_clean}\')"
                            class="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-bold text-blue-900 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-md shadow-2xs transition-all active:scale-95 cursor-pointer">
                        <i class="fa-solid fa-expand text-[10px]"></i>
                        <span>全螢幕放大閱讀</span>
                    </button>
                </div>
                <div id="{viewer_id}"
                     class="pdf-viewer-container w-full h-[620px] sm:h-[680px] rounded-xl border border-slate-200 bg-slate-100/70 p-2 sm:p-3 overflow-y-auto select-none"
                     data-pdf-url="{pdf_url}"
                     data-pdf-title="{doc_title_clean}"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">技術文件載入中...</span>
                    </div>
                </div>
            </div>\'\'\'

    advantages_items = []
    for idx, adv in enumerate(doc.get("advantages", [])):
        adv_li = f\'\'\'                        <li class="flex items-start gap-1.5">
                            <span class="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">{idx + 1}</span>
                            <span>{adv}</span>
                        </li>\'\'\'
        advantages_items.append(adv_li)
    advantages_html = "\\n".join(advantages_items)

    apps_items = []
    for app in doc.get("applications", []):
        app_span = f\'\'\'                            <span class="px-2 py-0.5 rounded bg-white text-slate-700 text-xs font-medium border border-slate-200">{app}</span>\'\'\'
        apps_items.append(app_span)
    apps_html = "\\n".join(apps_items)

    inquiry_title = f"{item['menu_name']}-{doc.get('title')}"

    return f\'\'\'        <div class="tech-principles-grid bg-slate-50/70 rounded-xl border border-slate-200 p-3 sm:p-3.5">
            <!-- 左欄：線上文件瀏覽視窗 (視窗拉長補滿空白，無下載按鈕，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
{preview_box_html}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 (依圖 1 指示：移除被劃掉的語言/版本標籤與檔案名字串) -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        {doc.get("title")}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    {doc.get("desc")}
                </p>

                <!-- 主要技術特點 -->
                <div class="space-y-1.5">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
                    <ul class="space-y-1 text-sm text-slate-700">
{advantages_html}
                    </ul>
                </div>

                <!-- 適用範疇標籤 -->
                <div class="space-y-1 pt-0.5">
                    <span class="text-xs font-bold text-slate-700">原廠適用範疇 / 相關領域：</span>
                    <div class="flex flex-wrap gap-1">
{apps_html}
                    </div>
                </div>

                <!-- 諮詢動作列 -->
                <div class="pt-2 flex flex-wrap items-center gap-2 border-t border-slate-200">
                    <a href="contact/?mode=detailed&inquiry={urllib.parse.quote(inquiry_title)}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                        <i class="fa-solid fa-envelope text-xs"></i>
                        <span>索取規格諮詢 / 申請樣品</span>
                    </a>
                    <a href="{item["product_link"]}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>查看相關產品列表</span>
                    </a>
                </div>
            </div>
        </div>\'\'\'

'''
    py_content = py_content[:start_p] + new_func + py_content[end_p:]
    with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
        f.write(py_content)
    print(f"Updated {SUBPAGES_PY} successfully!")
else:
    print("Warning: target function in build_technology_subpages.py not found")

