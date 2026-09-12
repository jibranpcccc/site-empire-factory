import urllib.request
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for u in ["https://t.me/solana", "https://t.me/kubernetes", "https://t.me/wholefoodsperks"]:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
            soup = BeautifulSoup(r.read().decode("utf-8", errors="ignore"), "html.parser")
            title = soup.find("div", class_="tgme_page_title")
            extra = soup.find("div", class_="tgme_page_extra")
            desc = soup.find("div", class_="tgme_page_description")
            action = soup.find("div", class_="tgme_page_action")
            print(f"=== {u} ===")
            print("  Title:", title.text.strip() if title else None)
            print("  Extra:", extra.text.strip() if extra else None)
            print("  Desc:", (desc.text.strip()[:60] + "...") if desc else None)
            print("  Action:", action.text.strip() if action else None)
    except Exception as e:
        print(f"=== {u} === Error:", e)
