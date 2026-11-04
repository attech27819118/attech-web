import os
import re

ROOT_DIR = r"d:\Jay\vscode\attech0824 - test"
SUBPAGES_PY = os.path.join(ROOT_DIR, "scripts", "build_technology_subpages.py")
JS_PATH = os.path.join(ROOT_DIR, "js", "technology.js")

print("=== 1. Updating scripts/build_technology_subpages.py CSS ===")
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_code = f.read()

# 替換 #tech-pdf-fullscreen-modal 相關 CSS 為真正的 100vw x 100vh 全畫面
old_css_pat = re.compile(
    r'(/\* 全螢幕技術文件預覽模態視窗.*?#tech-pdf-fullscreen-modal\s*\{{.*?#tech-pdf-fullscreen-modal \.tech-modal-inner\s*\{{.*?\}}\s*)',
    re.DOTALL
)

new_fullscreen_css = '''/* 全螢幕技術文件預覽模態視窗 (全畫面滿版沉浸式閱讀，絕不被任何元素遮擋) */
        #tech-pdf-fullscreen-modal {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 99999 !important;
            background: #0f172a !important;
            display: flex !important;
            flex-direction: column !important;
            box-sizing: border-box !important;
        }
        #tech-pdf-fullscreen-modal.hidden {
            display: none !important;
        }
        #tech-pdf-fullscreen-modal .tech-modal-inner {
            position: relative !important;
            z-index: 100000 !important;
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            border-radius: 0 !important;
            border: none !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            background: #0f172a !important;
            overflow: hidden !important;
        }
'''

if old_css_pat.search(py_code):
    py_code = old_css_pat.sub(new_fullscreen_css.replace('{', '{{').replace('}', '}}'), py_code)
    print("Replaced fullscreen CSS in python script.")
else:
    print("Direct pattern match failed, trying alternative match...")
    start_m = py_code.find("/* 全螢幕技術文件預覽模態視窗")
    end_m = py_code.find(".tech-principles-grid {{", start_m)
    if start_m != -1 and end_m != -1:
        py_code = py_code[:start_m] + new_fullscreen_css.replace('{', '{{').replace('}', '}}') + py_code[end_m:]
        print("Replaced fullscreen CSS by boundary markers.")

# 更新快取破壞版本號至 20261007_fullscreen1
py_code = re.sub(r'js/technology\.js\?v=[^"\'`]*', 'js/technology.js?v=20261007_fullscreen1', py_code)

with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
    f.write(py_code)
print("Updated scripts/build_technology_subpages.py successfully!")


print("\n=== 2. Updating js/technology.js ===")
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_code = f.read()

