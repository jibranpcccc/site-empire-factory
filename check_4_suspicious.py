import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0"}

urls = [
    "https://chat.whatsapp.com/invite/foodpromoglitches",
    "https://t.me/testnet_news",
    "https://t.me/wholefoodsperks",
    "https://www.reddit.com/r/BaristaFIRE/"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            print(f"[OK {resp.status}] {u}")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {u}")
    except Exception as ex:
        print(f"[ERR] {u} -> {ex}")
