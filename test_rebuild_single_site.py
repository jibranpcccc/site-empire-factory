import os
import json
import factory
import community_database

output_dir = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
site_slug = "b2b-saas-founders-circle-hub"
site_path = os.path.join(output_dir, site_slug)

with open(os.path.join(factory.BASE_DIR, "niches.json"), "r", encoding="utf-8") as f:
    niches = json.load(f)

niche = next(n for n in niches if n["slug"] == site_slug)

# Get live_url from sitemap.xml
with open(os.path.join(site_path, "sitemap.xml"), "r", encoding="utf-8") as f:
    sitemap_text = f.read()

import re
m = re.search(r"<loc>(https?://[^<]+?/)</loc>", sitemap_text)
live_url = m.group(1)

# Generate fallback communities using community_database
communities = factory.generate_fallback_communities(niche["name"], niche.get("niche", ""))
print(f"Generated {len(communities)} communities for {site_slug}")
for c in communities[:3]:
    print(f"  {c['title']} ({c['platform']}) -> {c['joinUrl']}")

# Generate HTML
html = factory.build_html(niche, communities, live_url)
print(f"HTML length: {len(html)}")
assert "https://www.reddit.com/r/SaaS/" in html
assert "copyInviteLink" in html
assert "b2b-saas-founders-circle-hub.vercel.app/about.html" in html
print("Assertions passed for b2b-saas-founders-circle-hub!")
