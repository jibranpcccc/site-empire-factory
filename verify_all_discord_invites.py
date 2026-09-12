import json
import time
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse

with open("fleet2_community_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["urls"]
discord_urls = [u for u in urls if "discord.gg" in u or "discord.com" in u]
print(f"Testing all {len(discord_urls)} Discord URLs with controlled delay...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

results = {}
for i, url in enumerate(discord_urls, 1):
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split("/") if p and p != "invite"]
    if not path_parts:
        results[url] = {"status": 400, "msg": "invalid path"}
        continue
    code = path_parts[0]
    api_url = f"https://discord.com/api/v9/invites/{code}"
    
    # Try up to 3 times if 429
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                data_resp = json.loads(resp.read().decode("utf-8"))
                guild = data_resp.get("guild", {})
                guild_name = guild.get("name", "Valid Server")
                results[url] = {"status": 200, "valid": True, "guild": guild_name}
                print(f"[{i}/{len(discord_urls)}] 200 OK: {url} -> {guild_name}", flush=True)
                success = True
                break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[{i}/{len(discord_urls)}] 429 Rate Limit on {code}, sleeping 2.5s...", flush=True)
                time.sleep(2.5)
                continue
            elif e.code == 404:
                results[url] = {"status": 404, "valid": False, "msg": "Unknown/Dead Invite"}
                print(f"[{i}/{len(discord_urls)}] 404 DEAD: {url}", flush=True)
                success = True
                break
            else:
                results[url] = {"status": e.code, "valid": False, "msg": str(e)}
                print(f"[{i}/{len(discord_urls)}] {e.code} ERROR: {url}", flush=True)
                success = True
                break
        except Exception as ex:
            results[url] = {"status": "err", "valid": False, "msg": str(ex)}
            print(f"[{i}/{len(discord_urls)}] EXCEPTION: {url} -> {ex}", flush=True)
            success = True
            break

    time.sleep(0.4)

with open("fleet2_discord_audit_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

dead_discord = [u for u, r in results.items() if not r.get("valid")]
print(f"\nDiscord audit complete. Total: {len(results)}, Dead: {len(dead_discord)}")
for d in dead_discord:
    print(f"  DEAD: {d} -> {results[d]}")
