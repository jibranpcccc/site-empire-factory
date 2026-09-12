import os
import re
import json

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_part_3_audit_initial.json", "r") as f:
    data = json.load(f)

for site, info in data["report"].items():
    broken = info["broken_in_site"]
    if broken:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        idx_txt = open(index_path, encoding="utf-8").read() if os.path.exists(index_path) else ""
        grp_txt = open(groups_path, encoding="utf-8").read() if os.path.exists(groups_path) else ""

        print(f"Site: {site}")
        print(f"  Flagged in initial: {broken}")
        for b in broken:
            in_idx = b in idx_txt
            in_grp = b in grp_txt
            print(f"    {b}: in index.html? {in_idx} | in groups.json? {in_grp}")
