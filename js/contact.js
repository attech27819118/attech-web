/**
 * ====================================================================
 * ATTech Web - Contact & Sample Request Form Handler (contact.js)
 * ====================================================================
 */

let lastSubmitTime = 0;

function switchFormMode(mode) {
    const quick = document.getElementById('form-mode-quick');
    const detailed = document.getElementById('form-mode-detailed');
    const btnQuick = document.getElementById('mode-btn-quick');
    const btnDetailed = document.getElementById('mode-btn-detailed');

    const quickRequired = ['quick-company', 'quick-contact', 'quick-email', 'quick-contact-tel', 'quick-sample', 'quick-address'];
    const detailRequired = ['detail-company', 'detail-contact', 'detail-email', 'detail-contact-tel', 'detail-address', 'detail-sample-req'];

    // 雙向同步共有欄位內容，確保切換模式時使用者輸入與帶入之索樣產品不遺失
    const quickCompanyEl = document.getElementById('quick-company');
    const detailCompanyEl = document.getElementById('detail-company');
    const quickContactEl = document.getElementById('quick-contact');
    const detailContactEl = document.getElementById('detail-contact');
    const quickEmailEl = document.getElementById('quick-email');
    const detailEmailEl = document.getElementById('detail-email');
    const quickTelEl = document.getElementById('quick-contact-tel');
    const detailTelEl = document.getElementById('detail-contact-tel');
    const quickSampleEl = document.getElementById('quick-sample');
    const detailSampleEl = document.getElementById('detail-sample-req');
    const quickAddressEl = document.getElementById('quick-address');
    const detailAddressEl = document.getElementById('detail-address');
    const quickMsgEl = document.getElementById('quick-msg');
    const detailRemarksEl = document.getElementById('detail-remarks');

    const company = (quickCompanyEl?.value || detailCompanyEl?.value || '').trim();
    const contact = (quickContactEl?.value || detailContactEl?.value || '').trim();
    const email = (quickEmailEl?.value || detailEmailEl?.value || '').trim();
    const tel = (quickTelEl?.value || detailTelEl?.value || '').trim();
    const sample = (quickSampleEl?.value || detailSampleEl?.value || '').trim();
    const address = (quickAddressEl?.value || detailAddressEl?.value || '').trim();
    const msg = (quickMsgEl?.value || detailRemarksEl?.value || '').trim();

    if (quickCompanyEl && !quickCompanyEl.value && company) quickCompanyEl.value = company;
    if (detailCompanyEl && !detailCompanyEl.value && company) detailCompanyEl.value = company;

    if (quickContactEl && !quickContactEl.value && contact) quickContactEl.value = contact;
    if (detailContactEl && !detailContactEl.value && contact) detailContactEl.value = contact;

    if (quickEmailEl && !quickEmailEl.value && email) quickEmailEl.value = email;
    if (detailEmailEl && !detailEmailEl.value && email) detailEmailEl.value = email;

    if (quickTelEl && !quickTelEl.value && tel) quickTelEl.value = tel;
    if (detailTelEl && !detailTelEl.value && tel) detailTelEl.value = tel;

    if (quickSampleEl && !quickSampleEl.value && sample) quickSampleEl.value = sample;
    if (detailSampleEl && !detailSampleEl.value && sample) detailSampleEl.value = sample;

    if (quickAddressEl && !quickAddressEl.value && address) quickAddressEl.value = address;
    if (detailAddressEl && !detailAddressEl.value && address) detailAddressEl.value = address;

    if (quickMsgEl && !quickMsgEl.value && msg) quickMsgEl.value = msg;
    if (detailRemarksEl && !detailRemarksEl.value && msg) detailRemarksEl.value = msg;

    if (mode === 'quick') {
        quick?.classList.remove('hidden');
        detailed?.classList.add('hidden');
        if (btnQuick) {
            btnQuick.className = 'flex items-center justify-center gap-2.5 p-2.5 sm:p-3 rounded-lg border text-left bg-white text-blue-950 border-blue-900 shadow-sm ring-2 ring-blue-900/10 f-weight-bold transition-all cursor-pointer';
            btnQuick.setAttribute('aria-selected', 'true');
        }
        if (btnDetailed) {
            btnDetailed.className = 'flex items-center justify-center gap-2.5 p-2.5 sm:p-3 rounded-lg border border-slate-300/80 bg-slate-100/70 hover:bg-slate-200/70 text-left text-slate-700 hover:text-blue-950 f-weight-medium transition-all cursor-pointer';
            btnDetailed.setAttribute('aria-selected', 'false');
        }

        quickRequired.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.required = true;
        });
        detailRequired.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.required = false;
                el.setCustomValidity?.('');
            }
        });
    } else {
        quick?.classList.add('hidden');
        detailed?.classList.remove('hidden');
        if (btnDetailed) {
            btnDetailed.className = 'flex items-center justify-center gap-2.5 p-2.5 sm:p-3 rounded-lg border text-left bg-white text-blue-950 border-blue-900 shadow-sm ring-2 ring-blue-900/10 f-weight-bold transition-all cursor-pointer';
            btnDetailed.setAttribute('aria-selected', 'true');
        }
        if (btnQuick) {
            btnQuick.className = 'flex items-center justify-center gap-2.5 p-2.5 sm:p-3 rounded-lg border border-slate-300/80 bg-slate-100/70 hover:bg-slate-200/70 text-left text-slate-700 hover:text-blue-950 f-weight-medium transition-all cursor-pointer';
            btnQuick.setAttribute('aria-selected', 'false');
        }

        quickRequired.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.required = false;
                el.setCustomValidity?.('');
            }
        });
        detailRequired.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.required = true;
        });
    }
    if (typeof updateHashRoute === 'function') {
        updateHashRoute(false);
    }
}

