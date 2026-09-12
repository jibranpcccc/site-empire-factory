import json

with open("fleet_part1_initial_scan.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for bm in d["broken_matches"]:
    site = bm["site"]
    url = bm["url"]
    # check in site_summaries
    for s in d["site_summaries"]:
        if s["site"] == site:
            print(f"Site: {site}, URL: {url}, broken_count in summary: {s['broken_count']}")
