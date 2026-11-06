import sys
import io
import pandas as pd
import openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f9 = r'c:\Users\user\Downloads\9.xlsx'
f10 = r'c:\Users\user\Downloads\10.xlsx'
p9 = pd.read_excel(f9, sheet_name='網頁')
p10 = pd.read_excel(f10, sheet_name='網頁')
p_merged = pd.merge(p9, p10, on='熱門網頁', suffixes=('_9月', '_10月'), how='outer').fillna(0)
p_merged['曝光增減'] = p_merged['曝光_10月'] - p_merged['曝光_9月']
p_merged['點擊增減'] = p_merged['點擊_10月'] - p_merged['點擊_9月']

top20 = p_merged.sort_values(by=['點擊_10月', '曝光_10月'], ascending=[False, False]).head(20)
for idx, r in top20.iterrows():
    url = r['熱門網頁']
    c9, c10, cd = int(r['點擊_9月']), int(r['點擊_10月']), int(r['點擊增減'])
    i9, i10, idiff = int(r['曝光_9月']), int(r['曝光_10月']), int(r['曝光增減'])
    pos10 = r.get('排名_10月', 0)
    print(f"{url} | 點擊: {c9}->{c10} ({cd:+d}) | 曝光: {i9}->{i10} ({idiff:+d}) | 10月排名: {pos10:.1f}")

