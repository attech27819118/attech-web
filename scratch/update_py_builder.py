with open('scripts/build_technology_subpages.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = """    sec_start = html.find('id="tab-technology"')
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)"""

new_block = """    sec_start = html.find('id="tab-technology"')
    comment_marker = '<!-- Tab: 技術專區'
    prev_comment = html.rfind(comment_marker, 0, sec_start)
    if prev_comment != -1:
        while True:
            prev = html.rfind(comment_marker, 0, prev_comment)
            if prev != -1 and html[prev:prev_comment].strip().startswith('<!-- Tab: 技術專區'):
                prev_comment = prev
            else:
                break
    replace_start = prev_comment if prev_comment != -1 else html.rfind('<section', 0, sec_start)"""

print("Occurrences of old_block:", text.count(old_block))
if text.count(old_block) > 0:
    text = text.replace(old_block, new_block)
    with open('scripts/build_technology_subpages.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("build_technology_subpages.py updated successfully!")

