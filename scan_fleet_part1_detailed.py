import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ROOT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs"
OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

ROOT_HUBS = [
    "developer-coding-hub",
    "deals-loot-coupons-hub",
    "scholarships-study-abroad-hub",
    "remote-work-nomad-hub",
    "ai-prompts-generative-hub",
    "cybersecurity-infosec-hub",
    "devops-cloud-architect-hub",
    "data-science-machine-learning-hub",
    "indie-hackers-micro-saas-hub",
    "game-dev-indie-studios-hub"
]

OUTPUT_HUBS = [
    "3d-blender-unreal-artists-hub",
    "affiliate-marketing-masters-hub",
    "ai-agents-autonomous-systems-hub",
    "amazon-fba-private-label-hub",
    "architecture-design-masters-hub",
    "audiophile-high-fidelity-hub",
    "aviation-pilot-cadet-hub",
    "b2b-saas-founders-circle-hub",
    "biohacking-longevity-health-hub",
    "biohacking-longevity-protocols-hub",
    "bug-bounty-pentesting-hub",
    "chess-grandmasters-study-hub",
    "copywriting-high-ticket-hub",
    "crypto-airdrop-testnets-hub",
    "crypto-defi-yield-hub",
    "crypto-solana-memecoins-hub",
    "crypto-yield-farming-staking-hub",
    "cyber-threat-intelligence-hub",
    "digital-products-notion-hub",
    "dividend-growth-investing-hub",
    "dnd-tabletop-campaigns-hub",
    "ecommerce-amazon-fba-hub",
    "ethical-hacking-bugbounty-hub",
    "fire-personal-finance-hub",
    "flutter-crossplatform-mobile-hub",
    "forex-scalping-signals-hub",
    "freelance-copywriters-guild-hub",
    "generative-ai-video-creators-hub",
    "golang-microservices-distributed-hub",
    "growth-marketing-hackers-hub"
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

KNOWN_BROKEN = [
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

def main():
    sites = []
    for h in ROOT_HUBS:
        sites.append((os.path.join(ROOT_DIR, h), h, "root"))
    for h in OUTPUT_HUBS:
        sites.append((os.path.join(OUTPUT_DIR, h), h, "factory"))

    all_banned_urls = []
    all_broken_urls = []
    site_reports = {}
    all_unique_urls = set()

    for site_path, site_name, s_type in sites:
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a>
        a_hrefs = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                a_hrefs.append(href)
                all_unique_urls.add(href)

        # 2. copyInviteLink
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)
        for cl in copy_links:
            all_unique_urls.add(cl)

        # 3. schema
        schema_links = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract(obj):
                    if isinstance(obj, dict):
                        if "url" in obj and isinstance(obj["url"], str) and obj["url"].startswith("http"):
                            schema_links.append(obj["url"])
                            all_unique_urls.add(obj["url"])
                        for v in obj.values():
                            extract(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract(item)
                extract(data)
            except Exception:
                pass

        # 4. groups.json
        groups_links = []
        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
                for g in gdata:
                    u = g.get("joinUrl", "").strip()
                    if u:
                        groups_links.append(u)
                        all_unique_urls.add(u)

        # Community cards
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_join_links = []
        for c in cards:
            btn = c.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"].strip())

        # Scan for banned patterns in URLs
        site_banned = []
        site_urls = set(a_hrefs + copy_links + schema_links + groups_links)
        for u in site_urls:
            u_low = u.lower()
            for b in BANNED_PATTERNS:
                if b in u_low:
                    site_banned.append({"url": u, "pattern": b})
                    all_banned_urls.append({"site": site_name, "url": u, "pattern": b})

        # Scan for known broken URLs
        site_broken = []
        for u in site_urls:
            if u in KNOWN_BROKEN:
                site_broken.append(u)
                all_broken_urls.append({"site": site_name, "url": u})

        site_reports[site_name] = {
            "type": s_type,
            "cards_count": len(cards),
            "card_join_links": len(card_join_links),
            "copy_links": len(copy_links),
            "a_hrefs": len(a_hrefs),
            "schema_links": len(schema_links),
            "groups_links": len(groups_links),
            "banned": site_banned,
            "broken": site_broken
        }

    print("=" * 60)
    print("DETAILED SCAN OF FLEET PART 1 (40 SITES)")
    print("=" * 60)
    print(f"Total Unique URLs checked across all 40 sites: {len(all_unique_urls)}")
    print(f"Total Banned URLs found: {len(all_banned_urls)}")
    print(f"Total Known Broken URLs found: {len(all_broken_urls)}")

    if all_banned_urls:
        print("\n--- BANNED URLS FOUND ---")
        for b in all_banned_urls:
            print(f"[{b['site']}] URL: {b['url']} (pattern: {b['pattern']})")
    else:
        print("\n[OK] Zero banned synthetic placeholders in URLs!")

    if all_broken_urls:
        print("\n--- BROKEN URLS FOUND ---")
        broken_by_site = {}
        for b in all_broken_urls:
            broken_by_site.setdefault(b["site"], []).append(b["url"])
        for site, urls in broken_by_site.items():
            print(f"[{site}] ({len(urls)} broken):")
            for u in set(urls):
                print(f"   -> {u}")

    with open("fleet_part1_detailed_scan.json", "w", encoding="utf-8") as out:
        json.dump({
            "banned_urls": all_banned_urls,
            "broken_urls": all_broken_urls,
            "site_reports": site_reports,
            "all_unique_urls": list(sorted(all_unique_urls))
        }, out, indent=2)

if __name__ == "__main__":
    main()