# 替換 openPdfFullscreenModal 與 renderPdfFullscreen 函數
new_open_modal_func = '''/**
 * 開啟 PDF 全螢幕滿版檢視模態視窗 (真正全畫面滿版閱讀，支援縮放與鍵盤導航)
 */
function openPdfFullscreenModal(pdfUrl, title) {
    let modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'tech-pdf-fullscreen-modal';
        modal.style.cssText = 'position:fixed!important;top:0!important;left:0!important;right:0!important;bottom:0!important;width:100vw!important;height:100vh!important;margin:0!important;padding:0!important;z-index:99999!important;background:#0f172a!important;display:flex!important;flex-direction:column!important;box-sizing:border-box!important;';
        modal.setAttribute('oncontextmenu', 'return false;');
        modal.innerHTML = `
            <div class="tech-modal-inner relative w-screen h-screen flex flex-col bg-slate-900 overflow-hidden"
                 style="z-index:100000!important;width:100vw!important;height:100vh!important;max-width:100vw!important;max-height:100vh!important;border-radius:0!important;border:none!important;"
                 onclick="event.stopPropagation();">
                
                <!-- 頂部滿版操作列 -->
                <div class="flex items-center justify-between px-3 sm:px-6 py-2.5 bg-slate-900 border-b border-slate-800 shrink-0 gap-3 text-white"
                     style="z-index:100001!important;">
                    <div class="flex items-center gap-2.5 sm:gap-3 min-w-0 pr-2">
                        <span class="w-8 h-8 rounded-lg bg-red-500/20 text-red-400 flex items-center justify-center shrink-0 border border-red-500/30">
                            <i class="fa-solid fa-file-pdf text-sm"></i>
                        </span>
                        <div class="min-w-0">
                            <h3 id="tech-modal-title" class="text-sm sm:text-base font-bold text-white truncate leading-snug">技術文件全畫面閱讀</h3>
                            <div class="flex items-center gap-2 text-[11px] text-slate-400">
                                <span class="inline-flex items-center gap-1 text-emerald-400 font-medium">
                                    <i class="fa-solid fa-shield-halved text-[10px]"></i>
                                    <span>線上安全瀏覽</span>
                                </span>
                                <span class="hidden sm:inline text-slate-600">•</span>
                                <span class="hidden sm:inline text-slate-400">嚴格防複製 / 不開放下載</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 縮放工具列與關閉按鈕 -->
                    <div class="flex items-center gap-2 sm:gap-3 shrink-0">
                        <div class="flex items-center bg-slate-800 border border-slate-700 rounded-lg p-0.5 shadow-sm text-slate-300">
                            <button type="button" onclick="changeFullscreenZoom(-0.2)" title="縮小"
                                    class="w-7 sm:w-8 h-7 sm:h-8 flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <i class="fa-solid fa-magnifying-glass-minus text-xs"></i>
                            </button>
                            <button type="button" onclick="resetFullscreenZoom()" title="重設為 100%"
                                    class="px-2 sm:px-2.5 h-7 sm:h-8 text-xs font-bold text-slate-200 hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <span id="tech-modal-zoom-val">100%</span>
                            </button>
                            <button type="button" onclick="changeFullscreenZoom(0.2)" title="放大"
                                    class="w-7 sm:w-8 h-7 sm:h-8 flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <i class="fa-solid fa-magnifying-glass-plus text-xs"></i>
                            </button>
                        </div>

                        <button type="button" onclick="closePdfFullscreenModal()"
                                class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-1.5 sm:py-2 bg-red-600 hover:bg-red-500 text-white text-xs sm:text-sm font-bold rounded-lg shadow-sm transition-colors cursor-pointer">
                            <i class="fa-solid fa-xmark text-sm"></i>
                            <span>關閉 (ESC)</span>
                        </button>
                    </div>
                </div>

                <!-- 全畫面滿版 PDF 渲染容器 -->
                <div id="tech-modal-pdf-container"
                     class="flex-1 w-full h-full overflow-y-auto overflow-x-auto p-4 sm:p-8 bg-slate-950 flex flex-col items-center select-none"
                     style="scroll-behavior: smooth;"
                     oncontextmenu="return false;">
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-400"></i>
                        <span class="text-sm font-semibold text-slate-300">全畫面高解析文件載入中...</span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // 綁定 ESC 鍵關閉
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closePdfFullscreenModal();
        });
    }

    modal.classList.remove('hidden');
    modal.style.setProperty('display', 'flex', 'important');
    modal.style.setProperty('z-index', '99999', 'important');
    document.body.style.overflow = 'hidden';

    const titleEl = document.getElementById('tech-modal-title');
    if (titleEl) titleEl.textContent = title || '原廠技術文件';

    const container = document.getElementById('tech-modal-pdf-container');
    if (container) {
        container.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full py-16 text-slate-400 gap-2">
                <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-400"></i>
                <span class="text-sm font-semibold text-slate-300">正在以高解析度渲染全畫面文件...</span>
            </div>
        `;
        renderPdfFullscreen(container, pdfUrl, 1.0);
    }
}'''

