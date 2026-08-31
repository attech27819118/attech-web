/**
 * ====================================================================
 * ATTech Web - Product Repository & Data Management (data-repo.js)
 * ====================================================================
 */

function renderTableSkeleton(rowCount = 5, colCount = 5) {
    const tbody = document.getElementById('directory-matrix-body');
    if (!tbody) return;

    const skeletonRows = Array.from({length: rowCount}).map(() => `
        <tr class="animate-pulse border-b border-gray-200">
            ${Array.from({length: colCount}).map(() => `
                <td class="py-3 px-3.5">
                    <div class="h-4 bg-slate-200 rounded w-3/4 mb-1"></div>
                    <div class="h-3 bg-slate-100 rounded w-1/2"></div>
                </td>
            `).join('')}
        </tr>
    `).join('');

    tbody.innerHTML = skeletonRows;
}

class ProductRepository {
    static async loadBrandData(partnerKey) {
        const configKey = partnerConfigMap[partnerKey] || 'mpi';
        const brandConfig = AppState.configs[configKey];
        if (!brandConfig) return [];

        if (configKey === 'mpi') {
            if (AppState.allProductsCache['mpi_master']) {
                return AppState.allProductsCache['mpi_master'];
            }
            renderTableSkeleton(6, 6);
            try {
                const targetUrl = resolveAssetUrl(brandConfig.masterPath || './json/mpi/mpiall.json');
                const res = await fetch(targetUrl);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data = await res.json();
                AppState.allProductsCache['mpi_master'] = data;
                (brandConfig.files || []).forEach(file => {
                    AppState.allProductsCache[file.key] = data.filter(p => p.applications_data && p.applications_data[file.key]);
                });
                return data;
            } catch (err) {
                console.error("載入 MPI 主資料庫失敗:", err);
                return [];
            }
        }

        const isAllCached = (brandConfig.files || []).every(f => !!AppState.allProductsCache[f.key]);
        if (!isAllCached) {
            renderTableSkeleton(6, 6);
        }

        const loadPromises = (brandConfig.files || []).map(file => {
            if (AppState.allProductsCache[file.key]) {
                return Promise.resolve({key: file.key, data: AppState.allProductsCache[file.key]});
            }
            const targetUrl = resolveAssetUrl(file.jsonPath);
            return fetch(targetUrl)
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    AppState.allProductsCache[file.key] = Array.isArray(data) ? data : [];
                    return {key: file.key, data: AppState.allProductsCache[file.key]};
                })
                .catch(err => {
                    console.error(`載入產品線 ${file.key} (${targetUrl}) 失敗:`, err);
                    AppState.allProductsCache[file.key] = [];
                    return {key: file.key, data: []};
                });
        });
        return Promise.all(loadPromises);
    }
}

async function loadAllBrandsData() {
    if (AppState.allLoaded) return;
    const partners = ['MPI', 'DorfKetal', 'Orion', 'Others'];
    await Promise.all(partners.map(p => ProductRepository.loadBrandData(p)));
    AppState.allLoaded = true;
}

// 預先喚醒 Render 後端伺服器 (避免使用者填寫完畢送出時遭遇 30~50 秒冷啟動延遲)
let isPrewarming = false;
function prewarmBackendServer() {
    if (isPrewarming) return;
    const isLocalHost = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
    if (isLocalHost) return;

    isPrewarming = true;
    fetch('https://attech-web.onrender.com/api/health', { method: 'GET', mode: 'cors' })
        .then(res => res.json())
        .then(data => {
            console.log('✅ 後端伺服器已就緒 (Pre-warmed):', data.status);
        })
        .catch(err => {
            console.log('ℹ️ 後端喚醒訊號已送出:', err.message);
        });
}
