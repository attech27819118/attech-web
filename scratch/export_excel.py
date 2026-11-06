import os
import io
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

output_dir = r'd:\Jay\vscode\attech0824\analysis report'
excel_path = os.path.join(output_dir, '宏威應用材料_9月與10月數據指標彙整表.xlsx')

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
header_font = Font(name="Microsoft JhengHei", size=11, bold=True, color="FFFFFF")
data_font = Font(name="Microsoft JhengHei", size=10)
bold_font = Font(name="Microsoft JhengHei", size=10, bold=True)
thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

# --- Sheet 1: 核心營運指標 ---
ws1 = wb.create_sheet(title="全站核心營運矩陣")
data1 = [
    ["指標類別", "指標項目", "2026年9月", "2026年10月", "增減差額", "增減幅度 (%)", "營運評估與洞察說明"],
    ["GA4 流量", "活躍使用者 (Active Users)", 136, 294, 158, 116.2, "客群顯著翻倍擴張，市場觸及面大幅拓寬"],
    ["GA4 流量", "新使用者 (New Users)", 136, 279, 143, 105.1, "外部新客源源不絕湧入，拉新成效極佳"],
    ["GA4 互動", "事件總計數 (Event Count)", 2115, 3031, 916, 43.3, "深度滾動、規格下載與點擊互動全面走高"],
    ["GA4 黏著度", "平均參與時間 (秒/人)", 92.3, 80.8, -11.5, -12.5, "大量首訪新客湧入稀釋均值，屬健康常態"],
    ["GSC 搜尋", "總曝光次數 (Impressions)", 2294, 2690, 396, 17.3, "更多產品型號被 Google 索引並展現在搜尋結果"],
    ["GSC 搜尋", "總點擊次數 (Clicks)", 135, 126, -9, -6.7, "總點擊持平微調，但結構轉向高含金量精準長尾詞"],
    ["GSC 搜尋", "平均點閱率 (CTR %)", 5.88, 4.68, -1.20, -20.4, "因長尾詞曝光大幅膨脹（如 Tyzor 詞系），均值微降"],
    ["GSC 搜尋", "平均排名 (Position)", 12.08, 11.71, -0.37, "提升 0.37 名", "全站平均排名穩步向搜尋結果第 1 頁逼近"],
    ["GSC 裝置", "行動端點擊 (Mobile Clicks)", 25, 42, 17, 68.0, "行動裝置點擊狂飆，佔比自 18.5% 飆升至 33.3%"],
    ["GSC 裝置", "桌面端點擊 (Desktop Clicks)", 110, 83, -27, -24.5, "桌面端曝光增長 17.2%，點擊結構部分移轉至行動端"],
    ["GA4 商業", "樣品索取頁跳出率 (%)", 24.1, 11.1, -13.0, -53.9, "每10位訪客有近9位產生實質表單操作，意向極高"]
]

