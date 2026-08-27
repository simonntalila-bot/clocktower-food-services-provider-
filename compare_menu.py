import json

with open(r'D:\KCL\cloctoer\clock_tower_menu.json', encoding='utf-8') as f:
    menu = json.load(f)

with open(r'D:\KCL\cloctoer\data\foods.json', encoding='utf-8') as f:
    foods = json.load(f)

foods_map = {}
for item in foods:
    key = item['name'].strip().lower()
    foods_map[key] = item

menu_items = []
for cat in menu['categories']:
    for item in cat['items']:
        menu_items.append({
            'category': cat['category'],
            'name': item['name'].strip(),
            'price': item.get('price'),
            'price_eat_in': item.get('price_eat_in'),
            'id': item.get('id','')
        })

print("=== PRICE MISMATCHES ===")
found_mismatch = False
for mi in menu_items:
    name_lower = mi['name'].strip().lower()
    if name_lower in foods_map:
        fp = foods_map[name_lower]['price']
        mp = mi['price'] if mi['price'] else mi['price_eat_in']
        if mp is not None and fp != mp:
            print("  %s: JSON=%d, foods.json=%d" % (mi['name'], mp, fp))
            found_mismatch = True
if not found_mismatch:
    print("  None found!")

print()
print("=== IN JSON BUT NOT IN foods.json ===")
missing_in_foods = False
for mi in menu_items:
    name_lower = mi['name'].strip().lower()
    if name_lower not in foods_map:
        p = mi['price'] if mi['price'] else mi['price_eat_in']
        print("  %s (%s) - price: %s" % (mi['name'], mi['category'], p))
        missing_in_foods = True
if not missing_in_foods:
    print("  None found!")

print()
print("=== IN foods.json BUT NOT IN JSON ===")
missing_in_json = False
json_names = set(mi['name'].strip().lower() for mi in menu_items)
for item in foods:
    if item['name'].strip().lower() not in json_names:
        print("  %s - price: %d - category: %s" % (item['name'], item['price'], item['category']))
        missing_in_json = True
if not missing_in_json:
    print("  None found!")

print()
print("=== IMAGES AUDIT ===")
print("Items WITH images in foods.json:")
for item in foods:
    if item.get('img') and item['img'].strip():
        print("  id=%d %s -> %s" % (item['id'], item['name'], item['img']))

print()
print("Items with images in menu JSON:")
for cat in menu['categories']:
    for item in cat['items']:
        if item.get('img') and item['img'].strip():
            print("  %s -> %s" % (item['name'], item['img']))

print()
print("=== CATEGORY MAPPING (menu json category -> foods.json category) ===")
cat_map = {}
for mi in menu_items:
    key = mi['category']
    if key not in cat_map:
        cat_map[key] = set()
    name_lower = mi['name'].strip().lower()
    if name_lower in foods_map:
        cat_map[key].add(foods_map[name_lower]['category'])

for mc, fcs in sorted(cat_map.items()):
    print("  %s -> foods.json: %s" % (mc, ", ".join(sorted(fcs))))

print()
print("=== TOTALS ===")
print("  Menu JSON items: %d" % len(menu_items))
print("  foods.json items: %d" % len(foods))
print("  Menu JSON categories: %d" % len(menu['categories']))
