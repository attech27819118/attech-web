/**
 * ====================================================================
 * ATTech Web - Dynamic Table Renderer & Accordion Cards (table-renderer.js)
 * ====================================================================
 */

function renderProductActions(p, partnerKey = null, lineKey = null) {
    const isSelected = AppState.compareList.some(item => item.product_name === p.product_name);
    const pKey = partnerKey || AppState.partner;
    const lKey = lineKey || AppState.productLine;
    const compareTitle = isSelected
        ? (AppState.lang === 'zh' ? '從比較清單移除' : 'Remove from compare')
        : (AppState.lang === 'zh' ? '加入比較 (最多4項)' : 'Add to compare (max 4)');
    const compareLabel = isSelected
        ? (AppState.lang === 'zh' ? '已比' : 'Added')
        : (AppState.lang === 'zh' ? '比較' : 'Compare');

    return `
    <div class="flex items-center gap-1.5 shrink-0 select-none mt-1.5 whitespace-nowrap">
        <button data-action="toggle-compare" data-product="${p.product_name}" data-partner="${pKey}" data-line="${lKey}" class="compare-icon-btn inline-flex items-center gap-1 px-2 py-0.5 h-6 rounded-md transition-all ${isSelected ? 'bg-blue-900 text-white shadow-xs ring-1 ring-blue-400 border border-blue-900' : 'text-slate-600 hover:text-blue-900 hover:bg-blue-50 bg-slate-50 border border-slate-200'} active:scale-90 text-[11px] font-medium cursor-pointer shrink-0 whitespace-nowrap" title="${compareTitle}" aria-label="${isSelected ? '從比較清單移除' : '加入比較'}">
            <i class="fa-solid ${isSelected ? 'fa-check text-emerald-300' : 'fa-scale-balanced'} text-[10px] shrink-0"></i>
            <span class="shrink-0 whitespace-nowrap">${compareLabel}</span>
        </button>
    </div>`;
}

function renderCompareIcon(p, partnerKey = null, lineKey = null) {
    return renderProductActions(p, partnerKey, lineKey);
}

