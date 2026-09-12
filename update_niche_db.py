import json
import os
import new_categories_data

niche_db_path = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\data\niche_communities_database.json"

# Backup niche_communities_database.json
with open(niche_db_path, "r", encoding="utf-8") as f:
    niche_db = json.load(f)

with open(niche_db_path + ".bak", "w", encoding="utf-8") as f:
    json.dump(niche_db, f, indent=2)

# Fix 4 broken URLs in niche_db
replacements = {
    "https://discord.gg/dexscreener": "https://www.reddit.com/r/CryptoCurrency/",
    "https://discord.gg/amazonsellers": "https://www.reddit.com/r/FulfillmentByAmazon/",
    "https://discord.gg/affiliatemarketing": "https://www.reddit.com/r/AffiliateMarketing/",
    "https://discord.gg/copywriting": "https://www.reddit.com/r/copywriting/"
}

for cat, items in niche_db.items():
    for item in items:
        u = item.get("joinUrl", "")
        if u in replacements:
            item["joinUrl"] = replacements[u]
            if "reddit.com" in replacements[u]:
                item["platform"] = "Reddit"

# Add the 9 new categories
for cat_name, items in new_categories_data.NEW_CATEGORIES.items():
    niche_db[cat_name] = items

with open(niche_db_path, "w", encoding="utf-8") as f:
    json.dump(niche_db, f, indent=2)

print(f"Updated {niche_db_path}. Total categories now: {len(niche_db)}")
