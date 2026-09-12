import json
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_3_unique_urls.json", "r", encoding="utf-8") as f:
    all_urls = json.load(f)

# Filter for community links
community_domains = ["discord.gg", "t.me", "reddit.com", "github.com", "discuss.", "forum", "users.rust-lang.org", "ethresear.ch", "biggerpockets.com", "stackoverflow.com", "kaggle.com", "huggingface.co", "medium.com"]

community_urls = [u for u in all_urls if any(d in u.lower() for d in community_domains)]

print(f"Total community URLs to verify: {len(community_urls)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def check_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    # Discord invite check
    if "discord.gg" in domain:
        code = parsed.path.strip("/")
        api_url = f"https://discord.com/api/v9/invites/{code}"
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                data = json.loads(resp.read().decode())
                return url, {"status": 200, "type": "discord_valid", "guild": data.get("guild", {}).get("name")}
        except urllib.error.HTTPError as e:
            return url, {"status": e.code, "type": "discord_error", "msg": str(e)}
        except Exception as ex:
            return url, {"status": "err", "type": "discord_err", "msg": str(ex)}

    # Telegram check
    if "t.me" in domain:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                is_real = ("tgme_page_title" in content or "tgme_page_extra" in content or "tgme_page_action" in content)
                return url, {"status": 200 if is_real else 404, "type": "telegram", "is_real": is_real}
        except Exception as ex:
            return url, {"status": "err", "type": "telegram_err", "msg": str(ex)}

    # GitHub discussions or repos
    if "github.com" in domain:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                return url, {"status": resp.status, "type": "github_ok"}
        except urllib.error.HTTPError as e:
            return url, {"status": e.code, "type": "github_error", "msg": str(e)}
        except Exception as ex:
            return url, {"status": "err", "type": "github_err", "msg": str(ex)}

    # General HTTP check
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            return url, {"status": resp.status, "type": "http_ok"}
    except urllib.error.HTTPError as e:
        return url, {"status": e.code, "type": "http_error", "msg": str(e)}
    except Exception as ex:
        return url, {"status": "err", "type": "http_err", "msg": str(ex)}

results = {}
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(check_url, u): u for u in community_urls}
    for future in as_completed(futures):
        u, res = future.result()
        results[u] = res

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_3_community_url_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

dead_urls = []
for u, r in results.items():
    st = r.get("status")
    if st == 404:
        dead_urls.append((u, r))
    elif r.get("type") == "telegram" and not r.get("is_real"):
        dead_urls.append((u, r))

print(f"\nCompleted verification of {len(results)} URLs.")
print(f"Total 404/dead URLs found: {len(dead_urls)}")
for u, r in dead_urls:
    print(f"  DEAD: {u} -> {r}")
