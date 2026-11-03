with open(r'D:\Jay\vscode\attech0824 - test\index.html', encoding='utf-8') as f:
    text = f.read()

startIdx = text.find('id="tab-technology"')
idx = 0
found = []
while True:
    i = text.find('<!-- Tab: 技術專區', idx)
    if i == -1: break
    found.append(i)
    idx = i + 1

print('Total found:', len(found))
print('Any after startIdx?', any(i > startIdx for i in found))
print('First pos:', found[0], 'startIdx:', startIdx)

