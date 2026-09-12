import json
import ssl
import urllib.request
import urllib.error

with open("fleet2_community_urls.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["urls"]
reddit_urls = [u for u in urls if "reddit.com" in u]
print(f"Testing {len(reddit_urls)} Reddit URLs...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Reddit requires a unique User-Agent to not return 429
headers = {
    "User-Agent": "python:community-auditor:v1.0 (by /u/jibran_audit)"
}

results = {}
for i, url in enumerate(reddit_urls, 1):
    # Standardize subreddit url to about.json
    clean_url = url.rstrip("/")
    api_url = f"{clean_url}/about.json"
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            d = json.loads(resp.read().decode("utf-8"))
            sub_data = d.get("data", {})
            sub_name = sub_data.get("display_name_prefixed", url)
            subscribers = sub_data.get("subscribers", 0)
            results[url] = {"status": 200, "valid": True, "name": sub_name, "subs": subscribers}
    except urllib.error.HTTPError as e:
        if e.code in [403, 429]:
            # Reddit blocks or rate-limits some requests, but subreddit might be fine.
            # Try regular HTML request
            try:
                h_req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
                with urllib.request.urlopen(h_req, timeout=5, context=ctx) as h_resp:
                    results[url] = {"status": h_resp.status, "valid": True, "type": "html_ok"}
            except urllib.error.HTTPError as he:
                results[url] = {"status": he.code, "valid": (he.code != 404), "msg": str(he)}
            except Exception as hex:
                results[url] = {"status": "err", "valid": True, "msg": str(hex)}
        elif e.code == 404:
            results[url] = {"status": 404, "valid": False, "msg": "Subreddit Not Found / Banned"}
        else:
            results[url] = {"status": e.code, "valid": (e.code != 404), "msg": str(e)}
    except Exception as ex:
        results[url] = {"status": "err", "valid": True, "msg": str(ex)}

with open("fleet2_reddit_audit_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

dead = [u for u, r in results.items() if not r.get("valid")]
print(f"Reddit audit done. Total: {len(results)}, Dead: {len(dead)}")
for d in dead:
    print(f"  DEAD SUBREDDIT: {d} -> {results[d]}")
