from PyPDF2 import PdfMerger

pdfs = [
    "AquaPoly 511 TDS.pdf",
    "MicroKlear 116 TDS.pdf",
    "MicroKlear 418AL TDS.pdf",
    "MicroMatte 1415-EZ TDS.pdf",
    "Micromide 520 TDS.pdf",
    "Micropro 400 TDS.pdf",
    "MicroTouch 800F TDS.pdf",
    "MicroTouch 800XF TDS.pdf",
    "MP-22XF TDS.pdf",
    "MP-28AL TDS.pdf",
    "MPP-611AL TDS.pdf",
    "MPP-620VF TDS.pdf",
    "MPP-620XF TDS.pdf",
    "MPP-635VF TDS.pdf",
    "PolyGlide 1226XF TDS.pdf",
    "Polysilk 750 TDS.pdf",
    "PolyTuf 1229 TDS.pdf",
    "PropylMatte 31 TDS.pdf",
    "PropylMatte 31HD TDS.pdf",
    "SuperGlide 1231 TDS.pdf",
    "Superslip 6515AL TDS.pdf"
]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("ink.pdf")
merger.close()

