from PyPDF2 import PdfMerger

pdfs = [
  "MPP-635VF TDS.pdf",
  "MicroTouch 800F TDS.pdf",
  "MPP-611XF TDS.pdf",
  "Micropro 400 TDS.pdf",
  "MicroTouch 800XF TDS.pdf",
  "MP-28AL TDS.pdf",
  "MicroTex 975 TDS.pdf",
  "MPP-620VF TDS.pdf",
  "MP-22VF TDS.pdf",
  "GraphShield 730 TDS.pdf",
  "MPP-611AL TDS.pdf",
  "MicroTex 950 TDS.pdf",
  "Micromide 520 TDS.pdf",
  "MicroTex 580 TDS.pdf",
  "MicroKlear 418AL TDS.pdf",
  "PolyTuf 1229 TDS.pdf",
  "MP-22XF TDS.pdf",
  "PolyGlide 1226XF TDS.pdf",
  "PropylMatte 31 TDS.pdf",
  "PropylTex 100S,140S,200S,200SF.pdf",
  "SuperGlide 1231 TDS.pdf",
  "Superslip 6515AL TDS.pdf"
]


merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("powder.pdf")
merger.close()