function highlightInputError(inputId, msg) {
    showToast(msg, 'error');
    const el = document.getElementById(inputId);
    if (el) {
        el.classList.add('input-error-highlight');
        el.focus();
        setTimeout(() => {
            el.classList.remove('input-error-highlight');
        }, 2500);
    }
}

async function handleContactSubmit(event) {
    event.preventDefault();
    const form = event.target;

    const honeypot = form.querySelector('#website_hp');
    if (honeypot && honeypot.value.trim() !== '') {
        console.warn('Spam detected via honeypot.');
        return;
    }

    const now = Date.now();
    if (now - lastSubmitTime < 4000) {
        showToast('請勿頻繁重複送出，請稍後再試。', 'warning');
        return;
    }

    const mobileRegex = /^(\+?886\-?|0)?9\d{8}$|^(\+?886\-?|0)?9\d{2}[\s\-]?\d{3}[\s\-]?\d{3}$/;
    const phoneRegex = /^(\+?886\-?|0)?\d{1,2}[\s\-]?\d{6,8}(#\d+)?$|^[0-9+\-\s()#]{7,20}$/;

    const isQuick = !document.getElementById('form-mode-quick')?.classList.contains('hidden');
    let payload = {};

    if (isQuick) {
        const company = document.getElementById('quick-company')?.value.trim();
        const contact = document.getElementById('quick-contact')?.value.trim();
        const email = document.getElementById('quick-email')?.value.trim();
        const mobile = document.getElementById('quick-contact-tel')?.value.trim();
        const sample = document.getElementById('quick-sample')?.value.trim();
        const address = document.getElementById('quick-address')?.value.trim();
        const message = document.getElementById('quick-msg')?.value.trim();

        if (!company) {
            highlightInputError('quick-company', '請填寫公司名稱');
            return;
        }
        if (!contact) {
            highlightInputError('quick-contact', '請填寫聯絡人姓名與職稱');
            return;
        }
        if (!email) {
            highlightInputError('quick-email', '請填寫電子信箱');
            return;
        }

        if (!mobile) {
            highlightInputError('quick-contact-tel', '請填寫聯絡電話或手機號碼');
            return;
        }

        if (!mobileRegex.test(mobile.replace(/\s+/g, '')) && !phoneRegex.test(mobile.replace(/\s+/g, ''))) {
            highlightInputError('quick-contact-tel', '請輸入正確的電話或手機號碼格式（例：0912-345-678 或 04-2239-8056）');
            return;
        }

        if (!sample) {
            highlightInputError('quick-sample', '請填寫欲索取的樣品型號與數量');
            return;
        }

        if (!address) {
            highlightInputError('quick-address', '請填寫樣品寄送地址');
            return;
        }

        payload = {
            type: '快速詢價',
            company,
            contact,
            email,
            mobile: mobile || '未提供',
            phone: mobile || '未提供',
            sample: sample || '未提供',
            address: address || '未提供',
            message: message || '無'
        };
    } else {
        const company = document.getElementById('detail-company')?.value.trim();
        const contact = document.getElementById('detail-contact')?.value.trim();
        const email = document.getElementById('detail-email')?.value.trim();
        const mobile = document.getElementById('detail-contact-tel')?.value.trim();
        const fax = document.getElementById('detail-fax')?.value.trim();
        const address = document.getElementById('detail-address')?.value.trim();
        const sampleReq = document.getElementById('detail-sample-req')?.value.trim();

        if (!company) {
            highlightInputError('detail-company', '請填寫公司名稱');
            return;
        }
        if (!contact) {
            highlightInputError('detail-contact', '請填寫聯絡人姓名與職稱');
            return;
        }
        if (!email) {
            highlightInputError('detail-email', '請填寫電子信箱');
            return;
        }

        if (!mobile) {
            highlightInputError('detail-contact-tel', '請填寫聯絡電話或手機號碼');
            return;
        }

        if (!mobileRegex.test(mobile.replace(/\s+/g, '')) && !phoneRegex.test(mobile.replace(/\s+/g, ''))) {
            highlightInputError('detail-contact-tel', '請輸入正確的電話或手機號碼格式（例：0912-345-678 或 04-2239-8056）');
            return;
        }

        if (!address) {
            highlightInputError('detail-address', '請填寫樣品寄送地址');
            return;
        }

        if (!sampleReq) {
            highlightInputError('detail-sample-req', '請填寫欲索取的樣品型號與數量');
            return;
        }

        const getCheckedValues = (name) => {
            return Array.from(form.querySelectorAll(`input[name="${name}"]:checked`)).map(cb => cb.value);
        };

        const appFields = getCheckedValues('app_domain[]');
        const functions = getCheckedValues('app_func[]');
        const otherFunc = document.getElementById('detail-other-func')?.value.trim();
        const systems = getCheckedValues('sys_type[]');
        const compType = form.querySelector('input[name="comp-type"]:checked')?.value || '未指定';
        const appType = form.querySelector('input[name="app-type"]:checked')?.value || '未指定';

        const substrates = getCheckedValues('substrate[]');
        const otherSubstrate = document.getElementById('detail-substrate-other')?.value.trim();
        const filmThick = document.getElementById('detail-film-thick')?.value.trim();
        const noBake = document.getElementById('detail-no-bake')?.checked ? '是' : '否';
        const bakeTemp = document.getElementById('detail-bake-temp')?.value.trim();
        const bakeTime = document.getElementById('detail-bake-time')?.value.trim();
        const resins = getCheckedValues('resin[]');
        const restricted = document.getElementById('detail-restricted')?.value.trim();
        const docs = getCheckedValues('doc_req[]');
        const pastSamples = document.getElementById('detail-past-samples')?.value.trim();
        const remarks = document.getElementById('detail-remarks')?.value.trim();

        payload = {
            type: '詳細需求',
            company,
            contact,
            email,
            mobile: mobile || '未提供',
            phone: mobile || '未提供',
            fax: fax || '未提供',
            address: address || '未提供',
            appFields,
            functions,
            otherFunc: otherFunc || '無',
            systems,
            compType,
            appType,
            substrates,
            otherSubstrate: otherSubstrate || '無',
            filmThick: filmThick || '',
            noBake,
            bakeTemp: bakeTemp || '未填寫',
            bakeTime: bakeTime || '未填寫',
            resins,
            restricted: restricted || '無',
            sampleReq: sampleReq || '未提供',
            docs,
            pastSamples: pastSamples || '無',
            remarks: remarks || '無'
        };
    }

    const submitBtn = document.getElementById('form-submit');
    const originalBtnHTML = submitBtn ? submitBtn.innerHTML : '';
    let stepTimer = null;

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin f-size-sm" aria-hidden="true"></i> 正在傳送需求資料...';
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');

        let elapsed = 0;
        stepTimer = setInterval(() => {
            elapsed += 1;
            if (elapsed === 2) {
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin f-size-sm" aria-hidden="true"></i> 正在生成 PDF 申請單並寄出...';
            }
        }, 1000);
    }

    lastSubmitTime = now;

    // 後端 API 網址設定：本地連 localhost:3000，Vercel 站點連同源 /api，GitHub Pages 連 Vercel 雲端
    const isLocalHost = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
    const isVercelHost = window.location.hostname.endsWith('.vercel.app');
    const VERCEL_API_BASE = 'https://attech-web.vercel.app';
    const apiBase = isLocalHost ? 'http://localhost:3000' : (isVercelHost ? '' : VERCEL_API_BASE);

    // 設置 15 秒逾時中斷控制器
    const abortController = new AbortController();
    const timeoutId = setTimeout(() => abortController.abort(), 15000);

    try {
        const response = await fetch(`${apiBase}/api/send-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload),
            signal: abortController.signal
        });
        clearTimeout(timeoutId);

        const result = await response.json();

        if (response.ok && result.success) {
            showToast(result.message || '需求表單已成功送出！專人將儘速與您聯繫。', 'success');
            form.reset();
        } else {
            showToast(result.message || '伺服器傳送失敗，請稍後再試。', 'error');
        }
    } catch (err) {
        clearTimeout(timeoutId);
        console.error('Submit form error:', err);
        if (err.name === 'AbortError') {
            showToast('連線逾時，請檢查網路連線或稍後再試。', 'error');
        } else {
            showToast(isLocalHost
                ? '無法連線至本地後端伺服器 (port 3000)，請確認本機 server.js 已啟動。'
                : '連線至伺服器失敗，請確認 Vercel 服務或網路連線正常。', 'error');
        }
    } finally {
        if (stepTimer) clearInterval(stepTimer);
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHTML;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        }
    }
}

function requestProductSample(productName, preferredMode = 'quick') {
    if (!productName) return;
    if (typeof closeCompareModal === 'function') closeCompareModal();
    if (typeof toggleTdsModal === 'function') toggleTdsModal(false);
    if (typeof switchTab === 'function') switchTab('contact');
    switchFormMode(preferredMode);

    const sampleText = `${productName}`;
    const quickInput = document.getElementById('quick-sample');
    const detailInput = document.getElementById('detail-sample-req');

    if (quickInput) {
        quickInput.value = sampleText;
        quickInput.classList.add('input-prefilled-highlight');
        setTimeout(() => quickInput.classList.remove('input-prefilled-highlight'), 2500);
    }
    if (detailInput) {
        detailInput.value = sampleText;
        detailInput.classList.add('input-prefilled-highlight');
        setTimeout(() => detailInput.classList.remove('input-prefilled-highlight'), 2500);
    }

    const activeInput = preferredMode === 'detailed' ? detailInput : quickInput;
    if (activeInput) {
        activeInput.focus({preventScroll: true});
    }

    const t = uiText[AppState.lang] || uiText.zh;
    showToast(t.sample_prefill_msg.replace('{name}', productName), 'success');

    // 平滑捲動至表單主卡片位置
    const targetCard = document.getElementById('contact-form-card') || document.getElementById('attech-contact-form') || document.getElementById('tab-contact');
    if (targetCard) {
        const navEl = document.querySelector('nav');
        const navHeight = navEl ? navEl.offsetHeight : 64;
        const targetY = targetCard.getBoundingClientRect().top + window.pageYOffset - (navHeight + 16);
        window.scrollTo({top: Math.max(0, targetY), behavior: 'smooth'});
    }
}
