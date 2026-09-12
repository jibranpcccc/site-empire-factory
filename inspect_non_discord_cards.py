import os
import json
from bs4 import BeautifulSoup

ROOT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs"
OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

targets = [
    ("developer-coding-hub", os.path.join(ROOT_DIR, "developer-coding-hub"), "https://communityinviter.com/apps/cloud-native/cncf"),
    ("growth-marketing-hackers-hub", os.path.join(OUTPUT_DIR, "growth-marketing-hackers-hub"), "https://growthhackers.com/posts"),
    ("scholarships-study-abroad-hub", os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"), "https://careers.cern/students"),
    ("scholarships-study-abroad-hub", os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"), "https://investyourtalent.esteri.it/en/"),
    ("scholarships-study-abroad-hub", os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"), "https://www.moe.gov.tw/elitescholars"),
    ("scholarships-study-abroad-hub", os.path.join(ROOT_DIR, "scholarships-study-abroad-hub"), "https://www.a-star.edu.sg/Scholarships/for-graduate-studies/singapore-international-graduate-award-singa")
]

for site_name, site_path, target_url in targets:
    idx_p = os.path.join(site_path, "index.html")
    grp_p = os.path.join(site_path, "data", "groups.json")

    print("=" * 60)
    print(f"Site: {site_name} | Target: {target_url}")

    # Check groups.json
    if os.path.exists(grp_p):
        with open(grp_p, "r", encoding="utf-8") as gf:
            gdata = json.load(gf)
            for item in gdata:
                if item.get("joinUrl") == target_url:
                    print("  In groups.json:")
                    print("   ", item)

    # Check card in index.html
    if os.path.exists(idx_p):
        with open(idx_p, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.find_all("div", class_=lambda c: c and "card" in c.split()):
            if target_url in str(card):
                title = card.find("h3")
                print("  Card in HTML:")
                print("    Title:", title.text if title else "No title")
                print("    HTML snippet:", str(card)[:250] + "...")
