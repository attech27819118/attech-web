import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_t2(filepath):
    lines = open(filepath, encoding='utf-8').readlines()
    t2_start = -1
    for i, line in enumerate(lines):
        if '網頁標題與畫面類別' in line:
            t2_start = i
            break
    rows = []
    for r in csv.reader(lines[t2_start+1:]):
        if not r or not r[0]: break
        rows.append(r)
    return rows

r9 = parse_t2(r'c:\Users\user\Downloads\99.csv')
r10 = parse_t2(r'c:\Users\user\Downloads\1010.csv')

print(f"9月 Table 2 共 {len(r9)} 行")
print(f"10月 Table 2 共 {len(r10)} 行")

# 分類：類別頁 vs 單一產品頁
# 判斷依據：單一產品頁通常在標題中含有具體產品型號，如 FW 200, OK 412, RS 6227 等，或者以 "|" 分隔的特徵
# 讓我們看看標題的結構
print("\n--- 10月前 40 筆標題 ---")
for i, r in enumerate(r10[:40]):
    print(f"{i+1:2d}. [{r[1]} views, {r[2]} users] {r[0]}")

