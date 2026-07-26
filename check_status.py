import json, os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('product_data.js', 'r', encoding='utf-8') as f:
    pdata = f.read()

with open('shop_products_with_images.json', 'r', encoding='utf-8') as f:
    pjson = json.load(f)

print('--- FEATURE VERIFICATION ---')
print('1. Search by salt page in HTML:', 'id="salts"' in html)
print('2. Google Maps link in HTML:', 'maps.app.goo.gl' in html)
print('3. Store hours (9:00 AM) in HTML:', '9:00 AM' in html)
print('4. loadMoreProducts in HTML:', 'loadMoreProducts' in html)
print('5. seeAllProducts in HTML:', 'seeAllProducts' in html)
print('6. Admin panel removed from HTML:', 'admin-panel' not in html)

print('7. renderSalts in JS:', 'renderSalts' in js)
print('8. getBrandLogo in JS:', 'getBrandLogo' in js)

print('9. Total products in product_data.js:', pdata.count('"name":'))
print('10. Total products in shop_products_with_images.json:', len(pjson))

for p in pjson:
    if 'mercazole' in p['name'].lower():
        print('  Neo Mercazole brand:', p['brand'])

ecosprin_count = sum(1 for p in pjson if 'ecosprin' in p['name'].lower())
print('11. Total Ecosprin products:', ecosprin_count)
