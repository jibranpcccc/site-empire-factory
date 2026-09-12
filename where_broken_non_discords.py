import json

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fleet = data["fleet_data"]

broken = [
    "https://communityinviter.com/apps/cloud-native/cncf",
    "https://careers.cern/students",
    "https://investyourtalent.esteri.it/en/",
    "https://growthhackers.com/posts",
    "https://www.moe.gov.tw/elitescholars",
    "https://www.a-star.edu.sg/Scholarships/for-graduate-studies/singapore-international-graduate-award-singa"
]

for b in broken:
    found_in = []
    for site_name, sinfo in fleet.items():
        if b in sinfo["card_join_links"] or b in sinfo["copy_links"] or b in sinfo["groups_links"]:
            found_in.append(site_name)
    print(f"{b} found in: {found_in}")
