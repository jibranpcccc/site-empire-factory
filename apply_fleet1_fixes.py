import os
import re
import json
from bs4 import BeautifulSoup

ROOT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs"
OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

FIXES = [
    {
        "site": "devops-cloud-architect-hub",
        "path": os.path.join(ROOT_DIR, "devops-cloud-architect-hub"),
        "old_url": "https://discord.gg/ansible",
        "new_url": "https://www.reddit.com/r/ansible/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/ansible Automation & Infrastructure",
        "card_id": "community-card-20",
        "group_id": "devops-cloud-architect-hub-discord-20"
    },
    {
        "site": "deals-loot-coupons-hub",
        "path": os.path.join(ROOT_DIR, "deals-loot-coupons-hub"),
        "old_url": "https://discord.gg/awardtravel",
        "new_url": "https://www.reddit.com/r/awardtravel/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/awardtravel Points & Flight Guild",
        "card_id": "community-card-52",
        "group_id": "points-miles-flight-guild"
    },
    {
        "site": "deals-loot-coupons-hub",
        "path": os.path.join(ROOT_DIR, "deals-loot-coupons-hub"),
        "old_url": "https://discord.gg/buildapcsales",
        "new_url": "https://www.reddit.com/r/buildapcsales/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/buildapcsales Hardware Deals Radar",
        "card_id": "community-card-28",
        "group_id": "buildapcsales-discord-server"
    },
    {
        "site": "deals-loot-coupons-hub",
        "path": os.path.join(ROOT_DIR, "deals-loot-coupons-hub"),
        "old_url": "https://t.me/wholefoodsperks",
        "new_url": "https://www.reddit.com/r/coupons/",
        "old_platform": "Telegram",
        "new_platform": "Reddit",
        "new_title": "r/coupons Verified Grocery & Food Savings",
        "card_id": "community-card-36",
        "group_id": "whole-foods-prime-perks"
    },
    {
        "site": "fire-personal-finance-hub",
        "path": os.path.join(OUTPUT_DIR, "fire-personal-finance-hub"),
        "old_url": "https://discord.gg/bogleheads",
        "new_url": "https://www.reddit.com/r/Bogleheads/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/Bogleheads Passive Indexing Guild",
        "card_id": "community-card-23",
        "group_id": "fire-discord-bogleheads"
    },
    {
        "site": "indie-hackers-micro-saas-hub",
        "path": os.path.join(ROOT_DIR, "indie-hackers-micro-saas-hub"),
        "old_url": "https://discord.gg/buildinpublic",
        "new_url": "https://www.reddit.com/r/buildinpublic/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/buildinpublic Creator Collective",
        "card_id": "community-card-16",
        "group_id": "build-in-public-discord-16"
    },
    {
        "site": "golang-microservices-distributed-hub",
        "path": os.path.join(OUTPUT_DIR, "golang-microservices-distributed-hub"),
        "old_url": "https://discord.gg/confluent",
        "new_url": "https://www.reddit.com/r/apachekafka/",
        "old_platform": "Discord",
        "new_platform": "Reddit",
        "new_title": "r/apachekafka Distributed Streaming Guild",
        "card_id": "community-card-21",
        "group_id": "go-microservices-distributed-architecture-hub-discord-21"
    },
    {
        "site": "developer-coding-hub",
        "path": os.path.join(ROOT_DIR, "developer-coding-hub"),
        "old_url": "https://communityinviter.com/apps/cloud-native/cncf",
        "new_url": "https://community.cncf.io/",
        "old_platform": "Discord",
        "new_platform": "Official Community",
        "new_title": "CNCF Official Community Hub",
        "card_id": "community-card-17",
        "group_id": "cncf-community"
    },
    {
        "site": "growth-marketing-hackers-hub",
        "path": os.path.join(OUTPUT_DIR, "growth-marketing-hackers-hub"),
        "old_url": "https://growthhackers.com/posts",
        "new_url": "https://growthhackers.com/",
        "old_platform": "Forum",
        "new_platform": "Forum",
        "new_title": "GrowthHackers Community Forum",
        "card_id": "community-card-26",
        "group_id": "growth-marketing-programmatic-seo-hub-forum-26"
    },
    {
        "site": "scholarships-study-abroad-hub",
        "path": os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"),
        "old_url": "https://careers.cern/students",
        "new_url": "https://careers.cern/early-career",
        "old_platform": "Official Portal",
        "new_platform": "Official Portal",
        "new_title": "CERN Doctoral & Technical Student Fellowship",
        "card_id": "community-card-36",
        "group_id": "cern-doctoral-technical-student-programme"
    },
    {
        "site": "scholarships-study-abroad-hub",
        "path": os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"),
        "old_url": "https://investyourtalent.esteri.it/en/",
        "new_url": "https://studyinitaly.esteri.it/",
        "old_platform": "Official Portal",
        "new_platform": "Official Portal",
        "new_title": "Invest Your Talent in Italy (MAECI-ICE)",
        "card_id": "community-card-32",
        "group_id": "invest-your-talent-italy"
    },
    {
        "site": "scholarships-study-abroad-hub",
        "path": os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"),
        "old_url": "https://www.moe.gov.tw/elitescholars",
        "new_url": "https://taiwanscholarship.moe.gov.tw/",
        "old_platform": "Official Portal",
        "new_platform": "Official Portal",
        "new_title": "Taiwanese Ministry of Education Elite Scholars Program",
        "card_id": "community-card-31",
        "group_id": "taiwan-moe-elite-scholars"
    },
    {
        "site": "scholarships-study-abroad-hub",
        "path": os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"),
        "old_url": "https://www.a-star.edu.sg/Scholarships/for-graduate-studies/singapore-international-graduate-award-singa",
        "new_url": "https://www.a-star.edu.sg/scholarships",
        "old_platform": "Official Portal",
        "new_platform": "Official Portal",
        "new_title": "Singapore International Graduate Award (SINGA)",
        "card_id": "community-card-15",
        "group_id": "singapore-international-graduate-award"
    }
]

