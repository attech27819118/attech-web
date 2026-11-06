import pdfplumber
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r'c:\Users\user\Downloads\宏威應用材料 9月與10月數據分析報告.pdf'

with pdfplumber.open(pdf_path) as pdf:
    for page_idx, page in enumerate(pdf.pages):
        print(f"==================== PAGE {page_idx + 1} ====================")
        words = page.extract_words(extra_attrs=['fontname', 'size', 'stroking_color', 'non_stroking_color'])
        print(f"Total words: {len(words)}")
        # sample some unique font styles
        styles = set()
        for w in words:
            styles.add((w.get('fontname'), round(w.get('size'), 1), str(w.get('non_stroking_color'))))
        print("Styles (font, size, color):")
        for s in sorted(styles, key=lambda x: (x[1] if x[1] else 0), reverse=True):
            print("  ", s)
        
        # print words in vertical order to reconstruct layout
        print("\nTop 40 lines of text with y-positions:")
        sorted_words = sorted(words, key=lambda w: (round(w['top'] / 5) * 5, w['x0']))
        current_y = None
        current_line = []
        for w in sorted_words:
            y_bucket = round(w['top'] / 8) * 8
            if current_y is None or abs(y_bucket - current_y) > 4:
                if current_line:
                    print(f"y={current_y:3.0f} | size={current_line[0].get('size'):.1f} | {' '.join([x['text'] for x in current_line])}")
                current_y = y_bucket
                current_line = [w]
            else:
                current_line.append(w)
        if current_line:
            print(f"y={current_y:3.0f} | size={current_line[0].get('size'):.1f} | {' '.join([x['text'] for x in current_line])}")

