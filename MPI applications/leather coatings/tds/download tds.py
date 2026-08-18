import requests

# 把所有 PDF 連結放在 list
urls = [
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20270S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20325S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroMatte%201415-EZ%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031HD%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800F%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620VF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-G%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-611AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Superslip%206515AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyGlide%201226XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyTuf%201229%20TDS.pdf"
]


tdsname = [
    "PropylTex 270S TDS",
    "PropylTex 325S TDS",
    "MicroMatte 1415-EZ TDS",
    "PropylMatte 31 TDS",
    "PropylMatte 31HD TDS",
    "MicroTouch 800XF TDS",
    "MicroTouch 800F TDS",
    "MPP-620VF TDS",
    "MP-28AL TDS",
    "MP-28AL-XF TDS",
    "MP-28AL-G TDS",
    "MPP-611AL TDS",
    "MPP-620AL-XF TDS",
    "Superslip 6515AL TDS",
    "PolyGlide 1226XF TDS",
    "PolyTuf 1229 TDS"
]




# 逐一下載
for url, name in zip(urls, tdsname):
    filename = f"{name}.pdf"   # 檔名直接用品項名稱
    print(f"Downloading {name}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {name}")
