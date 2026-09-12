import os
import json

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
with open("replacements_verified.json", "r", encoding="utf-8") as f:
    replacements = json.load(f)

sites_with_broken = [
    "ios-android-mobile-dev-hub",
    "no-code-automation-hub",
    "no-code-bubble-automation-hub",
    "options-trading-wealth-hub",
    "personal-finance-fire-movement-hub",
    "phd-fellowships-research-hub",
    "podcast-creators-audio-network-hub",
    "rust-systems-engineering-hub",
    "seo-growth-hackers-hub",
    "shopify-dropshipping-growth-hub",
    "shopify-dropshipping-viral-hub",
    "smma-agency-founders-hub",
    "solana-defi-developers-hub",
    "sound-design-music-production-hub",
    "study-in-canada-pgwp-hub"
]

for s in sites_with_broken:
    gp = os.path.join(OUTPUT_DIR, s, "data", "groups.json")
    if os.path.exists(gp):
        with open(gp, "r", encoding="utf-8") as gf:
            groups = json.load(gf)
        broken = [g for g in groups if g.get("joinUrl") in replacements]
        print(f"=== {s} ({len(broken)} broken) ===")
        for b in broken:
            old_url = b.get("joinUrl")
            new_info = replacements.get(old_url, {})
            print(f"  ID: {b.get('id')}")
            print(f"  Title: {b.get('title')}")
            print(f"  Platform: {b.get('platform')}")
            print(f"  Old URL: {old_url}")
            print(f"  New URL: {new_info.get('new')}")
            print()
