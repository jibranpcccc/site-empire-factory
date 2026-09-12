import os
import re
import json
import urllib.request
from urllib.parse import urlparse

INDEXNOW_KEY = "4a123bc89fe04b56ad781290cde456fa"

sites = [
    r"c:\Users\jibra\Desktop\1\20 blogs\developer-coding-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\deals-loot-coupons-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\scholarships-study-abroad-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\devops-cloud-architect-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\indie-hackers-micro-saas-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output\fire-personal-finance-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output\golang-microservices-distributed-hub",
    r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output\growth-marketing-hackers-hub"
]

canonical_urls = []
for s in sites:
    idx = os.path.join(s, "index.html")
    with open(idx, "r", encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'rel="canonical"\s+href="([^"]+)"', html)
    if m:
        canonical_urls.append(m.group(1))

print(f"Submitting IndexNow for {len(canonical_urls)} updated sites...")

for site_url in canonical_urls:
    domain = urlparse(site_url).netloc
    url_list = [
        site_url.rstrip('/') + '/',
        site_url.rstrip('/') + '/about.html',
        site_url.rstrip('/') + '/submit.html',
        site_url.rstrip('/') + '/contact.html',
        site_url.rstrip('/') + '/privacy.html',
        site_url.rstrip('/') + '/terms.html'
    ]
    payload = {
        "host": domain,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{site_url.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }
    data = json.dumps(payload).encode("utf-8")
    for endpoint in ["https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow"]:
        try:
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Antigravity-IndexNow/2.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[{resp.status}] {endpoint} -> {site_url}")
        except urllib.error.HTTPError as e:
            print(f"[{e.code}] {endpoint} -> {site_url}")
        except Exception as e:
            print(f"[ERR] {endpoint} -> {site_url}: {e}")
