import os
from bs4 import BeautifulSoup

site = r"c:\Users\jibra\Desktop\1\20 blogs\deals-loot-coupons-hub"
with open(os.path.join(site, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
for url in ["https://discord.gg/awardtravel", "https://discord.gg/buildapcsales", "https://t.me/wholefoodsperks"]:
    for card in soup.find_all("div", class_=lambda c: c and "card" in c.split()):
        if url in str(card):
            print(f"=== Card for {url} ===")
            print(str(card))
