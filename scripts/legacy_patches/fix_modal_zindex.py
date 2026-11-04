# -*- coding: utf-8 -*-
"""
Fix Fullscreen Modal Z-Index and Stacking Bug
徹底修復全螢幕放大閱讀時被導覽列與標籤頁卡片覆蓋擋住的 BUG：
1. 為 #tech-pdf-fullscreen-modal 注入強制 inline style: z-index: 99999 !important
2. 在 build_technology_subpages.py 的 <style> 區塊注入全域 #tech-pdf-fullscreen-modal 樣式
3. 重新編譯 11 大獨立技術子頁面與首頁
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
# 1. 更新 js/technology.js
# =========================================================================
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 替換 openPdfFullscreenModal 與 closePdfFullscreenModal
old_open_start = "function openPdfFullscreenModal(pdfUrl, title) {"
old_open_idx = js_content.find(old_open_start)

old_close_marker = "function closePdfFullscreenModal() {"
old_close_end_marker = "document.body.style.overflow = '';\n}"
old_close_end_idx = js_content.find(old_close_end_marker)

if old_open_idx != -1 and old_close_end_idx != -1:
    new_modal_code = '''function openPdfFullscreenModal(pdfUrl, title) {
    let modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'tech-pdf-fullscreen-modal';
        // 強制頂層 z-index 與滿版全螢幕樣式，確保絕不被導覽列 (z-50) 或任何標籤卡片覆蓋
        modal.style.cssText = 'position:fixed!important;top:0!important;left:0!important;right:0!important;bottom:0!important;width:100vw!important;height:100vh!important;z-index:99999!important;background:rgba(2,6,23,0.85)!important;backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;padding:8px!important;box-sizing:border-box!important;cursor:pointer;';
        modal.setAttribute('oncontextmenu', 'return false;');
        modal.innerHTML = `
            <div class="tech-modal-inner relative w-full max-w-5xl h-[94vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-slate-200 cursor-default"
                 style="z-index:100000!important;max-height:94vh!important;box-shadow:0 25px 50px -12px rgba(0,0,0,0.6)!important;"
                 onclick="event.stopPropagation();">
                <div class="flex items-center justify-between px-3 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-b border-slate-200 shrink-0 gap-2"
                     style="z-index:100001!important;">
                    <div class="flex items-center gap-2 sm:gap-2.5 min-w-0 pr-2">
                        <span class="w-8 h-8 rounded-lg bg-red-50 text-red-600 flex items-center justify-center shrink-0 border border-red-200">
                            <i class="fa-solid fa-file-pdf text-sm"></i>
                        </span>
                        <div class="min-w-0">
                            <h3 id="tech-modal-title" class="text-sm sm:text-base font-bold text-slate-900 truncate">技術文件全螢幕放大檢視</h3>
                            <p class="text-xs text-slate-500 font-normal hidden sm:block">原廠技術文件線上清晰預覽 (不開放下載)</p>
                        </div>
                    </div>
                    
                    <!-- 縮放工具列與關閉按鈕 -->
                    <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
                        <div class="flex items-center bg-white border border-slate-300 rounded-lg p-0.5 shadow-2xs">
                            <button type="button" onclick="changeFullscreenZoom(-0.25)" title="縮小"
                                    class="w-7 h-7 flex items-center justify-center text-slate-600 hover:text-blue-900 hover:bg-slate-100 rounded cursor-pointer transition-colors">
                                <i class="fa-solid fa-magnifying-glass-minus text-xs"></i>
                            </button>
                            <button type="button" onclick="resetFullscreenZoom()" title="重設為 100%"
                                    class="px-2 h-7 text-xs font-bold text-slate-700 hover:bg-slate-100 rounded cursor-pointer transition-colors">
                                <span id="tech-modal-zoom-val">100%</span>
                            </button>
                            <button type="button" onclick="changeFullscreenZoom(0.25)" title="放大"
                                    class="w-7 h-7 flex items-center justify-center text-slate-600 hover:text-blue-900 hover:bg-slate-100 rounded cursor-pointer transition-colors">
                                <i class="fa-solid fa-magnifying-glass-plus text-xs"></i>
                            </button>
                        </div>

                        <button type="button" onclick="closePdfFullscreenModal()"
                                class="inline-flex items-center gap-1 px-2.5 sm:px-3 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-bold rounded-lg transition-colors cursor-pointer">
                            <i class="fa-solid fa-xmark text-sm"></i>
                            <span class="hidden sm:inline">關閉 (ESC)</span>
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

        // 點擊黑色遮罩關閉模態視窗
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closePdfFullscreenModal();
        });

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
                <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-900"></i>
                <span class="text-sm font-semibold text-slate-600">正在以高解析度渲染技術文件...</span>
            </div>
        `;
        renderPdfFullscreen(container, pdfUrl, 1.0);
    }
}

function closePdfFullscreenModal() {
    const modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.style.setProperty('display', 'none', 'important');
    }
    document.body.style.overflow = '';
}'''
    js_content = js_content[:old_open_idx] + new_modal_code + js_content[old_close_end_idx + len(old_close_end_marker):]

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Updated {JS_PATH} with z-index: 99999 !important modal!")

# =========================================================================
# 2. 更新 scripts/build_technology_subpages.py 中的 CSS 樣式
# =========================================================================
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_content = f.read()

modal_css = '''        /* 全螢幕技術文件預覽模態視窗 (確保置於最頂層，絕不被導覽列或標籤卡片覆蓋) */
        #tech-pdf-fullscreen-modal {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 99999 !important;
            background: rgba(2, 6, 23, 0.85) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0.5rem !important;
            box-sizing: border-box !important;
        }}
        #tech-pdf-fullscreen-modal.hidden {{
            display: none !important;
        }}
        #tech-pdf-fullscreen-modal .tech-modal-inner {{
            position: relative !important;
            z-index: 100000 !important;
            width: 100% !important;
            max-width: 1080px !important;
            max-height: 94vh !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6) !important;
        }}
'''

if "#tech-pdf-fullscreen-modal" not in py_content:
    marker = ".tech-principles-grid {{"
    idx = py_content.find(marker)
    if idx != -1:
        py_content = py_content[:idx] + modal_css + "        " + py_content[idx:]

with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
    f.write(py_content)
print(f"Updated {SUBPAGES_PY} with modal CSS rules!")

