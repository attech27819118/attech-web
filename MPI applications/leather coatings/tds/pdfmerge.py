from PyPDF2 import PdfMerger

pdfs = [
    "PolyTuf 1229 TDS.pdf",
    "MicroTouch 800F TDS.pdf",
    "MP-28AL-G TDS.pdf",
    "PropylTex 270S TDS.pdf",
    "PropylMatte 31HD TDS.pdf",
    "PolyGlide 1226XF TDS.pdf",
    "MPP-620VF TDS.pdf",
    "MP-28AL-XF TDS.pdf",
    "MicroTouch 800XF TDS.pdf",
    "MP-28AL TDS.pdf",
    "Superslip 6515AL TDS.pdf",
    "MPP-611AL TDS.pdf",
    "MicroMatte 1415-EZ TDS.pdf",
    "PropylMatte 31 TDS.pdf",
    "MPP-620AL-XF TDS.pdf",
    "PropylTex 325S TDS.pdf"
]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("leather.pdf")
merger.close()

