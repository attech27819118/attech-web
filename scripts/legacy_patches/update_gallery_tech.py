import os
import re

def build_gallery_tech_section():
    return '''    <!-- Tab: 技術專區 (Technology) - 11 大產品系列分類完備呈現 (畫廊展開型) -->
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
                            <span class="text-xs text-blue-300 font-semibold">11 大技術專題畫廊展示</span>
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
                     分類 1: 鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®) - 畫廊縮圖展開
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
                        <div class="shrink-0 flex items-center gap-2">
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

                    <!-- 機密保護說明橫幅 -->
                    <div class="flex items-center justify-between gap-2 text-xs text-slate-600 bg-slate-50 px-4 py-2.5 rounded-xl border border-slate-200">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-lock text-slate-500"></i>
                            <span><strong>原廠技術圖表（點擊縮圖可放大檢視，不開放存取下載）</strong></span>
                        </div>
                        <span class="text-slate-400 hidden sm:inline text-[11px]">共 4 項技術機理圖解</span>
                    </div>

                    <!-- 畫廊縮圖展開區 (Gallery Grid) -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                        <!-- 縮圖卡片 1: 催化應用 -->
                        <div class="bg-slate-50/70 border border-slate-200 rounded-xl p-3 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <!-- 圖上方打標題 -->
                            <div class="mb-2 pb-2 border-b border-slate-200/80">
                                <span class="text-[11px] font-bold text-blue-700 tracking-wider">類別一・催化應用</span>
                                <h4 class="text-sm font-bold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為催化劑">鈦（鋯）酸酯作為催化劑</h4>
                            </div>
                            <!-- 縮圖容器 -->
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-white border border-slate-200/80 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/catalyst.webp', '鈦（鋯）酸酯作為催化劑 (Tyzor® Catalysts)', 'Tyzor-Catalyst')">
                                <img src="techdata/tyzor/catalyst.webp" alt="鈦（鋯）酸酯作為催化劑"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 2: 交聯改性 -->
                        <div class="bg-slate-50/70 border border-slate-200 rounded-xl p-3 flex flex-col hover:border-emerald-400 hover:shadow-md transition-all group">
                            <!-- 圖上方打標題 -->
                            <div class="mb-2 pb-2 border-b border-slate-200/80">
                                <span class="text-[11px] font-bold text-emerald-700 tracking-wider">類別二・交聯改性</span>
                                <h4 class="text-sm font-bold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為交聯劑">鈦（鋯）酸酯作為交聯劑</h4>
                            </div>
                            <!-- 縮圖容器 -->
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-white border border-slate-200/80 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/crosslinker.webp', '鈦（鋯）酸酯作為交聯劑 (Tyzor® Crosslinkers)', 'Tyzor-Crosslinker')">
                                <img src="techdata/tyzor/crosslinker.webp" alt="鈦（鋯）酸酯作為交聯劑"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 3: 介面附著 -->
                        <div class="bg-slate-50/70 border border-slate-200 rounded-xl p-3 flex flex-col hover:border-blue-400 hover:shadow-md transition-all group">
                            <!-- 圖上方打標題 -->
                            <div class="mb-2 pb-2 border-b border-slate-200/80">
                                <span class="text-[11px] font-bold text-blue-700 tracking-wider">類別三・介面附著</span>
                                <h4 class="text-sm font-bold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯提高附著力">鈦（鋯）酸酯提高附著力</h4>
                            </div>
                            <!-- 縮圖容器 -->
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-white border border-slate-200/80 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/adhesion.webp', '鈦（鋯）酸酯提高附著力 (Tyzor® Adhesion Promoters)', 'Tyzor-Adhesion')">
                                <img src="techdata/tyzor/adhesion.webp" alt="鈦（鋯）酸酯提高附著力"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 縮圖卡片 4: 表面改性 -->
                        <div class="bg-slate-50/70 border border-slate-200 rounded-xl p-3 flex flex-col hover:border-amber-400 hover:shadow-md transition-all group">
                            <!-- 圖上方打標題 -->
                            <div class="mb-2 pb-2 border-b border-slate-200/80">
                                <span class="text-[11px] font-bold text-amber-700 tracking-wider">類別四・表面改性</span>
                                <h4 class="text-sm font-bold text-slate-900 line-clamp-1 mt-0.5" title="鈦（鋯）酸酯作為表面改性">鈦（鋯）酸酯作為表面改性</h4>
                            </div>
                            <!-- 縮圖容器 -->
                            <div class="relative aspect-[4/3] rounded-lg overflow-hidden bg-white border border-slate-200/80 cursor-pointer flex items-center justify-center p-1.5"
                                 onclick="openTechImageModal('techdata/tyzor/surface_treatment.webp', '鈦（鋯）酸酯作為表面改性 (Tyzor® Surface Modification)', 'Tyzor-Surface')">
                                <img src="techdata/tyzor/surface_treatment.webp" alt="鈦（鋯）酸酯作為表面改性"
                                     class="w-full h-full object-contain select-none transition-transform duration-300 group-hover:scale-105"
                                     loading="lazy" oncontextmenu="return false;" draggable="false">
                                <div class="absolute inset-0 bg-slate-950/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[1px]">
                                    <span class="px-2.5 py-1 bg-slate-900/90 text-white text-[11px] font-bold rounded-lg shadow-md flex items-center gap-1">
                                        <i class="fa-solid fa-magnifying-glass-plus"></i> 點擊放大
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 2: 矽烷偶合劑系列技術 (Silane) - 畫廊空白展位
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
                        <div class="shrink-0 flex items-center gap-2">
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

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">矽烷水解縮合機理與各底材配方比較表</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需特定樹脂（如水性 PU、環氧重防腐）之添加比例與催化指引，歡迎直接聯繫技術團隊。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=Silane-Formulation"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取具體配方指引
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 3: 擴鏈劑 (Chain Extenders) - 畫廊空白展位
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
                        <div class="shrink-0 flex items-center gap-2">
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

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">聚脲/聚氨酯擴鏈配方動力學曲線與比較指引</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需特定受阻胺反應速率、凝膠時間或固化劑配比諮詢，請與我們聯絡。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=ChainExtender-Formula"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 預約擴鏈技術評估
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 4: 特級碳黑 (Special Carbon Black) - 畫廊空白展位
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
                        <div class="shrink-0 flex items-center gap-2">
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

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">特級碳黑黑度 (My) 與色相 (dM) 分佈及分散機理圖</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需特級碳黑粒徑分佈、研磨流變性對照或抗靜電導電網絡配方指引，歡迎與我們聯絡。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=CarbonBlack-Dispersion"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取分散技術報告
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 5: 微粉蠟 (Micronized Wax) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-wax" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Micro Powders (MPI) 原廠技術</span>
                                <span>微粉蠟與 PTFE 替代方案</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                微粉化蠟極致耐磨耐刮與抗擦傷技術 (Micronized Wax)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                美國 Micro Powders 微米級表面改性助劑，針對木器漆、卷材塗料、油墨及工業塗料，提供卓越的耐刮擦性、平滑爽滑感及抗黏連性，具備完整無氟 PTFE-Free 解決方案。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/mpi/all/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 70+ 款 MPI 微粉蠟</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=MPI-Wax"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取 PTFE 替代對照表</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">微粉蠟表面浮移機理與動摩擦係數 (COF) 對照曲線</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需 PTFE-Free 無氟環保微粉蠟替代測試數據或耐磨耗測試報告，歡迎直接洽詢。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=PTFE-Free-Guide"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取 PTFE 替代指引
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 6: 消光粉 (Matting Agent) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-matting" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Evonik 原廠技術</span>
                                <span>ACEMATT® & AEROSIL® 系列消光粉</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                二氧化矽精密消光與表面紋理調控 (Matting Agent)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                高性能沉澱法與氣相二氧化矽消光劑，具備卓越消光效率、高透明度、細膩手感及極佳懸浮防硬沉特性，廣泛應用於木器塗料、塑膠塗料及皮革塗飾。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/others/matting_agent/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 7 款精密消光粉</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=Matting-Agent"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取消光粉規格比較手冊</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">消光粉粒徑分佈微觀散射光學模型與透明度測試數據</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需 60°/85° 消光光澤對照、透明度無霧影評估或防沉蠟處理指引，歡迎直接聯繫技術團隊。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=Matting-Efficiency"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 預約消光效率評估
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 7: 馬林酸樹脂 (Maleic Resin) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-maleic" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">捷通達 / 宏威特化</span>
                                <span>松香改性馬林酸樹脂</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                馬林酸樹脂快乾高光與環保醇溶改性技術 (Maleic Resin)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                天然松香經馬林酸酐改性並甘油/季戊四醇酯化的高性能樹脂，具備極快溶劑釋放性、極致光澤與豐滿度，醇溶型 MP 系列更是環保凹版油墨與水性光油的標竿選擇。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/others/maleic_acid_resin/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 11 款馬林酸樹脂</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=Maleic-Resin"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取樹脂配方應用指南</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">馬林酸樹脂醇溶性相容體系與耐熱性測試圖表</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需 MP-130 / MP-150 醇溶性耐溫油墨評估或顏料潤濕力測試數據，請洽詢技術團隊。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=Maleic-Inquiry"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取樹脂樣品與建議
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 8: 密著樹脂 (Adhesion Resin) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-adhesion" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">宏威特化</span>
                                <span>CPO 氯化聚烯烴與非氯系密著樹脂</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                密著促進劑與難附著非極性底材架橋技術 (Adhesion Promoters)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                針對未經電暈處理之聚丙烯 (PP)、TPO 及非極性塑膠基材，提供強效分子咬合；非氯系特種樹脂更具備優異耐高溫蒸煮與無鹵環保特性。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/others/cpo_adhesion_promoter/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 CPO 密著促進劑</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=Adhesion-Promoter"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取難附著底材測試評估</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">CPO 於 PP 底材熱熔滲透咬合微觀介面機理圖</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需 PP/EPDM 汽車保險桿底漆、鋁箔覆膜或難附著金屬架橋測試方案，歡迎預約技術評估。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=CPO-Substrate-Test"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 預約底材密著測試
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 9: 粉體塗料助劑 (Powder Coating Additives) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-powder" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">宏威特化</span>
                                <span>SA 系列粉體塗料專用功能助劑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                粉體塗料專用功能性紋理與消光助劑技術 (Powder Additives)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                專為環氧、聚酯與混合型粉體塗料開發之特種助劑，精確控制立體砂紋質感、流平排氣及物理消光，賦予塗層極高機械硬度與戶外耐候性。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/others/coating_additive/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽粉體塗料助劑</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=Powder-Additive"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取砂紋助劑樣品</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">粉體塗料反應速度差砂紋成形動力學機理圖</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需大/中/細砂紋立體質感樣板、消光固化劑比較或擠出工藝調整建議，歡迎聯繫技術專家。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=Powder-Texture"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取砂紋效果樣板
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 10: PX 潤滑油添加劑 (PX Lubricants) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-px" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">Dorf Ketal (原 ExxonMobil)</span>
                                <span>PX 系列潤滑油添加劑</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                PX 潤滑油特用抗磨與熱氧化穩定添加劑 (PX Lubricants)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                承襲原埃克森美孚技術傳承的高性能潤滑添加劑，在高溫極壓工況下形成高強度化學保護膜，大幅延長機械運轉壽命與換油週期。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/dorfketal/px/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 PX 潤滑油添加劑</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=PX-Lubricant"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取潤滑添加劑配方方案</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">極壓摩擦反應保護膜 (Tribofilm) 生成機制與磨損曲線</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需特種高溫鏈條油、抗磨液壓油複合劑或四球機磨斑測試對照數據，歡迎索取專用報告。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=PX-Tribo-Report"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取潤滑抗磨技術報告
                            </a>
                        </div>
                    </div>
                </section>

                <!-- ========================================================
                     分類 11: 聚酯樹脂 (Polyester Resin) - 畫廊空白展位
                     ======================================================== -->
                <section id="tech-polyester" class="scroll-mt-24 bg-white border border-gray-200 rounded-2xl shadow-xs p-6 sm:p-8 space-y-6">
                    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-gray-100">
                        <div>
                            <div class="inline-flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1.5">
                                <span class="px-2 py-0.5 rounded bg-blue-50 border border-blue-100">昆勒 / 宏威特化</span>
                                <span>飽和共聚聚酯樹脂與多元醇</span>
                            </div>
                            <h3 class="text-xl sm:text-2xl font-extrabold text-blue-950 flex items-center gap-2.5">
                                <span class="w-2.5 h-6 bg-blue-700 rounded-full inline-block"></span>
                                飽和共聚聚酯樹脂與多元醇比較技術 (Polyester Resin)
                            </h3>
                            <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
                                全系列飽和共聚聚酯，專為卷材塗料、食品罐頭內外壁塗料及 PUR 熱熔膠量身打造，具備極致衝壓柔韌性、耐蒸煮性與國際 FDA 食品接觸合規性，同級比照國際一線品牌。
                            </p>
                        </div>
                        <div class="shrink-0 flex items-center gap-2">
                            <a href="products/others/polyester_resin/"
                               class="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                                <i class="fa-solid fa-table-list"></i>
                                <span>瀏覽 37 款聚酯規格</span>
                            </a>
                            <a href="contact/?mode=detailed&inquiry=Polyester-Resin"
                               class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-xs transition-colors active:scale-95">
                                <i class="fa-solid fa-file-shield"></i>
                                <span>索取聚酯型號規格比較對照表</span>
                            </a>
                        </div>
                    </div>

                    <!-- 畫廊展位區：圖上方打標題，內容呈現暫無資料 -->
                    <div class="bg-slate-50/70 border border-dashed border-slate-300 rounded-2xl p-6 sm:p-8">
                        <div class="max-w-xl mx-auto text-center mb-5 pb-3 border-b border-slate-200">
                            <span class="text-xs font-bold text-blue-700 tracking-wider uppercase">原廠技術圖解與機理展位</span>
                            <h4 class="text-base font-bold text-slate-900 mt-1">共聚聚酯玻璃化轉變溫度 (Tg) 與柔韌深衝性能關聯圖</h4>
                        </div>
                        <div class="max-w-md mx-auto bg-white rounded-xl border border-slate-200 p-6 text-center shadow-xs">
                            <div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-3 text-lg">
                                <i class="fa-solid fa-image"></i>
                            </div>
                            <div class="inline-block px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold mb-2">
                                暫無資料
                            </div>
                            <p class="text-xs text-slate-500 leading-relaxed mb-4">
                                原廠技術資料整理中，暫無資料。<br>如需 DYNAPOL / DYNACOLL 替代型號比較表、FDA 食品接觸認證或 PUR 熱熔膠初黏力曲線，歡迎洽詢。
                            </p>
                            <a href="contact/?mode=detailed&inquiry=Polyester-Benchmark"
                               class="inline-flex items-center gap-1.5 px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-bold transition-colors">
                                <i class="fa-solid fa-envelope-open-text"></i> 索取型號規格比較手冊
                            </a>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </section>

    <!-- 技術圖檔全螢幕 Lightbox 放大檢視彈窗 (配合視窗自動調整 100% 完整畫面大小，無下載、保護原廠機密) -->
    <div id="tech-image-modal"
         class="hidden select-none"
         style="position: fixed; inset: 0; z-index: 99999; background: rgba(2, 6, 23, 0.92); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; padding: 12px; box-sizing: border-box; user-select: none;"
         onclick="closeTechImageModal(event)">
        <div style="position: relative; display: flex; flex-direction: column; width: 100%; max-width: 920px; height: calc(100vh - 24px); max-height: calc(100vh - 24px); background: #0f172a; border-radius: 16px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); overflow: hidden; border: 1px solid rgba(51, 65, 85, 0.8); margin: auto;"
             onclick="event.stopPropagation()">
            <!-- Modal Header (高度 48px) -->
            <div style="height: 48px; min-height: 48px; padding: 0 16px; background: #0f172a; color: white; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e293b; flex-shrink: 0; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
                    <i class="fa-solid fa-file-image" style="color: #60a5fa; font-size: 15px; flex-shrink: 0;"></i>
                    <h3 id="tech-image-modal-title" style="font-size: 13px; font-weight: bold; color: white; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 320px;">原廠技術說明圖表</h3>
                    <span style="font-size: 11px; color: #fde047; background: rgba(113, 63, 18, 0.5); padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(161, 98, 7, 0.5); white-space: nowrap; flex-shrink: 0;" class="hidden sm:inline-block">
                        <i class="fa-solid fa-lock" style="font-size: 9px;"></i> 原廠機密，不可下載
                    </span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                    <button type="button" id="tech-modal-zoom-btn" onclick="toggleTechModalZoom()"
                            style="height: 32px; padding: 0 10px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; color: #93c5fd; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.2s;"
                            title="切換檢視模式">
                        <i id="tech-modal-zoom-icon" class="fa-solid fa-magnifying-glass-plus"></i>
                        <span id="tech-modal-zoom-text" class="hidden sm:inline">放大滾動閱讀</span>
                    </button>
                    <button type="button" onclick="closeTechImageModal()"
                            style="width: 32px; height: 32px; border-radius: 8px; background: #1e293b; border: 1px solid #334155; color: #cbd5e1; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;"
                            title="關閉 (ESC)">
                        <i class="fa-solid fa-xmark" style="font-size: 16px;"></i>
                    </button>
                </div>
            </div>
            <!-- Modal Image Body (依視窗高度 100% 完整貼合顯示全圖) -->
            <div id="tech-image-container"
                 style="flex: 1 1 auto; min-height: 0; min-width: 0; width: 100%; height: calc(100% - 96px); padding: 8px; box-sizing: border-box; background: #020617; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                <img id="tech-image-modal-img" src="" alt="技術說明圖"
                     style="max-width: 100%; max-height: calc(100vh - 120px); width: auto; height: auto; object-fit: contain; display: block; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); pointer-events: auto; user-select: none;"
                     oncontextmenu="return false;" draggable="false">
            </div>
            <!-- Modal Footer (高度 48px) -->
            <div style="height: 48px; min-height: 48px; padding: 0 16px; background: #0f172a; border-top: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 11px; color: #94a3b8; flex-shrink: 0;">
                <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" class="hidden sm:inline">宏威應用材料原廠特化技術資料</span>
                <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0; margin-left: auto;">
                    <a id="tech-image-modal-inquiry-btn" href="contact/?mode=detailed"
                       style="padding: 6px 14px; background: #1e3a8a; color: white; border-radius: 8px; font-weight: bold; font-size: 12px; text-decoration: none; display: flex; align-items: center; gap: 6px; transition: background 0.2s;">
                        <i class="fa-solid fa-envelope" style="font-size: 11px;"></i> 諮詢此技術配方
                    </a>
                    <button type="button" onclick="closeTechImageModal()"
                            style="padding: 6px 14px; background: #1e293b; border: 1px solid #334155; color: #cbd5e1; border-radius: 8px; font-size: 12px; cursor: pointer; transition: all 0.2s;">
                        關閉
                    </button>
                </div>
            </div>
        </div>
    </div>'''

def update_file(file_path, is_technology_page=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    tech_html = build_gallery_tech_section()
    if not is_technology_page:
        # In index.html, tab-technology should not have active by default (about is active)
        tech_html = tech_html.replace('id="tab-technology" class="tab-content active"', 'id="tab-technology" class="tab-content"')

    sec_start = html.find('id="tab-technology"')
    if sec_start == -1:
        print(f"Error: tab-technology not found in {file_path}")
        return False
    
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)

    next_sec = html.find('id="tab-partners"')
    if next_sec == -1:
        print(f"Error: tab-partners not found in {file_path}")
        return False
    prev_partner_comment = html.rfind('<!-- Tab 3: 合作夥伴', 0, next_sec)
    replace_end = prev_partner_comment if prev_partner_comment != -1 else html.rfind('<section', 0, next_sec)

    new_html = html[:replace_start] + tech_html + "\n    " + html[replace_end:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Successfully updated {file_path} (length before: {len(html)}, after: {len(new_html)})")
    return True

if __name__ == '__main__':
    update_file('index.html', is_technology_page=False)
    import subprocess
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'build_technology_subpages.py')])
