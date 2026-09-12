import os
import json

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

for s in SITES:
    gp = os.path.join(OUTPUT_DIR, s, "data", "groups.json")
    with open(gp, "r", encoding="utf-8") as f:
        groups = json.load(f)
    print(f"=== {s} (count={len(groups)}) ===")
    for idx, g in enumerate(groups, 1):
        print(f"  {idx:2d}. {g['title']} [{g['platform']}] -> {g['joinUrl']}")
    print()