const DynamicTableRenderer = {
    layoutDefinitions: {
        powder_coating_additive: [
            {
                id: 'product_name',
                title: '產品名稱',
                class: 'w-[22%] min-w-[150px]',
                getValue: p => p.product_name,
                render: p => `
                <div class="flex flex-col items-start gap-1 w-full py-0.5">
                    <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                    ${renderCompareIcon(p, 'Others', 'powder_coating_additive')}
                </div>`
            },
            {
                id: 'main_usage',
                title: '主要用途',
                class: 'w-[25%] min-w-[150px]',
                getValue: p => p.main_usage || p.composition_zh,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.main_usage || p.composition_zh || '—'}</span>`
            },
            {
                id: 'performance',
                title: '應用性能',
                class: 'w-[25%] min-w-[180px]',
                getValue: p => p.performance || p.properties,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.performance || p.properties || '—'}</span>`
            },
            {
                id: 'usage',
                title: '用法與用量',
                class: 'w-[28%] min-w-[130px]',
                getValue: p => p.suggested_use_level_zh || p.suggested_use_level || p.dosage,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.suggested_use_level_zh || p.suggested_use_level || p.dosage || '—'}</span>`
            }
        ],
        matting_agent: {
            headerRows: [
                [
                    {title: '產品名稱', class: 'w-[15%] min-w-[140px] text-center'},
                    {title: '表面處理\n化學性質', class: 'w-[12%] min-w-[130px] text-center'},
                    {title: '適用系統', class: 'w-[10%] min-w-[80px] text-center'},
                    {
                        title: '粒徑<br><span class="f-size-xs f-weight-normal text-slate-500">(µm)</span>',
                        class: 'w-[6%] min-w-[55px] text-center'
                    },
                    {
                        title: '吸油量<br><span class="f-size-xs f-weight-normal text-slate-500">(g/100g)</span>',
                        class: 'w-[8%] min-w-[60px] text-center'
                    },
                    {
                        title: '密度<br><span class="f-size-xs f-weight-normal text-slate-500">(g/cm³)</span>',
                        class: 'w-[6%] min-w-[55px] text-center'
                    },
                    {title: '作用', class: 'w-[21%] min-w-[160px]'},
                    {title: '木器漆', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '烤漆', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '塑膠塗料', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '皮革塗料', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '尼龍織物', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '油墨', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: '水性', class: 'w-[3.5%] min-w-[35px] text-center'},
                    {title: 'UV', class: 'w-[3.5%] min-w-[35px] text-center'}
                ]
            ],
            columns: [
                {
                    id: 'product_name',
                    class: 'w-[15%] min-w-[140px]',
                    getValue: p => p.product_name,
                    render: p => `
                    <div class="flex flex-col items-start gap-1 w-full py-0.5">
                        <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                        ${renderCompareIcon(p, 'Others', 'matting_agent')}
                    </div>`
                },
                {
                    id: 'surface_treatment',
                    class: 'w-[13%] min-w-[130px]',
                    getValue: p => p.surface_treatment || p.chemical_component || (Array.isArray(p.featured_categories) ? p.featured_categories.join(', ') : p.featured_categories),
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.featured_categories || '—'}</span>`
                },
                {
                    id: 'system',
                    class: 'w-[8%] min-w-[80px] text-center',
                    getValue: p => p.recommended_system_type_zh || p.recommended_system_type || p.system,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.recommended_system_type_zh || p.recommended_system_type || (typeof p.system === 'string' ? p.system : '') || '—'}</span>`
                },
                {
                    id: 'mean_size',
                    class: 'w-[6%] min-w-[55px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.mean_particle_size_um || p.particle_size
                },
                {
                    id: 'oil',
                    class: 'w-[6%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.oil_absorption_number || p.oil_absorption
                },
                {
                    id: 'density',
                    class: 'w-[6%] min-w-[55px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.density_g_cc_25c || p.density
                },
                {
                    id: 'properties',
                    class: 'w-[21%] min-w-[160px]',
                    getValue: p => p.properties,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
                },
                {
                    id: 'wood',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_wood_coating || p.solvent_base_wood_coating) ? '✓' : ' '
                },
                {
                    id: 'baking',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_powder_coatings || p.solvent_base_powder_coatings) ? '✓' : ' '
                },
                {
                    id: 'plastic',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_plastic_coatings || p.solvent_base_plastic_coatings) ? '✓' : ' '
                },
                {
                    id: 'leather',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_leather_coatings || p.solvent_base_leather_coatings) ? '✓' : ' '
                },
                {
                    id: 'nylon',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_nylon_coated_fabric || p.solvent_base_nylon_coated_fabric) ? '✓' : ' '
                },
                {
                    id: 'ink',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_inks || p.solvent_base_inks) ? '✓' : ' '
                },
                {
                    id: 'waterbased',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.system?.waterborne || p.waterborne) ? '✓' : ' '
                },
                {
                    id: 'uv',
                    class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.system?.uv_coatings_and_inks || p.uv_coatings_and_inks) ? '✓' : ' '
                }
            ]
        },
        maleic_acid_resin: {
            headerRows: [
                [
                    {title: '產品名稱', class: 'w-[18%] min-w-[145px] text-center'},
                    {title: '色澤', class: 'w-[8%] min-w-[60px] text-center'},
                    {title: '軟化點', class: 'w-[8%] min-w-[60px] text-center'},
                    {
                        title: '酸值<br><span class="f-size-xs f-weight-normal text-slate-500">(mgKOH/g)</span>',
                        class: 'w-[10%] min-w-[80px] text-center'
                    },
                    {title: '特性', class: 'w-[25%] min-w-[180px] text-center'},
                    {title: '木器漆', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: '噴瓷漆', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: 'PU機械漆', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: '路標漆', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: '油墨', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: '熱熔膠', class: 'w-[5%] min-w-[40px] text-center'},
                    {title: '密封膠', class: 'w-[5%] min-w-[40px] text-center'}
                ]
            ],
            columns: [
                {
                    id: 'product_name',
                    class: 'w-[18%] min-w-[145px]',
                    getValue: p => p.product_name,
                    render: p => `
                    <div class="flex flex-col items-start gap-1 w-full py-0.5">
                        <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                        ${renderCompareIcon(p, 'Others', 'maleic_acid_resin')}
                    </div>`
                },
                {
                    id: 'appearance',
                    class: 'w-[8%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.appearance || p.chemical_component || (Array.isArray(p.appearance) ? p.appearance.join(', ') : p.appearance)
                },
                {
                    id: 'softening_point',
                    class: 'w-[8%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.softening_point || p.softening_point
                },
                {
                    id: 'acid_value',
                    class: 'w-[10%] min-w-[80px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.acid_value || p.acid_value
                },
                {
                    id: 'properties',
                    class: 'w-[25%] min-w-[180px]',
                    getValue: p => p.properties,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
                },
                {
                    id: 'wood_coating',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.wood_coating || p.wood_coating) ? '✓' : ' '
                },
                {
                    id: 'enamel_paint',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.enamel_paint || p.enamel_paint) ? '✓' : ' '
                },
                {
                    id: 'pu_industrial_coating',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.pu_industrial_coating || p.pu_industrial_coating) ? '✓' : ' '
                },
                {
                    id: 'traffic_paint',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.traffic_paint || p.traffic_paint) ? '✓' : ' '
                },
                {
                    id: 'ink',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.ink || p.ink) ? '✓' : ' '
                },
                {
                    id: 'hot_glue',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.hot_glue || p.hot_glue) ? '✓' : ' '
                },
                {
                    id: 'sealant',
                    class: 'w-[5%] min-w-[40px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.sealant || p.sealant) ? '✓' : ' '
                }
            ]
        },
        silane: {
            headerRows: [
                [
                    {title: '產品名稱', class: 'w-[16%] min-w-[140px] text-center'},
                    {title: '描述 / 主成分', class: 'w-[15%] min-w-[150px] text-center'},
                    {
                        title: '密度<br><span class="f-size-xs f-weight-normal text-slate-500">(g/cm³)</span>',
                        class: 'w-[7%] min-w-[60px] text-center'
                    },
                    {
                        title: '閃點<br><span class="f-size-xs f-weight-normal text-slate-500">(°C)</span>',
                        class: 'w-[7%] min-w-[60px] text-center'
                    },
                    {
                        title: '沸點<br><span class="f-size-xs f-weight-normal text-slate-500">(°C)</span>',
                        class: 'w-[7%] min-w-[60px] text-center'
                    },
                    {title: 'pH', class: 'w-[8%] min-w-[50px] text-center'},
                    {title: '特性 / 優點', class: 'w-[23%] min-w-[180px]'},
                    {title: '密著促進', class: 'w-[3%] min-w-[35px] text-center'},
                    {title: '化學合成', class: 'w-[3%] min-w-[35px] text-center'},
                    {title: '共黏合劑', class: 'w-[3%] min-w-[35px] text-center'},
                    {title: '交聯劑', class: 'w-[3%] min-w-[35px] text-center'},
                    {title: '表面改質', class: 'w-[3%] min-w-[35px] text-center'}
                ]
            ],
            columns: [
                {
                    id: 'product_name',
                    class: 'w-[16%] min-w-[140px]',
                    getValue: p => p.product_name,
                    render: p => `
                    <div class="flex flex-col items-start gap-1 w-full py-0.5">
                        <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                        ${renderCompareIcon(p, 'Others', 'silane')}
                    </div>`
                },
                {
                    id: 'comp',
                    class: 'w-[15%] min-w-[150px]',
                    getValue: p => p.chemical_component || p.composition_zh,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.chemical_component || p.composition_zh || '—'}</span>`
                },
                {
                    id: 'density',
                    class: 'w-[7%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.density_g_cc_25c || p.density
                },
                {
                    id: 'flash_point',
                    class: 'w-[7%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.flash_point || p.flash_point
                },
                {
                    id: 'boiling_point',
                    class: 'w-[7%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.boiling_point || p.boiling_point
                },
                {
                    id: 'ph_value',
                    class: 'w-[8%] min-w-[50px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.ph_value || p.ph_value
                },
                {
                    id: 'properties',
                    class: 'w-[23%] min-w-[180px]',
                    getValue: p => p.properties,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
                },
                {
                    id: 'adhesion_promoter',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.adhesion_promoter || p.system?.adhesion_promoter || p.applications?.adhesion_promoter) ? '✓' : ' '
                },
                {
                    id: 'chemical_synthesis',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.chemical_synthesis || p.system?.chemical_synthesis || p.applications?.chemical_synthesis) ? '✓' : ' '
                },
                {
                    id: 'comonomer',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.comonomer || p.system?.comonomer || p.applications?.comonomer) ? '✓' : ' '
                },
                {
                    id: 'crosslinking_agent',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.crosslinking_agent || p.system?.crosslinking_agent || p.applications?.crosslinking_agent) ? '✓' : ' '
                },
                {
                    id: 'surface_modifier',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.surface_modifier || p.system?.surface_modifier || p.applications?.surface_modifier) ? '✓' : ' '
                }
            ]
        },
        cpo_adhesion_promoter: {
            headerRows: [
                [
                    {title: '產品名稱', class: 'w-[16%] min-w-[140px] text-center'},
                    {title: '化學性質', class: 'w-[14%] min-w-[130px] text-center'},
                    {title: '適用系統', class: 'w-[12%] min-w-[100px] text-center'},
                    {title: '玻璃轉化點\nTg°C', class: 'w-[10%] min-w-[70px] text-center'},
                    {title: '氯含量', class: 'w-[8%] min-w-[60px] text-center'},
                    {title: '黏度mPa.s', class: 'w-[8%] min-w-[60px] text-center'},
                    {title: '作用', class: 'w-[20%] min-w-[150px]'},
                    {title: '油墨', class: 'w-[6%] min-w-[45px] text-center'},
                    {title: '塗料', class: 'w-[6%] min-w-[45px] text-center'}
                ]
            ],
            columns: [
                {
                    id: 'product_name',
                    class: 'w-[16%] min-w-[140px]',
                    getValue: p => p.product_name,
                    render: p => `
                    <div class="flex flex-col items-start gap-1 w-full py-0.5">
                        <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                        ${renderCompareIcon(p, 'Others', 'cpo_adhesion_promoter')}
                    </div>`
                },
                {
                    id: 'composition',
                    class: 'w-[14%] min-w-[130px]',
                    getValue: p => p.composition_zh || (Array.isArray(p.composition_zh) ? p.composition_zh.join(', ') : p.composition_zh),
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.composition_zh || '—'}</span>`
                },
                {
                    id: 'system',
                    class: 'w-[12%] min-w-[100px] text-center',
                    getValue: p => p.recommended_system_type_zh,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.recommended_system_type_zh || (typeof p.system === 'string' ? p.system : '') || '—'}</span>`
                },
                {
                    id: 'softening_point',
                    class: 'w-[9%] min-w-[70px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.softening_point || p.softening_point
                },
                {
                    id: 'chlorine_content',
                    class: 'w-[8%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.chlorine_content || p.chlorine_content
                },
                {
                    id: 'viscosity',
                    class: 'w-[8%] min-w-[60px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.viscosity || p.viscosity
                },
                {
                    id: 'properties',
                    class: 'w-[22%] min-w-[150px]',
                    getValue: p => p.properties,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
                },
                {
                    id: 'ink',
                    class: 'w-[6%] min-w-[45px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.ink || p.ink) ? '✓' : ' '
                },
                {
                    id: 'industrial coating',
                    class: 'w-[6%] min-w-[45px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.industrial_coating || p.industrial_coating) ? '✓' : ' '
                }
            ]
        },
        adhesion_promoter: {
            headerRows: [
                [
                    {title: '產品名稱', class: 'w-[15%] min-w-[145px] text-center'},
                    {title: '化學性質', class: 'w-[15%] min-w-[120px] text-center'},
                    {title: '適用系統', class: 'w-[10%] min-w-[85px] text-center'},
                    {title: '玻璃轉化點\nTg°C', class: 'w-[12%] min-w-[70px] text-center'},
                    {title: '羥基OH value', class: 'w-[8%] min-w-[65px] text-center'},
                    {title: '酸價', class: 'w-[7%] min-w-[55px] text-center'},
                    {title: '作用', class: 'w-[18%] min-w-[140px]'},
                    {
                        title: '木器漆',
                        class: 'w-[3%] min-w-[35px] text-center'
                    },
                    {
                        title: '烤漆',
                        class: 'w-[3%] min-w-[35px] text-center'
                    },
                    {
                        title: '塑膠塗料',
                        class: 'w-[3%] min-w-[35px] text-center'
                    },
                    {
                        title: '皮革塗料',
                        class: 'w-[3%] min-w-[35px] text-center'
                    },
                    {
                        title: '油墨',
                        class: 'w-[3%] min-w-[35px] text-center'
                    },
                    {title: '水性', class: 'w-[3%] min-w-[35px] text-center'},
                    {title: 'UV', class: 'w-[3%] min-w-[35px] text-center'}
                ]
            ],
            columns: [
                {
                    id: 'product_name',
                    class: 'w-[15%] min-w-[145px]',
                    getValue: p => p.product_name,
                    render: p => `
                    <div class="flex flex-col items-start gap-1 w-full py-0.5">
                        <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                        ${renderCompareIcon(p, 'Others', 'adhesion_promoter')}
                    </div>`
                },
                {
                    id: 'composition_zh',
                    class: 'w-[15%] min-w-[120px]',
                    getValue: p => p.composition_zh || (Array.isArray(p.composition_zh) ? p.composition_zh.join(', ') : p.composition_zh),
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.composition_zh || '—'}</span>`
                },
                {
                    id: 'system',
                    class: 'w-[10%] min-w-[85px] text-center',
                    getValue: p => p.recommended_system_type_zh || p.recommended_system_type || p.system,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.recommended_system_type_zh || p.recommended_system_type || (typeof p.system === 'string' ? p.system : '') || '—'}</span>`
                },
                {
                    id: 'softening_point',
                    class: 'w-[8%] min-w-[65px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.softening_point || p.softening_point
                },
                {
                    id: 'OH_value',
                    class: 'w-[8%] min-w-[65px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.OH_value || p.OH_value
                },
                {
                    id: 'acid_value',
                    class: 'w-[7%] min-w-[55px] text-center f-weight-medium text-slate-900',
                    getValue: p => p.typical_properties?.acid_value || p.acid_value
                },
                {
                    id: 'properties',
                    class: 'w-[18%] min-w-[140px]',
                    getValue: p => p.properties,
                    render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
                },
                {
                    id: 'wood',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_wood_coating || p.solvent_base_wood_coating) ? '✓' : ' '
                },
                {
                    id: 'baking',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_powder_coatings || p.solvent_base_powder_coatings) ? '✓' : ' '
                },
                {
                    id: 'plastic',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_plastic_coatings || p.solvent_base_plastic_coatings) ? '✓' : ' '
                },
                {
                    id: 'leather',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_leather_coatings || p.solvent_base_leather_coatings) ? '✓' : ' '
                },
                {
                    id: 'nylon',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.applications?.solvent_base_nylon_coated_fabric || p.solvent_base_nylon_coated_fabric) ? '✓' : ' '
                },
                {
                    id: 'waterbased',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.system?.waterborne || p.waterborne) ? '✓' : ' '
                },
                {
                    id: 'uv',
                    class: 'w-[3%] min-w-[35px] text-center f-weight-bold text-blue-950 f-size-sm',
                    getValue: p => (p.system?.uv_coatings_and_inks || p.uv_coatings_and_inks) ? '✓' : ' '
                }
            ]
        }
    },

    fieldDefinitions: {
        'mpi': [
            {
                id: 'product_name',
                title: '產品名稱',
                class: 'w-[22%] min-w-[190px]',
                getValue: p => p.product_name,
                isHtml: true,
                render: (p, index, arrowClass) => {
                    const compRaw = p['composition_' + AppState.lang] || p.composition_zh || p.composition || p.chemistry || '';
                    const comp = compRaw && compRaw !== '—' ? `<div class="f-size-xs text-slate-600 f-weight-normal leading-tight mt-0.5 break-words whitespace-pre-line">${compRaw}</div>` : '';
                    return `
        <div class="flex items-start gap-2 w-full select-none py-0.5">
            <i class="fa-solid fa-chevron-right f-size-xs text-slate-500 shrink-0 transform transition-transform mt-1.5 ${arrowClass}" id="arrow-${index}"></i>
            <div class="min-w-0 flex-1">
                <span class="block f-size-sm break-words f-weight-bold text-blue-950 hover:underline leading-snug" title="${p.product_name}">${p.product_name}</span>
                ${comp}
                ${renderCompareIcon(p, 'MPI', AppState.productLine || 'ptfe')}
            </div>
        </div>`;
                }
            },
            {
                id: 'melt_point',
                title: '熔點 (°C)',
                class: 'w-[9%] min-w-[80px] text-center',
                getValue: p => p.typical_properties?.melt_point_c
            },
            {
                id: 'density',
                title: '密度',
                class: 'w-[7%] min-w-[70px] text-center',
                getValue: p => p.typical_properties?.density_g_cc_25c
            },
            {
                id: 'mean_size',
                title: '平均粒徑(µm)',
                class: 'w-[9%] min-w-[95px] text-center',
                getValue: p => p.typical_properties?.mean_particle_size_um,
                render: p => {
                    const val = p.typical_properties?.mean_particle_size_um;
                    return (val !== null && val !== undefined && val !== '' && val !== '—') ? val : 'N/A';
                }
            },
            {
                id: 'categories',
                title: '附加性能評分',
                class: 'w-[25%] min-w-[160px]',
                getValue: p => {
                    const appData = getAppSpecificData(p);
                    return appData.performance_ratings || appData.featured_categories || p.featured_categories;
                },
                render: p => renderCategorizedBadges(p)
            },
            {
                id: 'tds',
                title: '文件',
                class: 'w-[8%] min-w-[65px] text-center whitespace-nowrap',
                getValue: p => (p.website && p.website !== 'N/A') || (p.tech_data_url && p.tech_data_url !== 'N/A'),
                render: p => {
                    const t = uiText[AppState.lang];
                    return `<div class="flex flex-row justify-center gap-2">
            ${p.website && p.website !== 'N/A' ? `<button data-action="tds" data-product="${p.product_name}" class="text-red-600 hover:text-red-800 f-size-sm f-weight-bold" title="${p.product_name} - ${t.official_doc}" aria-label="${p.product_name} - ${t.official_doc}"><i class="fa-solid fa-file-pdf"></i></button>` : ''}
            ${p.tech_data_url && p.tech_data_url !== 'N/A' ? `<button data-action="data" data-product="${p.product_name}" class="text-blue-700 hover:text-blue-900 f-size-sm f-weight-bold" title="${p.product_name} - ${t.tech_data}" aria-label="${p.product_name} - ${t.tech_data}"><i class="fa-solid fa-file-lines"></i></button>` : ''}
        </div>`;
                }
            }
        ],

        'dorfketal_tyzor': [
            {
                id: 'product_name',
                title: '品項',
                class: 'w-[22%] min-w-[150px] f-weight-bold text-blue-950',
                getValue: p => p.product_name,
                render: p => `
                <div class="flex flex-col items-start gap-1 w-full py-0.5">
                    <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                    ${renderCompareIcon(p, 'DorfKetal', 'tyzor')}
                </div>`
            },
            {
                id: 'comp',
                title: '主要化學成分',
                class: 'w-[25%] min-w-[180px]',
                getValue: p => p.chemical_component || p.composition_zh,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.chemical_component || p.composition_zh || '—'}</span>`
            },
            {
                id: 'properties',
                title: '性質 / 特點描述',
                class: 'w-[40%] min-w-[220px]',
                getValue: p => p.properties,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
            }
        ],

        'dorfketal_px': [
            {
                id: 'product_name',
                title: '產品名稱',
                class: 'w-[16%] min-w-[140px] f-weight-bold text-blue-950',
                getValue: p => p.product_name,
                render: p => `
                <div class="flex flex-col items-start gap-1 w-full py-0.5">
                    <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                    ${renderCompareIcon(p, 'DorfKetal', 'px')}
                </div>`
            },
            {
                id: 'comp',
                title: '主要化學用途',
                class: 'w-[28%] min-w-[170px]',
                getValue: p => p.chemical_component || p.composition_zh,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.chemical_component || p.composition_zh || '—'}</span>`
            },
            {
                id: 'properties',
                title: '性質 / 特點描述',
                class: 'w-[36%] min-w-[210px]',
                getValue: p => p.properties,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
            },
            {
                id: 'suggested_use_level',
                title: '應用與用量',
                class: 'w-[20%] min-w-[130px]',
                getValue: p => p.suggested_use_level_zh,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.suggested_use_level_zh || '—'}</span>`
            }
        ],

        'dorfketal_chain': [
            {
                id: 'product_name',
                title: '產品名稱',
                class: 'w-[14%] min-w-[145px] f-weight-bold text-blue-950 text-center',
                getValue: p => p.product_name,
                render: p => `
                <div class="flex flex-col items-start gap-1 w-full py-0.5">
                    <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                    ${renderCompareIcon(p, 'DorfKetal', 'chain')}
                </div>`
            },
            {
                id: 'comp',
                title: '作用',
                class: 'w-[12%] min-w-[150px] text-center',
                getValue: p => p.chemical_component || p.composition_zh,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.chemical_component || p.composition_zh || '—'}</span>`
            },
            {
                id: 'molecular_weight',
                title: '分子量\n[g/mol]',
                class: 'w-[8%] min-w-[60px] text-center',
                getValue: p => p.typical_properties?.molecular_weight,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800">${p.typical_properties?.molecular_weight || '—'}</span>`
            },
            {
                id: 'density',
                title: '密度\n[g/cm3]',
                class: 'w-[8%] min-w-[60px] text-center',
                getValue: p => p.typical_properties?.density_g_cc_25c,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800">${p.typical_properties?.density_g_cc_25c || '—'}</span>`
            },
            {
                id: 'properties',
                title: '特性',
                class: 'w-[23%] min-w-[170px]',
                getValue: p => p.properties,
                render: p => `<span class="whitespace-pre-line leading-relaxed f-weight-normal text-slate-800 break-words">${p.properties || '—'}</span>`
            },
            {
                id: 'industrial_coating',
                title: '塗料',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.industrial_coating || p.industrial_coatings || p.system?.industrial_coating || p.system?.industrial_coatings || p.applications?.industrial_coating || p.applications?.industrial_coatings) ? '✓' : ' '
            },
            {
                id: 'casting_elastomers',
                title: '灌注型彈性體',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.casting_elastomers || p.casting_elastomer || p.system?.casting_elastomers || p.system?.casting_elastomer || p.applications?.casting_elastomers || p.applications?.casting_elastomer) ? '✓' : ' '
            },
            {
                id: 'cold_casting_elastomers',
                title: '灌注型彈性體(冷)',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.cold_casting_elastomers || p.cold_casting_elastomer || p.system?.cold_casting_elastomers || p.system?.cold_casting_elastomer || p.applications?.cold_casting_elastomers || p.applications?.cold_casting_elastomer) ? '✓' : ' '
            },
            {
                id: 'hot_casting_elastomers',
                title: '灌注型彈性體(熱)',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.hot_casting_elastomers || p.hot_casting_elastomer || p.system?.hot_casting_elastomers || p.system?.hot_casting_elastomer || p.applications?.hot_casting_elastomers || p.applications?.hot_casting_elastomer) ? '✓' : ' '
            },
            {
                id: 'pu_foam_soft_and_rigid_foams',
                title: '軟質及硬質發泡',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.pu_foam_soft_and_rigid_foams || p.pu_foam || p.system?.pu_foam_soft_and_rigid_foams || p.system?.pu_foam || p.applications?.pu_foam_soft_and_rigid_foams || p.applications?.pu_foam) ? '✓' : ' '
            },
            {
                id: 'sealants',
                title: '黏著劑與密封膠',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.sealants || p.sealant || p.system?.sealants || p.system?.sealant || p.applications?.sealants || p.applications?.sealant) ? '✓' : ' '
            },
            {
                id: 'composites',
                title: '複合材料',
                class: 'w-[3.5%] min-w-[35px] text-center f-weight-bold text-blue-950',
                getValue: p => (p.composites || p.composite || p.system?.composites || p.system?.composite || p.applications?.composites || p.applications?.composite) ? '✓' : ' '
            }
        ],

        'orion': [
            {
                id: 'product_name',
                propKey: 'product_name',
                title: '產品名稱',
                class: 'w-[20%] min-w-[150px] f-weight-bold text-blue-950',
                getValue: p => p.product_name,
                render: p => `
                <div class="flex flex-col items-start gap-1 w-full py-0.5">
                    <span class="f-weight-bold text-blue-950 break-words leading-snug min-w-0 w-full text-left">${p.product_name}</span>
                    ${renderCompareIcon(p, 'Orion', AppState.productLine || 'coating')}
                </div>`
            },
            {
                id: 'production_method',
                propKey: 'production_method',
                title: '生產方法',
                class: 'w-[10%] min-w-[75px] f-weight-bold text-blue-950 text-center',
                getValue: p => p.production_method
            },
            {
                id: 'blackness',
                propKey: 'blackness_my',
                title: '黑度 (My)',
                class: 'w-[8%] min-w-[65px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.blackness_my
            },
            {
                id: 'tinting',
                propKey: 'tinting_strength',
                title: '著色力',
                class: 'w-[8%] min-w-[65px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.tinting_strength
            },
            {
                id: 'particle_size',
                propKey: 'average_primary_particle_size_nm',
                title: '原生粒徑 (nm)',
                class: 'w-[10%] min-w-[80px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.average_primary_particle_size_nm
            },
            {
                id: 'bet',
                propKey: 'bet_surface_area',
                title: 'BET (m²/g)',
                class: 'w-[10%] min-w-[80px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.bet_surface_area
            },
            {
                id: 'oil',
                propKey: 'oil_absorption_number',
                title: '吸油量',
                class: 'w-[8%] min-w-[65px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.oil_absorption_number
            },
            {
                id: 'ph',
                propKey: 'ph_value',
                title: 'pH',
                class: 'w-[8%] min-w-[50px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.ph_value
            },
            {
                id: 'volatile',
                propKey: 'volatile_matter_950c',
                title: '揮發分(%)',
                class: 'w-[9%] min-w-[65px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.volatile_matter_950c
            },
            {
                id: 'ash',
                propKey: 'ash_content',
                title: '灰分(%)',
                class: 'w-[9%] min-w-[65px] text-center f-weight-medium text-slate-900',
                getValue: p => p.typical_properties?.ash_content
            }
        ]
    },

    getActiveFields(partnerKey, products) {
        if (partnerKey === 'others') {
            switch (AppState.productLine) {
                case 'matting_agent':
                    return this.layoutDefinitions.matting_agent;
                case 'maleic_acid_resin':
                    return this.layoutDefinitions.maleic_acid_resin;
                case 'silane':
                    return this.layoutDefinitions.silane;
                case 'cpo_adhesion_promoter':
                    return this.layoutDefinitions.cpo_adhesion_promoter;
                case 'adhesion_promoter':
                    return this.layoutDefinitions.adhesion_promoter;
                default:
                    return this.layoutDefinitions.powder_coating_additive;
            }
        }

        let keyToUse = partnerKey;
        if (partnerKey === 'dorfketal') {
            if (AppState.productLine === 'px') keyToUse = 'dorfketal_px';
            else if (AppState.productLine === 'chain' || AppState.productLine === 'dorfketal_chain') keyToUse = 'dorfketal_chain';
            else keyToUse = 'dorfketal_tyzor';
        }

        return this.fieldDefinitions[keyToUse] || this.fieldDefinitions['mpi'];
    },

    getHeaderHTML(activeFields) {
        if (activeFields && activeFields.headerRows) {
            return activeFields.headerRows.map(row => {
                const rowHTML = row.map(col => {
                    const titleWithLineBreak = col.title.replace(/\n/g, '<br>');
                    return `<th class="py-2.5 px-3 border-r border-b border-gray-200 text-center align-middle f-weight-bold text-slate-900 bg-slate-100 ${col.class || ''}">${titleWithLineBreak}</th>`;
                }).join('');

                return `<tr class="select-none f-size-sm f-weight-bold text-slate-900">${rowHTML}</tr>`;
            }).join('');
        }

        const currentPartnerKey = partnerConfigMap[AppState.partner] || 'mpi';

        const colsHTML = activeFields.map(f => {
            let sortIcon = '';
            let clickAttr = '';

            if (currentPartnerKey === 'orion' && f.propKey) {
                clickAttr = `onclick="handleSort('${f.propKey}')" style="cursor: pointer;"`;
                if (AppState.sortColumn === f.propKey) {
                    sortIcon = AppState.sortOrder === 'asc'
                        ? ' <i class="fa-solid fa-arrow-up text-blue-600 f-size-xs"></i>'
                        : ' <i class="fa-solid fa-arrow-down text-blue-600 f-size-xs"></i>';
                } else {
                    sortIcon = ' <i class="fa-solid fa-sort text-slate-400 f-size-xs"></i>';
                }
            }

            return `<th ${clickAttr} class="py-3 px-3.5 f-weight-bold text-slate-900 bg-slate-100 hover:bg-slate-200/70 transition-colors ${f.class || ''}">
    ${f.title}${sortIcon}
</th>`;
        }).join('');

        return `<tr class="bg-slate-100 border-b border-gray-200 text-slate-900 f-weight-bold select-none f-size-sm">${colsHTML}</tr>`;
    },

    getRowHTML(p, index, activeFields, partnerKey) {
        const columns = activeFields.columns || activeFields;
        const isExpanded = AppState.expandedDetails.includes(p.product_name);
        const trHighlight = isExpanded ? 'row-expanded' : '';
        const arrowClass = isExpanded ? 'rotate-90 text-blue-900' : '';

        const cellsHTML = columns.map(f => {
            let displayVal = '—';
            if (f.id === 'product_name' && partnerKey === 'mpi') {
                displayVal = f.render ? f.render(p, index, arrowClass) : p.product_name;
            } else {
                const rawVal = f.getValue ? f.getValue(p) : '—';
                displayVal = hasValidValue(rawVal) ? (f.render ? f.render(p) : rawVal) : '—';
            }
            return `<td class="py-3 px-3.5 border-r border-gray-200 text-slate-800 ${f.class || ''}">${displayVal}</td>`;
        }).join('');

        const primaryRow = `<tr class="hover:bg-blue-50/50 border-b border-gray-200 f-size-sm ${partnerKey === 'mpi' ? 'cursor-pointer' : ''} ${trHighlight}" data-index="${index}" data-product-name="${p.product_name}">${cellsHTML}</tr>`;

        if (partnerKey !== 'mpi') return primaryRow;

        const detailCardHTML = renderAccordionDetailCard(p);

        return `
    ${primaryRow}
    <tr id="detail-${index}" class="${isExpanded ? '' : 'hidden'} bg-slate-100/80 border-b border-gray-200">
        <td colspan="${columns.length}" class="p-4 overflow-hidden">${detailCardHTML}</td>
    </tr>`;
    }
};

