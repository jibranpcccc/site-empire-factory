import os
import re
import json
from bs4 import BeautifulSoup

site_path = r"c:\Users\jibra\Desktop\1\20 blogs\developer-coding-hub"
index_path = os.path.join(site_path, "index.html")
groups_path = os.path.join(site_path, "data", "groups.json")

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
outbound_hrefs = []
for a in soup.find_all("a", href=True):
    href = a["href"].strip()
    if href.startswith("http://") or href.startswith("https://"):
        outbound_hrefs.append(href)

copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

groups_links = []
if os.path.exists(groups_path):
    with open(groups_path, "r", encoding="utf-8") as gf:
        gdata = json.load(gf)
        for g in gdata:
            u = g.get("joinUrl", "").strip()
            if u:
                groups_links.append(u)

all_site_urls = set(outbound_hrefs + copy_links + groups_links)

KNOWN_BROKEN = [
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
    "https://github.com/rust-lang/rust/discussions",
    "https://research.ethdev.com",
    "https://discord.gg/dexscreener",
    "https://discord.gg/amazonsellers",
    "https://discord.gg/affiliatemarketing",
    "https://discord.gg/copywriting"
]

print("Outbound hrefs count:", len(outbound_hrefs))
print("Copy links count:", len(copy_links))
print("Groups links count:", len(groups_links))
print("All site URLs count:", len(all_site_urls))

found_broken = [u for u in all_site_urls if u in KNOWN_BROKEN]
print("Found broken in developer-coding-hub:", found_broken)
if found_broken:
    for fb in found_broken:
        in_hrefs = fb in outbound_hrefs
        in_copy = fb in copy_links
        in_groups = fb in groups_links
        print(f"  {fb}: in_hrefs={in_hrefs}, in_copy={in_copy}, in_groups={in_groups}")
