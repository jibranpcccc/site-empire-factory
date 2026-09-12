import new_categories_data
import community_database

banned = community_database.BANNED_URL_SUBSTRINGS

total = 0
for cat, items in new_categories_data.NEW_CATEGORIES.items():
    assert len(items) == 30, f"{cat} has {len(items)} items instead of 30!"
    for idx, item in enumerate(items, 1):
        total += 1
        url = item["joinUrl"]
        assert url.startswith("https://") or url.startswith("http://"), f"Bad scheme in {url}"
        for b in banned:
            assert b not in url.lower(), f"Banned {b} found in {url}"
        assert not community_database.is_fake_or_synthetic_url(url), f"Fake URL detected: {url}"
        for k in ["title", "platform", "category", "memberCount", "description", "joinUrl", "tags"]:
            assert k in item, f"Missing {k} in {cat} item {idx}"

print(f"All {total} items in all {len(new_categories_data.NEW_CATEGORIES)} new categories passed validation!")