function renderCategorizedBadges(p) {
    const appData = getAppSpecificData(p);
    const ratings = appData.performance_ratings || p.performance_ratings;
    if (!ratings) return '—';

    const plusMap = {1: '+', 2: '++', 3: '+++'};
    const primaryBadges = [];
    const secondaryBadges = [];

    Object.entries(featureConfig[AppState.lang]).forEach(([key, label]) => {
        const score = ratings[key] || 0;
        if (score <= 0) return;

        const cat = featureCategories[key] || 'scratch_and_abrasion';
        const displayScore = plusMap[score] || score;
        const isTarget = isCurrentCategoryKey(key, AppState.category, AppState.productLine);

        let colorClass = "";
        if (cat === 'ptfe') colorClass = 'bg-blue-700 text-white';
        else if (cat === 'scratch_and_abrasion') colorClass = 'bg-amber-700 text-white';
        else if (cat === 'texture') colorClass = 'bg-emerald-700 text-white';
        else if (cat === 'special') colorClass = 'bg-purple-700 text-white';

        if (isTarget) {
            primaryBadges.push(`
            <span class="f-size-xs px-2 py-0.5 rounded ${colorClass} font-extrabold shadow ring-2 ring-blue-500/40 inline-flex items-center gap-1 shrink-0">
                <i class="fa-solid fa-star f-size-xs text-amber-300"></i> ${label}
                <span class="tracking-wider text-amber-200">${displayScore}</span>
            </span>
        `);
        } else if (score >= 3) {
            secondaryBadges.push(`
            <span class="f-size-xs px-1.5 py-0.5 rounded ${colorClass} opacity-90 inline-flex items-center gap-0.5 shrink-0">
                ${label} <span class="font-bold">${displayScore}</span>
            </span>
        `);
        }
    });

    if (primaryBadges.length > 0) {
        let html = `<div class="flex flex-wrap gap-1.5 items-center my-0.5 w-full">${primaryBadges.join('')}</div>`;
        if (secondaryBadges.length > 0) {
            html += `<div class="border-b border-slate-300/80 my-1 w-full"></div>`;
            html += `<div class="flex flex-wrap gap-1 items-center my-0.5 w-full">${secondaryBadges.join('')}</div>`;
        }
        return html;
    }

    if (secondaryBadges.length > 0) {
        return `<div class="flex flex-wrap gap-1 items-center my-0.5 w-full">${secondaryBadges.join('')}</div>`;
    }

    return `<span class="text-slate-500 italic f-size-xs">（展開查看全部指標）</span>`;
}

