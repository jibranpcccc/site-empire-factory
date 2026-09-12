import json

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fleet = data["fleet_data"]

broken = [
    "https://discord.gg/ansible",
    "https://discord.gg/awardtravel",
    "https://discord.gg/bogleheads",
    "https://discord.gg/buildapcsales",
    "https://discord.gg/buildinpublic",
    "https://discord.gg/confluent"
]

for b in broken:
    found_in = []
    for site_name, sinfo in fleet.items():
        if b in sinfo["card_join_links"] or b in sinfo["copy_links"] or b in sinfo["groups_links"]:
            found_in.append(site_name)
    print(f"{b} found in: {found_in}")
