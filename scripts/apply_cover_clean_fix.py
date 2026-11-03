import os
import re

ROOT_DIR = r"d:\Jay\vscode\attech0824 - test"
SUBPAGES_PY = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")
JS_PATH = os.path.join(ROOT_DIR, "js", "technology.js")
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")

print("--- Step 1: Updating scripts/build_technology_subpages.py ---")
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_content = f.read()

# 替換 build_single_doc_layout_html 中的 preview_box_html (移除浮動按鈕/標籤，保持純封面點擊)
old_preview_pat = re.compile(
    r'(# 文件封面卡片：第一頁作為封面.*?preview_box_html = f\'\'\'.*?)(<!-- 懸浮提示：點擊全螢幕放大閱讀 -->.*?</span>\s*</div>\s*)(</div>\s*</div>\'\'\')',
    re.DOTALL
)

if old_preview_pat.search(py_content):
    py_content = old_preview_pat.sub(r'\1\3', py_content)
    print("Found and removed floating hover button from build_single_doc_layout_html in python script.")
else:
    print("Pattern for floating hover button not directly matched, performing targeted replacement...")
    # 手動替換
    old_box = '''                    <!-- 懸浮提示：點擊全螢幕放大閱讀 -->
                    <div class="absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center pointer-events-none z-10 backdrop-blur-[1px]">
                        <span class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-blue-950/90 text-white text-xs font-bold shadow-xl border border-white/20 transform translate-y-1 group-hover:translate-y-0 transition-transform duration-200">
                            <i class="fa-solid fa-expand text-xs"></i>
                            <span>點擊全螢幕放大閱讀</span>
                        </span>
                    </div>'''
    if old_box in py_content:
        py_content = py_content.replace(old_box + "\n", "")
        print("Replaced old_box successfully.")
    else:
        print("old_box was not found, check content.")

# 更新版本號至 20261007_cover2
py_content = re.sub(r'js/technology\.js\?v=[^"\'`]*', 'js/technology.js?v=20261007_cover2', py_content)

with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
    f.write(py_content)
print("Updated scripts/build_technology_subpages.py")


