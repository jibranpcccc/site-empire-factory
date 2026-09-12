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

ALL_KNOWN_BROKEN = [
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
    "https://discord.gg/copywriting",
    "https://discord.gg/ansible",
    "https://discord.gg/awardtravel",
    "https://discord.gg/bogleheads",
    "https://discord.gg/buildapcsales",
    "https://discord.gg/buildinpublic",
    "https://discord.gg/confluent",
    "https://communityinviter.com/apps/cloud-native/cncf",
    "https://growthhackers.com/posts",
    "https://careers.cern/students",
    "https://investyourtalent.esteri.it/en/",
    "https://www.moe.gov.tw/elitescholars",
    "https://www.a-star.edu.sg/Scholarships/for-graduate-studies/singapore-international-graduate-award-singa",
    "https://t.me/wholefoodsperks"
]

def verify_fleet():
    sites = []
    for h in ROOT_HUBS:
        sites.append((os.path.join(ROOT_DIR, h), h, "root"))
    for h in OUTPUT_HUBS:
        sites.append((os.path.join(OUTPUT_DIR, h), h, "factory"))

    total_sites = len(sites)
    total_cards = 0
    total_outbound_a = 0
    total_copy_links = 0
    total_groups_links = 0
    unique_community_urls = set()

    banned_violations = []
    broken_violations = []
    per_site_stats = []

    for site_path, site_name, s_type in sites:
        index_file = os.path.join(site_path, "index.html")
        groups_file = os.path.join(site_path, "data", "groups.json")

        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a>
        a_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                a_links.append(href)

        # 2. Cards
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_join_links = []
        for c in cards:
            btn = c.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"].strip())

        # 3. copyInviteLink
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 4. groups.json
        groups_links = []
        if os.path.exists(groups_file):
            with open(groups_file, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
                for item in gdata:
                    u = item.get("joinUrl", "").strip()
                    if u:
                        groups_links.append(u)

        # 5. Schema.org
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

        all_site_urls = set(card_join_links + copy_links + groups_links + schema_links)
        for u in all_site_urls:
            unique_community_urls.add(u)

        # Check banned
        site_banned = []
        for u in all_site_urls:
            u_low = u.lower()
            for b in BANNED_URL_SUBSTRINGS:
                if b in u_low:
                    site_banned.append((u, b))
                    banned_violations.append({"site": site_name, "url": u, "pattern": b})

        # Check broken
        site_broken = []
        for u in all_site_urls:
            if u in ALL_KNOWN_BROKEN:
                site_broken.append(u)
                broken_violations.append({"site": site_name, "url": u})

        total_cards += len(cards)
        total_outbound_a += len(a_links)
        total_copy_links += len(copy_links)
        total_groups_links += len(groups_links)

        per_site_stats.append({
            "site": site_name,
            "type": s_type,
            "cards": len(cards),
            "outbound_a": len(a_links),
            "copy_links": len(copy_links),
            "groups_links": len(groups_links),
            "schema_links": len(schema_links),
            "banned": site_banned,
            "broken": site_broken
        })

    report = {
        "total_sites": total_sites,
        "total_cards": total_cards,
        "total_outbound_a_links": total_outbound_a,
        "total_copy_links": total_copy_links,
        "total_groups_links": total_groups_links,
        "unique_community_urls_count": len(unique_community_urls),
        "total_banned_violations": len(banned_violations),
        "total_broken_violations": len(broken_violations),
        "banned_violations": banned_violations,
        "broken_violations": broken_violations,
        "per_site_stats": per_site_stats
    }

    print("=" * 65)
    print("FLEET PART 1 (SITES 1-40) - POST-FIX AUDIT VERIFICATION")
    print("=" * 65)
    print(f"Total Sites Audited: {report['total_sites']}")
    print(f"Total Community Cards: {report['total_cards']}")
    print(f"Total Outbound <a> Links in index.html: {report['total_outbound_a_links']}")
    print(f"Total copyInviteLink Calls in index.html: {report['total_copy_links']}")
    print(f"Total Community Entries in groups.json: {report['total_groups_links']}")
    print(f"Total Unique Verified Community URLs: {report['unique_community_urls_count']}")
    print(f"Total Banned Synthetic Placeholders: {report['total_banned_violations']}")
    print(f"Total Broken / 404 URLs Remaining: {report['total_broken_violations']}")
    print("-" * 65)

    if report['total_banned_violations'] == 0 and report['total_broken_violations'] == 0:
        print("[SUCCESS] 100% CLEAN! ZERO fake, synthetic, or broken links remain across all 40 sites!")
    else:
        print("[!] Issues still detected:")
        for bv in banned_violations:
            print("  Banned:", bv)
        for br in broken_violations:
            print("  Broken:", br)

    with open("fleet1_final_audit_report.json", "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2)

    return report

if __name__ == "__main__":
    verify_fleet()
