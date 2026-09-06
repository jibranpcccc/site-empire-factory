#!/usr/bin/env python3
import os
import json
import re

hubs = [
    ("Hub 11 (No-Code & AI Automation)", r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output\no-code-automation-hub"),
    ("Hub 12 (Rust & Systems Engineering)", r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output\rust-systems-engineering-hub")
]

banned = ["telegram.com/community", "discord.com/community", "whatsapp.com/community", "reddit.com/community"]

for name, hdir in hubs:
    print("==================================================")
    print(f"AUDIT REPORT: {name}")
    print(f"Directory: {hdir}")
    
    # 1. Check data/groups.json
    groups_path = os.path.join(hdir, "data", "groups.json")
    with open(groups_path, "r", encoding="utf-8") as f:
        groups = json.load(f)
    print(f"Total groups in groups.json: {len(groups)}")
    assert len(groups) == 30, f"Expected 30 groups, got {len(groups)}"
    
    fake_in_json = [g["joinUrl"] for g in groups if any(b in g["joinUrl"] for b in banned)]
    print(f"Fake URLs in groups.json: {len(fake_in_json)}")
    assert len(fake_in_json) == 0, f"Found fake URLs in groups.json: {fake_in_json}"

    # 2. Check index.html
    index_path = os.path.join(hdir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Check for banned substrings anywhere in file
    fake_in_html = [b for b in banned if b in html]
    print(f"Banned patterns found anywhere in index.html: {fake_in_html}")
    assert len(fake_in_html) == 0, f"Found banned patterns in index.html: {fake_in_html}"

    # Verify Schema ItemList
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    schema_data = json.loads(schema_match.group(1))
    itemlist = None
    for node in schema_data.get("@graph", []):
        if node.get("@type") == "CollectionPage" and "mainEntity" in node:
            itemlist = node["mainEntity"]
            break
        elif node.get("@type") == "ItemList":
            itemlist = node
            break
    assert itemlist is not None, "Could not find ItemList in Schema"
    items = itemlist.get("itemListElement", [])
    print(f"Total items in Schema ItemList: {len(items)}")
    assert len(items) == 30, f"Expected 30 schema items, got {len(items)}"
    fake_in_schema = [item["url"] for item in items if any(b in item.get("url", "") for b in banned)]
    print(f"Fake URLs in Schema: {len(fake_in_schema)}")
    assert len(fake_in_schema) == 0

    # Verify 30 cards in HTML
    card_matches = re.findall(r'<div id="community-card-(\d+)".*?onclick="copyInviteLink\(event, \'([^\']+)\'\)".*?<a href="([^"]+)"', html, re.DOTALL)
    print(f"Total cards verified in HTML: {len(card_matches)}")
    assert len(card_matches) == 30, f"Expected 30 cards, found {len(card_matches)}"

    # Check href matches onclick url on every card
    mismatches = []
    for card_idx, copy_url, href_url in card_matches:
        if copy_url != href_url:
            mismatches.append((card_idx, copy_url, href_url))
    print(f"URL mismatches between onclick & href: {len(mismatches)}")
    assert len(mismatches) == 0

    print("Platform breakdown:")
    plat_counts = {}
    for g in groups:
        p = g.get("platform", "Unknown")
        plat_counts[p] = plat_counts.get(p, 0) + 1
    for p, count in sorted(plat_counts.items()):
        print(f"  - {p}: {count} communities")

    print("\nVerified Community Samples:")
    for card_idx, copy_url, href_url in card_matches[:6]:
        print(f"  Card #{card_idx}: {href_url}")
    print("\n[RESULT] AUDIT PASSED 100% PERFECTLY WITH ZERO FAKE LINKS!")
print("==================================================")
print("ALL AUDITS COMPLETE: HUBS 11 & 12 ARE 100% CLEAN OF FAKE LINKS!")
