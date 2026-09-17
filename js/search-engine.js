/**
 * ====================================================================
 * ATTech Web - Multi-Keyword Search Engine (search-engine.js)
 * ====================================================================
 */

class SearchEngine {
    /**
     * 解析搜尋字串為小寫且去重的關鍵字陣列（支援片語引號、空格、全形空格、逗號、加號）
     */
    static parseTokens(query) {
        if (!query || typeof query !== 'string') return [];
        const normalized = query.replace(/[\u3000,，+]/g, ' ').trim();
        if (!normalized) return [];

        const regex = /"([^"]+)"|'([^']+)'|(\S+)/g;
        const tokens = [];
        let match;
        while ((match = regex.exec(normalized)) !== null) {
            const token = (match[1] || match[2] || match[3] || '').trim();
            if (token && !tokens.some(t => t.toLowerCase() === token.toLowerCase())) {
                tokens.push(token);
            }
        }
        return tokens;
    }

    /**
     * 建立適用於中英文字符特性的搜尋正規表達式
     * - 中文字符：標準包含匹配 (因為中文詞彙間通常無空格分隔)
     * - 全純數字 (如 7212, 500, 100)：支援以非數字為邊界匹配 (例如 K7212 / SA501 也能精準匹配數字型號)
     * - 短英文字符 (<= 2 字元，如 SK, PE, PU, UV)：嚴格於單詞/標點/中英邊界匹配，避免像 anti-skid、temperature 誤判
     * - 一般英數字 (>= 3 字元)：於單詞開頭邊界匹配 (支援字首搜尋，但不會匹配到單詞中間)
     */
    static buildTokenRegex(token, forHighlight = false) {
        if (!token || typeof token !== 'string') return null;
        const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const isCJK = /[\u4e00-\u9fa5]/.test(token);
        const isAllDigits = /^\d+$/.test(token);

        if (isCJK) {
            return new RegExp(forHighlight ? `(${escaped})` : escaped, 'i');
        }

        if (isAllDigits) {
            if (token.length <= 2) {
                return new RegExp(forHighlight ? `(?<=^|[^0-9])(${escaped})(?=[^0-9]|$)` : `(?<=^|[^0-9])${escaped}(?=[^0-9]|$)`, 'i');
            }
            return new RegExp(forHighlight ? `(?<=^|[^0-9])(${escaped})` : `(?<=^|[^0-9])${escaped}`, 'i');
        }

        if (token.length <= 2) {
            return new RegExp(forHighlight ? `(?<=^|[^a-zA-Z0-9]|[\\u4e00-\\u9fa5])(${escaped})(?=[^a-zA-Z0-9]|[\\u4e00-\\u9fa5]|$)` : `(?<=^|[^a-zA-Z0-9]|[\\u4e00-\\u9fa5])${escaped}(?=[^a-zA-Z0-9]|[\\u4e00-\\u9fa5]|$)`, 'i');
        }

        return new RegExp(forHighlight ? `(?<=^|[^a-zA-Z0-9]|[\\u4e00-\\u9fa5])(${escaped})` : `(?<=^|[^a-zA-Z0-9]|[\\u4e00-\\u9fa5])${escaped}`, 'i');
    }

    /**
     * 計算產品與關鍵字的相關度權重分數 (AND 邏輯：所有 token 皆必須命中，否則分數為 0)
     * 分數分級：
     * - 產品型號完全一致：1000
     * - 產品型號標準化一致 (例如 SA501 匹配 SA 501 / SA-501)：800
     * - 產品型號字首符合：600
     * - 產品型號包含單詞：400
     * - 品牌名稱/代號符合：250
     * - 化學成分/組成符合：180
     * - 應用領域/特選分類/主要用途符合：120
     * - 性能描述/物理特性數值符合：50
     */
    static scoreProduct(p, tokens, lineKey = (typeof AppState !== 'undefined' ? AppState.productLine : ''), brandName = '') {
        if (!p) return 0;
        if (!tokens || tokens.length === 0) return 1;

        const appData = (typeof getAppSpecificData === 'function') ? getAppSpecificData(p, lineKey) : (p.applications_data?.[lineKey] || p);
        const pName = (p.product_name || '').trim();
        const brandCode = (p.brand_code || '').trim();
        const comp = [p.composition_zh, p.composition_en, p.chemical_component].filter(Boolean).join(' ');
        const usage = [
            p.main_usage,
            p.application_fields_zh,
            p.application_fields_en,
            (appData.featured_categories || p.featured_categories || []).join(' '),
            appData.application_fields_zh,
            appData.application_fields_en
        ].filter(Boolean).join(' ');

        // 僅提取數值內容，排除內部物件鍵名 (避免 density_g_cm3、anti_skinning 等鍵名被當成產品描述搜尋)
        const extractValuesOnly = (obj) => {
            if (!obj || typeof obj !== 'object') return '';
            return Object.values(obj).map(v => {
                if (v === null || v === undefined || v === false || v === '' || v === '—' || v === 'N/A') return '';
                if (typeof v === 'object') return extractValuesOnly(v);
                return String(v);
            }).join(' ');
        };

        const props = [
            p.properties,
            p.performance,
            p.features,
            p.function,
            extractValuesOnly(p.typical_properties),
            extractValuesOnly(appData.performance_descriptions_zh || p.performance_descriptions_zh),
            extractValuesOnly(appData.performance_descriptions_en || p.performance_descriptions_en),
            p.examples,
            appData.examples
        ].filter(Boolean).join(' ');

        const pNameNorm = pName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '').toLowerCase();

        let totalScore = 0;

        for (const token of tokens) {
            const regex = this.buildTokenRegex(token);
            if (!regex) continue;

            const tokLower = token.toLowerCase();
            const tokNorm = token.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '').toLowerCase();
            let tokenScore = 0;

            // 1. 產品名稱精確命中
            if (pName.toLowerCase() === tokLower) {
                tokenScore = Math.max(tokenScore, 1000);
            }
            // 2. 產品名稱去符號標準化完全相同 (例如 SA501 匹配 SA 501 / SA-501)
            else if (tokNorm && pNameNorm === tokNorm) {
                tokenScore = Math.max(tokenScore, 800);
            }
            // 3. 產品名稱字首符合或標準化包含 (例如 PropylTex 匹配 propyl)
            else if (pName.toLowerCase().startsWith(tokLower) || (tokNorm.length >= 3 && pNameNorm.startsWith(tokNorm))) {
                tokenScore = Math.max(tokenScore, 600);
            }
            // 4. 產品名稱邊界命中 (例如 PropylTex 100S 命中 100S 或 100)
            else if (regex.test(pName) || (tokNorm.length >= 3 && pNameNorm.includes(tokNorm))) {
                tokenScore = Math.max(tokenScore, 400);
            }

            // 5. 品牌代號或品牌名稱命中
            if (brandCode && regex.test(brandCode)) {
                tokenScore = Math.max(tokenScore, 250);
            }
            if (brandName && regex.test(brandName)) {
                tokenScore = Math.max(tokenScore, 200);
            }

            // 6. 化學組成 / 成分命中
            if (comp && regex.test(comp)) {
                tokenScore = Math.max(tokenScore, 180);
            }

            // 7. 應用領域 / 特選分類 / 主要用途命中
            if (usage && regex.test(usage)) {
                tokenScore = Math.max(tokenScore, 120);
            }

            // 8. 性能描述 / 特性數值內容命中
            if (props && regex.test(props)) {
                tokenScore = Math.max(tokenScore, 50);
            }

            // AND 邏輯：只要有任何一個 token 完全未在任何欄位命中，此產品即不符合
            if (tokenScore === 0) {
                return 0;
            }

            totalScore += tokenScore;
        }

        return totalScore;
    }

    /**
     * 提取產品所有可搜尋字串內容 (供除錯或純文字檢視)
     */
    static getSearchableText(p, lineKey = (typeof AppState !== 'undefined' ? AppState.productLine : ''), brandName = '') {
        if (!p) return '';
        const appData = (typeof getAppSpecificData === 'function') ? getAppSpecificData(p, lineKey) : (p.applications_data?.[lineKey] || p);
        const appCats = (appData.featured_categories || p.featured_categories || []).join(' ');

        const extractValuesOnly = (obj) => {
            if (!obj || typeof obj !== 'object') return '';
            return Object.values(obj).map(v => {
                if (v === null || v === undefined || v === false || v === '' || v === '—' || v === 'N/A') return '';
                if (typeof v === 'object') return extractValuesOnly(v);
                return String(v);
            }).join(' ');
        };

        return [
            p.product_name || '',
            p.brand_code || '',
            brandName || '',
            p.composition_zh || '',
            p.composition_en || '',
            p.chemical_component || '',
            p.properties || '',
            p.performance || '',
            p.main_usage || '',
            p.application_fields_zh || '',
            p.application_fields_en || '',
            p.recommended_system_type_zh || '',
            p.recommended_system_type_en || '',
            p.suggested_use_level_zh || '',
            p.suggested_use_level_en || '',
            p.appearance || '',
            p.active_content || '',
            p.production_method || '',
            p.examples || '',
            appData.examples || '',
            appData.application_fields_zh || '',
            appData.application_fields_en || '',
            appData.recommended_system_type_zh || '',
            appData.recommended_system_type_en || '',
            appData.suggested_use_level_zh || '',
            appData.suggested_use_level_en || '',
            p.features || '',
            p.function || '',
            appCats,
            extractValuesOnly(p.typical_properties),
            extractValuesOnly(appData.performance_descriptions_zh || p.performance_descriptions_zh),
            extractValuesOnly(appData.performance_descriptions_en || p.performance_descriptions_en),
            extractValuesOnly(p.system),
            extractValuesOnly(p.applications)
        ].join(' ');
    }

    /**
     * 判斷產品是否符合多個關鍵字（AND 邏輯）
     */
    static matchProduct(p, tokens, lineKey = (typeof AppState !== 'undefined' ? AppState.productLine : ''), brandName = '') {
        if (!tokens || tokens.length === 0) return true;
        return this.scoreProduct(p, tokens, lineKey, brandName) > 0;
    }

    /**
     * 關鍵字高亮渲染（HTML 安全轉義 + 柔和色彩標記，遵守單詞邊界規則避免破壞其他單詞）
     */
    static highlight(text, tokens) {
        if (!text || typeof text !== 'string') return text || '';
        if (!tokens || tokens.length === 0) return text;

        const sortedTokens = [...tokens]
            .filter(t => t && t.trim().length > 0)
            .sort((a, b) => b.length - a.length);

        if (sortedTokens.length === 0) return text;

        let marked = text;
        for (const token of sortedTokens) {
            const regex = this.buildTokenRegex(token, true);
            if (!regex) continue;
            // 使用保留之 Unicode Private Use Area 字元做標記，避免先跳脫 HTML 導致搜尋關鍵字破壞 HTML Entity
            marked = marked.replace(regex, '\uE000$1\uE001');
        }

        const escaped = marked
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');

        return escaped
            .replace(/\uE000/g, '<mark class="bg-amber-200/90 text-amber-950 px-1 py-0.5 rounded font-semibold shadow-2xs">')
            .replace(/\uE001/g, '</mark>');
    }
}