function renderAccordionDetailCard(p) {
    const t = uiText[AppState.lang];
    const appData = getAppSpecificData(p);

    const usage = p['suggested_use_level_' + AppState.lang] || p.suggested_use_level_zh || p.suggested_use_level || '—';
    const systemType = p['recommended_system_type_' + AppState.lang] || p.recommended_system_type_zh || '—';
    const appFields = p['application_fields_' + AppState.lang] || p.application_fields_zh || '—';
    const examples = appData['example_' + AppState.lang] || appData.example_zh || appData.example || p['examples_' + AppState.lang] || p.examples || p.example || '—';
    const maxParticleSize = p.typical_properties?.max_particle_size_um || '—';
    const meanParticleSize = (p.typical_properties?.mean_particle_size_um && p.typical_properties.mean_particle_size_um !== '—')
        ? p.typical_properties.mean_particle_size_um
        : 'N/A';
    const density = p.typical_properties?.density_g_cc_25c || '—';

    const descSource = appData['performance_descriptions_' + AppState.lang] || appData.performance_descriptions_zh || p['performance_descriptions_' + AppState.lang] || p.performance_descriptions_zh || {};
    const descList = Object.entries(descSource)
        .filter(([_, desc]) => desc && desc !== 'N/A')
        .map(([key, desc]) => {
            const label = featureConfig[AppState.lang][key] || key;
            return `<li class="text-slate-900 mb-1 f-size-sm"><strong class="text-slate-950 f-weight-bold">${label}：</strong><span class="whitespace-pre-line f-weight-normal">${desc}</span></li>`;
        }).join('');

    const plusMap = {1: '+', 2: '++', 3: '+++'};

    const categoryHierarchyStyles = {
        "ptfe": {
            1: "bg-blue-100 text-blue-950 border border-blue-300 f-weight-medium",
            2: "bg-blue-600/85 text-white f-weight-semibold shadow-sm",
            3: "bg-blue-700 text-white f-weight-extrabold shadow-md ring-1 ring-blue-900/30"
        },
        "scratch_and_abrasion": {
            1: "bg-amber-100 text-amber-950 border border-amber-300 f-weight-medium",
            2: "bg-amber-600/85 text-white f-weight-semibold shadow-sm",
            3: "bg-amber-700 text-white f-weight-extrabold shadow-md ring-1 ring-amber-900/30"
        },
        "texture": {
            1: "bg-emerald-100 text-emerald-950 border border-emerald-300 f-weight-medium",
            2: "bg-emerald-600/85 text-white f-weight-semibold shadow-sm",
            3: "bg-emerald-700 text-white f-weight-extrabold shadow-md ring-1 ring-emerald-900/30"
        },
        "special": {
            1: "bg-purple-100 text-purple-950 border border-purple-300 f-weight-medium",
            2: "bg-purple-600/85 text-white f-weight-semibold shadow-sm",
            3: "bg-purple-700 text-white f-weight-extrabold shadow-md ring-1 ring-purple-900/30"
        }
    };

    const categoryOrder = ["ptfe", "scratch_and_abrasion", "texture", "special"];
    const groupedBadges = {"ptfe": [], "scratch_and_abrasion": [], "texture": [], "special": []};

    const ratings = appData.performance_ratings || p.performance_ratings;
    if (ratings) {
        Object.entries(featureConfig[AppState.lang]).forEach(([key, label]) => {
            const score = ratings[key] || 0;
            if (score === 0) return;

            const cat = featureCategories[key] || 'scratch_and_abrasion';
            const catStyles = categoryHierarchyStyles[cat] || categoryHierarchyStyles["scratch_and_abrasion"];
            const styleClass = catStyles[score] || catStyles[1];
            const displayScore = plusMap[score] || score;

            const badgeHtml = `<span title="${label}" class="f-size-xs px-2.5 py-0.5 rounded-md ${styleClass} inline-flex items-center gap-1 select-none">${label} <span class="tracking-wider">${displayScore}</span></span>`;
            if (groupedBadges[cat]) {
                groupedBadges[cat].push(badgeHtml);
            }
        });
    }

    const categorisedBadgesHTML = categoryOrder.map(catKey => {
        const badges = groupedBadges[catKey];
        if (!badges || badges.length === 0) return '';
        return `
    <div class="flex flex-wrap items-center gap-1.5 my-1.5 w-full">
        ${badges.join('')}
    </div>`;
    }).filter(Boolean).join('');

    return `
<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 f-size-sm fade-in-down w-full max-w-full">
    <div class="space-y-3">
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm grid grid-cols-2 gap-3 text-slate-900">
            <div><span class="text-slate-800 f-weight-bold f-size-xs block mb-0.5">${t.mean_size}</span><strong class="f-size-base f-weight-bold text-slate-950">${meanParticleSize}</strong></div>
            <div><span class="text-slate-800 f-weight-bold f-size-xs block mb-0.5">${t.max_size}</span><strong class="f-size-base f-weight-bold text-slate-950">${maxParticleSize} µm</strong></div>
        </div>
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm">
            <span class="f-size-xs text-blue-950 f-weight-bold block mb-1 flex items-center gap-1.5"><i class="fa-solid fa-prescription-bottle-droplet"></i> ${t.suggested_use_level_title}</span>
            <p class="text-slate-900 leading-relaxed f-weight-bold f-size-sm whitespace-pre-line">${usage}</p>
        </div>
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm">
            <span class="f-size-xs text-blue-950 f-weight-bold block mb-1 flex items-center gap-1.5"><i class="fa-solid fa-network-wired"></i> ${t.system_type_title}</span>
            <p class="text-slate-900 f-weight-normal f-size-sm leading-relaxed whitespace-pre-line">${systemType}</p>
        </div>
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm">
            <span class="f-size-xs text-blue-950 f-weight-bold block mb-1 flex items-center gap-1.5"><i class="fa-solid fa-bullseye"></i> ${t.app_fields_title}</span>
            <p class="text-slate-900 f-weight-normal f-size-sm leading-relaxed whitespace-pre-line">${appFields}</p>
        </div>
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm">
            <span class="f-size-xs text-amber-950 f-weight-bold block mb-1 flex items-center gap-1.5"><i class="fa-solid fa-tag"></i> ${t.example}</span>
            <p class="text-slate-900 f-weight-normal f-size-sm leading-relaxed whitespace-pre-line">${examples}</p>
        </div>
    </div>

    <div class="space-y-3">
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm">
            <span class="f-size-xs text-blue-950 f-weight-bold block mb-2 flex items-center gap-1.5">
                <i class="fa-solid fa-star"></i> 所有性能指標評分 (All Performance Ratings)
            </span>
            <div class="space-y-1">
                ${categorisedBadgesHTML || `<span class="text-slate-700 f-size-xs">無評分資料</span>`}
            </div>
        </div>
        <div class="bg-white p-3.5 rounded-lg border border-gray-300 shadow-sm space-y-3">
            <div>
                <span class="f-size-xs text-blue-950 f-weight-bold block mb-1.5 flex items-center gap-1.5"><i class="fa-solid fa-wand-magic-sparkles"></i> ${t.perf_descriptions}</span>
                <ul class="list-disc pl-4 space-y-1 leading-relaxed">${descList || `<li class="text-slate-700 f-weight-normal f-size-sm">${t.no_specific_desc}</li>`}</ul>
            </div>
        </div>
    </div>

    <div class="col-span-1 lg:col-span-2 pt-2.5 border-t border-gray-300 flex flex-wrap items-center justify-between gap-2">
        <span class="text-xs text-slate-600 font-medium flex items-center gap-1.5">
            <i class="fa-solid fa-scale-balanced text-blue-700"></i> 可加入比較表橫向對比最多 4 款產品規格
        </span>
        <div class="flex items-center gap-2">
            <button data-product="${p.product_name}" onclick="event.stopPropagation(); toggleCompareProduct('${p.product_name}', 'MPI', '${AppState.productLine}')" class="compare-toggle-btn px-3.5 py-1.5 rounded-lg border text-xs font-bold transition-all flex items-center gap-1.5 ${AppState.compareList.some(item => item.product_name === p.product_name) ? 'bg-blue-900 text-white border-blue-900 shadow-sm' : 'bg-white text-slate-700 border-slate-300 hover:bg-blue-50 hover:border-blue-300'}">
                <i class="fa-solid ${AppState.compareList.some(item => item.product_name === p.product_name) ? 'fa-check' : 'fa-plus'}"></i>
                <span>${AppState.compareList.some(item => item.product_name === p.product_name) ? t.compared : t.compare}</span>
            </button>
        </div>
    </div>
</div>`;
}

function updateRatingLegend() {
    const ratingLegend = document.getElementById('mpi-rating-legend');
    if (!ratingLegend) return;
    const configKey = partnerConfigMap[AppState.partner] || 'mpi';
    const isMpi = (AppState.partner === 'MPI' || configKey === 'mpi');
    const isSearching = !!(AppState.searchQuery && AppState.searchQuery.trim() !== '');

    if (isMpi && !isSearching) {
        ratingLegend.classList.remove('hidden');
        ratingLegend.classList.add('flex');
        ratingLegend.innerText = uiText[AppState.lang].rating_guide_text;
    } else {
        ratingLegend.classList.add('hidden');
        ratingLegend.classList.remove('flex');
    }
}
