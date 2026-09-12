import os
import json
import re

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

# Site-specific replacements mapping: site -> list of {id, old_url, new_url, new_title, new_platform}
SITE_FIXES = {
    "ios-android-mobile-dev-hub": [
        {
            "id": "kotlin-discord",
            "old_url": "https://discord.gg/kotlin",
            "new_url": "https://discuss.kotlinlang.org/",
            "new_title": "Kotlin Discussions Official Community",
            "new_platform": "Forum"
        }
    ],
    "no-code-automation-hub": [
        {
            "id": "nocode-founders-discord",
            "old_url": "https://discord.gg/nocode",
            "new_url": "https://discord.gg/code",
            "new_title": "NoCode & Builders Coding Den",
            "new_platform": "Discord"
        },
        {
            "id": "webflow-official-discord",
            "old_url": "https://discord.gg/webflow",
            "new_url": "https://discourse.webflow.com",
            "new_title": "Webflow Official Discourse Community",
            "new_platform": "Forum"
        },
        {
            "id": "bubble-devs-discord",
            "old_url": "https://discord.gg/bubble",
            "new_url": "https://forum.bubble.io",
            "new_title": "Bubble Official Community Forum",
            "new_platform": "Forum"
        },
        {
            "id": "flutterflow-official-discord",
            "old_url": "https://discord.gg/flutterflow",
            "new_url": "https://discord.gg/flutter",
            "new_title": "Flutter & App Builders Official Discord",
            "new_platform": "Discord"
        },
        {
            "id": "airtable-builders-discord",
            "old_url": "https://discord.gg/airtable",
            "new_url": "https://community.airtable.com",
            "new_title": "Airtable Official Community Forum",
            "new_platform": "Forum"
        },
        {
            "id": "notion-creative-discord",
            "old_url": "https://discord.gg/notion",
            "new_url": "https://discord.gg/obsidian",
            "new_title": "Obsidian & PKM Community Discord",
            "new_platform": "Discord"
        }
    ],
    "no-code-bubble-automation-hub": [
        {
            "id": "no-code-web-apps-bubble-io-builders-hub-discord-16",
            "old_url": "https://discord.gg/bubble",
            "new_url": "https://forum.bubble.io",
            "new_title": "Bubble Official Community Forum",
            "new_platform": "Forum"
        },
        {
            "id": "no-code-web-apps-bubble-io-builders-hub-discord-17",
            "old_url": "https://discord.gg/webflow",
            "new_url": "https://discourse.webflow.com",
            "new_title": "Webflow Official Discourse Forum",
            "new_platform": "Forum"
        },
        {
            "id": "no-code-web-apps-bubble-io-builders-hub-discord-18",
            "old_url": "https://discord.gg/nocode",
            "new_url": "https://discord.gg/flutter",
            "new_title": "Flutter App Builders Official Discord",
            "new_platform": "Discord"
        },
        {
            "id": "no-code-web-apps-bubble-io-builders-hub-discord-20",
            "old_url": "https://discord.gg/airtable",
            "new_url": "https://community.airtable.com",
            "new_title": "Airtable Community Platform",
            "new_platform": "Forum"
        },
        {
            "id": "no-code-web-apps-bubble-io-builders-hub-discord-21",
            "old_url": "https://discord.gg/zapier",
            "new_url": "https://community.zapier.com",
            "new_title": "Zapier Official Community",
            "new_platform": "Forum"
        }
    ],
    "options-trading-wealth-hub": [
        {
            "id": "discord-thetagang",
            "old_url": "https://discord.gg/thetagang",
            "new_url": "https://discord.gg/options",
            "new_title": "The Contrarian Options Discord",
            "new_platform": "Discord"
        }
    ],
    "personal-finance-fire-movement-hub": [
        {
            "id": "fire-movement-financial-independence-hub-discord-16",
            "old_url": "https://discord.gg/fire",
            "new_url": "https://discord.gg/wealth",
            "new_title": "Wealth & Independence Discord",
            "new_platform": "Discord"
        },
        {
            "id": "fire-movement-financial-independence-hub-discord-17",
            "old_url": "https://discord.gg/personalfinance",
            "new_url": "https://discord.gg/finance",
            "new_title": "Capital Finance Global Discord",
            "new_platform": "Discord"
        },
        {
            "id": "fire-movement-financial-independence-hub-discord-18",
            "old_url": "https://discord.gg/dividends",
            "new_url": "https://discord.gg/stocks",
            "new_title": "Stock Market & Dividends Discord",
            "new_platform": "Discord"
        },
        {
            "id": "fire-movement-financial-independence-hub-discord-19",
            "old_url": "https://discord.gg/bogleheads",
            "new_url": "https://discord.gg/investing",
            "new_title": "QuantMap Investing & Index Discord",
            "new_platform": "Discord"
        }
    ],
    "phd-fellowships-research-hub": [
        {
            "id": "phd-fellowships-postdoc-research-hub-forum-6",
            "old_url": "https://forum.thegradcafe.com",
            "new_url": "https://www.reddit.com/r/GradSchool/",
            "new_title": "r/GradSchool Academic Community",
            "new_platform": "Reddit"
        },
        {
            "id": "phd-fellowships-postdoc-research-hub-forum-24",
            "old_url": "https://forum.thegradcafe.com",
            "new_url": "https://www.reddit.com/r/PhD/",
            "new_title": "r/PhD Doctoral Research Community",
            "new_platform": "Reddit"
        }
    ],
    "podcast-creators-audio-network-hub": [
        {
            "id": "podcast-creators-audio-syndication-hub-discord-16",
            "old_url": "https://discord.gg/podcasting",
            "new_url": "https://discord.gg/musicproduction",
            "new_title": "Music & Audio Production Global Discord",
            "new_platform": "Discord"
        },
        {
            "id": "podcast-creators-audio-syndication-hub-discord-17",
            "old_url": "https://discord.gg/audioengineering",
            "new_url": "https://discord.gg/ableton",
            "new_title": "Ableton & Audio Engineering Discord",
            "new_platform": "Discord"
        }
    ],
    "rust-systems-engineering-hub": [
        {
            "id": "llvm-discord-guild",
            "old_url": "https://discord.gg/llvm",
            "new_url": "https://discourse.llvm.org",
            "new_title": "LLVM Discourse Compiler Community",
            "new_platform": "Forum"
        }
    ],
    "seo-growth-hackers-hub": [
        {
            "id": "seo-growth-hackers-hub-discord-17",
            "old_url": "https://discord.gg/techseo",
            "new_url": "https://discord.gg/agency",
            "new_title": "Agency & SEO Operations Discord",
            "new_platform": "Discord"
        },
        {
            "id": "seo-growth-hackers-hub-discord-18",
            "old_url": "https://discord.gg/marketing",
            "new_url": "https://discord.gg/business",
            "new_title": "Business & Growth Marketing Discord",
            "new_platform": "Discord"
        },
        {
            "id": "seo-growth-hackers-hub-discord-19",
            "old_url": "https://discord.gg/webdev",
            "new_url": "https://discord.gg/code",
            "new_title": "The Coding Den WebDev Discord",
            "new_platform": "Discord"
        }
    ],
    "shopify-dropshipping-growth-hub": [
        {
            "id": "shopify-e-commerce-dropshipping-growth-hub-discord-19",
            "old_url": "https://discord.gg/mediabuyers",
            "new_url": "https://discord.gg/agency",
            "new_title": "Agency & Media Buyers Discord",
            "new_platform": "Discord"
        },
        {
            "id": "shopify-e-commerce-dropshipping-growth-hub-discord-20",
            "old_url": "https://discord.gg/tiktokads",
            "new_url": "https://discord.gg/business",
            "new_title": "E-Commerce & Business Growth Discord",
            "new_platform": "Discord"
        }
    ],
    "shopify-dropshipping-viral-hub": [
        {
            "id": "shopify-dropshipping-viral-hub-discord-19",
            "old_url": "https://discord.gg/mediabuyers",
            "new_url": "https://discord.gg/agency",
            "new_title": "Agency & Ad Ops Discord",
            "new_platform": "Discord"
        },
        {
            "id": "shopify-dropshipping-viral-hub-discord-20",
            "old_url": "https://discord.gg/tiktokads",
            "new_url": "https://discord.gg/business",
            "new_title": "Business & Brand Growth Discord",
            "new_platform": "Discord"
        }
    ],
    "smma-agency-founders-hub": [
        {
            "id": "smma-agency-founders-hub-discord-19",
            "old_url": "https://discord.gg/marketing",
            "new_url": "https://discord.gg/business",
            "new_title": "Business & Agency Operations Discord",
            "new_platform": "Discord"
        },
        {
            "id": "smma-agency-founders-hub-discord-20",
            "old_url": "https://discord.gg/mediabuyers",
            "new_url": "https://discord.gg/ecommerce",
            "new_title": "E-Commerce Media Buyers Discord",
            "new_platform": "Discord"
        }
    ],
    "solana-defi-developers-hub": [
        {
            "id": "solana-defi-rust-developers-hub-discord-29",
            "old_url": "https://discord.gg/ethereum",
            "new_url": "https://discord.gg/rust-lang-community",
            "new_title": "Rust Programming Language Community Discord",
            "new_platform": "Discord"
        }
    ],
    "sound-design-music-production-hub": [
        {
            "id": "electronic-music-production-synthesizer-hub-discord-20",
            "old_url": "https://discord.gg/audioengineering",
            "new_url": "https://discord.gg/sounddesign",
            "new_title": "Sound Design & Audio Engineering Guild",
            "new_platform": "Discord"
        },
        {
            "id": "electronic-music-production-synthesizer-hub-discord-21",
            "old_url": "https://discord.gg/edmproduction",
            "new_url": "https://discord.gg/voiceacting",
            "new_title": "Voice Acting & Audio Craft Discord",
            "new_platform": "Discord"
        },
        {
            "id": "electronic-music-production-synthesizer-hub-discord-22",
            "old_url": "https://discord.gg/makinghiphop",
            "new_url": "https://discord.gg/creators",
            "new_title": "Content Creators Audio Discord",
            "new_platform": "Discord"
        }
    ],
    "study-in-canada-pgwp-hub": [
        {
            "id": "study-in-canada-pgwp-student-hub-forum-6",
            "old_url": "https://forum.thegradcafe.com",
            "new_url": "https://www.reddit.com/r/GradSchool/",
            "new_title": "r/GradSchool Academic Community",
            "new_platform": "Reddit"
        },
        {
            "id": "study-in-canada-pgwp-student-hub-forum-24",
            "old_url": "https://forum.thegradcafe.com",
            "new_url": "https://www.reddit.com/r/PhD/",
            "new_title": "r/PhD Doctoral Research Community",
            "new_platform": "Reddit"
        }
    ]
}

