import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default sheet

    font_family = "微软雅黑"
    
    # Fonts
    title_font = Font(name=font_family, size=14, bold=True, color="FFFFFF")
    title_fill = PatternFill(start_color="1B4332", end_color="1B4332", fill_type="solid") # Deep Forest Green
    
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2D6A4F", end_color="2D6A4F", fill_type="solid") # Brand Green
    
    subheader_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    subheader_fill = PatternFill(start_color="40916C", end_color="40916C", fill_type="solid") # Medium Green
    
    cat_font = Font(name=font_family, size=11, bold=True, color="1B4332")
    cat_fill = PatternFill(start_color="D8F3DC", end_color="D8F3DC", fill_type="solid") # Light mint
    
    data_font = Font(name=font_family, size=9.5)
    bold_data_font = Font(name=font_family, size=9.5, bold=True)
    check_font = Font(name=font_family, size=11, bold=True, color="1B4332")
    
    zebra_fill = PatternFill(start_color="F4F9F5", end_color="F4F9F5", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    thin_border_color = "D0D7D3"
    thin_side = Side(style='thin', color=thin_border_color)
    data_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    
    header_side = Side(style='thin', color="52796F")
    header_border = Border(left=header_side, right=header_side, top=header_side, bottom=header_side)

    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)

    # =============================================================
    # 0. 目录总览 (Catalog / Index)
    # =============================================================
    ws0 = wb.create_sheet(title="产品目录总览")
    ws0.views.sheetView[0].showGridLines = True

    ws0.merge_cells("A1:F1")
    ws0["A1"] = "KULPES® 树脂产品目录 - 汇总导航"
    ws0["A1"].font = title_font
    ws0["A1"].fill = title_fill
    ws0["A1"].alignment = center_align
    ws0.row_dimensions[1].height = 36

    index_headers = ["序号", "产品系列 / 类别", "工作表名称", "型号数量", "主要应用领域", "对应原文件"]
    for col_idx, text in enumerate(index_headers, start=1):
        cell = ws0.cell(row=3, column=col_idx, value=text)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = header_border
        cell.alignment = center_align
    ws0.row_dimensions[3].height = 26

    index_data = [
        [1, "全产品综合汇总表", "全产品总表", 70, "整合全部6大系列产品，支持多维度筛选与对比", "汇总整合"],
        [2, "KULPES® 聚酯多元醇", "聚酯多元醇", 22, "聚氨酯热熔胶、UV树脂、聚氨酯弹性体、软包装", "第 2 页"],
        [3, "KULPES® 改性多元醇", "改性多元醇", 6, "聚氨酯热熔胶、软包装", "第 2 页"],
        [4, "KULPES® 固体丙烯酸树脂", "固体丙烯酸树脂", 15, "热熔胶、胶粘剂、防腐涂料、UV涂料、热转印、印刷油墨、标线漆", "第 3 页"],
        [5, "KULPES® 高分子量聚酯树脂", "高分子量聚酯树脂", 9, "印刷油墨、粘合剂、罐听涂料、热密封涂料", "第 3 页"],
        [6, "KULPES® 溶剂型聚酯树脂", "溶剂型聚酯树脂", 12, "建筑卷材、家电卷材、罐听外涂/内涂、印刷油墨", "第 4 页"],
        [7, "KULPES® 附着力促进剂", "附着力促进剂", 6, "工业涂料、卷材涂料、木器涂料、罐听涂料、交通涂料、塑胶涂料等", "第 4 页"],
        [8, "特性指标测试方法与企业信息", "测试方法与企业信息", "-", "GB/T测试标准规范、企业联络信息", "第 4 页"],
    ]

    for row_idx, row_vals in enumerate(index_data, start=4):
        ws0.row_dimensions[row_idx].height = 24
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws0.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx in [1, 4, 6]:
                cell.font = data_font
                cell.alignment = center_align
            elif col_idx in [2, 3]:
                cell.font = bold_data_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = left_align

    # Total row
    tot_row = len(index_data) + 4
    ws0.cell(row=tot_row, column=1, value="合计").alignment = center_align
    ws0.cell(row=tot_row, column=1).font = bold_data_font
    ws0.cell(row=tot_row, column=1).fill = cat_fill
    ws0.cell(row=tot_row, column=1).border = data_border
    
    ws0.merge_cells(f"B{tot_row}:C{tot_row}")
    ws0.cell(row=tot_row, column=2, value="共计 6 大产品系列").alignment = center_align
    ws0.cell(row=tot_row, column=2).font = bold_data_font
    ws0.cell(row=tot_row, column=2).fill = cat_fill
    ws0.cell(row=tot_row, column=2).border = data_border
    ws0.cell(row=tot_row, column=3).border = data_border
    ws0.cell(row=tot_row, column=3).fill = cat_fill

    ws0.cell(row=tot_row, column=4, value="70 款型号").alignment = center_align
    ws0.cell(row=tot_row, column=4).font = bold_data_font
    ws0.cell(row=tot_row, column=4).fill = cat_fill
    ws0.cell(row=tot_row, column=4).border = data_border

    ws0.merge_cells(f"E{tot_row}:F{tot_row}")
    ws0.cell(row=tot_row, column=5, value="完整收录原 PDF 全部物性指标、应用矩阵与测试标准").alignment = left_align
    ws0.cell(row=tot_row, column=5).font = bold_data_font
    ws0.cell(row=tot_row, column=5).fill = cat_fill
    ws0.cell(row=tot_row, column=5).border = data_border
    ws0.cell(row=tot_row, column=6).border = data_border
    ws0.cell(row=tot_row, column=6).fill = cat_fill
    ws0.row_dimensions[tot_row].height = 24

    # =============================================================
    # 1. 全产品综合汇总表 (Master Unified Table)
    # =============================================================
    ws_all = wb.create_sheet(title="全产品总表")
    ws_all.views.sheetView[0].showGridLines = True

    ws_all.merge_cells("A1:O1")
    ws_all["A1"] = "KULPES® 全产品综合参数汇总表"
    ws_all["A1"].font = title_font
    ws_all["A1"].fill = title_fill
    ws_all["A1"].alignment = center_align
    ws_all.row_dimensions[1].height = 36

    master_headers = [
        "序号", "产品大类", "产品型号", "形态 / 基础单体", "供货固含 (%)",
        "溶剂", "玻璃化温度 Tg (°C)", "分子量 (g/mol)", "羟值 (mgKOH/g)", "酸值 (mgKOH/g)",
        "熔点 (°C)", "软化点 (°C)", "粘度 (MPa.s)", "PH值", "主要应用领域"
    ]
    for col_idx, text in enumerate(master_headers, start=1):
        cell = ws_all.cell(row=2, column=col_idx, value=text)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = header_border
        cell.alignment = center_align
    ws_all.row_dimensions[2].height = 28

    master_data = [
        # 聚酯多元醇
        [1, "聚酯多元醇", "RS 6059", "无定形态", 100, "-", 10, 1800, "50-60", "≤2", "", 55, "", "", "聚氨酯热熔胶"],
        [2, "聚酯多元醇", "RS 6067", "无定形态", 100, "-", 30, 3000, "30-40", "≤2", "", 78, "", "", "聚氨酯热熔胶"],
        [3, "聚酯多元醇", "RS 6069", "无定形态", 100, "-", 30, 3000, "30-40", "≤2", "", 77, "", "", "聚氨酯热熔胶"],
        [4, "聚酯多元醇", "RS 6073", "无定形态", 100, "-", 30, 5500, "18-24", "≤2", "", 87, "", "", "聚氨酯热熔胶、软包装"],
        [5, "聚酯多元醇", "RS 6078", "无定形态", 100, "-", 50, 2600, "37-45", "≤2", "", 96, "", "", "聚氨酯热熔胶"],
        [6, "聚酯多元醇", "RS 6131", "液态", 100, "-", -60, 3500, "25-35", "≤2", 30, 39, "", "", "聚氨酯热熔胶、UV树脂、聚氨酯弹性体、软包装"],
        [7, "聚酯多元醇", "RS 6128", "液态", 100, "-", -50, 5500, "18-25", "≤2", "", "", "", "", "聚氨酯热熔胶、UV树脂、聚氨酯弹性体、软包装"],
        [8, "聚酯多元醇", "RS 6119", "液态", 100, "-", -30, 3500, "25-35", "≤2", "", "", "", "", "聚氨酯热熔胶、聚氨酯弹性体、软包装"],
        [9, "聚酯多元醇", "RS 6071", "液态", 100, "-", -25, 1000, "100-120", "≤2", "", "", "", "", "聚氨酯热熔胶、UV树脂、聚氨酯弹性体、软包装"],
        [10, "聚酯多元醇", "RS 6108", "液态", 100, "-", -15, 3500, "25-35", "≤2", "", "", "", "", "聚氨酯热熔胶、聚氨酯弹性体"],
        [11, "聚酯多元醇", "RS 6183", "结晶态", 100, "-", -60, 3500, "25-35", "≤2", 56, 62, "", "", "聚氨酯热熔胶、软包装"],
        [12, "聚酯多元醇", "RS 6184", "结晶态", 100, "-", -60, 8500, "12-18", "≤2", 57, 64, "", "", "聚氨酯热熔胶"],
        [13, "聚酯多元醇", "RS 6173", "结晶态", 100, "-", -40, 3500, "25-35", "≤2", 95, "", "", "", "聚氨酯热熔胶"],
        [14, "聚酯多元醇", "RS 6193", "结晶态", 100, "-", "", 3500, "25-35", "≤2", 70, 77, "", "", "聚氨酯热熔胶"],
        [15, "聚酯多元醇", "RS 6194", "结晶态", 100, "-", "", 3500, "25-35", "≤2", 65, 73, "", "", "聚氨酯热熔胶"],
        [16, "聚酯多元醇", "RS 6195", "结晶态", 100, "-", "", 5500, "15-25", "≤2", 72, 79, "", "", "聚氨酯热熔胶"],
        [17, "聚酯多元醇", "RS 6197", "结晶态", 100, "-", -30, 3500, "25-35", "≤5", 115, 117, "", "", "聚氨酯热熔胶"],
        [18, "聚酯多元醇", "RS 6198", "结晶态", 100, "-", -30, 5000, "15-25", "≤5", 115, 118, "", "", "聚氨酯热熔胶"],
        [19, "聚酯多元醇", "RS 6248", "结晶态", 100, "-", "", 3500, "25-35", "≤3", 90, 95, "", "", "聚氨酯热熔胶、UV树脂"],
        [20, "聚酯多元醇", "RS 6168", "结晶态", 100, "-", "", 3500, "25-35", "≤2", "", 85, "", "", "聚氨酯热熔胶"],
        [21, "聚酯多元醇", "RS 6163", "结晶态", 100, "-", -18, 3500, "25-35", "≤2", "", 92, "", "", "聚氨酯热熔胶"],
        [22, "聚酯多元醇", "RS 6164", "结晶态", 100, "-", -25, 3500, "27-35", "≤2", "", 123, "", "", "聚氨酯热熔胶"],
        # 改性多元醇
        [23, "改性多元醇", "RS 6217", "液态", 100, "-", -60, 2000, "45-55", "≤2", "", "", "", "", "聚氨酯热熔胶"],
        [24, "改性多元醇", "RS 6227", "液态", 100, "-", -60, 2000, "51-58", "≤2", "", "", "", "", "聚氨酯热熔胶"],
        [25, "改性多元醇", "RS 6331", "液态", 100, "-", -60, 2400, "45-55", "≤6", "", "", "", "", "聚氨酯热熔胶"],
        [26, "改性多元醇", "RS 5806", "液态", 100, "-", -30, 50000, 25, "≤2", "", "", "", "", "聚氨酯热熔胶、软包装"],
        [27, "改性多元醇", "RS 5807", "液态", 100, "-", -15, 30000, 30, "≤2", "", "", "", "", "聚氨酯热熔胶"],
        [28, "改性多元醇", "RS 5800", "液态", 100, "-", -15, 10000, 25, "≤2", "", "", "", "", "聚氨酯热熔胶"],
        # 固体丙烯酸树脂
        [29, "固体丙烯酸树脂", "RS 530", "BMA/MMA", 100, "-", 44, 60000, "", 11, 125, "", "", "", "聚氨酯热熔胶、印刷油墨"],
        [30, "固体丙烯酸树脂", "RS 514", "BMA/MMA", 100, "-", 50, 57000, 1.5, 4, 120, "", "", "", "聚氨酯热熔胶、印刷油墨"],
        [31, "固体丙烯酸树脂", "RS 575", "BMA/MMA", 100, "-", 50, 35000, "", 8, 130, "", "", "", "聚氨酯热熔胶、UV涂料"],
        [32, "固体丙烯酸树脂", "RS 585", "BMA/MMA", 100, "-", 56, 60000, "", 9, 130, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨"],
        [33, "固体丙烯酸树脂", "RS 584", "BMA/MMA", 100, "-", 60, 57000, "", 8, 150, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨、马路标线漆"],
        [34, "固体丙烯酸树脂", "RS 516", "BMA/MMA", 100, "-", 61, 63000, "", 8, 150, "", "", "", "聚氨酯热熔胶、防腐涂料、UV涂料、热转印、印刷油墨、马路标线漆"],
        [35, "固体丙烯酸树脂", "RS 528", "MMA/BMA", 100, "-", 70, 67000, 4, "≤1", 165, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨"],
        [36, "固体丙烯酸树脂", "RS 586", "MMA/BMA", 100, "-", 75, 63000, "", "≤1", 160, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨、马路标线漆"],
        [37, "固体丙烯酸树脂", "RS 529", "MMA/BMA", 100, "-", 78, 35000, 3, 7, 155, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨、马路标线漆"],
        [38, "固体丙烯酸树脂", "RS 587", "MMA/BMA", 100, "-", 82, 35000, "", 6, 160, "", "", "", "聚氨酯热熔胶、防腐涂料、印刷油墨、马路标线漆"],
        [39, "固体丙烯酸树脂", "RS 501", "MMA/BMA", 100, "-", 87, 40000, 5, 6, 160, "", "", "", "聚氨酯热熔胶、UV涂料"],
        [40, "固体丙烯酸树脂", "RS 573", "MMA", 100, "-", 103, 110000, "", "≤1", 235, "", "", "", "胶粘剂、热转印"],
        [41, "固体丙烯酸树脂", "RS 580", "MMA", 100, "-", 106, 110000, "", "≤1", 235, "", "", "", "胶粘剂、热转印"],
        [42, "固体丙烯酸树脂", "RS 551", "MMA", 100, "-", 110, 110000, "", "≤1", 235, "", "", "", "胶粘剂、热转印"],
        [43, "固体丙烯酸树脂", "RS 591", "MMA", 100, "-", 119, 165000, "", "≤1", 250, "", "", "", "胶粘剂、热转印"],
        # 高分子量聚酯树脂
        [44, "高分子量聚酯树脂", "RS 6204", "液态", 100, "-", -30, 10000, "6-12", "≤2", "", "", "", "", "印刷油墨、粘合剂"],
        [45, "高分子量聚酯树脂", "RS 6208", "结晶态", 100, "-", -10, 15000, "4-10", "≤4", "", 95, "", "", "印刷油墨、粘合剂"],
        [46, "高分子量聚酯树脂", "CP 711", "固体", 100, "-", 45, 16000, "5-10", "≤2", "", "", "", "", "印刷油墨、粘合剂、罐听涂料、热密封涂料"],
        [47, "高分子量聚酯树脂", "CP 710", "固体", 100, "-", 63, 20000, "4-7", "≤2", "", "", "", "", "印刷油墨"],
        [48, "高分子量聚酯树脂", "CP 708", "固体", 100, "-", 65, 20000, "4-7", "≤5", "", "", "", "", "印刷油墨、热密封涂料"],
        [49, "高分子量聚酯树脂", "CP 706", "固体", 100, "-", 67, 20000, "4-7", "≤2", "", "", "", "", "印刷油墨、粘合剂"],
        [50, "高分子量聚酯树脂", "CP 705", "固体", 100, "-", 67, 15000, "4-7", "≤2", "", "", "", "", "印刷油墨"],
        [51, "高分子量聚酯树脂", "CP 752", "固体", 100, "-", 70, 18000, "4-7", "≤2", "", "", "", "", "罐听涂料"],
        [52, "高分子量聚酯树脂", "CP 712", "固体", 100, "-", 102, 15000, "4-7", "≤3", "", "", "", "", "罐听涂料"],
        # 溶剂型聚酯树脂
        [53, "溶剂型聚酯树脂", "CL 736 A", "溶液", 60, "溶剂型", -5, 7000, "15-20", "≤2", "", "", 4500, "", "建筑卷材、家电卷材、罐听外涂"],
        [54, "溶剂型聚酯树脂", "CL 730 D", "溶液", 65, "溶剂型", 15, 4000, "51-58", "≤3", "", "", 2000, "", "建筑卷材、家电卷材、印刷油墨"],
        [55, "溶剂型聚酯树脂", "CL 715 A", "溶液", 65, "溶剂型", 20, 5500, "15-25", "≤3", "", "", 15000, "", "建筑卷材、家电卷材、印刷油墨"],
        [56, "溶剂型聚酯树脂", "CL 798 L", "溶液", 65, "溶剂型", 20, 3000, "30-40", "≤3", "", "", 5000, "", "建筑卷材、家电卷材、印刷油墨"],
        [57, "溶剂型聚酯树脂", "CL 755 J", "溶液", 65, "溶剂型", 20, 2000, "70-80", "≤8", "", "", 5000, "", "建筑卷材、家电卷材、印刷油墨"],
        [58, "溶剂型聚酯树脂", "CL 737 F", "溶液", 55, "溶剂型", 25, 4000, "35-45", "≤4", "", "", 2000, "", "罐听外涂、印刷油墨"],
        [59, "溶剂型聚酯树脂", "CL 728 D", "溶液", 65, "溶剂型", 25, 2000, "90-100", "≤8", "", "", 5000, "", "印刷油墨"],
        [60, "溶剂型聚酯树脂", "CL 718 C", "溶液", 50, "溶剂型", 30, 5500, "18-24", "≤2", "", "", 3000, "", "建筑卷材、家电卷材、罐听外涂、罐听内涂、印刷油墨"],
        [61, "溶剂型聚酯树脂", "CL 718 D", "溶液", 55, "溶剂型", 30, 5500, "18-24", "≤2", "", "", 4000, "", "建筑卷材、家电卷材、罐听外涂、罐听内涂、印刷油墨"],
        [62, "溶剂型聚酯树脂", "CL 726 C", "溶液", 55, "溶剂型", 30, 6000, "18-24", "≤2", "", "", 4500, "", "建筑卷材、家电卷材、罐听外涂、罐听内涂"],
        [63, "溶剂型聚酯树脂", "CP 711 A", "溶液", 40, "溶剂型", 45, 15000, "7-11", "≤3", "", "", 5000, "", "建筑卷材、家电卷材、罐听外涂、罐听内涂、印刷油墨"],
        [64, "溶剂型聚酯树脂", "CL 720 A", "溶液", 50, "溶剂型", 60, 5500, "18-24", "≤2", "", "", 3000, "", "建筑卷材、家电卷材、罐听外涂、罐听内涂、印刷油墨"],
        # 附着力促进剂
        [65, "附着力促进剂", "KAW", "溶液", 60, "二甲苯", "", "", 30, "-", "", "", 500, "-", "工业涂料、卷材涂料、木器涂料、罐听涂料、交通涂料"],
        [66, "附着力促进剂", "KAW-B", "溶液", 60, "醋酸丁酯", "", "", 30, "-", "", "", 500, "-", "工业涂料、卷材涂料、罐听涂料、交通涂料、印刷油墨"],
        [67, "附着力促进剂", "KAW-100", "液体/树脂", 100, "-", "", "", 30, "-", "", "", "500 (60%XYL)", "", "工业涂料、木器涂料、罐听涂料、交通涂料、印刷油墨"],
        [68, "附着力促进剂", "KAH", "液体/树脂", 100, "-", "", "", 25, "-", "", "", 1000, "", "工业涂料、卷材涂料、木器涂料"],
        [69, "附着力促进剂", "KA-13", "水性分散体", 45, "水", "", "", 60, "-", "", "", 100, "-", "水性木器漆、水性塑胶漆、水性工业漆"],
        [70, "附着力促进剂", "KA-16", "液体/树脂", 100, "-", "", "", 60, "-", "", "", 15000, "", "工业涂料、罐听涂料、塑胶涂料"],
    ]

    for row_idx, row_vals in enumerate(master_data, start=3):
        ws_all.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 1 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws_all.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx in [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
                cell.font = data_font
                cell.alignment = center_align
            elif col_idx == 3:
                cell.font = bold_data_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = left_align

    ws_all.freeze_panes = "A3"
    ws_all.auto_filter.ref = f"A2:O{len(master_data)+2}"

    # =============================================================
    # 2. 聚酯多元醇
    # =============================================================
    ws1 = wb.create_sheet(title="聚酯多元醇")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:M1")
    ws1["A1"] = "KULPES® 聚酯多元醇"
    ws1["A1"].font = title_font
    ws1["A1"].fill = title_fill
    ws1["A1"].alignment = center_align
    ws1.row_dimensions[1].height = 36
    
    headers_t1_r2 = [
        ("A2:A3", "型号"),
        ("B2:B3", "形态"),
        ("C2:C3", "供货形式\n(%固含量)"),
        ("D2:D3", "玻璃化温度\n(°C)"),
        ("E2:E3", "分子量\n(g/mol)"),
        ("F2:F3", "羟值\n(mgKOH/g)"),
        ("G2:G3", "酸值\n(mgKOH/g)"),
        ("H2:H3", "熔点\n(°C)"),
        ("I2:I3", "软化点\n(°C)"),
        ("J2:M2", "应用领域"),
    ]
    subheaders_t1_r3 = [
        ("J3", "聚氨酯热熔胶"),
        ("K3", "UV 树脂"),
        ("L3", "聚氨酯弹性体"),
        ("M3", "软包装"),
    ]
    
    for cell_range, text in headers_t1_r2:
        if ":" in cell_range:
            ws1.merge_cells(cell_range)
            start_cell = cell_range.split(":")[0]
            ws1[start_cell] = text
        else:
            ws1[cell_range] = text
            
    for cell_ref, text in subheaders_t1_r3:
        ws1[cell_ref] = text

    ws1.row_dimensions[2].height = 24
    ws1.row_dimensions[3].height = 26

    data_t1 = [
        ["RS 6059", "无定形态", 100, 10, 1800, "50-60", "≤2", "", 55, "+", "", "", ""],
        ["RS 6067", "无定形态", 100, 30, 3000, "30-40", "≤2", "", 78, "+", "", "", ""],
        ["RS 6069", "无定形态", 100, 30, 3000, "30-40", "≤2", "", 77, "+", "", "", ""],
        ["RS 6073", "无定形态", 100, 30, 5500, "18-24", "≤2", "", 87, "+", "", "", "+"],
        ["RS 6078", "无定形态", 100, 50, 2600, "37-45", "≤2", "", 96, "+", "", "", ""],
        ["RS 6131", "液态", 100, -60, 3500, "25-35", "≤2", 30, 39, "+", "+", "+", "+"],
        ["RS 6128", "液态", 100, -50, 5500, "18-25", "≤2", "", "", "+", "+", "+", "+"],
        ["RS 6119", "液态", 100, -30, 3500, "25-35", "≤2", "", "", "+", "", "+", "+"],
        ["RS 6071", "液态", 100, -25, 1000, "100-120", "≤2", "", "", "+", "+", "+", "+"],
        ["RS 6108", "液态", 100, -15, 3500, "25-35", "≤2", "", "", "+", "", "+", ""],
        ["RS 6183", "结晶态", 100, -60, 3500, "25-35", "≤2", 56, 62, "+", "", "", "+"],
        ["RS 6184", "结晶态", 100, -60, 8500, "12-18", "≤2", 57, 64, "+", "", "", ""],
        ["RS 6173", "结晶态", 100, -40, 3500, "25-35", "≤2", 95, "", "+", "", "", ""],
        ["RS 6193", "结晶态", 100, "", 3500, "25-35", "≤2", 70, 77, "+", "", "", ""],
        ["RS 6194", "结晶态", 100, "", 3500, "25-35", "≤2", 65, 73, "+", "", "", ""],
        ["RS 6195", "结晶态", 100, "", 5500, "15-25", "≤2", 72, 79, "+", "", "", ""],
        ["RS 6197", "结晶态", 100, -30, 3500, "25-35", "≤5", 115, 117, "+", "", "", ""],
        ["RS 6198", "结晶态", 100, -30, 5000, "15-25", "≤5", 115, 118, "+", "", "", ""],
        ["RS 6248", "结晶态", 100, "", 3500, "25-35", "≤3", 90, 95, "+", "+", "", ""],
        ["RS 6168", "结晶态", 100, "", 3500, "25-35", "≤2", "", 85, "+", "", "", ""],
        ["RS 6163", "结晶态", 100, -18, 3500, "25-35", "≤2", "", 92, "+", "", "", ""],
        ["RS 6164", "结晶态", 100, -25, 3500, "27-35", "≤2", "", 123, "+", "", "", ""],
    ]

    for row_idx, row_vals in enumerate(data_t1, start=4):
        ws1.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx >= 10:
                cell.font = check_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    for r in range(2, 4):
        for c in range(1, 14):
            cell = ws1.cell(row=r, column=c)
            cell.border = header_border
            if r == 2:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align
            else:
                if c >= 10:
                    cell.fill = subheader_fill
                    cell.font = subheader_font
                    cell.alignment = center_align
                else:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

    ws1.freeze_panes = "A4"

    # =============================================================
    # 3. 改性多元醇
    # =============================================================
    ws2 = wb.create_sheet(title="改性多元醇")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:M1")
    ws2["A1"] = "KULPES® 改性多元醇"
    ws2["A1"].font = title_font
    ws2["A1"].fill = title_fill
    ws2["A1"].alignment = center_align
    ws2.row_dimensions[1].height = 36

    for cell_range, text in headers_t1_r2:
        if ":" in cell_range:
            ws2.merge_cells(cell_range)
            start_cell = cell_range.split(":")[0]
            ws2[start_cell] = text
        else:
            ws2[cell_range] = text
            
    for cell_ref, text in subheaders_t1_r3:
        ws2[cell_ref] = text

    ws2.row_dimensions[2].height = 24
    ws2.row_dimensions[3].height = 26

    data_t2 = [
        ["RS 6217", "液态", 100, -60, 2000, "45-55", "≤2", "", "", "+", "", "", ""],
        ["RS 6227", "液态", 100, -60, 2000, "51-58", "≤2", "", "", "+", "", "", ""],
        ["RS 6331", "液态", 100, -60, 2400, "45-55", "≤6", "", "", "+", "", "", ""],
        ["RS 5806", "液态", 100, -30, 50000, 25, "≤2", "", "", "+", "", "", "+"],
        ["RS 5807", "液态", 100, -15, 30000, 30, "≤2", "", "", "+", "", "", ""],
        ["RS 5800", "液态", 100, -15, 10000, 25, "≤2", "", "", "+", "", "", ""],
    ]

    for row_idx, row_vals in enumerate(data_t2, start=4):
        ws2.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx >= 10:
                cell.font = check_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    for r in range(2, 4):
        for c in range(1, 14):
            cell = ws2.cell(row=r, column=c)
            cell.border = header_border
            if r == 2:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align
            else:
                if c >= 10:
                    cell.fill = subheader_fill
                    cell.font = subheader_font
                    cell.alignment = center_align
                else:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

    ws2.freeze_panes = "A4"

    # =============================================================
    # 4. 固体丙烯酸树脂
    # =============================================================
    ws3 = wb.create_sheet(title="固体丙烯酸树脂")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:N1")
    ws3["A1"] = "KULPES® 固体丙烯酸树脂"
    ws3["A1"].font = title_font
    ws3["A1"].fill = title_fill
    ws3["A1"].alignment = center_align
    ws3.row_dimensions[1].height = 36

    headers_t3_r2 = [
        ("A2:A3", "型号"),
        ("B2:B3", "基础单体"),
        ("C2:C3", "玻璃化温度\n(°C)"),
        ("D2:D3", "分子量"),
        ("E2:E3", "羟值\n(mgKOH/g)"),
        ("F2:F3", "酸值\n(mgKOH/g)"),
        ("G2:G3", "熔点\n(°C)"),
        ("H2:N2", "应用领域"),
    ]
    subheaders_t3_r3 = [
        ("H3", "聚氨酯热熔胶"),
        ("I3", "胶粘剂"),
        ("J3", "防腐涂料"),
        ("K3", "UV 涂料"),
        ("L3", "热转印"),
        ("M3", "印刷油墨"),
        ("N3", "马路标线漆"),
    ]

    for cell_range, text in headers_t3_r2:
        if ":" in cell_range:
            ws3.merge_cells(cell_range)
            start_cell = cell_range.split(":")[0]
            ws3[start_cell] = text
        else:
            ws3[cell_range] = text
            
    for cell_ref, text in subheaders_t3_r3:
        ws3[cell_ref] = text

    ws3.row_dimensions[2].height = 24
    ws3.row_dimensions[3].height = 26

    data_t3 = [
        ["RS 530", "BMA/MMA", 44, 60000, "", 11, 125, "+", "", "", "", "", "+", ""],
        ["RS 514", "BMA/MMA", 50, 57000, 1.5, 4, 120, "+", "", "", "", "", "+", ""],
        ["RS 575", "BMA/MMA", 50, 35000, "", 8, 130, "+", "", "", "+", "", "", ""],
        ["RS 585", "BMA/MMA", 56, 60000, "", 9, 130, "+", "", "+", "", "", "+", ""],
        ["RS 584", "BMA/MMA", 60, 57000, "", 8, 150, "+", "", "+", "", "", "+", "+"],
        ["RS 516", "BMA/MMA", 61, 63000, "", 8, 150, "+", "", "+", "+", "+", "+", "+"],
        ["RS 528", "MMA/BMA", 70, 67000, 4, "≤1", 165, "+", "", "+", "", "", "+", ""],
        ["RS 586", "MMA/BMA", 75, 63000, "", "≤1", 160, "+", "", "+", "", "", "+", "+"],
        ["RS 529", "MMA/BMA", 78, 35000, 3, 7, 155, "+", "", "+", "", "", "+", "+"],
        ["RS 587", "MMA/BMA", 82, 35000, "", 6, 160, "+", "", "+", "", "", "+", "+"],
        ["RS 501", "MMA/BMA", 87, 40000, 5, 6, 160, "+", "", "", "+", "", "", ""],
        ["RS 573", "MMA", 103, 110000, "", "≤1", 235, "", "+", "", "", "+", "", ""],
        ["RS 580", "MMA", 106, 110000, "", "≤1", 235, "", "+", "", "", "+", "", ""],
        ["RS 551", "MMA", 110, 110000, "", "≤1", 235, "", "+", "", "", "+", "", ""],
        ["RS 591", "MMA", 119, 165000, "", "≤1", 250, "", "+", "", "", "+", "", ""],
    ]

    for row_idx, row_vals in enumerate(data_t3, start=4):
        ws3.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx >= 8:
                cell.font = check_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    for r in range(2, 4):
        for c in range(1, 15):
            cell = ws3.cell(row=r, column=c)
            cell.border = header_border
            if r == 2:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align
            else:
                if c >= 8:
                    cell.fill = subheader_fill
                    cell.font = subheader_font
                    cell.alignment = center_align
                else:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

    ws3.freeze_panes = "A4"

    # =============================================================
    # 5. 高分子量聚酯树脂
    # =============================================================
    ws4 = wb.create_sheet(title="高分子量聚酯树脂")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:M1")
    ws4["A1"] = "KULPES® 高分子量聚酯树脂"
    ws4["A1"].font = title_font
    ws4["A1"].fill = title_fill
    ws4["A1"].alignment = center_align
    ws4.row_dimensions[1].height = 36

    headers_t4_r2 = [
        ("A2:A3", "型号"),
        ("B2:B3", "形态"),
        ("C2:C3", "供货形式\n(%固含量)"),
        ("D2:D3", "玻璃化温度\n(°C)"),
        ("E2:E3", "分子量\n(g/mol)"),
        ("F2:F3", "羟值\n(mgKOH/g)"),
        ("G2:G3", "酸值\n(mgKOH/g)"),
        ("H2:H3", "熔点\n(°C)"),
        ("I2:I3", "软化点\n(°C)"),
        ("J2:M2", "应用领域"),
    ]
    subheaders_t4_r3 = [
        ("J3", "印刷油墨"),
        ("K3", "粘合剂"),
        ("L3", "罐听涂料"),
        ("M3", "热密封涂料"),
    ]

    for cell_range, text in headers_t4_r2:
        if ":" in cell_range:
            ws4.merge_cells(cell_range)
            start_cell = cell_range.split(":")[0]
            ws4[start_cell] = text
        else:
            ws4[cell_range] = text
            
    for cell_ref, text in subheaders_t4_r3:
        ws4[cell_ref] = text

    ws4.row_dimensions[2].height = 24
    ws4.row_dimensions[3].height = 26

    data_t4 = [
        ["RS 6204", "液态", 100, -30, 10000, "6-12", "≤2", "", "", "+", "+", "", ""],
        ["RS 6208", "结晶态", 100, -10, 15000, "4-10", "≤4", "", 95, "+", "+", "", ""],
        ["CP 711", "固体", 100, 45, 16000, "5-10", "≤2", "", "", "+", "+", "+", "+"],
        ["CP 710", "固体", 100, 63, 20000, "4-7", "≤2", "", "", "+", "", "", ""],
        ["CP 708", "固体", 100, 65, 20000, "4-7", "≤5", "", "", "+", "", "", "+"],
        ["CP 706", "固体", 100, 67, 20000, "4-7", "≤2", "", "", "+", "+", "", ""],
        ["CP 705", "固体", 100, 67, 15000, "4-7", "≤2", "", "", "+", "", "", ""],
        ["CP 752", "固体", 100, 70, 18000, "4-7", "≤2", "", "", "", "", "+", ""],
        ["CP 712", "固体", 100, 102, 15000, "4-7", "≤3", "", "", "", "", "+", ""],
    ]

    for row_idx, row_vals in enumerate(data_t4, start=4):
        ws4.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws4.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx >= 10:
                cell.font = check_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    for r in range(2, 4):
        for c in range(1, 14):
            cell = ws4.cell(row=r, column=c)
            cell.border = header_border
            if r == 2:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align
            else:
                if c >= 10:
                    cell.fill = subheader_fill
                    cell.font = subheader_font
                    cell.alignment = center_align
                else:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

    ws4.freeze_panes = "A4"

    # =============================================================
    # 6. 溶剂型聚酯树脂
    # =============================================================
    ws5 = wb.create_sheet(title="溶剂型聚酯树脂")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:L1")
    ws5["A1"] = "KULPES® 溶剂型聚酯树脂"
    ws5["A1"].font = title_font
    ws5["A1"].fill = title_fill
    ws5["A1"].alignment = center_align
    ws5.row_dimensions[1].height = 36

    headers_t5_r2 = [
        ("A2:A3", "型号"),
        ("B2:B3", "供货形式\n(%固含)"),
        ("C2:C3", "玻璃化温度\n(°C)"),
        ("D2:D3", "分子量\n(g/mol)"),
        ("E2:E3", "羟值\n(mgKOH/g)"),
        ("F2:F3", "酸值\n(mgKOH/g)"),
        ("G2:G3", "粘度\n(MPa.s)"),
        ("H2:L2", "应用领域"),
    ]
    subheaders_t5_r3 = [
        ("H3", "建筑卷材"),
        ("I3", "家电卷材"),
        ("J3", "罐听外涂"),
        ("K3", "罐听内涂"),
        ("L3", "印刷油墨"),
    ]

    for cell_range, text in headers_t5_r2:
        if ":" in cell_range:
            ws5.merge_cells(cell_range)
            start_cell = cell_range.split(":")[0]
            ws5[start_cell] = text
        else:
            ws5[cell_range] = text
            
    for cell_ref, text in subheaders_t5_r3:
        ws5[cell_ref] = text

    ws5.row_dimensions[2].height = 24
    ws5.row_dimensions[3].height = 26

    data_t5 = [
        ["CL 736 A", 60, -5, 7000, "15-20", "≤2", 4500, "+", "+", "+", "", ""],
        ["CL 730 D", 65, 15, 4000, "51-58", "≤3", 2000, "+", "+", "", "", "+"],
        ["CL 715 A", 65, 20, 5500, "15-25", "≤3", 15000, "+", "+", "", "", "+"],
        ["CL 798 L", 65, 20, 3000, "30-40", "≤3", 5000, "+", "+", "", "", "+"],
        ["CL 755 J", 65, 20, 2000, "70-80", "≤8", 5000, "+", "+", "", "", "+"],
        ["CL 737 F", 55, 25, 4000, "35-45", "≤4", 2000, "", "", "+", "", "+"],
        ["CL 728 D", 65, 25, 2000, "90-100", "≤8", 5000, "", "", "", "", "+"],
        ["CL 718 C", 50, 30, 5500, "18-24", "≤2", 3000, "+", "+", "+", "+", "+"],
        ["CL 718 D", 55, 30, 5500, "18-24", "≤2", 4000, "+", "+", "+", "+", "+"],
        ["CL 726 C", 55, 30, 6000, "18-24", "≤2", 4500, "+", "+", "+", "+", ""],
        ["CP 711 A", 40, 45, 15000, "7-11", "≤3", 5000, "+", "+", "+", "+", "+"],
        ["CL 720 A", 50, 60, 5500, "18-24", "≤2", 3000, "+", "+", "+", "+", "+"],
    ]

    for row_idx, row_vals in enumerate(data_t5, start=4):
        ws5.row_dimensions[row_idx].height = 20
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws5.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx >= 8:
                cell.font = check_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    for r in range(2, 4):
        for c in range(1, 13):
            cell = ws5.cell(row=r, column=c)
            cell.border = header_border
            if r == 2:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align
            else:
                if c >= 8:
                    cell.fill = subheader_fill
                    cell.font = subheader_font
                    cell.alignment = center_align
                else:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

    ws5.freeze_panes = "A4"

    # =============================================================
    # 7. 附着力促进剂
    # =============================================================
    ws6 = wb.create_sheet(title="附着力促进剂")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:G1")
    ws6["A1"] = "KULPES® 附着力促进剂"
    ws6["A1"].font = title_font
    ws6["A1"].fill = title_fill
    ws6["A1"].alignment = center_align
    ws6.row_dimensions[1].height = 36

    headers_t6 = ["型号", "供货形式\n(%固含)", "溶剂", "羟值\n(mgKOH/g)", "粘度\n(MPa.s)", "PH值", "应用领域–涂料"]
    for col_idx, text in enumerate(headers_t6, start=1):
        cell = ws6.cell(row=2, column=col_idx, value=text)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = header_border
        cell.alignment = center_align
    ws6.row_dimensions[2].height = 28

    data_t6 = [
        ["KAW", 60, "二甲苯", 30, "500", "-", "工业、卷材、木器、罐听、交通"],
        ["KAW-B", 60, "醋酸丁酯", 30, "500", "-", "工业、卷材、罐听、交通、印刷油墨"],
        ["KAW-100", 100, "-", 30, "500 (60%XYL)", "", "工业、木器、罐听、交通、印刷油墨"],
        ["KAH", 100, "-", 25, "1000", "", "工业、卷材、木器"],
        ["KA-13", 45, "水", 60, "100", "-", "水性木器，水性塑胶、水性工业"],
        ["KA-16", 100, "-", 60, "15000", "", "工业、罐听、塑胶"],
    ]

    for row_idx, row_vals in enumerate(data_t6, start=3):
        ws6.row_dimensions[row_idx].height = 22
        fill_color = zebra_fill if row_idx % 2 == 1 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws6.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx == 7:
                cell.font = data_font
                cell.alignment = left_align
            else:
                cell.font = data_font
                cell.alignment = center_align

    ws6.freeze_panes = "A3"

    # =============================================================
    # 8. 特性指标测试方法与公司信息
    # =============================================================
    ws7 = wb.create_sheet(title="测试方法与企业信息")
    ws7.views.sheetView[0].showGridLines = True

    ws7.merge_cells("A1:D1")
    ws7["A1"] = "特性指标测试方法与企业信息"
    ws7["A1"].font = title_font
    ws7["A1"].fill = title_fill
    ws7["A1"].alignment = center_align
    ws7.row_dimensions[1].height = 36

    ws7.merge_cells("A3:D3")
    ws7["A3"] = "一、 特性指标测试方法"
    ws7["A3"].font = Font(name=font_family, size=11, bold=True, color="1B4332")
    ws7["A3"].fill = cat_fill
    ws7.row_dimensions[3].height = 26

    test_headers = ["指标项目", "标准依据", "测试方法说明", "备注"]
    for col_idx, text in enumerate(test_headers, start=1):
        cell = ws7.cell(row=4, column=col_idx, value=text)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = header_border
        cell.alignment = center_align
    ws7.row_dimensions[4].height = 24

    test_methods = [
        ["玻璃化温度 (Tg)", "GB/T 19466.2-2004", "用 DSC（差示扫描式量热法）测定。", ""],
        ["分子量 (Mw)", "GB/T 27843-2011", "用 GPC（凝胶渗透色谱法）测定。", ""],
        ["粘度", "GB/T 7193-2008", "用旋转粘度计测定。", ""],
        ["软化点", "GB/T 4507-2014", "采用环球法测定。", ""],
        ["熔点", "GB/T 4507-2014", "采用 DSC 测定。", ""],
        ["固体份 (固含量)", "GB/T 1725-2007", "将大约3克样品在105度下加热烘烤30分钟，干燥后剩余物质与试样质量比较，以百分数表示。", ""],
        ["羟值", "GB/T 7383-2020", "将大约3克样品溶解到二氯甲烷，室温下用醋酸酐反应样品中的羟基基团。在酸酐水解后用0.5N KOH甲醇溶液滴定。", ""],
        ["酸值", "GB/T 6743-2008", "将大约4克样品溶解到二氯甲烷或四氢呋喃。用0.1N KOH甲醇或乙醇溶液滴定，酚酞作为指示剂。", ""],
    ]

    for row_idx, row_vals in enumerate(test_methods, start=5):
        ws7.row_dimensions[row_idx].height = 26
        fill_color = zebra_fill if row_idx % 2 == 1 else white_fill
        for col_idx, val in enumerate(row_vals, start=1):
            cell = ws7.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = fill_color
            cell.border = data_border
            if col_idx == 1:
                cell.font = bold_data_font
                cell.alignment = center_align
            elif col_idx == 2:
                cell.font = data_font
                cell.alignment = center_align
            else:
                cell.font = data_font
                cell.alignment = left_align

    ws7.merge_cells("A15:D15")
    ws7["A15"] = "二、 昆勒聚合物（上海）有限公司 联系信息"
    ws7["A15"].font = Font(name=font_family, size=11, bold=True, color="1B4332")
    ws7["A15"].fill = cat_fill
    ws7.row_dimensions[15].height = 26

    company_info = [
        ["公司名称", "昆勒聚合物（上海）有限公司 / Kuller Polymer (Shanghai) Co., Ltd."],
        ["地址", "上海市闵行区都庄路2350号2幢501室"],
        ["邮编", "201108"],
        ["电话", "021-6486 6300"],
        ["官方网址", "http://www.kullerpolymer.com"],
        ["电子邮箱", "kullerpolymer@163.com"],
        ["产品系列", "KULPES® 树脂产品（胶粘剂、涂料）"],
    ]

    for row_idx, row_vals in enumerate(company_info, start=16):
        ws7.row_dimensions[row_idx].height = 22
        fill_color = zebra_fill if row_idx % 2 == 0 else white_fill
        cell1 = ws7.cell(row=row_idx, column=1, value=row_vals[0])
        cell1.font = bold_data_font
        cell1.fill = fill_color
        cell1.border = data_border
        cell1.alignment = center_align
        
        ws7.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=4)
        cell2 = ws7.cell(row=row_idx, column=2, value=row_vals[1])
        cell2.font = data_font
        cell2.fill = fill_color
        cell2.border = data_border
        cell2.alignment = left_align
        for c in range(2, 5):
            ws7.cell(row=row_idx, column=c).border = data_border
            ws7.cell(row=row_idx, column=c).fill = fill_color

    # Column widths
    sheet_col_widths = {
        "产品目录总览": {1: 8, 2: 28, 3: 22, 4: 18, 5: 60, 6: 18},
        "全产品总表": {1: 8, 2: 20, 3: 15, 4: 16, 5: 14, 6: 14, 7: 20, 8: 16, 9: 16, 10: 16, 11: 12, 12: 12, 13: 16, 14: 10, 15: 45},
        "聚酯多元醇": {1: 14, 2: 12, 3: 14, 4: 15, 5: 14, 6: 15, 7: 15, 8: 12, 9: 12, 10: 14, 11: 12, 12: 14, 13: 12},
        "改性多元醇": {1: 14, 2: 12, 3: 14, 4: 15, 5: 14, 6: 15, 7: 15, 8: 12, 9: 12, 10: 14, 11: 12, 12: 14, 13: 12},
        "固体丙烯酸树脂": {1: 14, 2: 14, 3: 15, 4: 14, 5: 15, 6: 15, 7: 12, 8: 14, 9: 12, 10: 12, 11: 12, 12: 12, 13: 12, 14: 13},
        "高分子量聚酯树脂": {1: 14, 2: 12, 3: 14, 4: 15, 5: 14, 6: 15, 7: 15, 8: 12, 9: 12, 10: 13, 11: 13, 12: 13, 13: 14},
        "溶剂型聚酯树脂": {1: 14, 2: 14, 3: 15, 4: 14, 5: 15, 6: 15, 7: 14, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13},
        "附着力促进剂": {1: 14, 2: 14, 3: 14, 4: 15, 5: 18, 6: 10, 7: 42},
        "测试方法与企业信息": {1: 18, 2: 22, 3: 65, 4: 15},
    }

    for ws in wb.worksheets:
        widths = sheet_col_widths.get(ws.title, {})
        for col_idx, width in widths.items():
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

    excel_file = r"d:\Jay\vscode\attech0824\KULPES_产品目录_2026_V5.0.xlsx"
    wb.save(excel_file)
    print("Excel successfully created.")

if __name__ == "__main__":
    build_excel()
