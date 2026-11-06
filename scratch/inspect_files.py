import sys
import os
import io
import pandas as pd
import pypdf
import openpyxl

# Force utf-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("==================== PDF INSPECTION ====================")
pdf_path = r'c:\Users\user\Downloads\宏威應用材料 9月與10月數據分析報告.pdf'
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")
for i, p in enumerate(reader.pages):
    print(f"\n--- PAGE {i+1} ---")
    print(p.extract_text())

print("\n==================== 9.xlsx INSPECTION ====================")
f9_path = r'c:\Users\user\Downloads\9.xlsx'
wb9 = openpyxl.load_workbook(f9_path, data_only=True)
print("9.xlsx sheets:", wb9.sheetnames)
for s in wb9.sheetnames:
    df = pd.read_excel(f9_path, sheet_name=s)
    print(f"\nSheet [{s}] shape: {df.shape}")
    print(df.head(10))

print("\n==================== 10.xlsx INSPECTION ====================")
f10_path = r'c:\Users\user\Downloads\10.xlsx'
wb10 = openpyxl.load_workbook(f10_path, data_only=True)
print("10.xlsx sheets:", wb10.sheetnames)
for s in wb10.sheetnames:
    df = pd.read_excel(f10_path, sheet_name=s)
    print(f"\nSheet [{s}] shape: {df.shape}")
    print(df.head(10))

print("\n==================== 99.csv INSPECTION ====================")
c99_path = r'c:\Users\user\Downloads\99.csv'
# try detecting encoding
for enc in ['utf-8', 'utf-8-sig', 'cp950', 'big5']:
    try:
        df99 = pd.read_csv(c99_path, encoding=enc)
        print(f"99.csv successfully read with {enc}, shape: {df99.shape}")
        print(df99.head(10))
        break
    except Exception as e:
        pass

print("\n==================== 1010.csv INSPECTION ====================")
c1010_path = r'c:\Users\user\Downloads\1010.csv'
for enc in ['utf-8', 'utf-8-sig', 'cp950', 'big5']:
    try:
        df1010 = pd.read_csv(c1010_path, encoding=enc)
        print(f"1010.csv successfully read with {enc}, shape: {df1010.shape}")
        print(df1010.head(10))
        break
    except Exception as e:
        pass