# 替換 renderPdfFullscreen 函數，使用全畫面自適應寬度
new_render_fullscreen_func = '''async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {
    const cleanPdfUrl = pdfUrl.split('#')[0];
    currentModalScaleMultiplier = scaleMultiplier;
    currentModalPdfUrl = pdfUrl;

    const zoomIndicator = document.getElementById('tech-modal-zoom-val');
    if (zoomIndicator) {
        zoomIndicator.textContent = `${Math.round(scaleMultiplier * 100)}%`;
    }

    try {
        if (typeof window.pdfjsLib === 'undefined') {
            container.innerHTML = `<iframe src="${cleanPdfUrl}#toolbar=0&navpanes=0" class="w-full h-full border-0"></iframe>`;
            return;
        }

        window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

        let pdf = techPdfDocCache[cleanPdfUrl];
        if (!pdf) {
            const loadingTask = window.pdfjsLib.getDocument(cleanPdfUrl);
            pdf = await loadingTask.promise;
            techPdfDocCache[cleanPdfUrl] = pdf;
        }

        container.innerHTML = '';
        const modalWidth = container.clientWidth || window.innerWidth || 1200;
        // 全畫面模式下，提供寬廣舒適的滿版閱讀視野 (桌面滿版達 1180px，自適應且支援放大縮小)
        const baseTargetWidth = Math.min(1180, Math.max(680, modalWidth - 64));
        const targetWidth = Math.max(320, baseTargetWidth * scaleMultiplier);
        const dpr = window.devicePixelRatio || 1;

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const unscaledViewport = page.getViewport({ scale: 1 });
            const scale = targetWidth / unscaledViewport.width;
            const finalScale = Math.max(1.0, scale);
            const viewport = page.getViewport({ scale: finalScale * dpr });

            const canvasWrapper = document.createElement('div');
            canvasWrapper.className = 'w-full flex flex-col items-center mb-8 select-none';
            canvasWrapper.setAttribute('oncontextmenu', 'return false;');
            canvasWrapper.setAttribute('draggable', 'false');

            const pageLabel = document.createElement('div');
            pageLabel.className = 'text-[11px] font-bold text-slate-400 mb-2 px-3 py-0.5 rounded-full bg-slate-900 border border-slate-800 shadow-sm';
            pageLabel.textContent = `第 ${pageNum} 頁 / 共 ${pdf.numPages} 頁`;

            const canvas = document.createElement('canvas');
            canvas.className = 'rounded-md shadow-2xl bg-white block max-w-none border border-slate-700/60';
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
            <div class="text-center py-16 text-slate-400">
                <i class="fa-solid fa-triangle-exclamation text-3xl text-amber-500 mb-3"></i>
                <p class="text-base font-semibold">文件載入失敗，請檢查網路連線或稍後重試。</p>
            </div>
        `;
    }
}'''

# 替換 renderPdfFullscreen
r_start = js_code.find("async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {")
r_end = js_code.find("/**\n * 全螢幕放大縮放控制", r_start)
if r_start != -1 and r_end != -1:
    js_code = js_code[:r_start] + new_render_fullscreen_func + "\n\n" + js_code[r_end:]
    print("Replaced renderPdfFullscreen in js/technology.js.")

# 替換 openPdfFullscreenModal
o_start = js_code.find("function openPdfFullscreenModal(pdfUrl, title) {")
o_end = js_code.find("function closePdfFullscreenModal() {", o_start)
if o_start != -1 and o_end != -1:
    # 找到 openPdfFullscreenModal 之前的註解
    comm_start = js_code.rfind("/**", 0, o_start)
    if comm_start != -1 and o_start - comm_start < 200:
        o_start = comm_start
    js_code = js_code[:o_start] + new_open_modal_func + "\n\n" + js_code[o_end:]
    print("Replaced openPdfFullscreenModal in js/technology.js.")

# 縮放限制放寬 (0.5x ~ 3.0x)
old_zoom = "newMultiplier = Math.max(0.8, Math.min(2.5, newMultiplier));"
new_zoom = "newMultiplier = Math.max(0.5, Math.min(3.0, newMultiplier));"
if old_zoom in js_code:
    js_code = js_code.replace(old_zoom, new_zoom)
    print("Expanded zoom range to 0.5x ~ 3.0x in js/technology.js.")

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_code)
print("Updated js/technology.js successfully!")
