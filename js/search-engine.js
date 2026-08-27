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
            const token = (match[1] || match[2] || match[3] || '').trim().toLowerCase();
            if (token && !tokens.includes(token)) {
                tokens.push(token);
            }
        }
        return tokens;
    }

    /**
     * 提取產品所有可搜尋字串內容
     */
    static getSearchableText(p, lineKey = AppState.productLine, brandName = '') {
        if (!p) return '';
        const appData = getAppSpecificData(p, lineKey);
        const appCats = (appData.featured_categories || p.featured_categories || []).join(' ');

        const extractValues = (obj) => {
            if (!obj || typeof obj !== 'object') return '';
            return Object.entries(obj).map(([k, v]) => {
                if (v === null || v === undefined || v === false || v === '' || v === '—' || v === 'N/A') return '';
                if (typeof v === 'object') return extractValues(v);
                if (typeof v === 'boolean') return v ? k : '';
                return `${k} ${v}`;
            }).join(' ');
        };

        const propsText = extractValues(p.typical_properties);
        const perfDescZh = extractValues(appData.performance_descriptions_zh || p.performance_descriptions_zh);
        const perfDescEn = extractValues(appData.performance_descriptions_en || p.performance_descriptions_en);
        const systemText = extractValues(p.system);
        const appsText = extractValues(p.applications);

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
            propsText,
            perfDescZh,
            perfDescEn,
            systemText,
            appsText
        ].join(' ').toLowerCase();
    }

    /**
     * 判斷產品是否符合多個關鍵字（AND 邏輯：所有 token 皆必須存在於產品欄位中）
     */
    static matchProduct(p, tokens, lineKey = AppState.productLine, brandName = '') {
        if (!tokens || tokens.length === 0) return true;
        const searchBase = this.getSearchableText(p, lineKey, brandName);
        return tokens.every(token => searchBase.includes(token));
    }

    /**
     * 關鍵字高亮渲染（HTML 安全轉義 + 柔和色彩標記）
     */
    static highlight(text, tokens) {
        if (!text || typeof text !== 'string') return text || '';
        if (!tokens || tokens.length === 0) return text;

        const escaped = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');

        const sortedTokens = [...tokens]
            .filter(t => t && t.trim().length > 0)
            .sort((a, b) => b.length - a.length);

        if (sortedTokens.length === 0) return escaped;

        const escapedRegexTokens = sortedTokens.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        const regex = new RegExp(`(${escapedRegexTokens.join('|')})`, 'gi');

        return escaped.replace(regex, '<mark class="bg-amber-200/90 text-amber-950 px-1 py-0.5 rounded font-semibold shadow-2xs">$1</mark>');
    }
}
