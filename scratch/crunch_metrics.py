import sys
import io
import pandas as pd
import openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. GSC Analysis
f9_path = r'c:\Users\user\Downloads\9.xlsx'
f10_path = r'c:\Users\user\Downloads\10.xlsx'

gsc_q9 = pd.read_excel(f9_path, sheet_name='查詢')
gsc_q10 = pd.read_excel(f10_path, sheet_name='查詢')

gsc_p9 = pd.read_excel(f9_path, sheet_name='網頁')
gsc_p10 = pd.read_excel(f10_path, sheet_name='網頁')

gsc_d9 = pd.read_excel(f9_path, sheet_name='圖表')
gsc_d10 = pd.read_excel(f10_path, sheet_name='圖表')

gsc_c9 = pd.read_excel(f9_path, sheet_name='國家_地區')
gsc_c10 = pd.read_excel(f10_path, sheet_name='國家_地區')

gsc_dev9 = pd.read_excel(f9_path, sheet_name='裝置')
gsc_dev10 = pd.read_excel(f10_path, sheet_name='裝置')

print("=== GSC OVERVIEW TOTALS ===")
print(f"Sep GSC Clicks: {gsc_d9['點擊'].sum()}, Impressions: {gsc_d9['曝光'].sum()}, Avg CTR: {gsc_d9['點擊'].sum()/gsc_d9['曝光'].sum():.4f}, Mean Pos: {gsc_d9['排名'].mean():.2f}")
print(f"Oct GSC Clicks: {gsc_d10['點擊'].sum()}, Impressions: {gsc_d10['曝光'].sum()}, Avg CTR: {gsc_d10['點擊'].sum()/gsc_d10['曝光'].sum():.4f}, Mean Pos: {gsc_d10['排名'].mean():.2f}")

print("\n=== GSC TOP QUERIES SEP (Clicks > 0) ===")
print(gsc_q9[gsc_q9['點擊'] > 0].to_string())

print("\n=== GSC TOP QUERIES OCT (Clicks > 0) ===")
print(gsc_q10[gsc_q10['點擊'] > 0].to_string())

# Emerging queries in Oct
q9_set = set(gsc_q9['熱門查詢項目'].dropna().str.lower().str.strip())
q10_new = gsc_q10[~gsc_q10['熱門查詢項目'].dropna().str.lower().str.strip().isin(q9_set)]
print(f"\n=== NEW QUERIES IN OCT (Total new: {len(q10_new)}) ===")
print(q10_new.sort_values(by=['點擊', '曝光'], ascending=[False, False]).head(25).to_string())

# High impression queries in Oct
print("\n=== TOP 20 IMPRESSION QUERIES IN OCT ===")
print(gsc_q10.sort_values(by='曝光', ascending=False).head(20).to_string())

# 2. GA4 CSV Analysis
def load_ga_table2(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # find table 2
    t2_lines = []
    in_t2 = False
    for l in lines:
        if '網頁標題與畫面類別,瀏覽,活躍使用者,事件計數,跳出率' in l:
            in_t2 = True
            t2_lines.append(l)
            continue
        if in_t2:
            if l.startswith('#') or not l.strip():
                break
            t2_lines.append(l)
    return pd.read_csv(io.StringIO(''.join(t2_lines)))

ga_p9 = load_ga_table2(r'c:\Users\user\Downloads\99.csv')
ga_p10 = load_ga_table2(r'c:\Users\user\Downloads\1010.csv')

print("\n=== GA4 TOP PAGES SEP ===")
print(ga_p9.head(15).to_string())

print("\n=== GA4 TOP PAGES OCT ===")
print(ga_p10.head(15).to_string())

# Merged GA4 comparison
ga_merged = pd.merge(ga_p9, ga_p10, on='網頁標題與畫面類別', suffixes=('_9月', '_10月'), how='outer').fillna(0)
ga_merged['瀏覽增減'] = ga_merged['瀏覽_10月'] - ga_merged['瀏覽_9月']
ga_merged['瀏覽成長率%'] = ((ga_merged['瀏覽_10月'] - ga_merged['瀏覽_9月']) / ga_merged['瀏覽_9月'].replace(0, 1) * 100).round(1)
print("\n=== GA4 TOP GROWING PAGES ===")
print(ga_merged.sort_values(by='瀏覽增減', ascending=False)[['網頁標題與畫面類別', '瀏覽_9月', '瀏覽_10月', '瀏覽增減', '活躍使用者_10月', '跳出率_10月']].head(15).to_string())

# Conversion page analysis
contact_page = ga_merged[ga_merged['網頁標題與畫面類別'].str.contains('樣品索取', na=False)]
print("\n=== GA4 SAMPLE REQUEST CONVERSION PAGE ===")
print(contact_page.to_string())

