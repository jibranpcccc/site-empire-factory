import os
import re

output_dir = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
sites = [
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

for s in sites:
    sm = os.path.join(output_dir, s, "sitemap.xml")
    with open(sm, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"<loc>(https?://[^<]+?/)</loc>", content)
    url = m.group(1) if m else "none"
    print(f"{s} -> {url}")
