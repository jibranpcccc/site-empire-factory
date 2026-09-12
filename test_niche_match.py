import json
import community_database

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\niches.json", "r", encoding="utf-8") as f:
    niches = json.load(f)

slugs = [
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

for idx, n in enumerate(niches, 1):
    if n.get("slug") in slugs:
        matched_cat = community_database.find_matching_category(n.get("name"), n.get("niche"))
        print(f"#{idx}: {n.get('slug')} -> matched: '{matched_cat}'")
