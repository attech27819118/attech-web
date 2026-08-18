from PyPDF2 import PdfMerger

pdfs = [
    "MPP-611AL TDS.pdf",
    "MP-28AL-G TDS.pdf",
    "Spherex 200 TDS.pdf",
    "PolyGlide 1226XF TDS.pdf",
    "PolyTuf 1229 TDS.pdf",
    "MicroKlear 418AL TDS.pdf",
    "MP-28AL TDS.pdf",
    "MP-28AL-XF TDS.pdf",
    "SuperGlide 1231 TDS.pdf",
    "Spherex 200XF TDS.pdf",
    "MPP-620AL-XF TDS.pdf",
    "Superslip 6515AL TDS.pdf"
]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("PTFE.pdf")
merger.close()

