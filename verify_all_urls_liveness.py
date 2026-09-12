import json
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlparse

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\unique_urls_to_verify.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

results = {}
for i, url in enumerate(urls, 1):
    parsed = urlparse(url)
    domain = parsed.netloc

    # For discord invite links, discord API can verify invite code!
    # e.g., https://discord.com/api/v9/invites/{code}
    if "discord.gg" in domain:
        invite_code = parsed.path.strip("/")
        api_url = f"https://discord.com/api/v9/invites/{invite_code}"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": headers["User-Agent"]})
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                data = json.loads(resp.read().decode())
                results[url] = {"status": resp.status, "type": "discord_valid", "guild": data.get("guild", {}).get("name", "Unknown")}
        except urllib.error.HTTPError as e:
            results[url] = {"status": e.code, "type": "discord_error", "msg": str(e)}
        except Exception as ex:
            results[url] = {"status": "err", "type": "discord_exception", "msg": str(ex)}
        continue

    # For telegram t.me links:
    if "t.me" in domain:
        channel_name = parsed.path.strip("/")
        # telegram t.me/{channel} returns 200 with HTML preview
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                # If channel doesn't exist, telegram page says "If you have Telegram, you can contact..." or doesn't have tgme_page_title
                is_real = "tgme_page_title" in content or "tgme_page_extra" in content or "tgme_page_action" in content
                results[url] = {"status": resp.status, "type": "telegram", "is_real": is_real}
        except Exception as ex:
            results[url] = {"status": "err", "type": "telegram_err", "msg": str(ex)}
        continue

    # For reddit, github, forums:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
            results[url] = {"status": resp.status, "type": "http_ok"}
    except urllib.error.HTTPError as e:
        results[url] = {"status": e.code, "type": "http_error", "msg": str(e)}
    except Exception as ex:
        results[url] = {"status": "err", "type": "exception", "msg": str(ex)}

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\url_verification_results.json", "w", encoding="utf-8") as out_f:
    json.dump(results, out_f, indent=2)

print(f"Checked {len(results)} URLs.")
