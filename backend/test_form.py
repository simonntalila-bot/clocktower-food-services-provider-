import requests
import re
import time

BASE = 'http://127.0.0.1:8888'
s = requests.Session()

print("=" * 60)
print("  TEST 1: Order with ONLY name + phone (minimal)")
print("=" * 60)

r = s.get(f'{BASE}/order/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
food_ids = re.findall(r'name="food_(\d+)"', r.text)

data = {
    'csrfmiddlewaretoken': csrf,
    'name': 'Hamisi Mwinyi',
    'phone': '0755123456',
}
if food_ids:
    data[f'food_{food_ids[0]}'] = '2'

r = s.post(f'{BASE}/order/', data=data, allow_redirects=True)
print(f"Status: {r.status_code}")
print(f"Success: {'success' in r.url or 'Asante' in r.text}")
if 'Asante' in r.text or 'order_num' in r.text:
    m = re.search(r'CTF-\d+', r.text)
    print(f"Order: {m.group() if m else '?'}")

time.sleep(1)

print("\n" + "=" * 60)
print("  TEST 2: Order with NO payment method (should default to cash)")
print("=" * 60)

r = s.get(f'{BASE}/order/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
food_ids = re.findall(r'name="food_(\d+)"', r.text)

data = {
    'csrfmiddlewaretoken': csrf,
    'name': 'Asha Juma',
    'phone': '0789111222',
    'email': 'asha@test.com',
    'table_location': 'Meza 7',
    'payment_method': '',  # intentionally empty
    'comments': 'Usilipe mgongo sana',
}
if food_ids and len(food_ids) >= 2:
    data[f'food_{food_ids[0]}'] = '1'
    data[f'food_{food_ids[1]}'] = '3'

r = s.post(f'{BASE}/order/', data=data, allow_redirects=True)
print(f"Status: {r.status_code}")
print(f"Success: {'success' in r.url or 'Asante' in r.text}")
if 'Asante' in r.text:
    m = re.search(r'CTF-\d+', r.text)
    print(f"Order: {m.group() if m else '?'}")

time.sleep(1)

print("\n" + "=" * 60)
print("  TEST 3: Order WITHOUT phone (should fail)")
print("=" * 60)

r = s.get(f'{BASE}/order/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)

data = {
    'csrfmiddlewaretoken': csrf,
    'name': 'Test No Phone',
}
r = s.post(f'{BASE}/order/', data=data, allow_redirects=True)
print(f"Status: {r.status_code}")
has_error = 'error-msg' in r.text or 'lazima' in r.text
print(f"Shows error: {has_error}")

print("\n" + "=" * 60)
print("  TEST 4: Order WITHOUT name (should fail)")
print("=" * 60)

r = s.get(f'{BASE}/order/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)

data = {
    'csrfmiddlewaretoken': csrf,
    'phone': '0711222333',
}
r = s.post(f'{BASE}/order/', data=data, allow_redirects=True)
print(f"Status: {r.status_code}")
has_error = 'error-msg' in r.text or 'lazima' in r.text
print(f"Shows error: {has_error}")

print("\n" + "=" * 60)
print("  TEST 5: Check DB — payment methods stored correctly")
print("=" * 60)

# Login and check
r = s.get(f'{BASE}/login/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
s.post(f'{BASE}/login/', data={'csrfmiddlewaretoken': csrf, 'username': 'admin', 'password': 'clocktower2026'}, allow_redirects=True)

r = s.get(f'{BASE}/admin-panel/orders/')
print(f"Admin orders: {r.status_code}")
# Check payment methods in table
for pattern in ['cash', 'mpesa', 'tigo', 'bank', 'unpaid']:
    count = r.text.lower().count(pattern)
    if count > 0:
        print(f"  '{pattern}' found {count}x")