print("\n--- Step 2: Updating js/technology.js ---")
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. 替換 renderPdfDocumentToContainer 函數
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

        // 僅渲染第 1 頁作為技術文件封面 (Cover)，計算等比例縮放，絕不拉伸變形
        const page = await pdf.getPage(1);
        if (currentTask.cancelled) return;

        let containerWidth = container.clientWidth;
        let containerHeight = container.clientHeight;
        if (!containerWidth || containerWidth < 200) {
            containerWidth = container.offsetWidth || Math.min(520, window.innerWidth - 48);
        }
        if (!containerHeight || containerHeight < 300) {
            containerHeight = container.offsetHeight || (window.innerWidth >= 640 ? 640 : 580);
        }
        const availWidth = Math.max(200, containerWidth - 24);
        const availHeight = Math.max(300, containerHeight - 24);

        const unscaledViewport = page.getViewport({ scale: 1 });
        
        // 嚴格等比例縮放：取寬與高容納比率的較小者，保證完整保留原文件版面比例，完全不拉伸
        const scaleW = availWidth / unscaledViewport.width;
        const scaleH = availHeight / unscaledViewport.height;
        const fitScale = Math.min(scaleW, scaleH);

        const dpr = window.devicePixelRatio || 1;
        const viewport = page.getViewport({ scale: fitScale * dpr });

        const canvasWrapper = document.createElement('div');
        canvasWrapper.className = 'cover-canvas-wrapper w-full h-full flex items-center justify-center p-2 select-none pointer-events-none';
        canvasWrapper.setAttribute('oncontextmenu', 'return false;');
        canvasWrapper.setAttribute('draggable', 'false');

        const canvas = document.createElement('canvas');
        canvas.className = 'rounded-lg shadow-sm border border-slate-200 bg-white block transition-transform duration-200 group-hover:scale-[1.01] pointer-events-none select-none';
        canvas.style.userSelect = 'none';
        canvas.style.webkitUserSelect = 'none';
        const cssW = Math.floor(unscaledViewport.width * fitScale);
        const cssH = Math.floor(unscaledViewport.height * fitScale);
        canvas.style.width = cssW + 'px';
        canvas.style.height = cssH + 'px';
        canvas.style.maxWidth = '100%';
        canvas.style.maxHeight = '100%';
        canvas.style.objectFit = 'contain';
        canvas.style.aspectRatio = `${unscaledViewport.width} / ${unscaledViewport.height}`;

        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        await page.render({
            canvasContext: context,
            viewport: viewport
        }).promise;

        if (currentTask.cancelled) return;

        // 移除載入轉圈文字及可能存在的舊 canvas
        container.querySelectorAll('.loading-spinner, .text-slate-400, .cover-canvas-wrapper').forEach(el => el.remove());

        // 插入封面 Canvas
        canvasWrapper.appendChild(canvas);
        container.appendChild(canvasWrapper);
    } catch (err) {
        console.error('PDF.js cover render error:', err);
    }
}'''

# 尋找 renderPdfDocumentToContainer 起迄點
render_start_idx = js_content.find("async function renderPdfDocumentToContainer(containerId, pdfUrl) {")
render_end_idx = js_content.find("async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {")

if render_start_idx != -1 and render_end_idx != -1:
    js_content = js_content[:render_start_idx] + new_render_func + "\n\n" + js_content[render_end_idx:]
    print("Replaced renderPdfDocumentToContainer in js/technology.js successfully!")
else:
    print("❌ Could not locate renderPdfDocumentToContainer markers in js/technology.js")

# 2. 替換 buildSingleDocLayoutHtml
new_build_single_doc = '''function buildSingleDocLayoutHtml(doc, slug, tabKey) {
    const cat = TECH_CATEGORIES.find(c => c.slug === slug) || { name: '特用化學品', productLink: 'products/' };
    const pdfUrl = getEncodedPdfUrl(doc.pdfPath);
    const isTyzorPrinciple = (slug === 'tyzor' && tabKey === 'principles' && doc.mechImg);
    const escapedTitle = (doc.title || '').replace(/'/g, "\\\\'").replace(/"/g, '&quot;');

    let previewBoxHtml = '';
    if (isTyzorPrinciple) {
        // 圖 2：Tyzor 反應機制圖 (純靜態展示，不需要點擊放大支援)
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
        previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div id="${viewerId}"
                     class="pdf-viewer-container group relative w-full h-[580px] sm:h-[640px] rounded-xl border border-slate-200 bg-white p-3 flex items-center justify-center overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-500 hover:shadow-lg"
                     data-pdf-url="${pdfUrl}"
                     data-pdf-title="${escapedTitle}"
                     onclick="openPdfFullscreenModal('${pdfUrl}', '${escapedTitle}')"
                     title="點擊封面全螢幕放大閱讀"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    
                    <div class="loading-spinner flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">文件封面載入中...</span>
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

    const applicationsHtml = (doc.applications || []).map(app => `
        <span class="px-2 py-0.5 rounded bg-white text-slate-700 text-xs font-medium border border-slate-200">${app}</span>
    `).join('');

    const docTitleClean = (doc.title || '').replace(/"/g, '&quot;');
    const inquiryParam = encodeURIComponent(`${cat.name}-${doc.title || ''}`);
    const productLink = cat.productLink || 'products/';

    return `
        <div class="tech-principles-grid bg-slate-50/70 rounded-xl border border-slate-200 p-3 sm:p-3.5">
            <!-- 左欄：線上文件封面預覽 (點擊封面直接全螢幕放大閱讀，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
                ${previewBoxHtml}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 (依圖 1 指示：移除被劃掉的語言/版本標籤與檔案名字串) -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        ${docTitleClean}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    ${doc.summary || ''}
                </p>

                ${advantagesHtml ? `
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
                ` : ''}

                ${applicationsHtml ? `
                <!-- 適用範疇標籤 -->
                <div class="space-y-1 pt-0.5">
                    <span class="text-xs font-bold text-slate-700">原廠適用範疇 / 相關領域：</span>
                    <div class="flex flex-wrap gap-1">
                        ${applicationsHtml}
                    </div>
                </div>
                ` : ''}

                <!-- 諮詢動作列 -->
                <div class="pt-2 flex flex-wrap items-center gap-2 border-t border-slate-200">
                    <a href="contact/?mode=detailed&inquiry=${inquiryParam}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                        <i class="fa-solid fa-envelope text-xs"></i>
                        <span>索取規格諮詢 / 申請樣品</span>
                    </a>
                    <a href="${productLink}"
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>查看相關產品列表</span>
                    </a>
                </div>
            </div>
        </div>
    `;
}'''

single_start_idx = js_content.find("function buildSingleDocLayoutHtml(doc, slug, tabKey) {")
single_end_idx = js_content.find("function buildCategoryContentHtml(cat) {")

if single_start_idx != -1 and single_end_idx != -1:
    js_content = js_content[:single_start_idx] + new_build_single_doc + "\n\n" + js_content[single_end_idx:]
    print("Replaced buildSingleDocLayoutHtml in js/technology.js successfully!")
else:
    print("❌ Could not locate buildSingleDocLayoutHtml markers in js/technology.js")

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated js/technology.js successfully!")
