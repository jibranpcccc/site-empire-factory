import os
import re
import json
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

BANNED_PATTERNS = [
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

REQUIRED_INTERNAL_PAGES = [
    "about.html",
    "submit.html",
    "contact.html",
    "privacy.html",
    "terms.html"
]

def audit_site(site_slug):
    site_path = os.path.join(OUTPUT_DIR, site_slug)
    index_file = os.path.join(site_path, "index.html")
    groups_file = os.path.join(site_path, "data", "groups.json")

    results = {
        "site": site_slug,
        "exists": os.path.exists(site_path),
        "index_exists": os.path.exists(index_file),
        "groups_exists": os.path.exists(groups_file),
        "community_hrefs": [],
        "copy_invite_links": [],
        "all_outbound_links": [],
        "schema_links": [],
        "banned_found": [],
        "internal_links_in_index": {},
        "missing_internal_files": [],
        "groups_count": 0,
        "groups_banned": []
    }

    if not results["index_exists"]:
        return results

    with open(index_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. Check internal links
    for page in REQUIRED_INTERNAL_PAGES:
        target_file = os.path.join(site_path, page)
        exists_on_disk = os.path.exists(target_file)
        if not exists_on_disk:
            results["missing_internal_files"].append(page)
        
        # Look for links to page
        page_pattern = r'href=[\'"](?:(?:\./)?' + re.escape(page) + r'|\b' + re.escape(page) + r')(?:[?#][^\'"]*)?[\'"]'
        found = bool(re.search(page_pattern, html_content))
        results["internal_links_in_index"][page] = found

    # 2. Extract copyInviteLink calls
    copy_matches = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html_content)
    results["copy_invite_links"] = copy_matches

    # 3. Extract community hrefs: href="..." on cards / buttons
    # Regex find all hrefs in <a> tags
    a_matches = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>', html_content, re.IGNORECASE)
    for href in a_matches:
        if href.startswith("http://") or href.startswith("https://"):
            results["all_outbound_links"].append(href)
            # Check if it looks like a community link (reddit, discord, t.me, github, forum)
            if any(dom in href.lower() for dom in ["reddit.com", "discord.gg", "t.me", "github.com", "huggingface.co", "openai.com", "blender", "notion"]):
                results["community_hrefs"].append(href)

    # 4. Check banned substrings in raw HTML
    for banned in BANNED_PATTERNS:
        if banned in html_content.lower():
            results["banned_found"].append(banned)

    # 5. Check groups.json
    if results["groups_exists"]:
        with open(groups_file, "r", encoding="utf-8") as f:
            try:
                groups_data = json.load(f)
                results["groups_count"] = len(groups_data)
                for g in groups_data:
                    u = g.get("joinUrl", "").lower()
                    for banned in BANNED_PATTERNS:
                        if banned in u:
                            results["groups_banned"].append((g.get("id"), u, banned))
            except Exception as e:
                results["groups_error"] = str(e)

    return results

if __name__ == "__main__":
    for s in SITES:
        res = audit_site(s)
        print(f"=== {res['site']} ===")
        print(f"  Internal missing files: {res['missing_internal_files']}")
        print(f"  Internal links present in index: {res['internal_links_in_index']}")
        print(f"  Community hrefs count: {len(res['community_hrefs'])}")
        print(f"  copyInviteLink count: {len(res['copy_invite_links'])}")
        print(f"  Groups in groups.json: {res['groups_count']}")
        print(f"  Banned in HTML: {res['banned_found']}")
        print(f"  Banned in groups.json: {res['groups_banned']}")
        print()
