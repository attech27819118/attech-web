import os, re

refs = []
for root, dirs, files in os.walk('.'):
    if any(ig in root for ig in ['.git', 'node_modules', '.idea', 'scratch', '__pycache__', 'techdata', 'img']):
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.py', '.md')):
            p = os.path.join(root, f)
            with open(p, encoding='utf-8', errors='ignore') as fh:
                c = fh.read()
                m = re.findall(r'[^a-zA-Z0-9_/]techdata/[^\s"\'<>]+', c)
                if m:
                    refs.append((p, m))

print("Total files referencing techdata/ without db:", len(refs))
for p, m in refs:
    print(p, m)

