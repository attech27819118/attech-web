with open('js/table-renderer.js', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            ${p.website && p.website !== 'N/A' ? `<button data-action="tds" data-product="${p.product_name}" class="text-red-600 hover:text-red-800 f-size-sm f-weight-bold" title="${p.product_name} - ${t.official_doc}" aria-label="${p.product_name} - ${t.official_doc}"><i class="fa-solid fa-file-pdf"></i></button>` : ''}
            ${p.tech_data_url && p.tech_data_url !== 'N/A' ? `<button data-action="data" data-product="${p.product_name}" class="text-blue-700 hover:text-blue-900 f-size-sm f-weight-bold" title="${p.product_name} - ${t.tech_data}" aria-label="${p.product_name} - ${t.tech_data}"><i class="fa-solid fa-file-lines"></i></button>` : ''}'''

repl1 = '''            ${p.website && p.website !== 'N/A' ? `<button data-action="tds" data-product="${p.product_name}" class="text-red-600 hover:text-red-800 f-size-sm f-weight-bold cursor-pointer" title="${p.product_name} - ${t.official_doc} (線上預覽)" aria-label="${p.product_name} - ${t.official_doc}"><i class="fa-solid fa-file-pdf"></i></button>` : ''}
            ${p.tech_data_url && p.tech_data_url !== 'N/A' ? `<button data-action="data" data-product="${p.product_name}" class="text-blue-700 hover:text-blue-900 f-size-sm f-weight-bold cursor-pointer" title="${p.product_name} - ${t.tech_data} (線上預覽)" aria-label="${p.product_name} - ${t.tech_data}"><i class="fa-solid fa-file-lines"></i></button>` : ''}'''

target2 = '''            {
                id: 'production_method',
                propKey: 'production_method',
                title: '<span class="th-title">類型</span>',
                class: 'min-w-[85px] f-weight-bold text-blue-950 text-center',
                getValue: p => p.production_method
            },'''

repl2 = '''            {
                id: 'production_method',
                propKey: 'production_method',
                title: '<span class="th-title">生產法</span>',
                class: 'min-w-[85px] f-weight-bold text-blue-950 text-center',
                getValue: p => p.production_method
            },'''

print('Found target1:', target1 in text)
print('Found target2:', target2 in text)

if target1 in text:
    text = text.replace(target1, repl1)
if target2 in text:
    text = text.replace(target2, repl2)

with open('js/table-renderer.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated table-renderer.js successfully!')

