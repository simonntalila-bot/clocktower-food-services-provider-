import requests
import re

BASE = 'http://127.0.0.1:8888'
s = requests.Session()

# Login
r = s.get(f'{BASE}/login/')
csrf = re.search(r'csrfmiddlewaretoken.*?value="([^"]+)"', r.text).group(1)
r = s.post(f'{BASE}/login/', data={'csrfmiddlewaretoken': csrf, 'username': 'admin', 'password': 'clocktower2026'}, allow_redirects=True)

# Check orders page error
r = s.get(f'{BASE}/admin-panel/orders/')
if r.status_code == 500:
    m = re.search(r'Template error.*?>(.*?)<', r.text, re.DOTALL)
    if m:
        print("ERROR:", m.group(1)[:300])
    # Find the actual URL name in the error
    m2 = re.search(r'NoReverseMatch.*? Reverse for.*?(\x27[^\x27]+\x27)', r.text)
    if m2:
        print("Missing URL:", m2.group(1))
    m3 = re.search(r"reverse.*?(\x27[^\x27]+.*?\x27)", r.text)
    if m3:
        print("URL trying to reverse:", m3.group(1)[:200])
    # Also try the stack trace
    m4 = re.search(r"Template.*?(\w+\.html.*?line \d+)", r.text)
    if m4:
        print("Template:", m4.group(1)[:200])

# Check settings page error  
r = s.get(f'{BASE}/admin-panel/settings/')
if r.status_code == 500:
    m = re.search(r"reverse.*?(\x27[^\x27]+.*?\x27)", r.text)
    if m:
        print("Settings URL error:", m.group(1)[:200])
