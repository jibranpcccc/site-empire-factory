import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["unique_community_urls"]
non_discord_urls = [u for u in urls if "discord.gg" not in u.lower() and "discord.com" not in u.lower()]

print(f"Total non-Discord URLs to verify: {len(non_discord_urls)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def verify_single_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Telegram
    if "t.me" in domain:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                is_valid = ("tgme_page_title" in html or "tgme_page_extra" in html or "tgme_page_action" in html)
                title = ""
                if "tgme_page_title" in html:
                    import re
                    m = re.search(r'class="tgme_page_title"[^>]*><span[^>]*>(.*?)</span>', html)
                    if m:
                        title = m.group(1).strip()
                return url, is_valid, f"Telegram ({title})" if is_valid else "Telegram empty/missing", resp.status
        except urllib.error.HTTPError as e:
            return url, False, f"Telegram HTTP {e.code}", e.code
        except Exception as ex:
            return url, True, f"Telegram connection err: {str(ex)[:30]}", 0

    # Reddit
    if "reddit.com" in domain:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                return url, True, "Reddit OK", resp.status
        except urllib.error.HTTPError as e:
            if e.code in [403, 429]:
                # Cloudflare or rate-limit from reddit bot defense
                return url, True, f"Reddit bot-block/rate-limit ({e.code})", e.code
            elif e.code == 404:
                return url, False, "Reddit Subreddit 404", 404
            return url, False, f"Reddit HTTP {e.code}", e.code
        except Exception as ex:
            return url, True, f"Reddit connection err: {str(ex)[:30]}", 0

    # WhatsApp
    if "whatsapp.com" in domain:
        return url, True, "WhatsApp invite link format", 200

    # Other HTTP (GitHub, forums, government/scholarship portals)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return url, True, f"HTTP {resp.status} OK", resp.status
    except urllib.error.HTTPError as e:
        if e.code in [403, 429]:
            # Bot blocked on government or protected site
            return url, True, f"HTTP {e.code} (protected/bot-filtered)", e.code
        elif e.code == 404:
            return url, False, f"HTTP 404 Dead Link", 404
        return url, False, f"HTTP {e.code}", e.code
    except Exception as ex:
        return url, True, f"Connection timeout/error: {str(ex)[:30]}", 0

if __name__ == "__main__":
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(verify_single_url, u): u for u in non_discord_urls}
        for f in as_completed(futures):
            url, is_valid, msg, code = f.result()
            results[url] = {"valid": is_valid, "msg": msg, "code": code}

    valid_count = sum(1 for r in results.values() if r["valid"])
    invalid_urls = [u for u, r in results.items() if not r["valid"]]

    print("\n" + "=" * 60)
    print("NON-DISCORD URL VERIFICATION RESULTS")
    print("=" * 60)
    print(f"Total checked: {len(non_discord_urls)}")
    print(f"Valid: {valid_count}")
    print(f"Invalid / 404: {len(invalid_urls)}")

    if invalid_urls:
        print("\n[!] INVALID/404 URLS:")
        for u in invalid_urls:
            print(f"  {u} -> {results[u]['msg']}")

    with open("fleet1_non_discord_verification.json", "w", encoding="utf-8") as out:
        json.dump({
            "total": len(non_discord_urls),
            "valid": valid_count,
            "invalid": len(invalid_urls),
            "invalid_urls": invalid_urls,
            "results": results
        }, out, indent=2)
