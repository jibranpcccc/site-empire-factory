import os
import re
import json
import factory

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

with open(os.path.join(factory.BASE_DIR, "niches.json"), "r", encoding="utf-8") as f:
    niches = json.load(f)

for s in sites:
    site_path = os.path.join(output_dir, s)
    niche = next(n for n in niches if n["slug"] == s)

    # Get live_url from sitemap.xml
    with open(os.path.join(site_path, "sitemap.xml"), "r", encoding="utf-8") as f:
        sitemap_text = f.read()
    m = re.search(r"<loc>(https?://[^<]+?/)</loc>", sitemap_text)
    live_url = m.group(1)

    # Generate 30 communities
    comms = factory.generate_fallback_communities(niche["name"], niche.get("niche", ""))
    assert len(comms) == 30, f"{s} generated {len(comms)} communities"

    # Save data/groups.json
    groups_path = os.path.join(site_path, "data", "groups.json")
    with open(groups_path, "w", encoding="utf-8") as f:
        json.dump(comms, f, indent=2)

    # Build and save index.html
    html = factory.build_html(niche, comms, live_url)
    index_path = os.path.join(site_path, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Successfully rebuilt {s}: 30 communities, index.html len={len(html)}")
