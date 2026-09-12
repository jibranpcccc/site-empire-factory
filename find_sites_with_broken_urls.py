import os
import re

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

BROKEN_URLS = [
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
    "https://github.com/rust-lang/rust/discussions"
]

for s in SITES:
    p = os.path.join(OUTPUT_DIR, s, "index.html")
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    found = [u for u in BROKEN_URLS if u in content]
    print(f"{s}: found {len(found)} broken URLs: {found}")
