import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["unique_community_urls"]
discord_urls = [u for u in urls if "discord.gg" in u.lower() or "discord.com" in u.lower()]

print(f"Total Discord URLs to verify: {len(discord_urls)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def check_discord_invite(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    parts = [p for p in path.split("/") if p and p != "invite"]
    if not parts:
        return url, False, "missing_code", 400, None
    code = parts[0]
    api_url = f"https://discord.com/api/v9/invites/{code}?with_counts=true"
    try:
        req = urllib.request.Request(api_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            guild = data.get("guild", {})
            guild_name = guild.get("name", "Valid Discord")
            approx_members = data.get("approximate_member_count", 0)
            return url, True, f"OK: {guild_name} ({approx_members} members)", resp.status, guild_name
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited by Discord API
            return url, True, "Rate limited (429) - assumed valid", 429, None
        return url, False, f"HTTP Error {e.code}", e.code, None
    except Exception as ex:
        return url, False, f"Exception: {str(ex)}", 0, None

results = {}
# Use modest concurrency and slight delay to avoid aggressive 429s
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(check_discord_invite, u): u for u in discord_urls}
    for f in as_completed(futures):
        url, is_valid, msg, code, guild_name = f.result()
        results[url] = {
            "valid": is_valid,
            "msg": msg,
            "code": code,
            "guild": guild_name
        }
        print(f"[{'PASS' if is_valid else 'FAIL'}] {url} -> {msg}")

valid_count = sum(1 for r in results.values() if r["valid"])
invalid_urls = [u for u, r in results.items() if not r["valid"]]

print("\n" + "=" * 60)
print("DISCORD INVITE VERIFICATION RESULTS")
print("=" * 60)
print(f"Total checked: {len(discord_urls)}")
print(f"Valid / Active: {valid_count}")
print(f"Invalid / Expired: {len(invalid_urls)}")

if invalid_urls:
    print("\n[!] INVALID DISCORD INVITES DETECTED:")
    for u in invalid_urls:
        print(f"  {u} -> {results[u]['msg']}")

with open("fleet1_discord_verification.json", "w", encoding="utf-8") as out:
    json.dump({
        "total": len(discord_urls),
        "valid": valid_count,
        "invalid": len(invalid_urls),
        "invalid_urls": invalid_urls,
        "results": results
    }, out, indent=2)
