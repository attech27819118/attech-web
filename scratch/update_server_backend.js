const fs = require('fs');
const path = require('path');

function updateFile(filePath, isIndexJs) {
    let content = fs.readFileSync(filePath, 'utf8');
    const isCRLF = content.includes('\r\n');
    const eol = isCRLF ? '\r\n' : '\n';

    const declTarget = [
        '            const filmThick = data.filmThick ? `${data.filmThick} µm` : \'未填寫\';',
        '            const noBake = data.noBake || \'否\';',
        '            const bakeTemp = data.bakeTemp || \'未填寫\';',
        '            const bakeTime = data.bakeTime || \'未填寫\';'
    ].join(eol);

    const declReplacement = [
        '            const filmThick = data.filmThick ? `${data.filmThick} µm` : \'未填寫\';',
        '            const isAirDry = (data.cureMethod === \'風乾\' || data.cureMethod === \'常溫風乾\' || data.noBake === \'是\' || data.noBake === true);',
        '            const rawTemp = (data.bakeTemp || \'\').trim();',
        '            const rawTime = (data.bakeTime || \'\').trim();',
        '            const hasTemp = rawTemp && rawTemp !== \'未填寫\' && rawTemp !== \'無 (風乾)\' && rawTemp !== \'無\';',
        '            const hasTime = rawTime && rawTime !== \'未填寫\' && rawTime !== \'無 (風乾)\' && rawTime !== \'無\';',
        '',
        '            let cureCondition = \'\';',
        '            if (isAirDry) {',
        '                cureCondition = \'常溫風乾（不烘烤）\';',
        '            } else if (hasTemp && hasTime) {',
        '                cureCondition = `烘烤（溫度: ${rawTemp} | 時間: ${rawTime}）`;',
        '            } else if (hasTemp) {',
        '                cureCondition = `烘烤（溫度: ${rawTemp} | 時間: 未填寫）`;',
        '            } else if (hasTime) {',
        '                cureCondition = `烘烤（溫度: 未填寫 | 時間: ${rawTime}）`;',
        '            } else if (data.cureMethod === \'烘烤\' || data.noBake === \'否\') {',
        '                cureCondition = \'烘烤（溫度/時間: 未指定）\';',
        '            } else {',
        '                cureCondition = \'未指定\';',
        '            }'
    ].join(eol);

    if (!content.includes(declTarget)) {
        throw new Error(`declTarget not found in ${filePath}`);
    }
    content = content.replace(declTarget, declReplacement);

    const textTarget = '乾燥固化條件：不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}';
    const textReplacement = '乾燥固化條件：${cureCondition}';
    if (!content.includes(textTarget)) {
        throw new Error(`textTarget not found in ${filePath}`);
    }
    content = content.replace(textTarget, textReplacement);

    const htmlTarget = isIndexJs
        ? '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">固化條件：</td><td style="padding: 6px;">不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}</td></tr>'
        : '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">乾燥固化條件：</td><td style="padding: 6px;">不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}</td></tr>';
    const htmlReplacement = '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px; font-weight: bold; color: #475569;">乾燥固化條件：</td><td style="padding: 6px;">${cureCondition}</td></tr>';
    if (!content.includes(htmlTarget)) {
        throw new Error(`htmlTarget not found in ${filePath}`);
    }
    content = content.replace(htmlTarget, htmlReplacement);

    const pdfTarget = '{ label: \'乾燥固化條件\', value: `不烘烤: ${noBake} | 溫度: ${bakeTemp} | 時間: ${bakeTime}` },';
    const pdfReplacement = '{ label: \'乾燥固化條件\', value: cureCondition },';
    if (!content.includes(pdfTarget)) {
        throw new Error(`pdfTarget not found in ${filePath}`);
    }
    content = content.replace(pdfTarget, pdfReplacement);

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ ${filePath} updated successfully!`);
}

updateFile(path.join(__dirname, '..', 'server.js'), false);
updateFile(path.join(__dirname, '..', 'index.js'), true);

