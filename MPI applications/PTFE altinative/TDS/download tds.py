import requests

# 把所有 PDF 連結放在 list
urls = [
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-G%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-611AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroKlear%20418AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Superslip%206515AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyGlide%201226XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/SuperGlide%201231%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyTuf%201229%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Spherex%20200%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Spherex%20200XF%20TDS.pdf"
]

tdsname = [
    "MP-28AL TDS",
    "MP-28AL-XF TDS",
    "MP-28AL-G TDS",
    "MPP-611AL TDS",
    "MPP-620AL-XF TDS",
    "MicroKlear 418AL TDS",
    "Superslip 6515AL TDS",
    "PolyGlide 1226XF TDS",
    "SuperGlide 1231 TDS",
    "PolyTuf 1229 TDS",
    "Spherex 200 TDS",
    "Spherex 200XF TDS"
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
