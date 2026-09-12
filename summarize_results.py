import json

with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\url_verification_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

by_type = {}
for u, r in results.items():
    t = r.get("type")
    by_type.setdefault(t, []).append((u, r))

for t, items in by_type.items():
    print(f"=== {t} ({len(items)}) ===")
    for u, r in items:
        status = r.get("status")
        extra = r.get("guild", "") or r.get("msg", "")
        if t != "discord_valid" and t != "http_ok":
            print(f"  {u} -> status={status}, {extra}")
        else:
            print(f"  [OK] {u} -> {status} {extra}")
    print()
