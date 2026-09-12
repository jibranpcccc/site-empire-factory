import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0"}

for u in ["https://t.me/s/wholefoodsperks", "https://t.me/wholefoodsperks"]:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            html = r.read().decode("utf-8", errors="ignore")
            m = re.search(r'class="tgme_page_title"[^>]*><span[^>]*>(.*?)</span>', html)
            title = m.group(1) if m else "No title"
            extra = "tgme_page_extra" in html
            print(f"{u} -> status: {r.status}, title: {title}, extra: {extra}")
    except Exception as e:
        print(f"{u} -> {e}")
