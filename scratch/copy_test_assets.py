import os, shutil

src_root = r"D:\Jay\vscode\attech0824 - test"
dst_root = r"D:\Jay\vscode\attech0824"

# 1. Copy techdatadb
print("Copying techdatadb...")
dst_techdata = os.path.join(dst_root, "techdatadb")
if os.path.exists(dst_techdata):
    shutil.rmtree(dst_techdata)
shutil.copytree(os.path.join(src_root, "techdatadb"), dst_techdata)
print("techdatadb copied successfully.")

# 2. Copy js/vendor
print("Copying js/vendor...")
dst_vendor = os.path.join(dst_root, "js", "vendor")
if os.path.exists(dst_vendor):
    shutil.rmtree(dst_vendor)
shutil.copytree(os.path.join(src_root, "js", "vendor"), dst_vendor)
print("js/vendor copied successfully.")

# 3. Copy js/technology.js
print("Copying js/technology.js...")
shutil.copy2(os.path.join(src_root, "js", "technology.js"), os.path.join(dst_root, "js", "technology.js"))

# 4. Copy json/tech_database.json
print("Copying json/tech_database.json...")
shutil.copy2(os.path.join(src_root, "json", "tech_database.json"), os.path.join(dst_root, "json", "tech_database.json"))

# 5. Copy technology/ directory
print("Copying technology/ directory...")
dst_tech = os.path.join(dst_root, "technology")
if os.path.exists(dst_tech):
    shutil.rmtree(dst_tech)
shutil.copytree(os.path.join(src_root, "technology"), dst_tech)
print("technology/ copied successfully.")

# 6. Copy new scripts
print("Copying new scripts...")
scripts_to_copy = [
    "README.md",
    "apply_cover_clean_fix.py",
    "apply_cover_fix.py",
    "apply_true_fullscreen.py",
    "build_tech_json.py",
    "build_technology_subpages.js",
    "build_technology_subpages.py",
    "fix_missing_data_bug.py",
    "fix_modal_zindex.py",
    "fix_tech_bugs.py",
    "sync_tech_updates.py",
    "update_cache_version.py",
    "update_cover_flow.py",
    "update_tech_all.py"
]
for s in scripts_to_copy:
    src_s = os.path.join(src_root, "scripts", s)
    dst_s = os.path.join(dst_root, "scripts", s)
    if os.path.exists(src_s):
        shutil.copy2(src_s, dst_s)
        print(f"Copied script: {s}")

# 7. Copy root files
root_files = [
    "start.bat",
    "start_server_9118.bat",
    "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx"
]
for rf in root_files:
    src_rf = os.path.join(src_root, rf)
    dst_rf = os.path.join(dst_root, rf)
    if os.path.exists(src_rf):
        shutil.copy2(src_rf, dst_rf)
        print(f"Copied root file: {rf}")

print("All copies completed!")

