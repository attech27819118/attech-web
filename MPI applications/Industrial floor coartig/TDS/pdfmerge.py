from PyPDF2 import PdfMerger

pdfs = [
    "AquaBead 519 TDS.pdf",
    "AquaPoly 511 TDS.pdf",
    "MicroTouch 800F TDS.pdf",
    "MicroTouch 800XF TDS.pdf",
    "MP-22XF TDS.pdf",
    "MP-28AL TDS.pdf",
    "NyloTex 50 TDS.pdf",
    "NyloTex 100 TDS.pdf",
    "NyloTex 140 TDS.pdf",
    "NyloTex 200 TDS.pdf",
    "PolyTuf 1229 TDS.pdf",
    "PropylMatte 31 TDS.pdf",
    "PropylMatte 31HD TDS.pdf",
    "PropylTex 20 TDS.pdf",
    "PropylTex 50 TDS.pdf",
    "PropylTex 100S TDS.pdf",
    "PropylTex 140S TDS.pdf",
    "PropylTex 200S TDS.pdf",
    "PropylTex 200SF TDS.pdf",
    "PropylTex 270S TDS.pdf",
    "PropylTex 270S-1518 TDS.pdf",
    "PropylTex 325S TDS.pdf"]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("industrial coatings.pdf")
merger.close()

