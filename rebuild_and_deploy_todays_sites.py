import os
import json
import re
import subprocess
import urllib.request
import factory
import community_database

FACTORY_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory"
OUTPUT_DIR = os.path.join(FACTORY_DIR, "output")

TODAY_SITES = [
    "crypto-yield-farming-staking-hub",
    "no-code-bubble-automation-hub",
    "golang-microservices-distributed-hub",
    "growth-marketing-hackers-hub",
    "ui-ux-design-systems-hub",
    "sound-design-music-production-hub",
    "amazon-fba-private-label-hub",
    "personal-finance-fire-movement-hub",
    "virtual-assistants-agency-hub",
    "podcast-creators-audio-network-hub"
]

with open(os.path.join(FACTORY_DIR, "niches.json"), "r", encoding="utf-8") as f:
    niches = json.load(f)

print("=== STARTING REBUILD & DEPLOY OF TODAY'S 10 SITES ===")

for slug in TODAY_SITES:
    site_path = os.path.join(OUTPUT_DIR, slug)
    niche = next(n for n in niches if n["slug"] == slug)
    live_url = niche.get("live_url")

    # Read live_url from sitemap.xml if not in niche
    if not live_url and os.path.exists(os.path.join(site_path, "sitemap.xml")):
        with open(os.path.join(site_path, "sitemap.xml"), "r", encoding="utf-8") as sm_f:
            m = re.search(r"<loc>(https?://[^<]+?/)</loc>", sm_f.read())
            if m:
                live_url = m.group(1)

    print(f"\nRebuilding {slug} -> {live_url}...")

    # 1. Generate 30 precision communities
    communities = factory.generate_fallback_communities(niche["name"], niche.get("niche", ""))
    print(f"  Generated {len(communities)} communities. Top: {communities[0]['title']} ({communities[0]['platform']}) -> {communities[0]['joinUrl']}")

    # Save data/groups.json
    groups_path = os.path.join(site_path, "data", "groups.json")
    os.makedirs(os.path.dirname(groups_path), exist_ok=True)
    with open(groups_path, "w", encoding="utf-8") as gf:
        json.dump(communities, gf, indent=2)

    # 2. Build and save index.html
    html = factory.build_html(niche, communities, live_url)
    index_path = os.path.join(site_path, "index.html")
    with open(index_path, "w", encoding="utf-8") as hf:
        hf.write(html)
    print(f"  Wrote index.html (length: {len(html)})")

    # 3. Ensure .nojekyll exists
    nojekyll_path = os.path.join(site_path, ".nojekyll")
    if not os.path.exists(nojekyll_path):
        with open(nojekyll_path, "w", encoding="utf-8") as njf:
            njf.write("")
        print("  Created .nojekyll")

    # 4. Commit and Push to Git
    subprocess.run(["git", "add", "index.html", "data/groups.json", ".nojekyll"], cwd=site_path, check=True)
    commit_res = subprocess.run(
        ["git", "commit", "-m", "fix(seo): rebuild with precision verified niche communities and .nojekyll"],
        cwd=site_path, capture_output=True, text=True
    )
    if commit_res.stdout.strip():
        print(f"  Git commit: {commit_res.stdout.strip()[:90]}")
    else:
        print("  Git commit: clean (no changes)")

    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=site_path, capture_output=True, text=True)
    push_out = push_res.stdout.strip() or push_res.stderr.strip()
    print(f"  Git push: {push_out[:90] if push_out else 'OK'}")

    # If Netlify hosting, deploy
    if niche.get("hosting_platform") == "netlify" or "netlify.app" in (live_url or ""):
        print("  Deploying to Netlify...")
        deploy_res = subprocess.run(["netlify.cmd", "deploy", "--prod", "--dir", ".", "--no-build"], cwd=site_path, capture_output=True, text=True, shell=True)
        print(f"  Netlify deploy output: {deploy_res.stdout.strip()[:100]}")

print("\n=== ALL 10 SITES REBUILT AND COMMITTED ===")
