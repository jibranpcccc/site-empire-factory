import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("all_db_urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

# Filter for discord.gg and github.com
targets = [u for u in urls if "discord.gg" in u or "github.com" in u]
print(f"Testing {len(targets)} discord and github URLs from database...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def check(url):
    p = urlparse(url)
    if "discord.gg" in p.netloc:
        code = p.path.strip("/")
        api = f"https://discord.com/api/v9/invites/{code}"
        try:
            req = urllib.request.Request(api, headers=headers)
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                return url, 200, data.get("guild", {}).get("name")
        except urllib.error.HTTPError as e:
            return url, e.code, str(e)
        except Exception as ex:
            return url, "err", str(ex)
    else:
        # github
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                return url, resp.status, "ok"
        except urllib.error.HTTPError as e:
            return url, e.code, str(e)
        except Exception as ex:
            return url, "err", str(ex)

results = {}
# Use moderate concurrency to avoid discord 429
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(check, u): u for u in targets}
    for f in as_completed(futures):
        u, status, msg = f.result()
        results[u] = (status, msg)

print("\n--- RESULTS ---")
broken = []
for u, (st, msg) in results.items():
    if st == 404:
        broken.append((u, st, msg))
        print(f"BROKEN 404: {u} -> {msg}")
    elif st != 200 and st != 429:
        print(f"OTHER: {u} -> {st} {msg}")

print(f"\nTotal broken in DB: {len(broken)}")
