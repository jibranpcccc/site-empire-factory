import os
import re
import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
SITES = [
    "gta-rp-whitelist-servers-hub",
    "high-yield-treasury-wealth-hub",
    "ielts-toefl-band8-hub",
    "ios-android-mobile-dev-hub",
    "kubernetes-cloud-native-hub",
    "law-school-bar-exam-hub",
    "mechanical-keyboards-custom-hub",
    "microsaas-bootstrappers-hub",
    "minecraft-smp-builders-hub",
    "nextjs-react-fullstack-hub",
    "no-code-automation-hub",
    "no-code-bubble-automation-hub",
    "notion-systems-productivity-hub",
    "notion-templates-productivity-hub",
    "nursing-nclex-international-hub",
    "options-trading-wealth-hub",
    "personal-finance-fire-movement-hub",
    "phd-fellowships-research-hub",
    "podcast-creators-audio-network-hub",
    "podcasting-creator-economy-hub",
    "postgresql-high-scale-db-hub",
    "prompt-engineering-mastery-hub",
    "prop-firm-forex-traders-hub",
    "prop-trading-challenge-hub",
    "real-estate-wholesaling-hub",
    "remote-developer-jobs-alpha-hub",
    "remote-tech-careers-salary-hub",
    "retro-emulation-handhelds-hub",
    "rust-systems-engineering-hub",
    "saas-marketing-b2b-hub",
    "seo-growth-hackers-hub",
    "shopify-dropshipping-growth-hub",
    "shopify-dropshipping-viral-hub",
    "sim-racing-rigs-f1-hub",
    "smart-home-homeassistant-hub",
    "smma-agency-founders-hub",
    "solana-defi-developers-hub",
    "sound-design-music-production-hub",
    "stoicism-ancient-philosophy-hub",
    "study-in-canada-pgwp-hub"
]

BANNED_URL_SUBSTRINGS = [
    "telegram.com/community",
    "discord.com/community",
    "whatsapp.com/community",
    "reddit.com/community",
    "vipflashloot_",
    "t.me/community",
    "discord.gg/community",
    "example.com",
    "{cid}",
    "test-community",
    "/placeholder"
]

def collect_all_data():
    site_data = {}
    all_community_urls = set()
    all_outbound_links_total = 0
    all_copy_links_total = 0
    banned_hits = []

    for site in SITES:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_file = os.path.join(site_path, "index.html")
        groups_file = os.path.join(site_path, "data", "groups.json")

        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a> tags
        outbound_a = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                outbound_a.append(href)

        # 2. Card join links
        card_links = []
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        for card in cards:
            btn = card.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_links.append(btn["href"].strip())

        # 3. copyInviteLink calls
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 4. JSON-LD links
        schema_links = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract_schema(obj):
                    if isinstance(obj, dict):
                        if obj.get("@type") == "ListItem" and "url" in obj:
                            schema_links.append(obj["url"].strip())
                        for v in obj.values():
                            extract_schema(v)
                    elif isinstance(obj, list):
                        for it in obj:
                            extract_schema(it)
                extract_schema(data)
            except Exception:
                pass

        # 5. groups.json
        groups_links = []
        if os.path.exists(groups_file):
            with open(groups_file, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
                for item in gdata:
                    groups_links.append(item.get("joinUrl", "").strip())

        # Check banned in card_links, copy_links, schema_links, groups_links
        site_banned = []
        for u in set(card_links + copy_links + schema_links + groups_links):
            u_low = u.lower()
            for b in BANNED_URL_SUBSTRINGS:
                if b in u_low:
                    site_banned.append((u, b))
                    banned_hits.append((site, u, b))

        for u in card_links + copy_links + groups_links:
            if u:
                all_community_urls.add(u)

        all_outbound_links_total += len(outbound_a)
        all_copy_links_total += len(copy_links)

        site_data[site] = {
            "card_links": card_links,
            "copy_links": copy_links,
            "schema_links": schema_links,
            "groups_links": groups_links,
            "outbound_a_count": len(outbound_a),
            "card_links_count": len(card_links),
            "copy_links_count": len(copy_links),
            "banned": site_banned
        }

    return site_data, sorted(list(all_community_urls)), all_outbound_links_total, all_copy_links_total, banned_hits

if __name__ == "__main__":
    site_data, all_urls, total_outbound, total_copy, banned_hits = collect_all_data()
    print(f"Collected data for {len(site_data)} sites.")
    print(f"Total Outbound <a> links across all 40 sites: {total_outbound}")
    print(f"Total Copy Invite calls across all 40 sites: {total_copy}")
    print(f"Total Unique Community URLs: {len(all_urls)}")
    print(f"Total Banned Hits: {len(banned_hits)}")
    for bh in banned_hits:
        print(f"  BANNED: {bh}")

    with open("fleet2_community_urls.json", "w", encoding="utf-8") as f:
        json.dump({
            "urls": all_urls,
            "banned_hits": banned_hits,
            "site_data": site_data
        }, f, indent=2)
