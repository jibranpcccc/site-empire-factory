import os
import re
import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs"
OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

SITES_CONFIG = [
    # 10 Root Hubs
    ("developer-coding-hub", os.path.join(ROOT_DIR, "developer-coding-hub"), "root"),
    ("deals-loot-coupons-hub", os.path.join(ROOT_DIR, "deals-loot-coupons-hub"), "root"),
    ("scholarships-study-abroad-hub", os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"), "root"),
    ("remote-work-nomad-hub", os.path.join(ROOT_DIR, "remote-work-nomad-hub"), "root"),
    ("ai-prompts-generative-hub", os.path.join(ROOT_DIR, "ai-prompts-generative-hub"), "root"),
    ("cybersecurity-infosec-hub", os.path.join(ROOT_DIR, "cybersecurity-infosec-hub"), "root"),
    ("devops-cloud-architect-hub", os.path.join(ROOT_DIR, "devops-cloud-architect-hub"), "root"),
    ("data-science-machine-learning-hub", os.path.join(ROOT_DIR, "data-science-machine-learning-hub"), "root"),
    ("indie-hackers-micro-saas-hub", os.path.join(ROOT_DIR, "indie-hackers-micro-saas-hub"), "root"),
    ("game-dev-indie-studios-hub", os.path.join(ROOT_DIR, "game-dev-indie-studios-hub"), "root"),
    # 30 Factory Output Hubs
    ("3d-blender-unreal-artists-hub", os.path.join(OUTPUT_DIR, "3d-blender-unreal-artists-hub"), "factory"),
    ("affiliate-marketing-masters-hub", os.path.join(OUTPUT_DIR, "affiliate-marketing-masters-hub"), "factory"),
    ("ai-agents-autonomous-systems-hub", os.path.join(OUTPUT_DIR, "ai-agents-autonomous-systems-hub"), "factory"),
    ("amazon-fba-private-label-hub", os.path.join(OUTPUT_DIR, "amazon-fba-private-label-hub"), "factory"),
    ("architecture-design-masters-hub", os.path.join(OUTPUT_DIR, "architecture-design-masters-hub"), "factory"),
    ("audiophile-high-fidelity-hub", os.path.join(OUTPUT_DIR, "audiophile-high-fidelity-hub"), "factory"),
    ("aviation-pilot-cadet-hub", os.path.join(OUTPUT_DIR, "aviation-pilot-cadet-hub"), "factory"),
    ("b2b-saas-founders-circle-hub", os.path.join(OUTPUT_DIR, "b2b-saas-founders-circle-hub"), "factory"),
    ("biohacking-longevity-health-hub", os.path.join(OUTPUT_DIR, "biohacking-longevity-health-hub"), "factory"),
    ("biohacking-longevity-protocols-hub", os.path.join(OUTPUT_DIR, "biohacking-longevity-protocols-hub"), "factory"),
    ("bug-bounty-pentesting-hub", os.path.join(OUTPUT_DIR, "bug-bounty-pentesting-hub"), "factory"),
    ("chess-grandmasters-study-hub", os.path.join(OUTPUT_DIR, "chess-grandmasters-study-hub"), "factory"),
    ("copywriting-high-ticket-hub", os.path.join(OUTPUT_DIR, "copywriting-high-ticket-hub"), "factory"),
    ("crypto-airdrop-testnets-hub", os.path.join(OUTPUT_DIR, "crypto-airdrop-testnets-hub"), "factory"),
    ("crypto-defi-yield-hub", os.path.join(OUTPUT_DIR, "crypto-defi-yield-hub"), "factory"),
    ("crypto-solana-memecoins-hub", os.path.join(OUTPUT_DIR, "crypto-solana-memecoins-hub"), "factory"),
    ("crypto-yield-farming-staking-hub", os.path.join(OUTPUT_DIR, "crypto-yield-farming-staking-hub"), "factory"),
    ("cyber-threat-intelligence-hub", os.path.join(OUTPUT_DIR, "cyber-threat-intelligence-hub"), "factory"),
    ("digital-products-notion-hub", os.path.join(OUTPUT_DIR, "digital-products-notion-hub"), "factory"),
    ("dividend-growth-investing-hub", os.path.join(OUTPUT_DIR, "dividend-growth-investing-hub"), "factory"),
    ("dnd-tabletop-campaigns-hub", os.path.join(OUTPUT_DIR, "dnd-tabletop-campaigns-hub"), "factory"),
    ("ecommerce-amazon-fba-hub", os.path.join(OUTPUT_DIR, "ecommerce-amazon-fba-hub"), "factory"),
    ("ethical-hacking-bugbounty-hub", os.path.join(OUTPUT_DIR, "ethical-hacking-bugbounty-hub"), "factory"),
    ("fire-personal-finance-hub", os.path.join(OUTPUT_DIR, "fire-personal-finance-hub"), "factory"),
    ("flutter-crossplatform-mobile-hub", os.path.join(OUTPUT_DIR, "flutter-crossplatform-mobile-hub"), "factory"),
    ("forex-scalping-signals-hub", os.path.join(OUTPUT_DIR, "forex-scalping-signals-hub"), "factory"),
    ("freelance-copywriters-guild-hub", os.path.join(OUTPUT_DIR, "freelance-copywriters-guild-hub"), "factory"),
    ("generative-ai-video-creators-hub", os.path.join(OUTPUT_DIR, "generative-ai-video-creators-hub"), "factory"),
    ("golang-microservices-distributed-hub", os.path.join(OUTPUT_DIR, "golang-microservices-distributed-hub"), "factory"),
    ("growth-marketing-hackers-hub", os.path.join(OUTPUT_DIR, "growth-marketing-hackers-hub"), "factory")
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
    "/placeholder",
    "{cid}",
    "test-community",
    "localhost"
]

KNOWN_BROKEN_URLS = [
    "https://discord.gg/theprogrammershangout",
    "https://discord.gg/kubernetes",
    "https://discord.gg/huggingface",
    "https://discord.gg/devops",
    "https://discord.gg/biggerpockets",
    "https://discord.gg/langchain",
    "https://discord.gg/proptrading",
    "https://discord.gg/technology",
    "https://github.com/pytorch/pytorch/discussions",
    "https://github.com/kubernetes/kubernetes/discussions",
    "https://github.com/rust-lang/rust/discussions",
    "https://research.ethdev.com",
    "https://discord.gg/dexscreener",
    "https://discord.gg/amazonsellers",
    "https://discord.gg/affiliatemarketing",
    "https://discord.gg/copywriting"
]

def step1_collect_all_site_data():
    fleet_data = {}
    total_outbound_links_index = 0
    total_copy_links_index = 0
    total_groups_links = 0
    all_unique_community_urls = set()
    banned_findings = []
    known_broken_findings = []

    for site_name, site_path, site_type in SITES_CONFIG:
        index_file = os.path.join(site_path, "index.html")
        groups_file = os.path.join(site_path, "data", "groups.json")

        if not os.path.exists(index_file):
            print(f"[!] MISSING index.html: {site_name}")
            continue

        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a> hrefs
        outbound_a = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                outbound_a.append(href)

        # 2. Card join links
        card_join_links = []
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        for card in cards:
            btn = card.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"].strip())

        # 3. copyInviteLink calls
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 4. Schema JSON-LD
        schema_links = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract(obj):
                    if isinstance(obj, dict):
                        if obj.get("@type") == "ListItem" and "url" in obj and isinstance(obj["url"], str) and obj["url"].startswith("http"):
                            schema_links.append(obj["url"].strip())
                        for v in obj.values():
                            extract(v)
                    elif isinstance(obj, list):
                        for it in obj:
                            extract(it)
                extract(data)
            except Exception:
                pass

        # 5. groups.json
        groups_links = []
        groups_raw = []
        if os.path.exists(groups_file):
            try:
                with open(groups_file, "r", encoding="utf-8") as gf:
                    groups_raw = json.load(gf)
                    for item in groups_raw:
                        u = item.get("joinUrl", "").strip()
                        if u:
                            groups_links.append(u)
            except Exception as e:
                print(f"[!] Error parsing {groups_file}: {e}")

        # Check banned in card_join_links, copy_links, schema_links, groups_links
        site_banned = []
        combined_comm_urls = set(card_join_links + copy_links + groups_links)
        for u in combined_comm_urls:
            u_low = u.lower()
            for b in BANNED_URL_SUBSTRINGS:
                if b in u_low:
                    site_banned.append({"url": u, "pattern": b})
                    banned_findings.append({"site": site_name, "url": u, "pattern": b})

        # Check known broken
        site_broken = []
        for u in combined_comm_urls:
            if u in KNOWN_BROKEN_URLS:
                site_broken.append(u)
                known_broken_findings.append({"site": site_name, "url": u})

        for u in combined_comm_urls:
            all_unique_community_urls.add(u)

        total_outbound_links_index += len(outbound_a)
        total_copy_links_index += len(copy_links)
        total_groups_links += len(groups_links)

        fleet_data[site_name] = {
            "path": site_path,
            "type": site_type,
            "cards_count": len(cards),
            "card_join_links_count": len(card_join_links),
            "card_join_links": card_join_links,
            "copy_links_count": len(copy_links),
            "copy_links": copy_links,
            "outbound_a_count": len(outbound_a),
            "schema_links_count": len(schema_links),
            "schema_links": schema_links,
            "groups_count": len(groups_links),
            "groups_links": groups_links,
            "banned": site_banned,
            "broken": site_broken
        }

    return {
        "fleet_data": fleet_data,
        "total_sites": len(SITES_CONFIG),
        "total_outbound_links_index": total_outbound_links_index,
        "total_copy_links_index": total_copy_links_index,
        "total_groups_links": total_groups_links,
        "unique_community_urls": sorted(list(all_unique_community_urls)),
        "banned_findings": banned_findings,
        "known_broken_findings": known_broken_findings
    }

if __name__ == "__main__":
    result = step1_collect_all_site_data()
    print("=" * 60)
    print("FLEET PART 1 (SITES 1-40) - STEP 1 AUDIT")
    print("=" * 60)
    print(f"Total Sites Audited: {result['total_sites']}")
    print(f"Total Outbound <a> Links in index.html: {result['total_outbound_links_index']}")
    print(f"Total copyInviteLink Calls in index.html: {result['total_copy_links_index']}")
    print(f"Total Groups in groups.json: {result['total_groups_links']}")
    print(f"Total Unique Community URLs: {len(result['unique_community_urls'])}")
    print(f"Total Banned Synthetic Placeholders Found: {len(result['banned_findings'])}")
    print(f"Total Known Broken URLs Found: {len(result['known_broken_findings'])}")

    if result['banned_findings']:
        print("\n[!] BANNED FINDINGS:")
        for b in result['banned_findings']:
            print(f"  [{b['site']}] {b['url']} (pattern: {b['pattern']})")

    if result['known_broken_findings']:
        print("\n[!] KNOWN BROKEN FINDINGS:")
        for b in result['known_broken_findings']:
            print(f"  [{b['site']}] {b['url']}")

    with open("fleet1_audit_data.json", "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2)
    print("\nSaved Step 1 data to fleet1_audit_data.json")
