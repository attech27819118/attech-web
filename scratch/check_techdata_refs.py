import os

def check_refs(root_dir):
    refs = []
    for root, dirs, files in os.walk(root_dir):
        if any(ig in root for ig in ['.git', 'node_modules', '.idea', 'scratch', '__pycache__']):
            continue
        for f in files:
            if f.endswith(('.html', '.js', '.json', '.py', '.md')):
                p = os.path.join(root, f)
                try:
                    with open(p, encoding='utf-8') as fh:
                        c = fh.read()
                        # check for "techdata/" but not "techdatadb/"
                        import re
                        m = re.findall(r'[^a-zA-Z0-9_]techdata/[^\s"\'<>]+', c)
                        if m:
                            refs.append((os.path.relpath(p, root_dir), m[:5]))
                except Exception:
                    pass
    return refs

print("=== References in TEST ===")
for p, m in check_refs(r"D:\Jay\vscode\attech0824 - test"):
    print(p, m)

print("\n=== References in 0824 ===")
for p, m in check_refs(r"D:\Jay\vscode\attech0824"):
    print(p, m)