def apply_all_fixes():
    fixed_count = 0

    for fix in FIXES:
        site_path = fix["path"]
        site_name = fix["site"]
        old_url = fix["old_url"]
        new_url = fix["new_url"]
        new_platform = fix["new_platform"]
        new_title = fix["new_title"]

        idx_file = os.path.join(site_path, "index.html")
        grp_file = os.path.join(site_path, "data", "groups.json")

        # 1. Update data/groups.json
        if os.path.exists(grp_file):
            with open(grp_file, "r", encoding="utf-8") as f:
                groups_data = json.load(f)

            grp_updated = False
            for item in groups_data:
                if item.get("joinUrl") == old_url or item.get("id") == fix["group_id"]:
                    item["joinUrl"] = new_url
                    if new_platform:
                        item["platform"] = new_platform
                    if new_title and "title" in item:
                        item["title"] = new_title
                    grp_updated = True

            if grp_updated:
                with open(grp_file, "w", encoding="utf-8") as f:
                    json.dump(groups_data, f, indent=2)
                print(f"[OK] Updated groups.json for {site_name}: {old_url} -> {new_url}")

        # 2. Update index.html
        if os.path.exists(idx_file):
            with open(idx_file, "r", encoding="utf-8") as f:
                html = f.read()

            old_count = html.count(old_url)
            if old_count > 0:
                html = html.replace(old_url, new_url)

                # If platform changed, update card platform badge and data-platform
                if fix["old_platform"] != new_platform and fix["card_id"]:
                    # Update data-platform
                    html = re.sub(
                        rf'(id="{fix["card_id"]}"[^>]*data-platform=")[^"]+(")',
                        rf'\g<1>{new_platform.lower()}\g<2>',
                        html
                    )
                    html = re.sub(
                        rf'(data-platform=")[^"]+("[^>]*id="{fix["card_id"]}")',
                        rf'\g<1>{new_platform.lower()}\g<2>',
                        html
                    )
                    # Update badge inside card
                    # We can use regex on card section
                    card_pattern = rf'(<div[^>]*id="{fix["card_id"]}".*?</div>\s*</div>)'
                    card_match = re.search(card_pattern, html, re.DOTALL)
                    if card_match:
                        card_html = card_match.group(1)
                        updated_card_html = card_html.replace(
                            f'<span class="badge badge-platform">{fix["old_platform"]}</span>',
                            f'<span class="badge badge-platform">{new_platform}</span>'
                        )
                        if new_title:
                            updated_card_html = re.sub(
                                r'<h3 class="card-title">.*?</h3>',
                                f'<h3 class="card-title">{new_title}</h3>',
                                updated_card_html
                            )
                        html = html.replace(card_html, updated_card_html)

                with open(idx_file, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"[OK] Updated index.html for {site_name}: replaced {old_count} occurrences of {old_url}")
                fixed_count += 1

    print(f"\nCompleted applying fixes across {fixed_count} sites.")

if __name__ == "__main__":
    apply_all_fixes()
