import os
import re

def build_tech_section_html():
    return '''    <!-- Tab: 技術專區 (Technology) - 11 大產品系列分類完備呈現 -->
    <section id="tab-technology" class="tab-content active" role="tabpanel" aria-labelledby="nav-technology">
        <div class="optimized-container px-4 py-8">
            <!-- 頂部技術專區標題列 (比照產品專區頂部結構) -->
            <div class="mb-8 pb-6 border-b border-gray-200">
                <div class="flex flex-wrap items-center gap-2 text-xs font-semibold text-slate-500 mb-2">
                    <a href="./" class="hover:text-blue-900 hover:underline">首頁</a>
                    <i class="fa-solid fa-chevron-right text-[10px] text-slate-400"></i>
                    <span class="text-blue-950 font-bold">技術專區</span>
                </div>
                <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                    <div>
                        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
                            <span class="w-2.5 h-8 bg-blue-900 rounded-full inline-block"></span>
                            技術專區 (Technology)
                        </h1>
                        <p class="text-sm sm:text-base text-slate-600 mt-2 font-medium leading-relaxed max-w-3xl">
                            宏威應用材料特化產品技術方案，涵蓋 11 大品類之材料特性、化學機理、配方建議、比較評估與原廠技術支援。
                        </p>
                    </div>
                    <div class="shrink-0 flex items-center gap-3">
                        <a href="contact/?mode=detailed"
                           class="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-sm font-bold shadow-xs transition-all active:scale-95">
                            <i class="fa-solid fa-flask-vial"></i>
                            <span>預約配方技術諮詢</span>
                        </a>
                    </div>
                </div>
            </div>

            <!-- STEP 1：技術分類導覽 (4 欄 11 項分類快速導航索引) -->
            <div class="mb-8 rounded-xl border border-slate-800 bg-slate-900 p-5 text-white shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="flex items-center text-lg font-bold tracking-wide text-blue-300">
                        <span class="mr-2 flex h-5 w-5 items-center justify-center rounded bg-blue-600 text-base font-bold text-white">1</span>
                        技術分類快速導航
                    </h2>
                    <span class="text-xs text-slate-400">點擊直接跳轉至各專題說明</span>
                </div>
                <!-- 4 欄式技術分類卡片快速索引 -->
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                    <!-- Column 1 -->
                    <div class="space-y-3">
                        <a href="technology/#tech-tyzor"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Organic Titanates & Zirconates
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">鈦酸酯與鋯酸酯 (Tyzor®)</div>
                        </a>
                        <a href="technology/#tech-silane"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Silane / 矽烷偶合劑
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">Dynasylan / hydrosil 系列</div>
                        </a>
                        <a href="technology/#tech-chain"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Chain Extender / 擴鏈劑
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">Unilink & Clearlink 系列</div>
                        </a>
                    </div>

                    <!-- Column 2 -->
                    <div class="space-y-3">
                        <a href="technology/#tech-carbon-black"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Special Carbon Black
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">特級碳黑 / 導電碳黑</div>
                        </a>
                        <a href="technology/#tech-wax"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Micronized Wax / 微粉蠟
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">PTFE 取代 / 耐磨耐刮助劑</div>
                        </a>
                        <a href="technology/#tech-matting"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Matting Agent / 消光粉
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">二氧化矽 / 表面處理消光</div>
                        </a>
                    </div>

                    <!-- Column 3 -->
                    <div class="space-y-3">
                        <a href="technology/#tech-maleic"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Maleic Resin / 馬林酸樹脂
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">松香改性馬林酸樹脂</div>
                        </a>
                        <a href="technology/#tech-adhesion"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Adhesion Resin / 密著樹脂
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">氯化聚烯烴 (CPO) & 非氯系</div>
                        </a>
                        <a href="technology/#tech-powder"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Powder Coating Additive
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">粉體塗料專用功能性助劑</div>
                        </a>
                    </div>

                    <!-- Column 4 -->
                    <div class="space-y-3">
                        <a href="technology/#tech-px"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                PX Lubricant Additives
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">潤滑油添加劑 (原 ExxonMobil)</div>
                        </a>
                        <a href="technology/#tech-polyester"
                           class="block p-3 rounded-lg bg-slate-800/90 hover:bg-slate-800 border border-slate-700/80 transition-all group">
                            <div class="text-sm font-bold text-blue-300 group-hover:text-blue-200 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                Polyester Resin / 聚酯樹脂
                            </div>
                            <div class="text-xs text-slate-400 mt-1 pl-3">聚酯樹脂 (DYNAPOL/DYNACOLL替代品)</div>
                        </a>
                        <div class="p-3 rounded-lg bg-blue-950/60 border border-blue-800/60 text-center">
                            <span class="text-xs text-blue-300 font-semibold">11 大技術專題已全面上線</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- STEP 2：11 個分類之技術專題內容專區 -->
            <div class="space-y-12">
                <div class="flex items-center justify-between pb-3 border-b border-gray-200">
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span class="flex h-5 w-5 items-center justify-center rounded bg-blue-100 text-blue-900 text-xs font-bold">2</span>
                        技術內容專區 (依產品品類分類)
                    </h2>
                    <span class="text-xs text-slate-500 font-medium">共 11 個產品系列技術專題</span>
                </div>

                <!-- ========================================================
                     分類 1: 鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®) - 單頁呈現
                     ======================================================== -->
                <section id="tech-tyzor" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <!-- 標題與簡介區 -->
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Dorf Ketal 原廠專用技術</span>
                                <span>Tyzor® 系列有機鈦／鋯</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                Tyzor® 有機鈦（鋯）化合物具備高反應性與特殊配位多重功能，針對高分子合成催化、三維網絡交聯、異質基材介面結合力提升及 Sol-Gel 表面改性，提供全面工業化解決方案。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">
                                <i class="fa-solid fa-lock text-[11px]"></i> 原廠機密技術，不可直接存取下載
                            </span>
                            <div class="flex items-center gap-2">
                                <a href="products/dorfketal/tyzor/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 Tyzor 產品</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Tyzor"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>申請技術評估與索樣</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- 機密文件聲明橫幅 -->
                    <div class="bg-gradient-to-r from-slate-50 via-blue-50/40 to-slate-50 border border-slate-200 rounded-xl p-3.5 sm:p-4 flex items-center justify-between gap-3 text-xs text-slate-600">
                        <div class="flex items-center gap-2.5">
                            <i class="fa-solid fa-shield-halved text-blue-800 text-base shrink-0"></i>
                            <span><strong>存取權限說明：</strong>本專題所呈現之圖解機理與工藝條件屬原廠專有技術，未開放原始 PDF 下載。請點擊圖表以清晰放大檢視，如需具體配方評估，請洽宏威技術團隊。</span>
                        </div>
                    </div>

                    <!-- 單頁呈現：頂部切換頁籤與頁碼導覽 -->
                    <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-100 p-2 sm:p-2.5 rounded-xl border border-slate-200">
                        <div class="flex flex-wrap items-center gap-1.5 sm:gap-2" role="tablist" id="tyzor-pages-nav">
                            <button type="button" onclick="showTyzorPage(0)" id="tyzor-tab-0"
                                    class="tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all bg-blue-900 text-white shadow-xs">
                                1. 酯化反應催化劑
                            </button>
                            <button type="button" onclick="showTyzorPage(1)" id="tyzor-tab-1"
                                    class="tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-700 hover:bg-white hover:text-blue-950 transition-all">
                                2. 交聯劑
                            </button>
                            <button type="button" onclick="showTyzorPage(2)" id="tyzor-tab-2"
                                    class="tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-700 hover:bg-white hover:text-blue-950 transition-all">
                                3. 密著促進劑
                            </button>
                            <button type="button" onclick="showTyzorPage(3)" id="tyzor-tab-3"
                                    class="tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-700 hover:bg-white hover:text-blue-950 transition-all">
                                4. 表面處理劑
                            </button>
                        </div>
                        <!-- 上一頁 / 下一頁導航 -->
                        <div class="flex items-center gap-2">
                            <button type="button" onclick="prevTyzorPage()"
                                    class="px-2.5 py-1.5 rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-bold transition-colors flex items-center gap-1" title="上一頁">
                                <i class="fa-solid fa-chevron-left text-[11px]"></i>
                                <span class="hidden sm:inline">上一頁</span>
                            </button>
                            <span id="tyzor-page-indicator" class="text-xs font-mono font-bold text-slate-600 px-2">1 / 4</span>
                            <button type="button" onclick="nextTyzorPage()"
                                    class="px-2.5 py-1.5 rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 text-xs font-bold transition-colors flex items-center gap-1" title="下一頁">
                                <span class="hidden sm:inline">下一頁</span>
                                <i class="fa-solid fa-chevron-right text-[11px]"></i>
                            </button>
                        </div>
                    </div>

                    <!-- 單頁展示區域 (滿幅清晰呈現，無多餘文字卡片擠壓) -->
                    <div class="max-w-4xl mx-auto pt-2">
                        <!-- 頁面 0: 催化劑 -->
                        <div id="tyzor-page-0" class="tyzor-page-item space-y-3">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
                                <div>
                                    <span class="text-xs font-bold text-blue-700 uppercase tracking-wider">類別一・催化應用</span>
                                    <h4 class="text-base sm:text-lg font-bold text-slate-900">鈦（鋯）酸酯作為催化劑 (Tyzor® Catalysts)</h4>
                                </div>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs text-slate-400 font-medium"><i class="fa-solid fa-lock text-[10px]"></i> 原廠機密技術</span>
                                    <a href="contact/?mode=detailed&inquiry=Tyzor-Catalyst" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                        <i class="fa-solid fa-envelope"></i> 諮詢此技術配方
                                    </a>
                                </div>
                            </div>
                            <div class="relative rounded-2xl overflow-hidden bg-slate-50 border border-slate-200/90 shadow-xs cursor-pointer group flex items-center justify-center p-2 sm:p-3"
                                 onclick="openTechImageModal('techdata/tyzor/catalyst.webp', '鈦（鋯）酸酯作為催化劑', 'Tyzor-Catalyst')">
                                <img src="techdata/tyzor/catalyst.webp" alt="鈦（鋯）酸酯作為催化劑"
                                     class="max-w-full h-auto object-contain rounded-xl select-none transition-transform duration-300 group-hover:scale-[1.01]"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-4 py-2 bg-slate-900/90 text-white text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大全螢幕檢視
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 頁面 1: 交聯劑 -->
                        <div id="tyzor-page-1" class="tyzor-page-item space-y-3 hidden">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
                                <div>
                                    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">類別二・交聯改性</span>
                                    <h4 class="text-base sm:text-lg font-bold text-slate-900">鈦（鋯）酸酯作為交聯劑 (Tyzor® Crosslinkers)</h4>
                                </div>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs text-slate-400 font-medium"><i class="fa-solid fa-lock text-[10px]"></i> 原廠機密技術</span>
                                    <a href="contact/?mode=detailed&inquiry=Tyzor-Crosslinker" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-800 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition-colors">
                                        <i class="fa-solid fa-envelope"></i> 諮詢此技術配方
                                    </a>
                                </div>
                            </div>
                            <div class="relative rounded-2xl overflow-hidden bg-slate-50 border border-slate-200/90 shadow-xs cursor-pointer group flex items-center justify-center p-2 sm:p-3"
                                 onclick="openTechImageModal('techdata/tyzor/crosslinker.webp', '鈦（鋯）酸酯作為交聯劑', 'Tyzor-Crosslinker')">
                                <img src="techdata/tyzor/crosslinker.webp" alt="鈦（鋯）酸酯作為交聯劑"
                                     class="max-w-full h-auto object-contain rounded-xl select-none transition-transform duration-300 group-hover:scale-[1.01]"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-4 py-2 bg-slate-900/90 text-white text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大全螢幕檢視
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 頁面 2: 密著促進劑 -->
                        <div id="tyzor-page-2" class="tyzor-page-item space-y-3 hidden">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
                                <div>
                                    <span class="text-xs font-bold text-blue-700 uppercase tracking-wider">類別三・介面附著</span>
                                    <h4 class="text-base sm:text-lg font-bold text-slate-900">鈦（鋯）酸酯提高附著力 (Tyzor® Adhesion Promoters)</h4>
                                </div>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs text-slate-400 font-medium"><i class="fa-solid fa-lock text-[10px]"></i> 原廠機密技術</span>
                                    <a href="contact/?mode=detailed&inquiry=Tyzor-Adhesion" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                        <i class="fa-solid fa-envelope"></i> 諮詢此技術配方
                                    </a>
                                </div>
                            </div>
                            <div class="relative rounded-2xl overflow-hidden bg-slate-50 border border-slate-200/90 shadow-xs cursor-pointer group flex items-center justify-center p-2 sm:p-3"
                                 onclick="openTechImageModal('techdata/tyzor/adhesion.webp', '鈦（鋯）酸酯提高附著力', 'Tyzor-Adhesion')">
                                <img src="techdata/tyzor/adhesion.webp" alt="鈦（鋯）酸酯提高附著力"
                                     class="max-w-full h-auto object-contain rounded-xl select-none transition-transform duration-300 group-hover:scale-[1.01]"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-4 py-2 bg-slate-900/90 text-white text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大全螢幕檢視
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 頁面 3: 表面改性 -->
                        <div id="tyzor-page-3" class="tyzor-page-item space-y-3 hidden">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
                                <div>
                                    <span class="text-xs font-bold text-amber-700 uppercase tracking-wider">類別四・表面改性</span>
                                    <h4 class="text-base sm:text-lg font-bold text-slate-900">鈦（鋯）酸酯作為表面改性 (Tyzor® Surface Modification)</h4>
                                </div>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs text-slate-400 font-medium"><i class="fa-solid fa-lock text-[10px]"></i> 原廠機密技術</span>
                                    <a href="contact/?mode=detailed&inquiry=Tyzor-Surface" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-800 hover:bg-amber-700 text-white rounded-lg text-xs font-bold transition-colors">
                                        <i class="fa-solid fa-envelope"></i> 諮詢此技術配方
                                    </a>
                                </div>
                            </div>
                            <div class="relative rounded-2xl overflow-hidden bg-slate-50 border border-slate-200/90 shadow-xs cursor-pointer group flex items-center justify-center p-2 sm:p-3"
                                 onclick="openTechImageModal('techdata/tyzor/surface_treatment.webp', '鈦（鋯）酸酯作為表面改性', 'Tyzor-Surface')">
                                <img src="techdata/tyzor/surface_treatment.webp" alt="鈦（鋯）酸酯作為表面改性"
                                     class="max-w-full h-auto object-contain rounded-xl select-none transition-transform duration-300 group-hover:scale-[1.01]"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-4 py-2 bg-slate-900/90 text-white text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大全螢幕檢視
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 2: 矽烷偶合劑系列技術 (Silane Coupling Agents)
                     ======================================================== -->
                <section id="tech-silane" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Evonik 原廠專用技術</span>
                                <span>Dynasylan® & Hydrosil® 系列矽烷</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                矽烷偶合劑系列技術應用 (Silane)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                矽烷分子具備有機與無機雙重反應性端基，扮演「分子橋樑」角色，廣泛應用於水性塗料改性、玻璃/金屬/填料表面處理、防腐底漆及密封膠交聯。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/silane/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 24 款矽烷規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Silane"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取矽烷型號手冊</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- 3 大技術要點簡介 -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-droplet text-blue-600"></i>
                                <span>水性環保預縮合體系 (Hydrosil®)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專利水性化寡聚物技術，已預水解並穩定分散於水中，VOC 極低，可直接添加於水性壓克力、PU 塗料與乳膠漆中，無需有機溶劑。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-link text-blue-600"></i>
                                <span>異質介面雙向共價架橋</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                無機矽烷醇 (-Si-OH) 與金屬、玻璃、二氧化矽縮合形成緻密 -Si-O-Si- 網絡；有機官能基 (氨基/環氧基/甲基丙烯醯氧基) 參與樹脂固化。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-shield-halved text-blue-600"></i>
                                <span>極致耐水耐鹽霧防腐改性</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                在金屬底材表面形成鈍化自修復保護薄膜，顯著阻止水分子及腐蝕性離子滲透，提升漆膜附著百格由 0B 至 5B。
                            </p>
                        </div>
                    </div>

                    <!-- 預留技術圖檔與資料展示版位 -->
                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-file-waveform"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">矽烷水解縮合機理與各底材配方比較表</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠專用技術文檔與各基材附著力對照數據整理中。如需特定樹脂（如水性聚氨酯、環氧重防腐）之添加比例與催化指引，歡迎直接聯繫技術團隊。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Silane-Formulation"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取具體配方指引
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 3: 擴鏈劑 (Chain Extenders)
                     ======================================================== -->
                <section id="tech-chain" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Dorf Ketal 原廠專用技術</span>
                                <span>Unilink® & Clearlink® 系列擴鏈劑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                擴鏈劑高性能彈性體改性技術 (Chain Extender)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                專為聚脲 (Polyurea)、聚氨酯 (Polyurethane) 與環氧樹脂體系開發之受阻二胺擴鏈劑，精準調控凝膠固化速度，賦予彈性體優異的機械強度與耐黃變性能。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/dorfketal/chain/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽擴鏈劑規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Chain-Extender"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取反應動力學報告</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-stopwatch text-blue-600"></i>
                                <span>反應速率與凝膠時間調控</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                仲胺二胺結構具空間位阻效應，能有效平緩異氰酸酯之劇烈放熱反應，延長開放流平時間，消除針孔與起泡缺陷。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-sun text-blue-600"></i>
                                <span>脂肪族耐黃變結構 (Clearlink®)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                Clearlink 1000 具備優異耐光老化特性，經長時間紫外線照射不黃變，是高裝飾性戶外聚脲防水防腐塗料的理想選擇。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-dumbbell text-blue-600"></i>
                                <span>力學與物理抗性倍增 (Unilink®)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                Unilink 4200 構築剛硬結晶微區，顯著提高彈性體的拉伸撕裂強度、耐磨損性與熱變形溫度，適用重工業防爆地坪與襯裡。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-microscope"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">聚脲/聚氨酯擴鏈配方動力學曲線與比較指引</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠受阻胺擴鏈劑反應速率與凝膠時間實驗圖表建置中。如需特定固化劑配比諮詢，請與我們聯絡。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=ChainExtender-Formula"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 預約擴鏈技術評估
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 4: 特級碳黑 (Special Carbon Black)
                     ======================================================== -->
                <section id="tech-carbon-black" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Orion Engineered Carbons 原廠技術</span>
                                <span>特級塗料與油墨碳黑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                特級碳黑高黑度與色相調控技術 (Carbon Black)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                全球領先特級碳黑，藉由精密原生粒徑、聚集體結構及化學氧化表面改性，在塗料與油墨中實現極致黑度 (Jetness)、純藍底色相 (Bluish Undertone) 及超低研磨黏度。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/orion/coating/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 40+ 款 Orion 碳黑</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Orion-CarbonBlack"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取碳黑分散研磨指引</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-palette text-blue-600"></i>
                                <span>極致黑度與純藍底色 (Bluish Undertone)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專利氣黑工藝生產之微細粒徑碳黑 (如 COLOUR BLACK FW 200)，吸光率極高，提供頂級汽車漆與鋼琴漆深邃純淨的高級黑感。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-flask-vial text-blue-600"></i>
                                <span>表面氧化後處理與高分散性</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                表面富含羥基、羧基等極性含氧官能基，顯著改善在水性及極性樹脂中的潤濕親和性，防止絮凝返粗，降低研磨黏度。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-bolt text-blue-600"></i>
                                <span>特種導電與防靜電網絡</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                高結構特種導電碳黑 (如 PRINTEX 系列)，能在極低添加量下迅速形成導電網絡，適用抗靜電地坪、電子包裝與導電塗料。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-chart-column"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">Orion 特級碳黑黑度 (My) 與色相 (dM) 座標圖表</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠黑度與底色色相分級座標圖整理中。如需特定塗料或油墨之最佳分散劑配比，請洽技術團隊。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=CarbonBlack-Dispersion"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取分散研磨建議
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 5: 微粉蠟與 PTFE 取代 (Micronized Wax)
                     ======================================================== -->
                <section id="tech-wax" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Micro Powders (MPI) 原廠技術</span>
                                <span>微粉蠟與 PTFE-Free 取代系列</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                微粉蠟與 PTFE 取代耐磨抗刮技術 (Micronized Wax)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                全球微粉蠟領導品牌 Micro Powders 提供專利改性聚乙烯/聚丙烯蠟、生質蠟及新一代無氟 PTFE Alternative 解決方案，賦予塗膜優異抗刮痕、滑度與表面紋理。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/mpi/ptfe/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 MPI 微粉蠟規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=MPI-PTFE-Alternative"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取 PTFE 取代白皮書</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-leaf text-blue-600"></i>
                                <span>PTFE-Free 無氟環保全面取代</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                符合歐盟 PFAS / REACH 最嚴格法規限制，專利複合高分子技術 (PolyGlide, SuperGlide 系列) 性能完全媲美甚至超越傳統含氟 PTFE 助劑。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-shield text-blue-600"></i>
                                <span>表面浮移與極低摩擦係數 (COF)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                微粉蠟在塗膜固化烘烤過程中定向浮移至漆膜表面，形成一層堅韌微觀防護層，大幅提升耐磨損 (Taber Abrasion) 與抗刮擦性能。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-braille text-blue-600"></i>
                                <span>精密粒徑控制與特殊消光紋理</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                精密窄粒徑分佈（如 PropylTex 系列），在粉體塗料與工業漆中創造細膩砂面、皮革手感及均勻柔和的啞光消光效果。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-file-contract"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">MPI 微粉蠟耐刮痕測試與 PTFE 比較性能雷達圖</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠耐刮擦、動摩擦係數與重塗附著力評估圖表建置中。如需特定塗料系統之無氟替代型號推薦，歡迎預約諮詢。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Wax-PTFE-Compare"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取 PTFE 替代測試數據
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 6: 消光粉 (Matting Agents)
                     ======================================================== -->
                <section id="tech-matting" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Evonik 原廠消光技術</span>
                                <span>ACEMATT® & AEROSIL® 二氧化矽消光</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                二氧化矽消光與透明度調控技術 (Matting Agent)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                沉澱法與氣相二氧化矽消光粉，具有極高消光效率、優異透明度及極低增稠副作用，廣泛應用於木器漆、卷材塗料、塑料塗料及皮革塗飾。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/matting_agent/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽消光粉規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Matting-Agent"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取消光型號手冊</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-eye-slash text-blue-600"></i>
                                <span>高孔隙率與極致消光效率</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                特殊孔隙結構與粒徑分佈使入射光線產生漫反射，極低添加量即可實現深啞光（60°光澤度 < 10），且不影響漆膜豐滿度。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-sparkles text-blue-600"></i>
                                <span>高透明度與極低霧影 (Low Haze)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                折射率與塗料常用樹脂高度匹配，在深色木器與高透明清漆中無發白、發灰現象，保持底材真實天然木紋質感。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-arrows-spin text-blue-600"></i>
                                <span>有機蠟表面處理防沉降易分散</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專利有機蠟改性技術 (如 OK 412, OK 520) 徹底杜絕塗料長期存放產生硬沉澱，沉積物極鬆軟易於快速攪拌重分散。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-sliders"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">ACEMATT® 消光粉粒徑、孔容與黏度關聯曲線</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠消光效率與耐刮傷平衡指南整理中。如需特定漆膜厚度之型號推薦，歡迎聯絡技術工程師。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Matting-Particle-Select"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取消光型號建議
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 7: 馬林酸樹脂 (Maleic Acid Resins)
                     ======================================================== -->
                <section id="tech-maleic" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">捷通達 / 宏威特化技術</span>
                                <span>松香改質與醇溶型馬林酸樹脂</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                馬林酸樹脂與改性松香技術應用 (Maleic Resin)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                松香改質馬林酸樹脂與醇溶型樹脂，具備極佳溶劑釋放性、快乾性、高硬度與優良顏料潤濕性，廣泛應用於凹版包裝印刷油墨、硝基漆及木器快乾底漆。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/maleic_acid_resin/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽馬林酸樹脂規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Maleic-Resin"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取相容性與型號指引</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-gauge-high text-blue-600"></i>
                                <span>極佳溶劑釋放性與快乾成膜</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                特殊酯化加成結構使溶劑能極迅速揮發脫出，漆膜在常溫下極速表乾硬化，大幅提高印刷線速度與生產週轉效率。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-wine-glass text-blue-600"></i>
                                <span>完全醇溶與無苯環保化 (MP-130/150)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                經特殊酸值與羥值分子設計，在乙醇、異丙醇等低毒溶劑中完全透明溶解，滿足現代食品包裝無苯無酮環保要求。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-gem text-blue-600"></i>
                                <span>高硬度高光澤與顏料親和潤濕</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                軟化點高、色澤淺淡、抗熱發黃性佳，對各類無機有機顏料具有出色展色力與研磨分散流平效果。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-cubes-stacked"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">馬林酸樹脂在醇水溶劑體系中溶解度與混溶對照表</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠樹脂酸值、軟化點與硝化棉 (NC) 樹脂相容性評估資料整理中。如需索取試驗配方，請與我們聯繫。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Maleic-Compatibility"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取相容性數據
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 8: 密著促進劑 (Adhesion Promoters)
                     ======================================================== -->
                <section id="tech-adhesion" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">宏威特化專利架橋技術</span>
                                <span>CPO 氯化聚烯烴與非氯系高分子</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                密著促進劑與難附著底材架橋技術 (Adhesion Promoter)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                專為 PP、TPO、PET、金屬等低表面能無極性難附著基材開發，免除繁複的火焰或電暈預處理工藝，提供優異的直接附著力、耐水煮與抗層間剝離性能。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/adhesion_promoter/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽密著促進劑規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Adhesion-Promoter"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取底材附著解決方案</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-crosshairs text-blue-600"></i>
                                <span>CPO 對聚丙烯晶格滲透咬合</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                氯化聚丙烯結構能於烘烤或溶劑揮發時直接滲透進入 PP、TPO 塑膠底材微觀晶格中，形成堅不可摧之分子互穿網絡。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-ban text-blue-600"></i>
                                <span>非氯系綠色環保架橋 (AT 194 / SK)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                符合電子產品與外銷無鹵素要求，利用多配位羥基與金屬、PET 底材螯合反應，耐熱耐黃變，百格測試穩達 5B。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-temperature-arrow-up text-blue-600"></i>
                                <span>耐沸水煮與耐濕熱抗剝離</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                介面鍵合具備優異耐水解耐酸鹼特性，經 100°C 沸水煮沸 2 小時或高溫高濕環境放置後，塗層依舊牢固不脫落。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-check-double"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">各類難附著基材 (PP / PET / 鋁合金) 百格測試對照報告</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            免電暈底塗處理劑技術說明與塗裝附著力報告整理中。如需寄送底材進行樣品附著力代測，歡迎聯繫技術顧問。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Adhesion-Test"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 預約底材附著力代測
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 9: 粉體塗料專用功能性助劑 (Powder Coating Additives)
                     ======================================================== -->
                <section id="tech-powder" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">宏威特化專利配方</span>
                                <span>粉體塗料專用功能性助劑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                粉體塗料專用功能性助劑技術 (Powder Additives)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                專為熱固性粉體塗料（環氧、聚酯、混合型）開發，涵蓋砂紋紋理劑、戶外耐候消光劑及塗層表面增硬抗劃傷功能材料。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/coating_additive/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽粉體助劑規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Powder-Additives"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取粉體配方手冊</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-mountain text-blue-600"></i>
                                <span>均勻立體砂紋紋理 (SA 207 / SA 208)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                藉由固化過程中的表面張力差引導，形成均勻立體、手感細緻的砂紋與皺紋質感，重現性極佳，遮蓋底材微瑕疵。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-sun-plant-wilt text-blue-600"></i>
                                <span>室外抗候消光不黃變 (K7212 / K7215)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專為戶外聚酯/TGIC、Primid 體系設計，反應型消光組分高溫烘烤不發黃，耐紫外線與耐氣候老化物性出眾。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-shield-virus text-blue-600"></i>
                                <span>表面增硬耐磨防金屬劃痕 (SA 2072)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                提高粉體塗層鉛筆硬度至 2H~3H，賦予塗膜優異抗重金屬劃痕 (Anti-Scratch) 與防黑印防指紋性能。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-wand-magic-sparkles"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">粉體塗料擠出工藝與紋理粒子大小調控技術資料</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            螺桿擠出溫度控制與固化爐升溫曲線對砂紋質感的影響分析圖表建置中。歡迎索取配方建議書。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Powder-Formula-Guide"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取粉體擠出工藝指引
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 10: PX 潤滑油添加劑 (PX Lubricant Additives)
                     ======================================================== -->
                <section id="tech-px" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Dorf Ketal 原廠技術 (原 ExxonMobil)</span>
                                <span>PX 系列特用潤滑添加劑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                PX 潤滑油特用添加劑技術 (PX Lubricant Additives)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                源自原 ExxonMobil 特用潤滑化學技術，涵蓋抗磨減摩劑、極壓抗咬合劑 (EP)、高溫抗氧化劑與腐蝕抑制劑，專門針對嚴苛工況提供極端接觸面摩擦保護。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/dorfketal/px/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽 PX 潤滑劑規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=PX-Lubricant"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取極壓抗磨評估報告</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-oil-well text-blue-600"></i>
                                <span>摩擦化學反應保護膜 (Tribofilm)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                在重載摩擦接觸點高溫瞬時壓力下，與金屬表面迅速化學反應生成低剪切力無機陶瓷保護膜，徹底防止擦傷與微點蝕。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-fire text-blue-600"></i>
                                <span>高溫熱氧化抑制與延長油品壽命</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                高效自由基捕獲與過氧化物分解能力，在渦輪機與天然氣引擎中顯著延緩油品酸值上升與沉渣生成，延長換油週期。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-circle-nodes text-blue-600"></i>
                                <span>高合成基礎油 (PAO / Ester) 相容性</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專為現代高純度合成 Group III、PAO 及多元醇酯類基礎油優化，低溫流動性優異，不渾濁不析出。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-gears"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">四球磨損測試 (Four-Ball Wear) 與極壓承載性能測試圖表</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            原廠齒輪油、金屬加工液與液壓油抗磨評估白皮書建置中。歡迎直接索取技術測試數據。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=PX-FourBall-Report"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取四球測試白皮書
                        </a>
                    </div>
                </section>

                <!-- ========================================================
                     分類 11: 聚酯樹脂與多元醇 (Polyester Resins)
                     ======================================================== -->
                <section id="tech-polyester" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">昆勒 / 宏威特化技術</span>
                                <span>同級 DYNAPOL® / DYNACOLL® 歐美一線</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                飽和共聚聚酯樹脂與多元醇比較技術 (Polyester Resin)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                提供食品級包裝罐頭塗料、捲材烤漆與反應型 PUR 熱熔膠專用高分子量飽和聚酯樹脂及低分子量端羥基聚酯多元醇，嚴格比照歐美一線同級規格。
                            </p>
                        </div>
                        <div class="shrink-0 flex flex-col sm:items-end gap-2">
                            <div class="flex items-center gap-2">
                                <a href="products/others/polyester_resin/"
                                   class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                    <i class="fa-solid fa-table-list"></i>
                                    <span>瀏覽聚酯樹脂規格</span>
                                </a>
                                <a href="contact/?mode=detailed&inquiry=Polyester-Benchmark"
                                   class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                    <i class="fa-solid fa-file-shield"></i>
                                    <span>索取歐美替代對照表</span>
                                </a>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-compass-drafting text-blue-600"></i>
                                <span>深抽衝壓成型與極致柔韌性 (0T 彎折)</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                高分子量共聚聚酯鏈段兼具高硬度與高延伸率，在金屬板捲材深衝壓、翻邊變形過程中漆膜無微裂紋、無脫落。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-bowl-food text-blue-600"></i>
                                <span>食品包裝合規與耐高溫蒸煮殺菌</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                符合 FDA 175.300 等食品接觸標準，高交聯密度漆膜經 121°C / 130°C 高壓殺菌釜蒸煮後，抗起泡與防腐蝕性極佳。
                            </p>
                        </div>
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <div class="flex items-center gap-2 text-blue-900 font-bold text-sm mb-1.5">
                                <i class="fa-solid fa-dna text-blue-600"></i>
                                <span>精準端羥基分子量與反應結晶性</span>
                            </div>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                專用多元醇 (CP 系列) 羥值精確、酸值極低、水分 < 0.05%，是合成高性能 PUR 熱熔膠與聚氨酯彈性體的關鍵先驅體。
                            </p>
                        </div>
                    </div>

                    <div class="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-6 text-center">
                        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center mx-auto mb-3 text-lg">
                            <i class="fa-solid fa-code-compare"></i>
                        </div>
                        <h4 class="text-sm font-bold text-slate-800 mb-1">聚酯樹脂 DYNAPOL® / DYNACOLL® 歐美同級型號全量對照手冊</h4>
                        <p class="text-xs text-slate-500 max-w-lg mx-auto mb-4">
                            分子量 (Mw)、玻璃化轉變溫度 (Tg) 與羥值對照清單整理中。如需索取測試樣品進行上機驗證，歡迎聯絡。
                        </p>
                        <a href="contact/?mode=detailed&inquiry=Polyester-Sample-Request"
                           class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fa-solid fa-envelope-open-text"></i> 索取測試樣品與型號指引
                        </a>
                    </div>
                </section>

            </div>
        </div>
    </section>

    <!-- 技術圖檔全螢幕 Lightbox 放大檢視彈窗 (無下載、保護原廠機密) -->
    <div id="tech-image-modal"
         class="fixed inset-0 z-50 hidden bg-slate-950/85 backdrop-blur-sm flex items-center justify-center p-3 sm:p-6"
         onclick="closeTechImageModal(event)">
        <div class="relative max-w-5xl w-full max-h-[95vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-slate-700/50"
             onclick="event.stopPropagation()">
            <!-- Modal Header -->
            <div class="px-5 py-3.5 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800 shrink-0">
                <div class="flex items-center gap-2.5">
                    <i class="fa-solid fa-file-image text-blue-400"></i>
                    <h3 id="tech-image-modal-title" class="text-sm sm:text-base font-bold text-white">原廠技術說明圖表</h3>
                    <span class="text-xs text-amber-400 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-800/80 hidden sm:inline-flex items-center gap-1">
                        <i class="fa-solid fa-lock text-[10px]"></i> 原廠機密技術，不可直接存取下載
                    </span>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="closeTechImageModal()"
                            class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors"
                            title="關閉 (ESC)">
                        <i class="fa-solid fa-xmark text-lg"></i>
                    </button>
                </div>
            </div>
            <!-- Modal Image Body -->
            <div class="flex-1 overflow-auto p-4 sm:p-6 bg-slate-100 flex items-center justify-center custom-scrollbar">
                <img id="tech-image-modal-img" src="" alt="技術說明圖"
                     class="max-w-full max-h-[78vh] object-contain rounded-lg shadow-md select-none pointer-events-auto"
                     oncontextmenu="return false;" draggable="false">
            </div>
            <!-- Modal Footer -->
            <div class="px-5 py-3 bg-white border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-600 shrink-0">
                <span>© 宏威應用材料 Alan & Thomas Technologies. All rights reserved.</span>
                <div class="flex items-center gap-3">
                    <a id="tech-image-modal-inquiry-btn" href="contact/?mode=detailed"
                       class="px-3.5 py-1.5 bg-blue-900 hover:bg-blue-800 text-white rounded-lg font-bold text-xs transition-colors flex items-center gap-1.5">
                        <i class="fa-solid fa-envelope"></i> 諮詢此技術配方
                    </a>
                    <button type="button" onclick="closeTechImageModal()"
                            class="px-3.5 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-lg font-semibold text-xs transition-colors">
                        關閉
                    </button>
                </div>
            </div>
        </div>
    </div>
'''

