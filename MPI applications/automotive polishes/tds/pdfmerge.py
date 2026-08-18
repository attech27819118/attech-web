from PyPDF2 import PdfMerger

pdfs = [
  "MPP-620AL-XF TDS.pdf",
  "MPP-611AL TDS.pdf",
  "GraphShield 730 TDS.pdf",
  "MPP-620VF TDS.pdf",
  "MP-22XF TDS.pdf",
  "PolyGlide 1226XF TDS.pdf",
  "MicroKlear 418AL TDS.pdf",
  "Superslip 6515AL TDS.pdf",
  "AquaPoly 511 TDS.pdf",
  "AquaBead 519 TDS.pdf",
  "MicroKlear 418 TDS.pdf"
]




merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("automotive polishes.pdf")
merger.close()

