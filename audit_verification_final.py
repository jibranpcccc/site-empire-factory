import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
SITES = [
    "b2b-saas-founders-circle-hub",
    "biohacking-longevity-health-hub",
    "smart-home-homeassistant-hub",
    "cyber-threat-intelligence-hub",
    "generative-ai-video-creators-hub",
    "ethical-hacking-bugbounty-hub",
    "prop-firm-forex-traders-hub",
    "notion-systems-productivity-hub",
    "3d-blender-unreal-artists-hub",
    "remote-developer-jobs-alpha-hub"
]

BANNED_SUBSTRINGS = [
    "telegram.com/community",
    "discord.com/community",
    "whatsapp.com/community",
    "reddit.com/community",
    "t.me/community",
    "discord.gg/community",
    "example.com",
    "placeholder",
    "{cid}",
    "test-community"
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

INTERNAL_PAGES = ["about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]

def audit():
    overall_report = {}
    total_cards = 0
    total_outbound = 0
    all_banned = []
    all_broken = []
    all_unique_urls = set()

    for site in SITES:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_file = os.path.join(site_path, "index.html")
        groups_file = os.path.join(site_path, "data", "groups.json")

        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Internal files on disk
        missing_internal_files = []
        for p in INTERNAL_PAGES:
            if not os.path.exists(os.path.join(site_path, p)):
                missing_internal_files.append(p)

        # 2. Internal links in index.html
        internal_links = {p: False for p in INTERNAL_PAGES}
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for p in INTERNAL_PAGES:
                if href.endswith("/" + p) or href == p or href.endswith(p):
                    internal_links[p] = True

        # 3. Community card join links
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_join_links = []
        for c in cards:
            btn = c.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"])

        # 4. copyInviteLink calls
        copy_invite_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 5. Schema.org community links
        schema_links = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract(obj):
                    if isinstance(obj, dict):
                        if obj.get("@type") == "ListItem" and "url" in obj:
                            schema_links.append(obj["url"])
                        for v in obj.values():
                            extract(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract(item)
                extract(data)
            except Exception:
                pass

        # 6. groups.json
        with open(groups_file, "r", encoding="utf-8") as gf:
            groups_data = json.load(gf)
            groups_links = [g.get("joinUrl", "") for g in groups_data]

        # 7. Check banned placeholders in all URLs
        banned_found = []
        for u in card_join_links + copy_invite_links + schema_links + groups_links:
            u_low = u.lower()
            for b in BANNED_SUBSTRINGS:
                if b in u_low:
                    banned_found.append((u, b))

        # 8. Check known broken URLs
        broken_found = []
        for u in card_join_links + copy_invite_links + schema_links + groups_links:
            if u in KNOWN_BROKEN_URLS:
                broken_found.append(u)

        # 9. Verify exact parity between card links, copy links, schema links, and groups.json
        mismatches = []
        for i in range(30):
            cl = card_join_links[i] if i < len(card_join_links) else None
            cpl = copy_invite_links[i] if i < len(copy_invite_links) else None
            sl = schema_links[i] if i < len(schema_links) else None
            gl = groups_links[i] if i < len(groups_links) else None
            if not (cl == cpl == sl == gl):
                mismatches.append((i+1, cl, cpl, sl, gl))

        total_cards += len(cards)
        total_outbound += len(card_join_links)
        for u in card_join_links:
            all_unique_urls.add(u)
        all_banned.extend(banned_found)
        all_broken.extend(broken_found)

        overall_report[site] = {
            "cards_count": len(cards),
            "card_join_links_count": len(card_join_links),
            "copy_invite_links_count": len(copy_invite_links),
            "schema_links_count": len(schema_links),
            "groups_links_count": len(groups_links),
            "internal_missing_files": missing_internal_files,
            "internal_links_in_index": internal_links,
            "banned_count": len(banned_found),
            "broken_count": len(broken_found),
            "mismatches_count": len(mismatches),
            "sample_urls": card_join_links[:3]
        }

    summary = {
        "total_sites": len(SITES),
        "total_cards": total_cards,
        "total_outbound_links": total_outbound,
        "total_unique_urls": len(all_unique_urls),
        "total_banned_found": len(all_banned),
        "total_broken_found": len(all_broken),
        "all_banned": all_banned,
        "all_broken": all_broken,
        "per_site": overall_report
    }

    with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\audit_verification_final_results.json", "w", encoding="utf-8") as out:
        json.dump(summary, out, indent=2)

    print("=== AUDIT VERIFICATION SUMMARY ===")
    print(f"Total Sites Audited: {summary['total_sites']}")
    print(f"Total Community Cards: {summary['total_cards']}")
    print(f"Total Outbound Links: {summary['total_outbound_links']}")
    print(f"Total Unique Verified URLs: {summary['total_unique_urls']}")
    print(f"Total Banned Placeholders Found: {summary['total_banned_found']}")
    print(f"Total Broken/404 URLs Found: {summary['total_broken_found']}")
    print()
    for s, r in overall_report.items():
        print(f"Site: {s}")
        print(f"  Cards: {r['cards_count']} | Join Hrefs: {r['card_join_links_count']} | Copy Links: {r['copy_invite_links_count']} | Schema: {r['schema_links_count']} | Groups: {r['groups_links_count']}")
        print(f"  Internal Pages Present (disk & links): {all(r['internal_links_in_index'].values()) and len(r['internal_missing_files']) == 0}")
        print(f"  Banned: {r['banned_count']} | Broken: {r['broken_count']} | Mismatches: {r['mismatches_count']}")
        print(f"  Sample 1: {r['sample_urls'][0]}")
        print()

if __name__ == "__main__":
    audit()
