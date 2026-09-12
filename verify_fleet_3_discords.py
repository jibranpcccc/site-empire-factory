import json
import urllib.request
import urllib.error
import time
from urllib.parse import urlparse

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_3_unique_urls.json", "r", encoding="utf-8") as f:
    all_urls = json.load(f)

discord_urls = sorted([u for u in all_urls if "discord.gg" in u])
print(f"Total unique discord URLs in Fleet Part 3: {len(discord_urls)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

results = {}
invalid_discords = []

for u in discord_urls:
    parsed = urlparse(u)
    code = parsed.path.strip("/")
    api_url = f"https://discord.com/api/v9/invites/{code}"
    
    success = False
    retries = 3
    while retries > 0 and not success:
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                guild = data.get("guild", {}).get("name", "Unknown")
                results[u] = {"status": 200, "guild": guild}
                print(f"[OK 200] {u} -> {guild}")
                success = True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                results[u] = {"status": 404, "msg": "Invite Invalid/Expired"}
                invalid_discords.append(u)
                print(f"[DEAD 404] {u}")
                success = True
            elif e.code == 429:
                # rate limit, wait 2 seconds
                time.sleep(2)
                retries -= 1
            else:
                results[u] = {"status": e.code, "msg": str(e)}
                print(f"[ERR {e.code}] {u}")
                success = True
        except Exception as ex:
            results[u] = {"status": "err", "msg": str(ex)}
            print(f"[EXCEPTION] {u} -> {ex}")
            success = True
    
    time.sleep(0.4)

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_3_discord_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n--- SUMMARY OF DEAD DISCORDS ---")
print(f"Total dead discords: {len(invalid_discords)}")
for d in invalid_discords:
    print(f"  {d}")
