import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_section(csv_path, header_str):
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    res = []
    in_sec = False
    for l in lines:
        if header_str in l:
            in_sec = True
            res.append(l)
            continue
        if in_sec:
            if l.startswith('#') or not l.strip():
                break
            res.append(l)
    return pd.read_csv(io.StringIO(''.join(res)))

print("=== GA4 USER FIRST SOURCE (Table 3) ===")
u_src9 = extract_section(r'c:\Users\user\Downloads\99.csv', '最初招攬到使用者的來源/媒介,活躍使用者')
u_src10 = extract_section(r'c:\Users\user\Downloads\1010.csv', '最初招攬到使用者的來源/媒介,活躍使用者')
u_merged = pd.merge(u_src9, u_src10, on='最初招攬到使用者的來源/媒介', suffixes=('_9月', '_10月'), how='outer').fillna(0)
u_merged['使用者增減'] = u_merged['活躍使用者_10月'] - u_merged['活躍使用者_9月']
print(u_merged.sort_values(by='活躍使用者_10月', ascending=False).to_string())

print("\n=== GA4 SESSION SOURCE / MEDIUM (Table 4) ===")
s_src9 = extract_section(r'c:\Users\user\Downloads\99.csv', '工作階段來源/媒介,工作階段')
s_src10 = extract_section(r'c:\Users\user\Downloads\1010.csv', '工作階段來源/媒介,工作階段')
s_merged = pd.merge(s_src9, s_src10, on='工作階段來源/媒介', suffixes=('_9月', '_10月'), how='outer').fillna(0)
s_merged['工作階段增減'] = s_merged['工作階段_10月'] - s_merged['工作階段_9月']
s_merged['成長率%'] = ((s_merged['工作階段_10月'] - s_merged['工作階段_9月']) / s_merged['工作階段_9月'].replace(0, 1) * 100).round(1)
print(s_merged.sort_values(by='工作階段_10月', ascending=False).to_string())

print("\n=== GA4 TOP CITIES (Table 7) ===")
c9 = extract_section(r'c:\Users\user\Downloads\99.csv', '城市,活躍使用者')
c10 = extract_section(r'c:\Users\user\Downloads\1010.csv', '城市,活躍使用者')
c_merged = pd.merge(c9, c10, on='城市', suffixes=('_9月', '_10月'), how='outer').fillna(0)
c_merged['使用者增減'] = c_merged['活躍使用者_10月'] - c_merged['活躍使用者_9月']
print(c_merged.sort_values(by='活躍使用者_10月', ascending=False).head(25).to_string())

