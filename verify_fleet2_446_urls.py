import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("fleet2_community_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["urls"]
print(f"Loaded {len(urls)} unique community URLs to verify.")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def verify_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # 1. Discord API verification
    if "discord.gg" in domain or "discord.com" in domain:
        path_parts = [p for p in parsed.path.split("/") if p and p != "invite"]
        if not path_parts:
            return url, False, "invalid_discord_path", 400
        invite_code = path_parts[0]
        api_url = f"https://discord.com/api/v9/invites/{invite_code}"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": HEADERS["User-Agent"]})
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                d = json.loads(resp.read().decode("utf-8", errors="ignore"))
                guild = d.get("guild", {})
                guild_name = guild.get("name", "Valid Discord")
                return url, True, f"discord_valid: {guild_name}", resp.status
        except urllib.error.HTTPError as e:
            return url, False, f"discord_http_error: {e.code}", e.code
        except Exception as ex:
            return url, False, f"discord_err: {str(ex)}", 0

    # 2. Telegram verification
    if "t.me" in domain:
        channel_name = parsed.path.strip("/")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                is_valid = ("tgme_page_title" in html or "tgme_page_extra" in html or "tgme_page_action" in html) and ("tgme_page_title" in html)
                return url, is_valid, "telegram_channel" if is_valid else "telegram_empty_or_missing", resp.status
        except urllib.error.HTTPError as e:
            return url, False, f"telegram_http_error: {e.code}", e.code
        except Exception as ex:
            return url, False, f"telegram_err: {str(ex)}", 0

    # 3. Reddit verification
    if "reddit.com" in domain:
        # Check subreddit
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                return url, True, "reddit_ok", resp.status
        except urllib.error.HTTPError as e:
            # 403 or 429 from reddit can happen due to bot protection, check if url structure is standard /r/...
            if e.code in [403, 429]:
                # Many subreddits block basic scrapers with 403/429
                return url, True, f"reddit_ratelimit_or_block_{e.code}", e.code
            elif e.code == 404:
                return url, False, "reddit_404", 404
            else:
                return url, False, f"reddit_http_error: {e.code}", e.code
        except Exception as ex:
            return url, False, f"reddit_err: {str(ex)}", 0

    # 4. General HTTP verification (GitHub, Forums, etc.)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return url, True, "http_ok", resp.status
    except urllib.error.HTTPError as e:
        return url, False, f"http_error: {e.code}", e.code
    except Exception as ex:
        return url, False, f"exception: {str(ex)}", 0

results = {}
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(verify_url, u): u for u in urls}
    for f in as_completed(futures):
        u, is_valid, msg, code = f.result()
        results[u] = {
            "valid": is_valid,
            "msg": msg,
            "code": code
        }

with open("fleet2_url_liveness_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

invalid_urls = {u: res for u, res in results.items() if not res["valid"]}
print(f"\nVerification Complete.")
print(f"Total URLs Tested: {len(results)}")
print(f"Total Valid URLs: {len(results) - len(invalid_urls)}")
print(f"Total Invalid/Broken URLs: {len(invalid_urls)}")

print("\n--- INVALID / BROKEN URLS FOUND ---")
for u, res in sorted(invalid_urls.items(), key=lambda x: x[1]['code']):
    print(f"[{res['code']}] {u} -> {res['msg']}")
