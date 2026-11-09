const { execSync } = require('child_process');
const path = require('path');

// 切換至專案根目錄
process.chdir(path.resolve(__dirname, '..'));

console.log('========================================================');
console.log('       ATTech 宏威應用材料 - 全站一鍵自動建置工具');
console.log('========================================================\n');

const steps = [
    {
        title: '[步驟 1/4] 編譯 Tailwind CSS 樣式 (css/output.css)...',
        cmd: 'cmd.exe /c "npm run build:css"',
        successMsg: '✅ CSS 編譯完成！'
    },
    {
        title: '[步驟 2/4] 更新技術專區 11 大靜態頁面與首頁...',
        cmd: 'python scripts/sync_tech_updates.py',
        successMsg: '✅ 技術專區建置完成！'
    },
    {
        title: '[步驟 3/4] 產生 420+ 產品獨立靜態頁面 (SSG)...',
        cmd: 'node scripts/build-static-pages.js',
        successMsg: '✅ 產品靜態頁面建置完成！'
    },
    {
        title: '[步驟 4/4] 產生全站 Sitemap (sitemap.xml)...',
        cmd: 'node scripts/generate_sitemap.js',
        successMsg: '✅ Sitemap 產生完成！'
    }
];

let hasError = false;

for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    console.log(step.title);
    try {
        execSync(step.cmd, { stdio: 'inherit', env: process.env });
        console.log(step.successMsg + '\n');
    } catch (err) {
        console.error(`\n❌ [錯誤] 在執行步驟 ${i + 1} 時失敗！`);
        hasError = true;
        break;
    }
}

console.log('========================================================');
if (hasError) {
    console.log('⚠️ 建置過程中發生錯誤，請查看上方詳細錯誤訊息。');
    console.log('========================================================\n');
    process.exit(1);
} else {
    console.log('🎉 [成功] 全站所有網頁與檔案已全數更新建置完成！');
    console.log('========================================================\n');
    process.exit(0);
}

