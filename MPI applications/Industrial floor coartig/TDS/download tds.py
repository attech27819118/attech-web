import requests

# 把所有 PDF 連結放在 list
urls = [
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20100S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20140S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20200S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20200SF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20270S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20270S-1518%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%20325S%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%2050%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylTex%2020%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/NyloTex%2050%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/NyloTex%20100%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/NyloTex%20140%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/NyloTex%20200%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroTouch%20800F%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PropylMatte%2031%20HD%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Aquapoly%20511%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-22XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-28AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyTuf%201229%20TDS.pdf"
]
tdsname = [
    "PropylTex 100S TDS",
    "PropylTex 140S TDS",
    "PropylTex 200S TDS",
    "PropylTex 200SF TDS",
    "PropylTex 270S TDS",
    "PropylTex 270S-1518 TDS",
    "PropylTex 325S TDS",
    "PropylTex 50 TDS",
    "PropylTex 20 TDS",
    "NyloTex 50 TDS",
    "NyloTex 100 TDS",
    "NyloTex 140 TDS",
    "NyloTex 200 TDS",
    "MicroTouch 800XF TDS",
    "MicroTouch 800F TDS",
    "PropylMatte 31 TDS",
    "PropylMatte 31HD TDS",
    "AquaPoly 511 TDS",
    "MP-22XF TDS",
    "MP-28AL TDS",
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
