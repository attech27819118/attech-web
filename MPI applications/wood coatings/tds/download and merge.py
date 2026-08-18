import requests
import os
from PyPDF2 import PdfMerger

# PDF 連結與檔名
urls = [
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20270S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20325S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800F%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031HD%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Micropro%20400%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Micropro%20440W%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroMatte%201415-EZ%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/AquaPoly%20511%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-22XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620VF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/AquaBead%20519%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Spherex%20200%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Spherex%20200XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL-G%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-611AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroKlear%20418AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Superslip%206515AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/SuperGlide%201231%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyTuf%201229%20TDS.pdf"
]


names = names = [
    "PropylTex 270S TDS",
    "PropylTex 325S TDS",
    "MicroTouch 800XF TDS",
    "MicroTouch 800F TDS",
    "PropylMatte 31 TDS",
    "PropylMatte 31HD TDS",
    "Micropro 400 TDS",
    "Micropro 440W TDS",
    "MicroMatte 1415-EZ TDS",
    "AquaPoly 511 TDS",
    "MP-22XF TDS",
    "MPP-620VF TDS",
    "AquaBead 519 TDS",
    "Spherex 200 TDS",
    "Spherex 200XF TDS",
    "MP-28AL TDS",
    "MP-28AL-XF TDS",
    "MP-28AL-G TDS",
    "MPP-611AL TDS",
    "MPP-620AL-XF TDS",
    "MicroKlear 418AL TDS",
    "Superslip 6515AL TDS",
    "SuperGlide 1231 TDS",
    "PolyTuf 1229 TDS"
]

merger = PdfMerger()
downloaded_files = []

# 下載並加入合併器
for url, name in zip(urls, names):
    print(f"Downloading {name}...")
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{name}.pdf"
        with open(filename, "wb") as f:
            f.write(response.content)
        merger.append(filename)
        downloaded_files.append(filename)
    else:
        print(f"Failed to download {name}")

# 輸出合併檔案
merger.write("leather.pdf")
merger.close()


