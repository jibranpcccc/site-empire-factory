import json
import ssl
import urllib.request
import urllib.error
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["unique_community_urls"]
tg_urls = [u for u in urls if "t.me" in u.lower()]

print(f"Total Telegram URLs to deep verify: {len(tg_urls)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def verify_tg(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r'class="tgme_page_title"[^>]*><span[^>]*>(.*?)</span>', html)
            title = m.group(1).strip() if m else None
            has_extra = "tgme_page_extra" in html
            has_action = "tgme_page_action" in html
            
            # An active channel/group has tgme_page_title and (has_extra or has_action)
            # If title is None and not has_extra, it's an empty/unclaimed handle
            is_valid = bool(title or has_extra)
            return url, is_valid, title, resp.status
    except Exception as ex:
        return url, False, f"Err: {str(ex)[:30]}", 0

results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(verify_tg, u): u for u in tg_urls}
    for f in as_completed(futures):
        u, is_valid, title, status = f.result()
        results[u] = {"valid": is_valid, "title": title, "status": status}
        if not is_valid:
            print(f"[FAIL] {u} -> title: {title}, status: {status}")

invalid_tg = [u for u, r in results.items() if not r["valid"]]

print("\n" + "=" * 60)
print("TELEGRAM DEEP VERIFICATION RESULTS")
print("=" * 60)
print(f"Total Telegram URLs checked: {len(tg_urls)}")
print(f"Valid Telegram channels/groups: {len(tg_urls) - len(invalid_tg)}")
print(f"Empty/unclaimed or invalid Telegram: {len(invalid_tg)}")

for u in invalid_tg:
    print(f"  {u} -> {results[u]}")

with open("fleet1_telegram_deep_verification.json", "w", encoding="utf-8") as out:
    json.dump({"invalid": invalid_tg, "results": results}, out, indent=2)