for row_idx, row in enumerate(data1, 1):
    for col_idx, val in enumerate(row, 1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=val)
        cell.border = thin_border
        if row_idx == 1:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.font = data_font
            if isinstance(val, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

# --- Sheet 2: GA4 熱門頁面消長 ---
ws2 = wb.create_sheet(title="GA4熱門產品專頁比較")
f99 = r'c:\Users\user\Downloads\99.csv'
f1010 = r'c:\Users\user\Downloads\1010.csv'

def load_ga_t2(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    res = []
    in_t2 = False
    for l in lines:
        if '網頁標題與畫面類別,瀏覽,活躍使用者,事件計數,跳出率' in l:
            in_t2 = True
            res.append(l)
            continue
        if in_t2:
            if l.startswith('#') or not l.strip():
                break
            res.append(l)
    return pd.read_csv(io.StringIO(''.join(res)))

ga9 = load_ga_t2(f99)
ga10 = load_ga_t2(f1010)
ga_merge = pd.merge(ga9, ga10, on='網頁標題與畫面類別', suffixes=('_9月', '_10月'), how='outer').fillna(0)
ga_merge['瀏覽增減'] = ga_merge['瀏覽_10月'] - ga_merge['瀏覽_9月']
ga_merge['瀏覽成長率%'] = ((ga_merge['瀏覽_10月'] - ga_merge['瀏覽_9月']) / ga_merge['瀏覽_9月'].replace(0, 1) * 100).round(1)
ga_merge['活躍使用者增減'] = ga_merge['活躍使用者_10月'] - ga_merge['活躍使用者_9月']

top_pages = ga_merge.sort_values(by=['瀏覽_10月', '瀏覽增減'], ascending=[False, False]).head(50)
headers2 = ["網頁標題與畫面類別", "9月瀏覽", "10月瀏覽", "瀏覽增減", "瀏覽成長率 (%)", "9月活躍訪客", "10月活躍訪客", "訪客增減", "10月跳出率 (%)"]
ws2.append(headers2)
for cell in ws2[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

for _, r in top_pages.iterrows():
    row_val = [
        r['網頁標題與畫面類別'],
        int(r['瀏覽_9月']),
        int(r['瀏覽_10月']),
        int(r['瀏覽增減']),
        f"{r['瀏覽成長率%']:.1f}%",
        int(r['活躍使用者_9月']),
        int(r['活躍使用者_10月']),
        int(r['活躍使用者增減']),
        f"{r['跳出率_10月']*100:.1f}%"
    ]
    ws2.append(row_val)
    row_cells = ws2[ws2.max_row]
    for idx, c in enumerate(row_cells):
        c.font = data_font
        c.border = thin_border
        if idx > 0:
            c.alignment = Alignment(horizontal="right", vertical="center")

# --- Sheet 3: GSC 關鍵字消長 ---
ws3 = wb.create_sheet(title="GSC搜尋關鍵字比較")
f9_xlsx = r'c:\Users\user\Downloads\9.xlsx'
f10_xlsx = r'c:\Users\user\Downloads\10.xlsx'
q9 = pd.read_excel(f9_xlsx, sheet_name='查詢')
q10 = pd.read_excel(f10_xlsx, sheet_name='查詢')

q_merge = pd.merge(q9, q10, on='熱門查詢項目', suffixes=('_9月', '_10月'), how='outer').fillna(0)
q_merge['點擊增減'] = q_merge['點擊_10月'] - q_merge['點擊_9月']
q_merge['曝光增減'] = q_merge['曝光_10月'] - q_merge['曝光_9月']
q_merge_sorted = q_merge.sort_values(by=['點擊_10月', '曝光_10月'], ascending=[False, False]).head(60)

headers3 = ["熱門查詢項目", "9月點擊", "10月點擊", "點擊增減", "9月曝光", "10月曝光", "曝光增減", "10月點閱率 (%)", "10月平均排名", "屬性備註"]
ws3.append(headers3)
for cell in ws3[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

for _, r in q_merge_sorted.iterrows():
    kw = r['熱門查詢項目']
    is_new = int(r['曝光_9月']) == 0
    note = "10月新入榜" if is_new else ("品牌核心詞" if '宏威' in kw or 'attech' in kw.lower() else "產品型號詞")
    row_val = [
        kw,
        int(r['點擊_9月']),
        int(r['點擊_10月']),
        int(r['點擊增減']),
        int(r['曝光_9月']),
        int(r['曝光_10月']),
        int(r['曝光增減']),
        f"{r['點閱率_10月']*100:.2f}%",
        f"{r['排名_10月']:.2f}",
        note
    ]
    ws3.append(row_val)
    for idx, c in enumerate(ws3[ws3.max_row]):
        c.font = data_font
        c.border = thin_border
        if 1 <= idx <= 8:
            c.alignment = Alignment(horizontal="right", vertical="center")

# --- Sheet 4: 渠道與地理分佈 ---
ws4 = wb.create_sheet(title="流量渠道與地理分佈")
def load_ga_sec(fn, header_str):
    with open(fn, 'r', encoding='utf-8') as f:
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

s9 = load_ga_sec(f99, '工作階段來源/媒介,工作階段')
s10 = load_ga_sec(f1010, '工作階段來源/媒介,工作階段')
s_merge = pd.merge(s9, s10, on='工作階段來源/媒介', suffixes=('_9月', '_10月'), how='outer').fillna(0)
s_merge['增減'] = s_merge['工作階段_10月'] - s_merge['工作階段_9月']
s_merge['成長率%'] = ((s_merge['工作階段_10月'] - s_merge['工作階段_9月']) / s_merge['工作階段_9月'].replace(0, 1) * 100).round(1)

ws4.append(["【A. 工作階段來源/媒介 (Session Source / Medium)】", "", "", "", ""])
ws4.append(["來源 / 媒介", "9月工作階段", "10月工作階段", "絕對增減", "成長率 (%)"])
for c in ws4[2]:
    c.fill = header_fill
    c.font = header_font
    c.border = thin_border
    c.alignment = Alignment(horizontal="center", vertical="center")

for _, r in s_merge.sort_values(by='工作階段_10月', ascending=False).iterrows():
    ws4.append([r['工作階段來源/媒介'], int(r['工作階段_9月']), int(r['工作階段_10月']), int(r['增減']), f"{r['成長率%']:.1f}%"])
    for idx, c in enumerate(ws4[ws4.max_row]):
        c.font = data_font
        c.border = thin_border
        if idx > 0:
            c.alignment = Alignment(horizontal="right", vertical="center")

ws4.append([])
ws4.append(["【B. 前 20 大造訪城市分佈 (Top Cities)】", "", "", "", ""])
ws4.append(["城市名稱", "9月活躍訪客", "10月活躍訪客", "訪客增減", "區域特徵分析"])
for c in ws4[ws4.max_row]:
    c.fill = header_fill
    c.font = header_font
    c.border = thin_border
    c.alignment = Alignment(horizontal="center", vertical="center")

c9 = load_ga_sec(f99, '城市,活躍使用者')
c10 = load_ga_sec(f1010, '城市,活躍使用者')
c_merge = pd.merge(c9, c10, on='城市', suffixes=('_9月', '_10月'), how='outer').fillna(0)
c_merge['增減'] = c_merge['活躍使用者_10月'] - c_merge['活躍使用者_9月']

geo_desc = {
    'Guangzhou': '中國華南塗料/油墨及電子化學品大省重鎮',
    'Shenzhen': '中國高科技電子材料、特種塗層與研發中心',
    'Singapore': '東南亞跨國化工集團區域採購與技服樞紐',
    'Beitun District': '宏威在地核心客群 (台中北屯)',
    'Zhongshan District': '台北市商業與研發企業總部',
    'East District': '台南工業與特化研發聚落',
    'Banqiao District': '新北板橋高科技與商業聚落',
    'Lingya District': '高雄特化與重工業聚落',
    'Ashburn': '美國高科技數據中心與跨國雲端IP',
    'Da’an District': '台北大安區生技與特化貿易商',
    'Zhongli District': '桃園中壢工業區 (PCB與塗裝重鎮)'
}

for _, r in c_merge.sort_values(by='活躍使用者_10月', ascending=False).head(20).iterrows():
    city = r['城市']
    desc = geo_desc.get(city, '國內外重要特用化學品造訪區域')
    ws4.append([city, int(r['活躍使用者_9月']), int(r['活躍使用者_10月']), int(r['增減']), desc])
    for idx, c in enumerate(ws4[ws4.max_row]):
        c.font = data_font
        c.border = thin_border
        if 1 <= idx <= 3:
            c.alignment = Alignment(horizontal="right", vertical="center")

# Auto-adjust column widths
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            # approximate width for cjk characters
            width = sum(2 if ord(char) > 256 else 1 for char in val_str)
            if width > max_len:
                max_len = width
        sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

wb.save(excel_path)
print(f"✅ Excel 已成功產出至: {excel_path}")

