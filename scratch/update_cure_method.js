const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let content = fs.readFileSync(indexPath, 'utf8');

const target = `<label
                                                class="inline-flex items-center gap-1 cursor-pointer border-l border-slate-300 pl-3"><input
                                                    type="checkbox" id="detail-no-bake" name="detail_no_bake"
                                                    class="rounded text-blue-900"> 不烘烤（風乾）</label>
                                            <div
                                                class="inline-flex items-center gap-1.5 border-l border-slate-300 pl-3">
                                                <label for="detail-bake-temp"
                                                    class="f-weight-bold text-slate-900 f-size-xs">烘烤溫度：</label>
                                                <input type="text" id="detail-bake-temp" name="detail_bake_temp"
                                                    placeholder="如: 120℃"
                                                    class="w-20 px-1.5 py-0.5 bg-white border border-slate-300 rounded text-center outline-none focus:border-blue-900 text-slate-900 f-weight-medium placeholder-slate-500">
                                                <label for="detail-bake-time"
                                                    class="f-weight-bold text-slate-900 ml-0.5 f-size-xs">時間：</label>
                                                <input type="text" id="detail-bake-time" name="detail_bake_time"
                                                    placeholder="如: 20 min"
                                                    class="w-20 px-1.5 py-0.5 bg-white border border-slate-300 rounded text-center outline-none focus:border-blue-900 text-slate-900 f-weight-medium placeholder-slate-500">
                                            </div>`;

const replacement = `<div class="inline-flex items-center gap-2 border-l border-slate-300 pl-3">
                                                <span class="f-weight-bold text-slate-900 f-size-xs">固化方式：</span>
                                                <label class="inline-flex items-center gap-1 cursor-pointer hover:text-blue-900">
                                                    <input type="radio" name="detail_cure_type" id="detail-cure-bake" value="烘烤"
                                                        class="text-blue-900 focus:ring-blue-500/20" checked> 烘烤
                                                </label>
                                                <label class="inline-flex items-center gap-1 cursor-pointer hover:text-blue-900">
                                                    <input type="radio" name="detail_cure_type" id="detail-cure-air" value="風乾"
                                                        class="text-blue-900 focus:ring-blue-500/20"> 常溫風乾
                                                </label>
                                            </div>
                                            <div id="detail-bake-params"
                                                class="inline-flex items-center gap-1.5 border-l border-slate-300 pl-3 transition-opacity duration-200">
                                                <label for="detail-bake-temp"
                                                    class="f-weight-bold text-slate-900 f-size-xs">烘烤溫度：</label>
                                                <input type="text" id="detail-bake-temp" name="detail_bake_temp"
                                                    placeholder="如: 120℃"
                                                    class="w-20 px-1.5 py-0.5 bg-white border border-slate-300 rounded text-center outline-none focus:border-blue-900 text-slate-900 f-weight-medium placeholder-slate-500">
                                                <label for="detail-bake-time"
                                                    class="f-weight-bold text-slate-900 ml-0.5 f-size-xs">時間：</label>
                                                <input type="text" id="detail-bake-time" name="detail_bake_time"
                                                    placeholder="如: 20 min"
                                                    class="w-20 px-1.5 py-0.5 bg-white border border-slate-300 rounded text-center outline-none focus:border-blue-900 text-slate-900 f-weight-medium placeholder-slate-500">
                                            </div>
                                            <input type="checkbox" id="detail-no-bake" name="detail_no_bake" class="hidden" tabindex="-1" aria-hidden="true">`;

const normalize = s => s.replace(/\r\n/g, '\n');

if (normalize(content).includes(normalize(target))) {
    const isCRLF = content.includes('\r\n');
    const actualTarget = isCRLF ? target.replace(/\r?\n/g, '\r\n') : target.replace(/\r?\n/g, '\n');
    const actualReplacement = isCRLF ? replacement.replace(/\r?\n/g, '\r\n') : replacement.replace(/\r?\n/g, '\n');
    content = content.replace(actualTarget, actualReplacement);
    fs.writeFileSync(indexPath, content, 'utf8');
    console.log('✅ index.html updated successfully!');
} else {
    console.error('❌ Target not found in index.html');
    process.exit(1);
}

