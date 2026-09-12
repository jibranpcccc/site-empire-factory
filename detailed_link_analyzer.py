import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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

BANNED_SUBSTRINGS = [
    "telegram.com/community",
    "discord.com/community",
    "whatsapp.com/community",
    "reddit.com/community",
    "t.me/community",
    "discord.gg/community",
    "example.com",
    "placeholder",
    "{cid}",
    "test-community"
]

INTERNAL_PAGES = ["about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]

def analyze_sites():
    all_site_data = {}
    total_outbound_links = 0
    all_unique_urls = set()

    for site in SITES:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # 1. Internal files on disk
        missing_files = []
        for p in INTERNAL_PAGES:
            if not os.path.exists(os.path.join(site_path, p)):
                missing_files.append(p)

        # 2. Internal links in index.html
        internal_links_found = {p: False for p in INTERNAL_PAGES}
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for p in INTERNAL_PAGES:
                if href.endswith("/" + p) or href == p or href.endswith(p):
                    internal_links_found[p] = True

        # 3. Community card links (<a> tag)
        cards = soup.find_all("div", class_=lambda c: c and "card" in c.split())
        card_links = []
        for c in cards:
            join_btn = c.find("a", class_=lambda cl: cl and "btn-join" in cl.split())
            if join_btn and join_btn.has_attr("href"):
                card_links.append(join_btn["href"])
            else:
                # check any external link in card
                ext_a = [a["href"] for a in c.find_all("a", href=True) if a["href"].startswith("http")]
                if ext_a:
                    card_links.append(ext_a[0])

        # 4. copyInviteLink calls
        copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

        # 5. Schema.org community links
        schema_urls = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string)
                def extract(obj):
                    if isinstance(obj, dict):
                        if obj.get("@type") == "ListItem" and "url" in obj:
                            schema_urls.append(obj["url"])
                        for v in obj.values():
                            extract(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            extract(item)
                extract(data)
            except Exception:
                pass

        # 6. groups.json URLs
        groups_urls = []
        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                gdata = json.load(gf)
                groups_urls = [g.get("joinUrl", "") for g in gdata]

        # Check banned in card_links, copy_links, schema_urls, groups_urls
        banned_found = []
        for u in card_links + copy_links + schema_urls + groups_urls:
            u_low = u.lower()
            for b in BANNED_SUBSTRINGS:
                if b in u_low:
                    banned_found.append((u, b))

        # Check matching between card_links and copy_links
        mismatches = []
        for i, (cl, cpl) in enumerate(zip(card_links, copy_links)):
            if cl != cpl:
                mismatches.append((i+1, cl, cpl))

        all_site_data[site] = {
            "missing_files": missing_files,
            "internal_links_found": internal_links_found,
            "cards_count": len(cards),
            "card_links_count": len(card_links),
            "copy_links_count": len(copy_links),
            "schema_urls_count": len(schema_urls),
            "groups_urls_count": len(groups_urls),
            "banned_found": banned_found,
            "mismatches": mismatches,
            "card_links": card_links,
            "copy_links": copy_links
        }

        for u in card_links:
            all_unique_urls.add(u)

    print(json.dumps({
        s: {
            "cards": all_site_data[s]["cards_count"],
            "card_links": all_site_data[s]["card_links_count"],
            "copy_links": all_site_data[s]["copy_links_count"],
            "schema_urls": all_site_data[s]["schema_urls_count"],
            "groups_urls": all_site_data[s]["groups_urls_count"],
            "banned": all_site_data[s]["banned_found"],
            "missing_internal": all_site_data[s]["missing_files"],
            "internal_links": all_site_data[s]["internal_links_found"],
            "mismatches": all_site_data[s]["mismatches"]
        } for s in SITES
    }, indent=2))

    print(f"\nTotal unique community URLs across 10 sites: {len(all_unique_urls)}")
    
    # Write unique URLs to a file so we can inspect and test them
    with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\unique_urls_to_verify.json", "w", encoding="utf-8") as uf:
        json.dump(sorted(list(all_unique_urls)), uf, indent=2)

if __name__ == "__main__":
    analyze_sites()
