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

def scan_fleet():
    sites = []
    for h in ROOT_HUBS:
        sites.append((os.path.join(ROOT_DIR, h), h, "root"))
    for h in OUTPUT_HUBS:
        sites.append((os.path.join(OUTPUT_DIR, h), h, "factory"))

    report = {
        "total_sites": len(sites),
        "total_outbound_links_index": 0,
        "total_copy_links_index": 0,
        "total_groups_links": 0,
        "unique_external_urls": set(),
        "banned_matches": [],
        "broken_matches": [],
        "site_summaries": []
    }

    for site_path, site_name, s_type in sites:
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        if not os.path.exists(index_path):
            print(f"[!] Missing index.html: {site_name}")
            continue

        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a> hrefs
        outbound_hrefs = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                outbound_hrefs.append(href)
                report["unique_external_urls"].add(href)

        # 2. copyInviteLink calls
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)
        for cl in copy_links:
            report["unique_external_urls"].add(cl)

        # 3. groups.json
        groups_links = []
        if os.path.exists(groups_path):
            try:
                with open(groups_path, "r", encoding="utf-8") as gf:
                    gdata = json.load(gf)
                    for g in gdata:
                        u = g.get("joinUrl", "").strip()
                        if u:
                            groups_links.append(u)
                            report["unique_external_urls"].add(u)
            except Exception as e:
                print(f"[!] Error parsing {groups_path}: {e}")

        # Check banned in index.html raw text and links
        site_banned = []
        all_site_urls = set(outbound_hrefs + copy_links + groups_links)
        for u in all_site_urls:
            u_low = u.lower()
            for b in BANNED_PATTERNS:
                if b in u_low:
                    site_banned.append({"site": site_name, "url": u, "pattern": b})

        # Also search raw html for banned patterns directly
        html_low = html.lower()
        for b in BANNED_PATTERNS:
            if b in html_low:
                # Find occurrences
                matches = [m.start() for m in re.finditer(re.escape(b), html_low)]
                if matches and not any(sb["pattern"] == b for sb in site_banned):
                    site_banned.append({"site": site_name, "url": f"RAW_HTML_MATCH:{b}", "pattern": b})

        # Check known broken
        site_broken = []
        for u in all_site_urls:
            if u in KNOWN_BROKEN:
                site_broken.append({"site": site_name, "url": u, "reason": "Known 404/expired"})

        report["total_outbound_links_index"] += len(outbound_hrefs)
        report["total_copy_links_index"] += len(copy_links)
        report["total_groups_links"] += len(groups_links)
        report["banned_matches"].extend(site_banned)
        report["broken_matches"].extend(site_broken)

        report["site_summaries"].append({
            "site": site_name,
            "type": s_type,
            "outbound_hrefs": len(outbound_hrefs),
            "copy_links": len(copy_links),
            "groups_links": len(groups_links),
            "banned_count": len(site_banned),
            "broken_count": len(site_broken),
            "banned_items": site_banned,
            "broken_items": site_broken
        })

    report["unique_external_urls_count"] = len(report["unique_external_urls"])
    report["unique_external_urls"] = list(sorted(report["unique_external_urls"]))

    return report

if __name__ == "__main__":
    rep = scan_fleet()
    print("=" * 60)
    print("FLEET PART 1 (SITES 1-40) INITIAL SCAN RESULTS")
    print("=" * 60)
    print(f"Total sites scanned: {rep['total_sites']}")
    print(f"Total outbound hrefs in index.html: {rep['total_outbound_links_index']}")
    print(f"Total copyInviteLink calls in index.html: {rep['total_copy_links_index']}")
    print(f"Total groups in groups.json: {rep['total_groups_links']}")
    print(f"Total unique external URLs discovered: {rep['unique_external_urls_count']}")
    print(f"BANNED synthetic placeholders found: {len(rep['banned_matches'])}")
    print(f"BROKEN/expired URLs found: {len(rep['broken_matches'])}")
    print("-" * 60)

    if rep['banned_matches']:
        print("\n[!] BANNED PLACEHOLDERS DETECTED:")
        for bm in rep['banned_matches']:
            print(f"  Site: {bm['site']} | URL: {bm['url']} | Matched: {bm['pattern']}")

    if rep['broken_matches']:
        print("\n[!] BROKEN URLS DETECTED:")
        for bm in rep['broken_matches']:
            print(f"  Site: {bm['site']} | URL: {bm['url']}")

    with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_part1_initial_scan.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)
    print("\nSaved scan details to fleet_part1_initial_scan.json")
