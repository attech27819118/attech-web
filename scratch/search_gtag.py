import glob, re

found = {}
for p in glob.glob('**/*.js', recursive=True) + glob.glob('**/*.html', recursive=True):
    if 'node_modules' in p or 'scratch' in p: continue
    try:
        content = open(p, encoding='utf-8').read()
        matches = re.findall(r"gtag\s*\(\s*['\"]event['\"]\s*,\s*['\"]([^'\"]+)['\"]", content)
        if matches:
            found[p] = list(set(matches))
    except Exception:
        pass

for k, v in found.items():
    print(k, '==>', v)