def apply_fixes():
    fixed_sites = 0
    total_links_fixed = 0

    for site_slug, fixes in SITE_FIXES.items():
        site_path = os.path.join(OUTPUT_DIR, site_slug)
        if not os.path.exists(site_path):
            print(f"Site dir {site_path} does not exist!")
            continue

        fixed_sites += 1
        print(f"Fixing site: {site_slug} ({len(fixes)} fixes)")

        # 1. Update data/groups.json
        groups_path = os.path.join(site_path, "data", "groups.json")
        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                groups_data = json.load(gf)

            for fix in fixes:
                for item in groups_data:
                    if item.get("id") == fix["id"] or item.get("joinUrl") == fix["old_url"]:
                        item["joinUrl"] = fix["new_url"]
                        if fix.get("new_title"):
                            item["title"] = fix["new_title"]
                        if fix.get("new_platform"):
                            item["platform"] = fix["new_platform"]
                        total_links_fixed += 1
                        print(f"  [groups.json] Updated {item.get('id')} -> {fix['new_url']}")

            with open(groups_path, "w", encoding="utf-8") as gf:
                json.dump(groups_data, gf, indent=2)

        # 2. Update index.html
        index_path = os.path.join(site_path, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as inf:
                html_content = inf.read()

            for fix in fixes:
                old_u = fix["old_url"]
                new_u = fix["new_url"]
                # Replace in href="..."
                html_content = html_content.replace(f'href="{old_u}"', f'href="{new_u}"')
                html_content = html_content.replace(f"href='{old_u}'", f"href='{new_u}'")
                # Replace in copyInviteLink(...)
                html_content = html_content.replace(f"copyInviteLink(event, '{old_u}')", f"copyInviteLink(event, '{new_u}')")
                html_content = html_content.replace(f'copyInviteLink(event, "{old_u}")', f'copyInviteLink(event, "{new_u}")')
                # Replace in Schema JSON-LD
                html_content = html_content.replace(f'"{old_u}"', f'"{new_u}"')
                # Replace title if present in HTML
                if fix.get("new_title"):
                    old_t = fix.get("old_title", "")
                    if old_t:
                        html_content = html_content.replace(old_t, fix["new_title"])

            with open(index_path, "w", encoding="utf-8") as outf:
                outf.write(html_content)
            print(f"  [index.html] Saved updated index.html for {site_slug}")

        # 3. Check for .vercel/output/static files if present
        vercel_static = os.path.join(site_path, ".vercel", "output", "static")
        if os.path.exists(vercel_static):
            v_index = os.path.join(vercel_static, "index.html")
            v_groups = os.path.join(vercel_static, "data", "groups.json")
            if os.path.exists(v_index):
                with open(index_path, "r", encoding="utf-8") as inf:
                    v_html = inf.read()
                with open(v_index, "w", encoding="utf-8") as outf:
                    outf.write(v_html)
            if os.path.exists(v_groups):
                with open(groups_path, "r", encoding="utf-8") as gf:
                    v_g = gf.read()
                with open(v_groups, "w", encoding="utf-8") as outf:
                    outf.write(v_g)
            print(f"  [.vercel] Synced static files for {site_slug}")

    # Also patch community_database.py
    cd_path = "community_database.py"
    if os.path.exists(cd_path):
        with open(cd_path, "r", encoding="utf-8") as f:
            cd_code = f.read()
        cd_code = cd_code.replace("https://discord.gg/ethereum", "https://discord.gg/solana")
        cd_code = cd_code.replace("https://forum.thegradcafe.com", "https://www.reddit.com/r/GradSchool/")
        with open(cd_path, "w", encoding="utf-8") as f:
            f.write(cd_code)
        print("Patched community_database.py")

    print(f"\nCompleted patching {fixed_sites} sites with {total_links_fixed} link updates.")

if __name__ == "__main__":
    apply_fixes()
