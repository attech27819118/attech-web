import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_ga_csv(filename):
    print(f"==================== {filename} ====================")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sections are separated by '#' comments or blocks
    lines = [l.strip() for l in content.split('\n')]
    
    current_block = []
    blocks = []
    for l in lines:
        if l.startswith('# ----------------------------------------') or l.startswith('# 開始日期') or l.startswith('# 報表數據'):
            if current_block:
                blocks.append(current_block)
                current_block = []
        current_block.append(l)
    if current_block:
        blocks.append(current_block)
        
    print(f"Total lines: {len(lines)}")
    # Print distinct tables in this file
    table_idx = 0
    in_table = False
    current_table = []
    for l in lines:
        if l.startswith('#') or not l:
            if current_table:
                table_idx += 1
                print(f"\n--- TABLE {table_idx} (rows: {len(current_table)}) ---")
                for r in current_table[:10]:
                    print(r)
                if len(current_table) > 10:
                    print(f"... and {len(current_table)-10} more rows")
                current_table = []
        else:
            current_table.append(l)
    if current_table:
        table_idx += 1
        print(f"\n--- TABLE {table_idx} (rows: {len(current_table)}) ---")
        for r in current_table[:10]:
            print(r)
        if len(current_table) > 10:
            print(f"... and {len(current_table)-10} more rows")

parse_ga_csv(r'c:\Users\user\Downloads\99.csv')
parse_ga_csv(r'c:\Users\user\Downloads\1010.csv')

