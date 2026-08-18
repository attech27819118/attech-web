import requests

# 把所有 PDF 連結放在 list
urls = [
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-611AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroKlear%20418AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/Superslip%206515AL%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620AL-XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/PolyGlide%201226XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MP-22XF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MPP-620VF%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/MicroKlear%20418%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/AquaBead%20519%20TDS.pdf",
    "https://www.micropowders.com/assets/pdfs/TDS/GraphShield%20730%20TDS.pdf"
]

tdsname = [
    "MPP-611AL",
    "MicroKlear 418AL",
    "Superslip 6515AL",
    "MPP-620AL-XF",
    "PolyGlide 1226XF",
    "MP-22XF",
    "MPP-620VF",
    "MicroKlear 418",
    "AquaBead 519",
    "GraphShield 730"
]



# 逐一下載
for url, name in zip(urls, tdsname):
    filename = f"{name} TDS.pdf"   # 檔名直接用品項名稱
    print(f"Downloading {name}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {name}")
