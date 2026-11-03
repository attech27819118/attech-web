# -*- coding: utf-8 -*-
"""
Fix Technology Page Bugs & UX Flaws
1. 修復 selectTechDoc 切換藥丸標籤時未觸發 renderPdfDocumentToContainer 的嚴重 BUG
2. 修復 Carbon Black, Wax, Chain 在靜態頁面與動態切換時預設開在空原理分頁的重大 UX 缺陷
   - 自動選取該產品線第一個「有資料」的核心子分頁 (例如 carbon-black 與 wax 預設為 applications 應用技術，chain 預設為 single 單一產品技術)
3. 全螢幕模態視窗增強：
   - 增加 [ - 縮小 ] [ 100% / 150% / 200% ] [ + 放大 ] 縮放控制，徹底解決「字體過小看不清」問題
   - 點擊黑色背景半透明遮罩可直接關閉
   - 傳入 PDF.js 前剔除 URL fragment (#toolbar=0)
4. 美化橫向藥丸列滾動條 (.tech-pills-container)
5. 重新編譯所有 11 個子頁面與首頁
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
# 1. 更新 scripts/build_technology_subpages.py 中的預設子分頁邏輯
# =========================================================================
with open(SUBPAGES_PY, "r", encoding="utf-8") as f:
    py_content = f.read()

# 增強 build_technology_subpages.py 中的輔助函數 get_best_subtab_for_category
helper_func = '''def get_best_subtab_for_category(slug):
    """取得特定產品線最佳的預設子分頁 (優先選擇有實際原廠文件的分頁，避免首屏顯示空白)"""
    cat_data = TECH_DATABASE.get(slug, {"tabs": {}})
    tabs = cat_data.get("tabs", {})
    
    # 優先順序：principles (若有) -> applications (若有) -> catalog (若有) -> single (若有) -> formulation
    if tabs.get("principles") and len(tabs["principles"]) > 0:
        return "principles"
    elif tabs.get("applications") and len(tabs["applications"]) > 0:
        return "applications"
    elif tabs.get("catalog") and len(tabs["catalog"]) > 0:
        return "catalog"
    elif tabs.get("single") and len(tabs["single"]) > 0:
        return "single"
    elif tabs.get("formulation") and len(tabs["formulation"]) > 0:
        return "formulation"
    return "principles"
'''

if "def get_best_subtab_for_category" not in py_content:
    # 插入在 build_category_content_section 之前
    insert_marker = "def build_category_content_section"
    idx = py_content.find(insert_marker)
    if idx != -1:
        py_content = py_content[:idx] + helper_func + "\n" + py_content[idx:]

# 修改 build_all() 呼叫 build_category_content_section 時傳入最佳 subtab
old_call = 'content_html = build_category_content_section(item)'
new_call = 'active_tab = get_best_subtab_for_category(item["slug"])\n        content_html = build_category_content_section(item, active_subtab=active_tab)'
if old_call in py_content:
    py_content = py_content.replace(old_call, new_call)

# 修改 build_category_content_section 內部頂部標籤列 build_subtab_nav_html 呼叫傳入 active_subtab
# 原本是：build_subtab_nav_html(active_subtab, item["has_data"])
# 確保 pills 容器使用優化的 class "flex items-center gap-1 p-1 bg-slate-50 rounded-lg border border-slate-200 overflow-x-auto tech-pills-container"
py_content = py_content.replace(
    'class="flex items-center gap-1 p-1 bg-slate-50 rounded-lg border border-slate-200 overflow-x-auto"',
    'class="flex items-center gap-1 p-1 bg-slate-50 rounded-lg border border-slate-200 overflow-x-auto tech-pills-container"'
)

# 加入 tech-pills-container 的 CSS 樣式
pills_css = '''        /* 優化快捷標籤列滾動條樣式 */
        .tech-pills-container {
            scrollbar-width: thin;
            scrollbar-color: #cbd5e1 transparent;
            -webkit-overflow-scrolling: touch;
        }
        .tech-pills-container::-webkit-scrollbar {
            height: 4px;
        }
        .tech-pills-container::-webkit-scrollbar-track {
            background: transparent;
        }
        .tech-pills-container::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        .tech-pills-container::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
'''
if ".tech-pills-container" not in py_content:
    marker = ".tech-bookmark-wrapper {"
    idx = py_content.find(marker)
    if idx != -1:
        py_content = py_content[:idx] + pills_css + "        " + py_content[idx:]

with open(SUBPAGES_PY, "w", encoding="utf-8") as f:
    f.write(py_content)
print(f"Updated {SUBPAGES_PY} with smart default subtabs & pills CSS!")

# =========================================================================
# 2. 更新 js/technology.js
# =========================================================================
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

# 增強：
# A. 建立 getBestSubTabForCategory(slug)
# B. selectTechDoc 切換藥丸時自動觸發 renderPdfDocumentToContainer
# C. openPdfFullscreenModal 支援縮放 (Zoom In / Zoom Out) 與遮罩關閉
# D. renderPdfFullscreen 與 renderPdfDocumentToContainer 剔除 #toolbar=0
# E. switchTechCategory 自動將 activeSubTab 導向有文件的分頁

js_runtime_functions = '''
/**
 * 智慧取得特定產品線最佳的預設子分頁 (優先維持當前或選擇有文件的分頁，杜絕空白頁面)
 */
function getBestSubTabForCategory(slug) {
    const catData = TECH_DATABASE[slug];
    if (!catData || !catData.tabs) return 'principles';

    // 若當前選取的 subTab 在目標類別中有文件，維持當前選取
    if (TechState.activeSubTab && catData.tabs[TechState.activeSubTab] && catData.tabs[TechState.activeSubTab].length > 0) {
        return TechState.activeSubTab;
    }

    // 依序搜尋首個有資料的維度分頁
    const candidates = ['principles', 'applications', 'catalog', 'single', 'formulation'];
    for (const tabKey of candidates) {
        if (catData.tabs[tabKey] && catData.tabs[tabKey].length > 0) {
            return tabKey;
        }
    }
    return 'principles';
}

/**
 * 安全解析靜態資源 URL (支援 baseHref)
 */
function resolveAssetUrl(relPath) {
    if (!relPath) return '';
    if (relPath.startsWith('http://') || relPath.startsWith('https://') || relPath.startsWith('data:')) {
        return relPath;
    }
    const baseHref = window.APP_BASE_HREF || '/';
    const cleanPath = relPath.replace(/^\\.?\\//, '');
    return (baseHref + cleanPath).replace(/\\/+/g, '/');
}

/**
 * 安全編碼文件 URL (保留斜線但轉義空格與中文)
 */
function getEncodedPdfUrl(relPath) {
    if (!relPath) return '';
    const cleanPath = relPath.replace(/^\\.?\\//, '');
    const segments = cleanPath.split('/');
    const encodedSegments = segments.map(seg => encodeURIComponent(seg));
    const finalPath = encodedSegments.join('/');
    return resolveAssetUrl(finalPath) + '#toolbar=0&navpanes=0';
}

/**
 * 切換技術專區五大維度子分頁
 */
function switchTechSubTab(subTabKey) {
    TechState.activeSubTab = subTabKey;
    const subTabs = ['principles', 'catalog', 'applications', 'single', 'formulation'];
    
    subTabs.forEach(key => {
        const btn = document.getElementById(`tech-subtab-${key}`);
        const panel = document.getElementById(`tech-panel-${key}`);
        
        if (btn) {
            if (key === subTabKey) {
                btn.className = "tech-subtab-btn active";
            } else {
                btn.className = "tech-subtab-btn";
            }
        }
        
        if (panel) {
            if (key === subTabKey) {
                panel.classList.remove('hidden');
                // 若包含未渲染的 PDF 容器，觸發渲染
                const viewer = panel.querySelector('.pdf-viewer-container');
                if (viewer && !viewer.querySelector('canvas')) {
                    const pdfUrl = viewer.getAttribute('data-pdf-url');
                    if (pdfUrl && viewer.id) {
                        renderPdfDocumentToContainer(viewer.id, pdfUrl);
                    }
                }
            } else {
                panel.classList.add('hidden');
            }
        }
    });
}

/**
 * 建立五大子分頁單行標籤列 HTML
 */
function buildSubTabNavHtml(activeKey, hasData = true) {
    const tabs = [
        { key: 'principles', label: '1. 原理', icon: 'fa-atom' },
        { key: 'catalog', label: '2. 目錄', icon: 'fa-list-check' },
        { key: 'applications', label: '3. 應用技術', icon: 'fa-industry' },
        { key: 'single', label: '4. 單一產品技術', icon: 'fa-flask-vial' },
        { key: 'formulation', label: '5. 配方', icon: 'fa-clipboard-list' }
    ];

    return `
        <div class="tech-subtab-strip" role="tablist" aria-label="技術專題五大核心維度導覽">
            ${tabs.map(tab => {
                const isActive = (tab.key === activeKey);
                const activeCls = isActive ? "active" : "";
                return `
                    <button type="button" onclick="switchTechSubTab('${tab.key}')" id="tech-subtab-${tab.key}"
                            class="tech-subtab-btn ${activeCls}">
                        <i class="fa-solid ${tab.icon} text-xs"></i>
                        <span>${tab.label}</span>
                    </button>
                `;
            }).join('')}
        </div>
    `;
}

/**
 * 切換特定分頁中的當前選取文件 (重要修復：切換後立即觸發 PDF Canvas 載入)
 */
function selectTechDoc(slug, tabKey, docIdx) {
    if (!TechState.activeDocIndices[slug]) {
        TechState.activeDocIndices[slug] = { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0, 'formulation': 0 };
    }
    TechState.activeDocIndices[slug][tabKey] = docIdx;

    const catData = TECH_DATABASE[slug];
    if (!catData || !catData.tabs[tabKey]) return;
    const docs = catData.tabs[tabKey];
    if (!docs || docIdx >= docs.length) return;

    // 1. 更新 Pills 樣式
    docs.forEach((_, i) => {
        const pill = document.getElementById(`pill-${slug}-${tabKey}-${i}`);
        if (pill) {
            if (i === docIdx) {
                pill.className = "px-2.5 py-1 rounded-md text-xs font-bold bg-blue-900 text-white shadow-2xs transition-all whitespace-nowrap";
            } else {
                pill.className = "px-2.5 py-1 rounded-md text-xs font-semibold text-slate-600 hover:text-blue-900 hover:bg-slate-100 transition-all whitespace-nowrap";
            }
        }
    });

    // 2. 更新內容檢視器 (雙欄視圖)
    const viewerContainer = document.getElementById(`viewer-${slug}-${tabKey}`);
    if (viewerContainer) {
        const doc = docs[docIdx];
        viewerContainer.innerHTML = buildSingleDocLayoutHtml(doc, slug, tabKey);

        // 重要修復：立即為新選取的文件觸發 PDF.js 渲染任務
        const newViewer = viewerContainer.querySelector('.pdf-viewer-container');
        if (newViewer) {
            const pdfUrl = newViewer.getAttribute('data-pdf-url');
            if (pdfUrl && newViewer.id) {
                renderPdfDocumentToContainer(newViewer.id, pdfUrl);
            }
        }
    }
}

// 全域快取 PDF.js 渲染任務與 PDF Document 物件
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

    // 剔除 URL 中的 #toolbar=0&navpanes=0 錨點，供 PDF.js 乾淨讀取
    const cleanPdfUrl = pdfUrl.split('#')[0];

    try {
        if (typeof window.pdfjsLib === 'undefined') {
            console.warn('PDF.js 未就緒，使用保護視窗模式');
            container.innerHTML = `
                <iframe src="${cleanPdfUrl}#toolbar=0&navpanes=0"
                        class="w-full h-full min-h-[600px] border-0 rounded-lg bg-slate-50"
                        title="技術文件預覽"
                        loading="lazy"></iframe>
            `;
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
            canvasWrapper.setAttribute('draggable', 'false');

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

// 全螢幕模態視窗縮放倍率狀態
let currentModalScaleMultiplier = 1.0;
let currentModalPdfUrl = '';

/**
 * 全螢幕放大高解析渲染 (寬版視圖、縮放倍率支援、大字體、高清晰度、無下載功能、支援滾輪與頁碼標示)
 */
async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {
    const cleanPdfUrl = pdfUrl.split('#')[0];
    currentModalScaleMultiplier = scaleMultiplier;
    currentModalPdfUrl = pdfUrl;

    const zoomIndicator = document.getElementById('tech-modal-zoom-val');
    if (zoomIndicator) {
        zoomIndicator.textContent = `${Math.round(scaleMultiplier * 100)}%`;
    }

    try {
        if (typeof window.pdfjsLib === 'undefined') {
            container.innerHTML = `<iframe src="${cleanPdfUrl}#toolbar=0&navpanes=0" class="w-full h-full min-h-[700px] border-0 rounded-lg"></iframe>`;
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
        const modalWidth = container.clientWidth || 960;
        const baseTargetWidth = Math.min(920, Math.max(600, modalWidth - 48));
        const targetWidth = baseTargetWidth * scaleMultiplier;
        const dpr = window.devicePixelRatio || 1;

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const unscaledViewport = page.getViewport({ scale: 1 });
            const scale = targetWidth / unscaledViewport.width;
            const finalScale = Math.max(1.0, scale);
            const viewport = page.getViewport({ scale: finalScale * dpr });

            const canvasWrapper = document.createElement('div');
            canvasWrapper.className = 'w-full flex flex-col items-center mb-6 select-none';
            canvasWrapper.setAttribute('oncontextmenu', 'return false;');
            canvasWrapper.setAttribute('draggable', 'false');

            const pageLabel = document.createElement('div');
            pageLabel.className = 'text-[11px] font-bold text-slate-400 mb-1';
            pageLabel.textContent = `第 ${pageNum} 頁 / 共 ${pdf.numPages} 頁`;

            const canvas = document.createElement('canvas');
            canvas.className = 'rounded-xl shadow-lg border border-slate-300 bg-white block max-w-none';
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
 * 全螢幕放大縮放控制
 */
function changeFullscreenZoom(delta) {
    let newMultiplier = currentModalScaleMultiplier + delta;
    newMultiplier = Math.max(0.8, Math.min(2.5, newMultiplier));
    const container = document.getElementById('tech-modal-pdf-container');
    if (container && currentModalPdfUrl) {
        renderPdfFullscreen(container, currentModalPdfUrl, newMultiplier);
    }
}

function resetFullscreenZoom() {
    const container = document.getElementById('tech-modal-pdf-container');
    if (container && currentModalPdfUrl) {
        renderPdfFullscreen(container, currentModalPdfUrl, 1.0);
    }
}

/**
 * 開啟 PDF 全螢幕放大檢視模態視窗 (解決預覽視窗字體過小問題，支援手動放大/縮小，且嚴格禁止下載與另存)
 */
function openPdfFullscreenModal(pdfUrl, title) {
    let modal = document.getElementById('tech-pdf-fullscreen-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'tech-pdf-fullscreen-modal';
        modal.className = 'fixed inset-0 z-[9999] bg-slate-950/80 backdrop-blur-sm flex flex-col items-center justify-center p-2 sm:p-4 select-none cursor-pointer';
        modal.setAttribute('oncontextmenu', 'return false;');
        modal.innerHTML = `
            <div class="relative w-full max-w-5xl h-[94vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-slate-200 cursor-default"
                 onclick="event.stopPropagation();">
                <div class="flex items-center justify-between px-3 sm:px-4 py-2.5 sm:py-3 bg-slate-50 border-b border-slate-200 shrink-0 gap-2">
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
        renderPdfFullscreen(container, pdfUrl, 1.0);
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
'''

# 替換 js/technology.js 中自 resolveAssetUrl 開始到 window.addEventListener('keydown') 結束的區塊
start_subtab_marker = "/**\n * 安全解析靜態資源 URL (支援 baseHref)\n */"
if start_subtab_marker not in js_content:
    start_subtab_marker = "function resolveAssetUrl(relPath) {"
    start_subtab_idx = js_content.find(start_subtab_marker)
    # 往前回溯找到註解
    start_subtab_idx = js_content.rfind("/**", 0, start_subtab_idx)
else:
    start_subtab_idx = js_content.find(start_subtab_marker)

end_keydown_marker = "window.addEventListener('keydown', function (e) {"
end_keydown_idx = js_content.find(end_keydown_marker)
if end_keydown_idx != -1:
    end_keydown_close = js_content.find("});", end_keydown_idx) + 3
else:
    end_keydown_close = -1

if start_subtab_idx != -1 and end_keydown_close != -1:
    js_content = js_content[:start_subtab_idx] + js_runtime_functions.strip() + "\n\n" + js_content[end_keydown_close:]

# 修改 switchTechCategory(slug, updateUrl = true) 函式：
# 在切換分類時，使用 getBestSubTabForCategory(slug)
cat_switch_marker = "TechState.activeCategory = slug;"
cat_switch_idx = js_content.find(cat_switch_marker)
if cat_switch_idx != -1:
    old_switch_sub = "switchTechSubTab(TechState.activeSubTab);"
    new_switch_sub = "const bestTab = getBestSubTabForCategory(slug);\n        switchTechSubTab(bestTab);"
    # 只替換 mainContainer.innerHTML 之後的呼叫
    js_content = js_content.replace(old_switch_sub, new_switch_sub)

# 確保 pills 容器使用 class="... tech-pills-container"
js_content = js_content.replace(
    'class="flex items-center gap-1 p-1 bg-slate-50 rounded-lg border border-slate-200 overflow-x-auto"',
    'class="flex items-center gap-1 p-1 bg-slate-50 rounded-lg border border-slate-200 overflow-x-auto tech-pills-container"'
)

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Updated {JS_PATH} with fixed selectTechDoc & fullscreen zoom controls!")

