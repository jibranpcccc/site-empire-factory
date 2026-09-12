import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("fleet2_community_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["urls"]
# Filter out discord urls (which we already tested thoroughly)
non_discord_urls = [u for u in urls if "discord.gg" not in u and "discord.com" not in u]
print(f"Testing {len(non_discord_urls)} non-Discord URLs...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def test_url(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            # Check for telegram / github specifics
            if "github.com" in url and "/discussions" in url:
                # If discussions tab is disabled, github redirects to / or issues or 404
                final_url = resp.geturl()
                if "/discussions" not in final_url and resp.status != 200:
                    return url, False, f"github_discussions_redirected_to_{final_url}", resp.status
            return url, True, "ok", resp.status
    except urllib.error.HTTPError as e:
        # 403 or 429 can happen with Reddit, Cloudflare protected forums (Bogleheads, etc.)
        # but 404 / 410 / 5xx are real dead URLs
        if e.code in [403, 429]:
            return url, True, f"blocked_{e.code}_likely_active", e.code
        else:
            return url, False, f"http_error_{e.code}", e.code
    except Exception as ex:
        return url, False, f"error_{str(ex)}", 0

results = {}
with ThreadPoolExecutor(max_workers=25) as executor:
    futures = {executor.submit(test_url, u): u for u in non_discord_urls}
    for f in as_completed(futures):
        u, is_valid, msg, code = f.result()
        results[u] = {"valid": is_valid, "msg": msg, "code": code}

with open("fleet2_non_discord_audit_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

dead = [u for u, r in results.items() if not r["valid"]]
print(f"\nNon-Discord test complete. Total: {len(results)}, Dead/Broken: {len(dead)}")
for d in dead:
    print(f"  BROKEN: {d} -> {results[d]}")
