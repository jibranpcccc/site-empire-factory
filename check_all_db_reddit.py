import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("all_db_urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

reddit_urls = [u for u in urls if "reddit.com" in u]
print(f"Testing {len(reddit_urls)} Reddit URLs...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def check(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return url, resp.status, "ok"
    except urllib.error.HTTPError as e:
        return url, e.code, str(e)
    except Exception as ex:
        return url, "err", str(ex)

results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check, u): u for u in reddit_urls}
    for f in as_completed(futures):
        u, status, msg = f.result()
        results[u] = (status, msg)

print("\n--- RESULTS ---")
broken = []
for u, (st, msg) in results.items():
    if st == 404:
        broken.append((u, st, msg))
        print(f"BROKEN REDDIT 404: {u} -> {msg}")
    elif st != 200:
        print(f"REDDIT STATUS {st}: {u} -> {msg}")

print(f"\nTotal broken Reddit URLs in DB: {len(broken)}")
