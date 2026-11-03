# -*- coding: utf-8 -*-
"""
Update PDF preview into interactive Cover and remove standalone Fullscreen button
1. 每一份技術文件左欄容器只渲染第 1 頁作為精美封面 (Cover)
2. 整個封面具備 cursor-pointer 與 hover 懸浮「點擊全螢幕放大閱讀」質感標籤
3. 點擊封面任意處立即開啟全螢幕高解析閱讀器 (支援多頁滾動、手動縮放、ESC/遮罩關閉)
4. 移除原本位於預覽盒上方的「全螢幕放大閱讀」獨立按鈕
5. 針對 Tyzor 原理反應機制圖亦支援點擊全螢幕放大
6. 重新編譯 11 大獨立技術子專頁與首頁
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_PATH = os.path.join(ROOT_DIR, "js", "technology.js")
SUBPAGES_PY = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")

# =========================================================================
# 1. 更新 scripts/build_technology_subpages.py
# =========================================================================
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_content = f.read()

# 替換 build_single_doc_layout_html 函數中的 preview_box_html
target_func_start = "def build_single_doc_layout_html(doc, slug, tab_key, item):"
target_func_end = "    advantages_items = []"

start_idx = py_content.find(target_func_start)
end_idx = py_content.find(target_func_end, start_idx)

if start_idx != -1 and end_idx != -1:
    new_func_top = '''def build_single_doc_layout_html(doc, slug, tab_key, item):
    """產生單一文件左右雙欄檢視視圖 (封面式預覽，點擊封面即開啟全螢幕高解析閱讀器)"""
    pdf_url = get_encoded_pdf_url(doc.get("pdfPath", ""))
    is_tyzor_principle = (slug == "tyzor" and tab_key == "principles" and doc.get("mechImg"))
    doc_title_clean = doc.get("title", "").replace('"', '&quot;').replace("'", "&#39;")

    if is_tyzor_principle:
        # 圖 2：Tyzor 反應機制圖 (點擊即可全螢幕放大檢視)
        preview_box_html = f\'\'\'            <div class="h-full flex flex-col justify-center">
                <div class="group relative bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col items-center justify-center min-h-[460px] sm:min-h-[560px] overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-400 hover:shadow-md"
                     onclick="openImageFullscreenModal(\'{doc.get("mechImg")}\', \'{doc_title_clean} 反應機制圖\')"
                     title="點擊全螢幕放大檢視"
                     oncontextmenu="return false;">
                    <div class="text-xs font-bold text-slate-500 mb-3 self-start flex items-center gap-1.5">
                        <i class="fa-solid fa-atom text-blue-900"></i>
                        <span>原廠化學反應機制</span>
                    </div>
                    <img src="{doc.get("mechImg")}" alt="{doc.get("title")} 反應機制圖"
                         class="w-full max-h-[420px] sm:max-h-[500px] object-contain rounded select-none pointer-events-none transition-transform duration-200 group-hover:scale-[1.02]"
                         draggable="false">

                    <!-- 懸浮提示：點擊全螢幕放大檢視 -->
                    <div class="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center pointer-events-none z-10 backdrop-blur-[1px]">
                        <span class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-blue-950/90 text-white text-xs font-bold shadow-xl border border-white/20 transform translate-y-1 group-hover:translate-y-0 transition-transform duration-200">
                            <i class="fa-solid fa-expand text-xs"></i>
                            <span>點擊全螢幕放大檢視</span>
                        </span>
                    </div>
                </div>
            </div>\'\'\'
    else:
        # 文件封面卡片：第一頁作為封面，點擊封面即可全螢幕放大閱讀，移除獨立全螢幕按鈕
        viewer_id = f"pdf-canvas-viewer-{slug}-{tab_key}"
        preview_box_html = f\'\'\'            <div class="h-full flex flex-col justify-center">
                <div id="{viewer_id}"
                     class="pdf-viewer-container group relative w-full h-[580px] sm:h-[640px] rounded-xl border border-slate-200 bg-slate-100/70 p-2 sm:p-3 flex items-center justify-center overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-400 hover:shadow-md"
                     data-pdf-url="{pdf_url}"
                     data-pdf-title="{doc_title_clean}"
                     onclick="openPdfFullscreenModal(\'{pdf_url}\', \'{doc_title_clean}\')"
                     title="點擊全螢幕放大閱讀"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">文件封面載入中...</span>
                    </div>

                    <!-- 懸浮提示：點擊全螢幕放大閱讀 -->
                    <div class="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center pointer-events-none z-10 backdrop-blur-[1px]">
                        <span class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-blue-950/90 text-white text-xs font-bold shadow-xl border border-white/20 transform translate-y-1 group-hover:translate-y-0 transition-transform duration-200">
                            <i class="fa-solid fa-expand text-xs"></i>
                            <span>點擊全螢幕放大閱讀</span>
                        </span>
                    </div>
                </div>
            </div>\'\'\'

'''
    py_content = py_content[:start_idx] + new_func_top + py_content[end_idx:]
    with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
        f.write(py_content)
    print(f"Updated {SUBPAGES_PY} with cover layout!")

# =========================================================================
# 2. 更新 js/technology.js
# =========================================================================
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 替換 renderPdfDocumentToContainer：只渲染第 1 頁作為封面
old_render_start = "async function renderPdfDocumentToContainer(containerId, pdfUrl) {"
old_render_idx = js_content.find(old_render_start)

old_fullscreen_marker = "async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {"
old_fullscreen_idx = js_content.find(old_fullscreen_marker)

if old_render_idx != -1 and old_fullscreen_idx != -1:
    new_render_func = '''async function renderPdfDocumentToContainer(containerId, pdfUrl) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (techPdfRenderTasks[containerId]) {
        techPdfRenderTasks[containerId].cancelled = true;
    }
    const currentTask = { cancelled: false };
    techPdfRenderTasks[containerId] = currentTask;

    const cleanPdfUrl = pdfUrl.split('#')[0];

    try {
        if (typeof window.pdfjsLib === 'undefined') {
            console.warn('PDF.js 未就緒');
            return;
        }

        window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

        let pdf = techPdfDocCache[cleanPdfUrl];
        if (!pdf) {
            const loadingTask = window.pdfjsLib.getDocument(cleanPdfUrl);
            pdf = await loadingTask.promise;
            techPdfDocCache[cleanPdfUrl] = pdf;
        }
        if (currentTask.cancelled) return;

        // 僅渲染第 1 頁作為高清技術文件封面 (Cover)
        const page = await pdf.getPage(1);
        if (currentTask.cancelled) return;

        const containerWidth = container.clientWidth || 520;
        const targetWidth = Math.max(280, containerWidth - 24);
        const dpr = window.devicePixelRatio || 1;

        const unscaledViewport = page.getViewport({ scale: 1 });
        const scale = targetWidth / unscaledViewport.width;
        const finalScale = Math.max(1.0, scale);
        const viewport = page.getViewport({ scale: finalScale * dpr });

        const canvasWrapper = document.createElement('div');
        canvasWrapper.className = 'w-full flex justify-center select-none';
        canvasWrapper.setAttribute('oncontextmenu', 'return false;');
        canvasWrapper.setAttribute('draggable', 'false');

        const canvas = document.createElement('canvas');
        canvas.className = 'rounded-lg shadow-sm border border-slate-200 bg-white block max-w-full transition-transform duration-200 group-hover:scale-[1.01]';
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

        if (currentTask.cancelled) return;

        // 移除載入轉圈文字
        const loadingEl = container.querySelector('.text-slate-400');
        if (loadingEl) loadingEl.remove();

        // 插入封面 Canvas (置於最前，保留 hover 浮層)
        canvasWrapper.appendChild(canvas);
        container.prepend(canvasWrapper);
    } catch (err) {
        console.error('PDF.js cover render error:', err);
    }
}

'''
    js_content = js_content[:old_render_idx] + new_render_func + js_content[old_fullscreen_idx:]

# 替換 js/technology.js 中的 buildSingleDocLayoutHtml
old_build_start = "function buildSingleDocLayoutHtml(doc, slug, tabKey) {"
old_build_idx = js_content.find(old_build_start)

old_build_end_marker = "/**\n * 建立暫無公開資料提示區塊 HTML\n */"
old_build_end_idx = js_content.find(old_build_end_marker)

if old_build_idx != -1 and old_build_end_idx != -1:
    new_js_layout_func = '''function buildSingleDocLayoutHtml(doc, slug, tabKey) {
    const cat = TECH_CATEGORIES.find(c => c.slug === slug) || { name: '特用化學品', productLink: 'products/' };
    const pdfUrl = getEncodedPdfUrl(doc.pdfPath);
    const isTyzorPrinciple = (slug === 'tyzor' && tabKey === 'principles' && doc.mechImg);
    const escapedTitle = (doc.title || '').replace(/'/g, "\\\\'").replace(/"/g, '&quot;');

    let previewBoxHtml = '';
    if (isTyzorPrinciple) {
        // 圖 2：Tyzor 反應機制圖 (點擊即可全螢幕放大檢視)
        previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div class="group relative bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col items-center justify-center min-h-[460px] sm:min-h-[560px] overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-400 hover:shadow-md"
                     onclick="openImageFullscreenModal('${resolveAssetUrl(doc.mechImg)}', '${escapedTitle} 反應機制圖')"
                     title="點擊全螢幕放大檢視"
                     oncontextmenu="return false;">
                    <div class="text-xs font-bold text-slate-500 mb-3 self-start flex items-center gap-1.5">
                        <i class="fa-solid fa-atom text-blue-900"></i>
                        <span>原廠化學反應機制</span>
                    </div>
                    <img src="${resolveAssetUrl(doc.mechImg)}" alt="${doc.title} 反應機制圖"
                         class="w-full max-h-[420px] sm:max-h-[500px] object-contain rounded select-none pointer-events-none transition-transform duration-200 group-hover:scale-[1.02]"
                         draggable="false">

                    <div class="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center pointer-events-none z-10 backdrop-blur-[1px]">
                        <span class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-blue-950/90 text-white text-xs font-bold shadow-xl border border-white/20 transform translate-y-1 group-hover:translate-y-0 transition-transform duration-200">
                            <i class="fa-solid fa-expand text-xs"></i>
                            <span>點擊全螢幕放大檢視</span>
                        </span>
                    </div>
                </div>
            </div>
        `;
    } else {
        const viewerId = `pdf-canvas-viewer-${slug}-${tabKey}`;
        previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div id="${viewerId}"
                     class="pdf-viewer-container group relative w-full h-[580px] sm:h-[640px] rounded-xl border border-slate-200 bg-slate-100/70 p-2 sm:p-3 flex items-center justify-center overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-400 hover:shadow-md"
                     data-pdf-url="${pdfUrl}"
                     data-pdf-title="${escapedTitle}"
                     onclick="openPdfFullscreenModal('${pdfUrl}', '${escapedTitle}')"
                     title="點擊全螢幕放大閱讀"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">文件封面載入中...</span>
                    </div>

                    <!-- 懸浮提示：點擊全螢幕放大閱讀 -->
                    <div class="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center pointer-events-none z-10 backdrop-blur-[1px]">
                        <span class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-blue-950/90 text-white text-xs font-bold shadow-xl border border-white/20 transform translate-y-1 group-hover:translate-y-0 transition-transform duration-200">
                            <i class="fa-solid fa-expand text-xs"></i>
                            <span>點擊全螢幕放大閱讀</span>
                        </span>
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
            <!-- 左欄：線上文件封面預覽 (點擊封面直接全螢幕放大閱讀，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
                ${previewBoxHtml}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        ${doc.title}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    ${doc.desc}
                </p>

                <!-- 主要技術特點 -->
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
'''
    js_content = js_content[:old_build_idx] + new_js_layout_func + js_content[old_build_end_idx:]

# 新增 openImageFullscreenModal 函數 (若尚未存在)
if "function openImageFullscreenModal" not in js_content:
    img_modal_code = '''
/**
 * 開啟圖片全螢幕檢視模態視窗 (供 Tyzor 反應機制圖使用)
 */
function openImageFullscreenModal(imgUrl, title) {
    let modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (!modal) {
        openPdfFullscreenModal('', title);
        modal = document.getElementById('tech-pdf-fullscreen-modal');
    }

    modal.classList.remove('hidden');
    modal.style.setProperty('display', 'flex', 'important');
    modal.style.setProperty('z-index', '99999', 'important');
    document.body.style.overflow = 'hidden';

    const titleEl = document.getElementById('tech-modal-title');
    if (titleEl) titleEl.textContent = title || '原廠反應機制圖';

    const container = document.getElementById('tech-modal-pdf-container');
    if (container) {
        container.innerHTML = `
            <div class="flex items-center justify-center h-full p-4">
                <img src="${imgUrl}" alt="${title}" class="max-w-full max-h-[82vh] object-contain rounded-xl shadow-lg bg-white p-3 border border-slate-200" draggable="false">
            </div>
        `;
    }
}
'''
    insert_pos = js_content.find("function closePdfFullscreenModal()")
    if insert_pos != -1:
        js_content = js_content[:insert_pos] + img_modal_code + "\n" + js_content[insert_pos:]

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Updated {JS_PATH} with cover click & removed fullscreen button!")