def build_tech_scripts_html():
    return '''
<!-- ==========================================
     技術專區單頁呈現切換與 Lightbox 控制腳本
     ========================================== -->
<script>
    let currentTyzorPage = 0;
    const totalTyzorPages = 4;

    function showTyzorPage(index) {
        if (index < 0) index = 0;
        if (index >= totalTyzorPages) index = totalTyzorPages - 1;
        currentTyzorPage = index;

        for (let i = 0; i < totalTyzorPages; i++) {
            const pageEl = document.getElementById('tyzor-page-' + i);
            const tabEl = document.getElementById('tyzor-tab-' + i);
            if (pageEl) {
                if (i === index) {
                    pageEl.classList.remove('hidden');
                } else {
                    pageEl.classList.add('hidden');
                }
            }
            if (tabEl) {
                if (i === index) {
                    tabEl.className = "tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all bg-blue-900 text-white shadow-xs";
                } else {
                    tabEl.className = "tyzor-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-700 hover:bg-white hover:text-blue-950 transition-all";
                }
            }
        }
        const indicator = document.getElementById('tyzor-page-indicator');
        if (indicator) indicator.textContent = (index + 1) + ' / ' + totalTyzorPages;
    }

    function prevTyzorPage() {
        showTyzorPage((currentTyzorPage - 1 + totalTyzorPages) % totalTyzorPages);
    }

    function nextTyzorPage() {
        showTyzorPage((currentTyzorPage + 1) % totalTyzorPages);
    }

    function openTechImageModal(imgSrc, title, inquiryTag) {
        const modal = document.getElementById('tech-image-modal');
        const modalImg = document.getElementById('tech-image-modal-img');
        const modalTitle = document.getElementById('tech-image-modal-title');
        const inquiryBtn = document.getElementById('tech-image-modal-inquiry-btn');
        if (!modal || !modalImg) return;
        modalImg.src = imgSrc;
        if (modalTitle) modalTitle.textContent = title || '原廠技術說明圖表';
        if (inquiryBtn && inquiryTag) {
            inquiryBtn.href = 'contact/?mode=detailed&inquiry=' + encodeURIComponent(inquiryTag);
        }
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeTechImageModal(e) {
        if (e && e.target && e.target.closest && e.target.closest('#tech-image-modal .relative')) {
            return;
        }
        const modal = document.getElementById('tech-image-modal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }

    window.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' || e.key === 'Esc') {
            closeTechImageModal();
        }
    });
</script>
'''


