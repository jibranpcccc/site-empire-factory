import os
import json
import urllib.request
from urllib.parse import urlparse

INDEXNOW_KEY = "4a123bc89fe04b56ad781290cde456fa"

TODAY_SITES = [
    "https://jibranpcccc.github.io/crypto-yield-farming-staking-hub/",
    "https://jibranpcccc.github.io/no-code-bubble-automation-hub/",
    "https://golang-microservices-distributed-hub.netlify.app/",
    "https://jibranpcccc.github.io/growth-marketing-hackers-hub/",
    "https://jibranpcccc.github.io/ui-ux-design-systems-hub/",
    "https://sound-design-music-production-hub.netlify.app/",
    "https://jibranpcccc.github.io/amazon-fba-private-label-hub/",
    "https://jibranpcccc.github.io/personal-finance-fire-movement-hub/",
    "https://jibranpcccc.github.io/virtual-assistants-agency-hub/",
    "https://jibranpcccc.github.io/podcast-creators-audio-network-hub/"
]

PAGES = ["", "about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]

print("=== BROADCASTING INDEXNOW FOR TODAY'S 10 SITES (60 URLS) ===")

total_urls = 0
results = []

for site_url in TODAY_SITES:
    domain = urlparse(site_url).netloc
    url_list = [f"{site_url.rstrip('/')}/{p}".rstrip('/') for p in PAGES]
    # Root URL must have trailing slash
    url_list[0] = site_url.rstrip('/') + '/'
    total_urls += len(url_list)

    payload = {
        "host": domain,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{site_url.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }
    data = json.dumps(payload).encode("utf-8")

    # 1. api.indexnow.org
    status1 = "ERR"
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Antigravity-IndexNow/2.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            status1 = f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        status1 = f"HTTP {e.code}"
    except Exception as e:
        status1 = f"ERR: {str(e)[:30]}"

    # 2. www.bing.com/indexnow
    status2 = "ERR"
    try:
        req2 = urllib.request.Request(
            "https://www.bing.com/indexnow",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Antigravity-IndexNow/2.0"}
        )
        with urllib.request.urlopen(req2, timeout=10) as resp:
            status2 = f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        status2 = f"HTTP {e.code}"
    except Exception as e:
        status2 = f"ERR: {str(e)[:30]}"

    # 3. Google WebSub Ping for feed.xml
    rss_url = f"{site_url.rstrip('/')}/feed.xml"
    websub_status = "ERR"
    try:
        websub_data = f"hub.mode=publish&hub.url={urllib.parse.quote(rss_url)}".encode("utf-8")
        ws_req = urllib.request.Request(
            "https://pubsubhubbub.appspot.com/",
            data=websub_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(ws_req, timeout=10) as ws_resp:
            websub_status = f"HTTP {ws_resp.status}"
    except urllib.error.HTTPError as e:
        websub_status = f"HTTP {e.code}"
    except Exception as e:
        websub_status = f"ERR: {str(e)[:30]}"

    print(f"{domain} (6 URLs) -> IndexNow: {status1} | Bing: {status2} | WebSub: {websub_status}")
    results.append({
        "domain": domain,
        "urls": len(url_list),
        "indexnow": status1,
        "bing": status2,
        "websub": websub_status
    })

print(f"\nAll {total_urls} URLs submitted across {len(TODAY_SITES)} sites.")
