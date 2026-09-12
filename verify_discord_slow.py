import json
import urllib.request
import urllib.error
import time

discord_429 = [
    "golang", "nextjs", "langchain", "gamedev", "proptrading", "devcord",
    "stocks", "rust-lang", "wallstreetbets", "realestate", "vue",
    "theprogrammershangout", "tailwind", "trading", "forex", "reactiflux",
    "typescript", "tryhackme", "wealth", "technology"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

results = {}
for code in discord_429:
    api_url = f"https://discord.com/api/v9/invites/{code}"
    time.sleep(0.8) # Avoid 429
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            results[code] = {"status": 200, "guild": data.get("guild", {}).get("name", "Unknown")}
    except urllib.error.HTTPError as e:
        results[code] = {"status": e.code, "msg": str(e)}
    except Exception as ex:
        results[code] = {"status": "err", "msg": str(ex)}

for code, r in results.items():
    print(f"discord.gg/{code} -> {r.get('status')} {r.get('guild', r.get('msg', ''))}")
