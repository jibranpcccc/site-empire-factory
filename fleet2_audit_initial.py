import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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

BANNED_PATTERNS = [
    "telegram.com/community",
    "discord.com/community",
    "whatsapp.com/community",
    "reddit.com/community",
    "vipflashloot_",
    "t.me/community",
    "discord.gg/community",
    "example.com",
    "placeholder",
    "{cid}",
    "test-community"
]

def scan():
    total_outbound = 0
    total_copy_links = 0
    total_card_links = 0
    all_unique_outbound = set()
    banned_in_sites = {}
    site_reports = {}

    for site in SITES:
        site_dir = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_dir, "index.html")
        groups_path = os.path.join(site_dir, "data", "groups.json")

        if not os.path.exists(index_path):
            print(f"ERROR: {site} missing index.html")
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # Find all <a> tags with outbound http/https links
        outbound_a = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                outbound_a.append(href)
                all_unique_outbound.add(href)

        # Find copyInviteLink calls
        copy_matches = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)
        for c in copy_matches:
            all_unique_outbound.add(c)

        # Card join links specifically
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_links = []
        for card in cards:
            btn = card.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_links.append(btn["href"])

        # Check banned in html, copy links, card links
        banned_found = []
        # Check raw html for banned substrings
        for b in BANNED_PATTERNS:
            if b in html.lower():
                banned_found.append((b, "in raw html"))

        for c in copy_matches:
            for b in BANNED_PATTERNS:
                if b in c.lower():
                    banned_found.append((b, f"in copy link: {c}"))

        for a in outbound_a:
            for b in BANNED_PATTERNS:
                if b in a.lower():
                    banned_found.append((b, f"in href: {a}"))

        # Check groups.json
        groups_links = []
        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                try:
                    gdata = json.load(gf)
                    for item in gdata:
                        u = item.get("joinUrl", "")
                        groups_links.append(u)
                        for b in BANNED_PATTERNS:
                            if b in u.lower():
                                banned_found.append((b, f"in groups.json: {u}"))
                except Exception as e:
                    print(f"Error reading groups.json for {site}: {e}")

        total_outbound += len(outbound_a)
        total_copy_links += len(copy_matches)
        total_card_links += len(card_links)

        site_reports[site] = {
            "outbound_a_count": len(outbound_a),
            "card_links_count": len(card_links),
            "copy_matches_count": len(copy_matches),
            "groups_links_count": len(groups_links),
            "banned_found": banned_found,
            "card_links": card_links,
            "copy_matches": copy_matches,
            "groups_links": groups_links
        }
        if banned_found:
            banned_in_sites[site] = banned_found

    print(f"=== INITIAL SCAN RESULTS FOR FLEET 2 (40 SITES) ===")
    print(f"Total Sites: {len(SITES)}")
    print(f"Total Outbound <a> links in index.html: {total_outbound}")
    print(f"Total Card Join links: {total_card_links}")
    print(f"Total copyInviteLink calls: {total_copy_links}")
    print(f"Total Unique Outbound URLs: {len(all_unique_outbound)}")
    print(f"Sites with Banned Placeholders: {len(banned_in_sites)}")

    for s, bans in banned_in_sites.items():
        print(f"  [BANNED] {s}: {len(bans)} occurrences")
        for b, loc in bans[:5]:
            print(f"    - {b} ({loc})")

    with open("fleet2_initial_report.json", "w", encoding="utf-8") as out:
        json.dump({
            "total_sites": len(SITES),
            "total_outbound_a": total_outbound,
            "total_card_links": total_card_links,
            "total_copy_links": total_copy_links,
            "total_unique_outbound": len(all_unique_outbound),
            "all_unique_urls": sorted(list(all_unique_outbound)),
            "banned_sites_count": len(banned_in_sites),
            "banned_details": banned_in_sites,
            "site_reports": site_reports
        }, out, indent=2)

if __name__ == "__main__":
    scan()
