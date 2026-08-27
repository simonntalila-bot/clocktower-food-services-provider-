import requests
import re
import json
import traceback

BASE = 'http://127.0.0.1:8888'
s = requests.Session()

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# =============================================
# 1. TEST LOGIN PAGE
# =============================================
section("1. LOGIN PAGE")
r = s.get(f'{BASE}/login/')
print(f"Status: {r.status_code}")
has_form = '<form' in r.text
has_disabled = 'disabled' in r.text
print(f"Has form: {has_form}")
print(f"Has disabled inputs: {has_disabled}")
csrf_m = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text)
csrf = csrf_m.group(1) if csrf_m else None
print(f"CSRF token: {'OK' if csrf else 'MISSING'}")

# =============================================
# 2. LOGIN AS ADMIN
# =============================================
section("2. LOGIN")
r = s.post(f'{BASE}/login/', data={
    'csrfmiddlewaretoken': csrf,
    'username': 'admin',
    'password': 'clocktower2026'
}, allow_redirects=True)
print(f"Status: {r.status_code}")
print(f"Redirected to: {r.url}")
logged_in = 'admin-panel' in r.url or 'admin' in r.url.lower()
print(f"Logged in: {logged_in}")

# =============================================
# 3. CHECK ADMIN PANEL
# =============================================
section("3. ADMIN PANEL")
r = s.get(f'{BASE}/admin-panel/')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    has_dashboard = 'Dashboard' in r.text or 'dashboard' in r.text.lower()
    has_stats = 'stat-card' in r.text
    print(f"Has dashboard: {has_dashboard}")
    print(f"Has stats: {has_stats}")
else:
    print(f"ERROR: {r.text[:200]}")

# =============================================
# 4. CHECK ORDER PAGE + FOOD ITEMS
# =============================================
section("4. ORDER PAGE")
r = s.get(f'{BASE}/order/')
print(f"Status: {r.status_code}")

# Get CSRF
csrf2_m = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text)
csrf2 = csrf2_m.group(1) if csrf2_m else csrf

# Get food IDs - check for both naming patterns
food_ids_pattern1 = re.findall(r'name="food_(\d+)"', r.text)
food_ids_pattern2 = re.findall(r'name="qty_(\d+)"', r.text)
food_ids = food_ids_pattern1 or food_ids_pattern2
field_prefix = "food_" if food_ids_pattern1 else "qty_"
print(f"Food items found: {len(food_ids)}")
print(f"Field prefix: {field_prefix}")
print(f"Sample IDs: {food_ids[:5]}")

# =============================================
# 5. PLACE TEST ORDER
# =============================================
section("5. PLACE ORDER")
order_data = {
    'csrfmiddlewaretoken': csrf2,
    'name': 'Test Mteja Wa Robot',
    'phone': '0712345678',
    'email': 'test@clocktower.co.tz',
    'table_location': 'Meza #3',
    'payment_method': 'mpesa',
    'notes': 'Namba ya M-Pesa: 0712345678',
    'comments': 'Test order from automated test script',
}

# Add qty for first 3 food items
if food_ids:
    for fid in food_ids[:3]:
        order_data[f'{field_prefix}{fid}'] = '1'
    print(f"Ordering {min(3, len(food_ids))} items with {field_prefix} prefix")

r = s.post(f'{BASE}/order/', data=order_data, allow_redirects=True)
print(f"Status: {r.status_code}")
print(f"Redirected to: {r.url}")
is_success = 'order-success' in r.url or 'success' in r.url or 'Asante' in r.text
print(f"Order success: {is_success}")

# Check for errors
error_divs = re.findall(r'<div class="error-msg"[^>]*>(.*?)</div>', r.text, re.DOTALL)
if error_divs:
    for err in error_divs:
        clean = re.sub(r'<[^>]+>', '', err).strip()
        print(f"ERROR: {clean}")

if is_success:
    order_num_m = re.search(r'CTF-\d+', r.text)
    if order_num_m:
        print(f"Order Number: {order_num_m.group()}")

# =============================================
# 6. CHECK NOTIFICATIONS API
# =============================================
section("6. NOTIFICATIONS API")
r = s.get(f'{BASE}/api/notifications/')
print(f"Status: {r.status_code}")
try:
    notifs = r.json()
    total = notifs.get('unread', 0)
    items = notifs.get('notifications', [])
    print(f"Unread: {total}")
    print(f"Total notifications: {len(items)}")
    for n in items[:5]:
        print(f"  - [{n.get('time','')}] {n.get('title','')}: {n.get('detail','')[:80]}")
except Exception as e:
    print(f"Parse error: {e}")
    print(f"Response: {r.text[:300]}")

# =============================================
# 7. CHECK ADMIN ORDERS
# =============================================
section("7. ADMIN ORDERS")
r = s.get(f'{BASE}/admin-panel/orders/')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    order_rows = re.findall(r'<tr[^>]*>(.*?)</tr>', r.text, re.DOTALL)
    print(f"Order rows: {len(order_rows) - 1}")  # minus header
    if 'Test Mteja' in r.text:
        print("Test order visible in admin: YES")
    else:
        print("Test order visible in admin: NO")

# =============================================
# 8. CHECK ADMIN DASHBOARD
# =============================================
section("8. ADMIN DASHBOARD")
r = s.get(f'{BASE}/admin-panel/')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    total_orders_m = re.search(r'total_orders.*?(\d+)', r.text)
    today_orders_m = re.search(r'today_orders.*?(\d+)', r.text)
    print(f"Has content: {len(r.text)} chars")

# =============================================
# 9. CHECK NOTIFICATION LOG
# =============================================
section("9. NOTIFICATION LOG (DB)")
from django.utils import timezone
import os, sys
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clocktower_backend.settings')

# Can't import Django models directly in script, check via API
r = s.get(f'{BASE}/api/notifications/')
try:
    data = r.json()
    print(f"Notifications in DB: {len(data.get('notifications', []))}")
except:
    pass

# =============================================
# 10. CHECK ACTIVITY LOG
# =============================================
section("10. ACTIVITY LOG")
r = s.get(f'{BASE}/admin-panel/activity/')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    has_activity = 'Agizo' in r.text or 'agizo' in r.text
    print(f"Has order activity: {has_activity}")

# =============================================
# SUMMARY
# =============================================
section("SUMMARY")
print(f"Login page:     {'PASS' if has_form and not has_disabled else 'FAIL'}")
print(f"Login auth:     {'PASS' if logged_in else 'FAIL'}")
print(f"Admin panel:    {'PASS' if r.status_code == 200 else 'FAIL'}")
print(f"Food items:     {'PASS' if food_ids else 'FAIL'} ({len(food_ids)} items)")
print(f"Order placed:   {'PASS' if is_success else 'FAIL'}")
print(f"Notifications:  {'CHECK'}")
