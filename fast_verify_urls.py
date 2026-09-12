import json
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\unique_urls_to_verify.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def verify_single_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    # For discord.gg
    if "discord.gg" in domain:
        invite_code = parsed.path.strip("/")
        api_url = f"https://discord.com/api/v9/invites/{invite_code}"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": headers["User-Agent"]})
            with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
                data = json.loads(resp.read().decode())
                return url, {"status": resp.status, "type": "discord_valid", "guild": data.get("guild", {}).get("name", "Unknown")}
        except urllib.error.HTTPError as e:
            # 404 means invite code is invalid/expired!
            return url, {"status": e.code, "type": "discord_error", "msg": str(e)}
        except Exception as ex:
            return url, {"status": "timeout_or_err", "type": "discord_exception", "msg": str(ex)}

    # For telegram
    if "t.me" in domain:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                is_real = "tgme_page_title" in content or "tgme_page_extra" in content or "tgme_page_action" in content
                return url, {"status": resp.status, "type": "telegram", "is_real": is_real}
        except Exception as ex:
            return url, {"status": "err", "type": "telegram_err", "msg": str(ex)}

    # For reddit, github, forums
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            return url, {"status": resp.status, "type": "http_ok"}
    except urllib.error.HTTPError as e:
        return url, {"status": e.code, "type": "http_error", "msg": str(e)}
    except Exception as ex:
        return url, {"status": "err", "type": "exception", "msg": str(ex)}

results = {}
with ThreadPoolExecutor(max_workers=25) as executor:
    futures = {executor.submit(verify_single_url, u): u for u in urls}
    for future in as_completed(futures):
        u, res = future.result()
        results[u] = res

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\url_verification_results.json", "w", encoding="utf-8") as out_f:
    json.dump(results, out_f, indent=2)

print(f"Successfully checked all {len(results)} URLs!")

# Check for failures (status 404, etc.)
invalid = []
for u, r in results.items():
    st = r.get("status")
    if st == 404:
        invalid.append((u, r))
    elif r.get("type") == "telegram" and not r.get("is_real"):
        invalid.append((u, r))

print(f"Total definitely invalid/404 URLs: {len(invalid)}")
for u, r in invalid:
    print(f"  INVALID: {u} -> {r}")
