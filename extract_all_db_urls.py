import community_database
from urllib.parse import urlparse
import json

db = community_database.VERIFIED_COMMUNITIES_DATABASE
all_db_urls = set()
for cat, items in db.items():
    for item in items:
        all_db_urls.add(item["joinUrl"])

print(f"Total unique URLs in community_database.py: {len(all_db_urls)}")
with open("all_db_urls.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(all_db_urls)), f, indent=2)
