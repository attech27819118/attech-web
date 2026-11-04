function formatCure(data) {
    const isAirDry = (data.cureMethod === '風乾' || data.cureMethod === '常溫風乾' || data.noBake === '是' || data.noBake === true);
    const rawTemp = (data.bakeTemp || '').trim();
    const rawTime = (data.bakeTime || '').trim();
    const hasTemp = rawTemp && rawTemp !== '未填寫' && rawTemp !== '無 (風乾)' && rawTemp !== '無';
    const hasTime = rawTime && rawTime !== '未填寫' && rawTime !== '無 (風乾)' && rawTime !== '無';

    let cureCondition = '';
    if (isAirDry) {
        cureCondition = '常溫風乾（不烘烤）';
    } else if (hasTemp && hasTime) {
        cureCondition = `烘烤（溫度: ${rawTemp} | 時間: ${rawTime}）`;
    } else if (hasTemp) {
        cureCondition = `烘烤（溫度: ${rawTemp} | 時間: 未填寫）`;
    } else if (hasTime) {
        cureCondition = `烘烤（溫度: 未填寫 | 時間: ${rawTime}）`;
    } else if (data.cureMethod === '烘烤' || data.noBake === '否') {
        cureCondition = '烘烤（溫度/時間: 未指定）';
    } else {
        cureCondition = '未指定';
    }
    return cureCondition;
}

const cases = [
    { name: '1. 烘烤，提供溫度與時間', input: { cureMethod: '烘烤', bakeTemp: '120℃', bakeTime: '20 min' }, expected: '烘烤（溫度: 120℃ | 時間: 20 min）' },
    { name: '2. 烘烤，僅提供溫度', input: { cureMethod: '烘烤', bakeTemp: '150℃' }, expected: '烘烤（溫度: 150℃ | 時間: 未填寫）' },
    { name: '3. 烘烤，僅提供時間', input: { cureMethod: '烘烤', bakeTime: '30 min' }, expected: '烘烤（溫度: 未填寫 | 時間: 30 min）' },
    { name: '4. 烘烤，未填溫度與時間', input: { cureMethod: '烘烤' }, expected: '烘烤（溫度/時間: 未指定）' },
    { name: '5. 常溫風乾', input: { cureMethod: '常溫風乾' }, expected: '常溫風乾（不烘烤）' },
    { name: '6. 風乾', input: { cureMethod: '風乾' }, expected: '常溫風乾（不烘烤）' },
    { name: '7. 舊版相容: noBake = 否，含溫度時間', input: { noBake: '否', bakeTemp: '150℃', bakeTime: '30 min' }, expected: '烘烤（溫度: 150℃ | 時間: 30 min）' },
    { name: '8. 舊版相容: noBake = 是', input: { noBake: '是' }, expected: '常溫風乾（不烘烤）' },
    { name: '9. 舊版相容: noBake = 否，未填溫時間', input: { noBake: '否' }, expected: '烘烤（溫度/時間: 未指定）' },
    { name: '10. 全空未填', input: {}, expected: '未指定' }
];

let allPassed = true;
for (const tc of cases) {
    const actual = formatCure(tc.input);
    const pass = actual === tc.expected;
    console.log(`${pass ? '✅' : '❌'} ${tc.name}: => "${actual}"`);
    if (!pass) {
        console.error(`   Expected: "${tc.expected}", got: "${actual}"`);
        allPassed = false;
    }
}

if (!allPassed) {
    process.exit(1);
} else {
    console.log('\n🎉 所有固化條件格式化測試案例全數通過！');
}

