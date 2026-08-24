/**
 * ====================================================================
 * ATTech Web - Product Filter Engine & Sorting Logic (filter-engine.js)
 * ====================================================================
 */

class ProductFilterEngine {
    static filter(products, {partner, category, searchQuery, filters}) {
        const currentPartnerKey = partnerConfigMap[partner] || 'mpi';
        const tokens = searchQuery ? SearchEngine.parseTokens(searchQuery) : [];

        return products.filter(p => {
            const appData = getAppSpecificData(p);

            if (tokens.length > 0) {
                if (!SearchEngine.matchProduct(p, tokens)) return false;
            }

            if (currentPartnerKey === 'mpi') {
                const activeFilters = Object.keys(filters || {}).filter(k => filters[k] === true);
                if (activeFilters.length > 0) {
                    const ratings = appData.performance_ratings || p.performance_ratings;
                    if (!ratings) return false;
                    const matchAll = activeFilters.every(fKey => (ratings[fKey] || 0) > 0);
                    if (!matchAll) return false;
                }
            }

            if (category && category !== 'all') {
                return ProductFilterEngine.matchCategory(p, category, currentPartnerKey);
            }

            return true;
        });
    }

    static matchCategory(p, catTarget, partnerKey, lineKey = AppState.productLine) {
        if (!catTarget || catTarget === 'all') return true;

        const appData = getAppSpecificData(p, lineKey);
        const cats = appData.featured_categories || p.featured_categories;

        if (cats) {
            const catArray = Array.isArray(cats) ? cats : String(cats).split(',').map(s => s.trim());
            if (catArray.includes(catTarget)) return true;
        }

        if (partnerKey === 'dorfketal') {
            const comp = String(p.chemical_component || p.composition_zh || '').toLowerCase();
            const isZirconate = comp.includes('鋯') || comp.includes('zircon');
            if (catTarget === '鈦酸酯') return !isZirconate;
            if (catTarget === '鋯酸酯') return isZirconate;
        }

        if (p.applications && typeof p.applications === 'object' && p.applications[catTarget]) return true;
        if (p.system && typeof p.system === 'object' && p.system[catTarget]) return true;

        const targetLower = catTarget.toLowerCase();
        const fields = [p.application_fields_zh, p.application_fields_en, p.properties, p.function, p.chemical_component, p.recommended_system_type_zh, p.main_usage];
        return fields.some(f => f && String(f).toLowerCase().includes(targetLower));
    }
}

function compareSortValues(aRaw, bRaw, sortOrder = 'desc') {
    const isInvalid = (val) => val === null || val === undefined || val === '' || val === '—' || val === 'N/A';
    const isInvalidA = isInvalid(aRaw);
    const isInvalidB = isInvalid(bRaw);

    if (isInvalidA && isInvalidB) return 0;
    if (isInvalidA) return 1;
    if (isInvalidB) return -1;

    const parseNum = (val) => {
        if (typeof val === 'number') return val;
        if (typeof val === 'string') {
            const trimmed = val.trim();
            if (/^-?\d+(\.\d+)?/.test(trimmed)) {
                return parseFloat(trimmed);
            }
        }
        return NaN;
    };

    const numA = parseNum(aRaw);
    const numB = parseNum(bRaw);

    let result = 0;
    if (!isNaN(numA) && !isNaN(numB)) {
        result = numA - numB;
    } else {
        result = String(aRaw).localeCompare(String(bRaw), 'zh-TW', {numeric: true, sensitivity: 'base'});
    }

    return sortOrder === 'desc' ? -result : result;
}

function handleSort(columnKey) {
    if (AppState.sortColumn === columnKey) {
        AppState.sortOrder = AppState.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        AppState.sortColumn = columnKey;
        AppState.sortOrder = 'desc';
    }
    if (typeof renderProducts === 'function') {
        renderProducts();
    }
}