def update_file(file_path, is_technology_page=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    tech_html = build_tech_section_html()
    if not is_technology_page:
        # In index.html, tab-technology should not have active by default (about is active)
        tech_html = tech_html.replace('id="tab-technology" class="tab-content active"', 'id="tab-technology" class="tab-content"')

    # Find the section to replace: from <!-- Tab: 技術專區 to <!-- Tab 3: 合作夥伴
    # Or find <section id="tab-technology" to <section id="tab-partners"
    sec_start = html.find('id="tab-technology"')
    if sec_start == -1:
        print(f"Error: tab-technology not found in {file_path}")
        return False
    
    # Back up to comment before it if present
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)

    # Find next section
    next_sec = html.find('id="tab-partners"')
    if next_sec == -1:
        print(f"Error: tab-partners not found in {file_path}")
        return False
    prev_partner_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, next_sec)
    replace_end = prev_partner_comment if prev_partner_comment != -1 else html.rfind('<section', 0, next_sec)

    # Perform replacement
    new_html = html[:replace_start] + tech_html + "\n    " + html[replace_end:]

    # Now add the scripts before </body> if not already present
    if 'function showTyzorPage' not in new_html:
        body_close = new_html.rfind('</body>')
        if body_close != -1:
            scripts_html = build_tech_scripts_html()
            new_html = new_html[:body_close] + scripts_html + "\n" + new_html[body_close:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Successfully updated {file_path} (length before: {len(html)}, after: {len(new_html)})")
    return True

if __name__ == '__main__':
    update_file('technology/index.html', is_technology_page=True)
    update_file('index.html', is_technology_page=False)

