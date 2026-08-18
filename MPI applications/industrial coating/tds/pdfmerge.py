from PyPDF2 import PdfMerger

pdfs = [
    "SuperGlide 1231 TDS.pdf",
    "Micropro 440W TDS.pdf",
    "AquaPoly 511 TDS.pdf",
    "Superslip 6515AL TDS.pdf",
    "PropylTex 100S,140S,200S,200SF TDS.pdf",
    "MPP-620VF 620XF TDS.pdf",
    "MP-28AL TDS.pdf",
    "PolyTuf 1229 TDS.pdf",
    "Polysilk 750 TDS.pdf",
    "MicroKlear 418 TDS.pdf",
    "PropylTex 325S TDS.pdf",
    "Micromide 520 TDS.pdf",
    "MP-22XF TDS.pdf",
    "MPP-611AL TDS.pdf",
    "MicroTouch 800XF 800F TDS.pdf",
    "MicroKlear 116 TDS.pdf",
    "PropylTex 270S,270S-1518 TDS.pdf",
    "NyloTex 50,100,140,200 TDS.pdf",
    "PropylTex 50,20 TDS.pdf",
    "PolyGlide 1226XF TDS.pdf",
    "PropylMatte 31HD TDS.pdf",
    "MPP-611XF TDS.pdf",
    "PropylMatte 31 TDS.pdf",
    "MicroKlear 418AL TDS.pdf",
    "AquaPoly 250 TDS.pdf"
]


merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("industrial.pdf")
merger.close()

