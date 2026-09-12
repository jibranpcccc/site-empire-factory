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
a_hrefs = [a["href"].strip() for a in soup.find_all("a", href=True) if a["href"].strip().startswith("http")]
copy_links = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)

groups_links = []
if os.path.exists(groups_path):
    with open(groups_path, "r", encoding="utf-8") as gf:
        gdata = json.load(gf)
        for g in gdata:
            u = g.get("joinUrl", "").strip()
            if u:
                groups_links.append(u)

print("In a_hrefs:", [u for u in a_hrefs if "langchain" in u])
print("In copy_links:", [u for u in copy_links if "langchain" in u])
print("In groups_links:", [u for u in groups_links if "langchain" in u])
