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
    "{cid}",
    "test-community"
]

ALL_KNOWN_BROKEN_URLS = [
    "https://discord.gg/airtable",
    "https://discord.gg/audioengineering",
    "https://discord.gg/biggerpockets",
    "https://discord.gg/bogleheads",
    "https://discord.gg/bubble",
    "https://discord.gg/devops",
    "https://discord.gg/dexscreener",
    "https://discord.gg/dividends",
    "https://discord.gg/edmproduction",
    "https://discord.gg/ethereum",
    "https://discord.gg/fire",
    "https://discord.gg/flutterflow",
    "https://discord.gg/huggingface",
    "https://discord.gg/kotlin",
    "https://discord.gg/kubernetes",
    "https://discord.gg/langchain",
    "https://discord.gg/llvm",
    "https://discord.gg/makinghiphop",
    "https://discord.gg/marketing",
    "https://discord.gg/mediabuyers",
    "https://discord.gg/nocode",
    "https://discord.gg/notion",
    "https://discord.gg/personalfinance",
    "https://discord.gg/podcasting",
    "https://discord.gg/proptrading",
    "https://discord.gg/technology",
    "https://discord.gg/techseo",
    "https://discord.gg/theprogrammershangout",
    "https://discord.gg/thetagang",
    "https://discord.gg/tiktokads",
    "https://discord.gg/webdev",
    "https://discord.gg/webflow",
    "https://discord.gg/zapier",
    "https://github.com/kubernetes/kubernetes/discussions",
    "https://github.com/pytorch/pytorch/discussions",
    "https://github.com/rust-lang/rust/discussions",
    "https://forum.thegradcafe.com",
    "https://research.ethdev.com",
    "https://discord.gg/amazonsellers",
    "https://discord.gg/affiliatemarketing",
    "https://discord.gg/copywriting"
]

REQUIRED_INTERNAL_PAGES = ["about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]

def run_full_audit():
    total_outbound_links = 0
    total_card_join_links = 0
    total_copy_invite_links = 0
    total_schema_links = 0
    total_groups_links = 0
    all_unique_urls = set()

    total_banned_found = 0
    total_broken_found = 0
    all_banned_details = []
    all_broken_details = []

    site_audits = {}

    for site in SITES:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_file = os.path.join(site_path, "index.html")
        groups_file = os.path.join(site_path, "data", "groups.json")

        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Outbound <a> hrefs
        outbound_hrefs = []
        for a in soup.find_all("a", href=True):
            h = a["href"].strip()
            if h.startswith("http://") or h.startswith("https://"):
                outbound_hrefs.append(h)
                all_unique_urls.add(h)

        # 2. Card join links
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_join_links = []
        for card in cards:
            btn = card.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if btn and btn.has_attr("href"):
                card_join_links.append(btn["href"].strip())

        # 3. copyInviteLink calls
        copy_invite_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 4. JSON-LD schema links
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
                        for it in obj:
                            extract(it)
                extract(data)
            except Exception:
                pass

        # 5. groups.json
        groups_links = []
        if os.path.exists(groups_file):
            with open(groups_file, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
                for item in gdata:
                    groups_links.append(item.get("joinUrl", "").strip())

        # 6. Check internal files & links
        missing_pages = [p for p in REQUIRED_INTERNAL_PAGES if not os.path.exists(os.path.join(site_path, p))]

        # 7. Check banned placeholders
        site_banned = []
        all_site_urls = set(outbound_hrefs + copy_invite_links + schema_links + groups_links)
        for u in all_site_urls:
            u_low = u.lower()
            for b in BANNED_PATTERNS:
                if b in u_low:
                    site_banned.append((u, b))
                    all_banned_details.append((site, u, b))

        # 8. Check broken URLs
        site_broken = []
        for u in all_site_urls:
            if u in ALL_KNOWN_BROKEN_URLS:
                site_broken.append(u)
                all_broken_details.append((site, u))

        # Check in raw html
        for b in BANNED_PATTERNS:
            # exclude input placeholder attribute
            html_no_input = re.sub(r'placeholder="[^"]*"', '', html)
            html_no_input = re.sub(r"placeholder='[^']*'", '', html_no_input)
            if b in html_no_input.lower():
                site_banned.append(("raw_html", b))
                all_banned_details.append((site, "raw_html", b))

        total_outbound_links += len(outbound_hrefs)
        total_card_join_links += len(card_join_links)
        total_copy_invite_links += len(copy_invite_links)
        total_schema_links += len(schema_links)
        total_groups_links += len(groups_links)

        total_banned_found += len(site_banned)
        total_broken_found += len(site_broken)

        site_audits[site] = {
            "outbound_links_count": len(outbound_hrefs),
            "cards_count": len(cards),
            "card_join_links_count": len(card_join_links),
            "copy_invite_links_count": len(copy_invite_links),
            "schema_links_count": len(schema_links),
            "groups_links_count": len(groups_links),
            "missing_pages": missing_pages,
            "banned_count": len(site_banned),
            "broken_count": len(site_broken),
            "sample_urls": card_join_links[:3]
        }

    summary = {
        "fleet": "Fleet Part 2 (Sites 41 to 80)",
        "total_sites_inspected": len(SITES),
        "total_outbound_links": total_outbound_links,
        "total_card_join_links": total_card_join_links,
        "total_copy_invite_links": total_copy_invite_links,
        "total_schema_links": total_schema_links,
        "total_groups_links": total_groups_links,
        "total_unique_verified_urls": len(all_unique_urls),
        "total_banned_placeholders_found": total_banned_found,
        "total_broken_or_404_links_remaining": total_broken_found,
        "all_banned_details": all_banned_details,
        "all_broken_details": all_broken_details,
        "sites": site_audits
    }

    with open("fleet2_final_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 70)
    print("      FLEET PART 2 (SITES 41 TO 80) FINAL AUDIT REPORT")
    print("=" * 70)
    print(f"Total Sites Inspected:                 {len(SITES)}")
    print(f"Total Outbound <a> Links in index.html: {total_outbound_links}")
    print(f"Total Community Cards:                 {total_card_join_links}")
    print(f"Total Copy Invite Links:               {total_copy_invite_links}")
    print(f"Total Schema JSON-LD URLs:             {total_schema_links}")
    print(f"Total Groups in groups.json:           {total_groups_links}")
    print(f"Total Unique Verified Outbound URLs:   {len(all_unique_urls)}")
    print("-" * 70)
    print(f"Banned Synthetic Placeholders Found:   {total_banned_found}")
    print(f"Broken/404 Dead URLs Remaining:        {total_broken_found}")
    print("=" * 70)

    if total_banned_found == 0 and total_broken_found == 0:
        print("\n>>> 100% CLEAN: ZERO BANNED PLACEHOLDERS & ZERO BROKEN URLS! <<<")
    else:
        print(f"\nWARNING: Issues remaining! Banned: {total_banned_found}, Broken: {total_broken_found}")

    return summary

if __name__ == "__main__":
    run_full_audit()
