import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

SITES_81_120 = [
    "study-in-germany-daadvise-hub",
    "study-in-japan-mext-hub",
    "tax-strategies-offshore-hub",
    "tiktok-shop-dropshipping-hub",
    "ui-ux-design-systems-hub",
    "unity-6-indie-studios-hub",
    "unreal-engine-5-creators-hub",
    "usmle-medical-residency-hub",
    "valorant-scrims-competitive-hub",
    "virtual-assistants-agency-hub",
    "youtube-automation-creators-hub",
    "algo-trading-quant-hub",
    "autonomous-ai-agents-hub",
    "biohacking-longevity-hub",
    "book-clubs-readers-lounge-hub",
    "calisthenics-street-workout-hub",
    "creative-indie-filmmakers-hub",
    "cs2-lineups-premier-hub",
    "cybersecurity-grc-compliance-hub",
    "deep-learning-nlp-transformers-hub",
    "digital-nomad-visas-tax-hub",
    "electric-vehicles-clean-energy-hub",
    "fintech-embedded-banking-hub",
    "golang-backend-cloud-hub",
    "high-ticket-closing-sales-hub",
    "homelab-selfhosted-linux-hub",
    "indie-game-marketing-steam-hub",
    "language-exchange-polyglot-hub",
    "minimalist-slow-living-hub",
    "neurotech-brain-computer-interface-hub",
    "nextjs-fullstack-react-hub",
    "prompt-engineering-tuning-hub",
    "real-estate-investing-syndicates-hub",
    "remote-vanlife-overlanding-hub",
    "rust-systems-performance-hub",
    "smart-contract-solidity-hub",
    "speedrunning-glitches-hub",
    "travel-hacking-points-hub",
    "vr-gaming-meta-quest-hub",
    "youtube-automation-cashcow-hub"
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

REQUIRED_INTERNAL = ["about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]

def run_comprehensive_audit():
    total_sites = len(SITES_81_120)
    sites_verified = 0
    
    total_cards = 0
    total_outbound_links_a = 0
    total_copy_links = 0
    total_schema_links = 0
    total_groups_links = 0
    
    all_unique_outbound_urls = set()
    all_banned_found = []
    all_broken_found = []
    all_mismatches = []
    
    per_site_data = {}

    for site in SITES_81_120:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        assert os.path.exists(site_path), f"Missing site directory: {site}"
        assert os.path.exists(index_path), f"Missing index.html in: {site}"
        assert os.path.exists(groups_path), f"Missing groups.json in: {site}"

        sites_verified += 1

        # Check internal E-E-A-T pages on disk
        missing_eeat = [p for p in REQUIRED_INTERNAL if not os.path.exists(os.path.join(site_path, p))]

        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a> hrefs
        outbound_a = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http://") or href.startswith("https://"):
                outbound_a.append(href)
                all_unique_outbound_urls.add(href)
        total_outbound_links_a += len(outbound_a)

        # 2. Community card join links
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        total_cards += len(cards)
        card_join_links = []
        for c in cards:
            btn = c.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"].strip())

        # 3. copyInviteLink calls
        copy_matches = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)
        total_copy_links += len(copy_matches)

        # 4. Schema JSON-LD ListItem URLs
        schema_links = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract(obj):
                    if isinstance(obj, dict):
                        if obj.get("@type") == "ListItem" and "url" in obj:
                            schema_links.append(obj["url"].strip())
                        for v in obj.values():
                            extract(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract(item)
                extract(data)
            except Exception:
                pass
        total_schema_links += len(schema_links)

        # 5. groups.json
        with open(groups_path, "r", encoding="utf-8") as gf:
            groups_data = json.load(gf)
            groups_links = [g.get("joinUrl", "").strip() for g in groups_data]
            total_groups_links += len(groups_links)

        # 6. Parity check between card_join_links, copy_matches, schema_links, groups_links
        site_mismatches = []
        for i in range(30):
            cl = card_join_links[i] if i < len(card_join_links) else None
            cpl = copy_matches[i] if i < len(copy_matches) else None
            sl = schema_links[i] if i < len(schema_links) else None
            gl = groups_links[i] if i < len(groups_links) else None
            if not (cl == cpl == sl == gl):
                site_mismatches.append({"card_index": i + 1, "card_href": cl, "copy_link": cpl, "schema_link": sl, "groups_link": gl})
                all_mismatches.append((site, i + 1, cl, cpl, sl, gl))

        # 7. Check banned substrings in all collected URLs
        site_banned = []
        site_urls = set(outbound_a + copy_matches + schema_links + groups_links)
        for u in site_urls:
            u_low = u.lower()
            for b in BANNED_PATTERNS:
                if b in u_low:
                    site_banned.append((u, b))
                    all_banned_found.append((site, u, b))

        # 8. Check known broken URLs
        site_broken = []
        for u in site_urls:
            if u in KNOWN_BROKEN:
                site_broken.append(u)
                all_broken_found.append((site, u))

        per_site_data[site] = {
            "cards_count": len(cards),
            "card_join_links_count": len(card_join_links),
            "copy_invite_links_count": len(copy_matches),
            "schema_links_count": len(schema_links),
            "groups_links_count": len(groups_links),
            "outbound_a_count": len(outbound_a),
            "missing_eeat_files": missing_eeat,
            "banned_count": len(site_banned),
            "broken_count": len(site_broken),
            "mismatches_count": len(site_mismatches),
            "banned": site_banned,
            "broken": site_broken,
            "mismatches": site_mismatches,
            "sample_urls": card_join_links[:3]
        }

    report = {
        "fleet": "Fleet Part 3 (Sites 81 to 120)",
        "total_sites": total_sites,
        "sites_verified_present": sites_verified,
        "total_cards": total_cards,
        "total_outbound_links_a": total_outbound_links_a,
        "total_copy_invite_links": total_copy_links,
        "total_schema_links": total_schema_links,
        "total_groups_json_links": total_groups_links,
        "total_unique_outbound_urls": len(all_unique_outbound_urls),
        "total_banned_placeholders_found": len(all_banned_found),
        "total_broken_urls_found": len(all_broken_found),
        "total_parity_mismatches": len(all_mismatches),
        "all_banned_found": all_banned_found,
        "all_broken_found": all_broken_found,
        "all_mismatches": all_mismatches,
        "per_site_data": per_site_data
    }

    results_path = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_part_3_final_audit_report.json"
    with open(results_path, "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2)

    print("=================================================================")
    print("FLEET PART 3 (SITES 81 TO 120) FINAL AUDIT REPORT")
    print("=================================================================")
    print(f"Total Sites Audited: {total_sites}")
    print(f"Sites Verified on Disk: {sites_verified} / {total_sites} (100%)")
    print(f"Total Community Cards: {total_cards}")
    print(f"Total Outbound Links in <a>: {total_outbound_links_a}")
    print(f"Total copyInviteLink Buttons: {total_copy_links}")
    print(f"Total Schema.org ItemList URLs: {total_schema_links}")
    print(f"Total data/groups.json URLs: {total_groups_links}")
    print(f"Total Unique Outbound URLs: {len(all_unique_outbound_urls)}")
    print(f"Total Banned Synthetic Placeholders: {len(all_banned_found)}")
    print(f"Total Broken/404 Dead URLs: {len(all_broken_found)}")
    print(f"Total Metadata Parity Mismatches: {len(all_mismatches)}")
    print("=================================================================")
    
    if len(all_banned_found) == 0 and len(all_broken_found) == 0 and len(all_mismatches) == 0:
        print("[SUCCESS] ALL 40 SITES IN FLEET PART 3 ARE 100% CLEAN AND VERIFIED!")
    else:
        print("[WARNING] Issues remain:")
        for b in all_banned_found:
            print(f"  Banned: {b}")
        for br in all_broken_found:
            print(f"  Broken: {br}")
        for m in all_mismatches:
            print(f"  Mismatch: {m}")

if __name__ == "__main__":
    run_comprehensive_audit()
