import requests
import re

BASE = 'http://127.0.0.1:8888'
s = requests.Session()

# Login
r = s.get(f'{BASE}/login/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
r = s.post(f'{BASE}/login/', data={'csrfmiddlewaretoken': csrf, 'username': 'admin', 'password': 'clocktower2026'}, allow_redirects=True)
print(f"Login: {r.status_code} -> {r.url}")

# Test all admin pages
pages = [
    'admin-panel/',
    'admin-panel/orders/',
    'admin-panel/customers/',
    'admin-panel/foods/',
    'admin-panel/users/',
    'admin-panel/activity/',
    'admin-panel/comments/',
    'admin-panel/settings/',
    'order/',
    'api/notifications/',
]

for page in pages:
    r = s.get(f'{BASE}/{page}')
    status = 'OK' if r.status_code == 200 else f'ERR {r.status_code}'
    print(f"  {status}  /{page}")
    if r.status_code == 500:
        # Find error
        err_m = re.search(r'TemplateSyntaxError.*?>(.*?)<', r.text)
        if err_m:
            print(f"       -> {err_m.group(1)}")
        else:
            print(f"       -> {r.text[:200]}")
