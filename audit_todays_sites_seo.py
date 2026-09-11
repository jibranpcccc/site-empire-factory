import os
import json
import re
from bs4 import BeautifulSoup

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
TODAY_SITES = [
    "crypto-yield-farming-staking-hub",
    "no-code-bubble-automation-hub",
    "golang-microservices-distributed-hub",
    "growth-marketing-hackers-hub",
    "ui-ux-design-systems-hub",
    "sound-design-music-production-hub",
    "amazon-fba-private-label-hub",
    "personal-finance-fire-movement-hub",
    "virtual-assistants-agency-hub",
    "podcast-creators-audio-network-hub"
]

REQUIRED_AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ClaudeBot", "Claude-Web",
    "PerplexityBot", "Applebot", "Applebot-Extended", "Google-Extended", "CCBot"
]

REQUIRED_EEAT_PAGES = ["about.html", "submit.html", "contact.html", "privacy.html", "terms.html"]
CTA_VERBS = ["explore", "discover", "submit", "learn", "review", "find", "access", "join", "browse", "connect"]

report = {}

for site in TODAY_SITES:
    sp = os.path.join(OUTPUT_DIR, site)
    site_rep = {"site": site, "errors": [], "warnings": [], "scores": {}}

    if not os.path.exists(sp):
        site_rep["errors"].append("Directory does not exist on disk")
        report[site] = site_rep
        continue

    # 1. robots.txt
    robots_path = os.path.join(sp, "robots.txt")
    if not os.path.exists(robots_path):
        site_rep["errors"].append("Missing robots.txt")
    else:
        with open(robots_path, "r", encoding="utf-8", errors="ignore") as f:
            robots_txt = f.read()
        missing_crawlers = [c for c in REQUIRED_AI_CRAWLERS if f"User-agent: {c}" not in robots_txt]
        if missing_crawlers:
            site_rep["errors"].append(f"robots.txt missing AI crawlers: {missing_crawlers}")
        if "Sitemap:" not in robots_txt:
            site_rep["errors"].append("robots.txt missing Sitemap directive")
        site_rep["scores"]["robots_txt"] = "PASS" if not missing_crawlers and "Sitemap:" in robots_txt else "FAIL"

    # 2. index.html checks
    index_path = os.path.join(sp, "index.html")
    if not os.path.exists(index_path):
        site_rep["errors"].append("Missing index.html")
    else:
        with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
            index_html = f.read()

        soup = BeautifulSoup(index_html, "html.parser")

        # Title tag
        title_tag = soup.find("title")
        title_text = title_tag.text.strip() if title_tag else ""
        site_rep["title"] = title_text
        site_rep["title_len"] = len(title_text)
        if not (30 <= len(title_text) <= 60):
            site_rep["warnings"].append(f"Title length {len(title_text)} not in 30-60 range: '{title_text}'")

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc_text = meta_desc.get("content", "").strip() if meta_desc else ""
        site_rep["meta_desc"] = desc_text
        site_rep["meta_desc_len"] = len(desc_text)
        if not (120 <= len(desc_text) <= 160):
            site_rep["warnings"].append(f"Meta description length {len(desc_text)} not in 120-160 range: '{desc_text}'")
        has_cta = any(verb in desc_text.lower() for verb in CTA_VERBS)
        if not has_cta:
            site_rep["warnings"].append("Meta description missing imperative CTA verb")

        # Princeton GEO Answer block
        geo_block = soup.find(class_="geo-answer-block")
        if not geo_block:
            site_rep["errors"].append("Missing .geo-answer-block")
        else:
            geo_p = geo_block.find("p")
            geo_text = geo_p.text.strip() if geo_p else ""
            words = geo_text.split()
            site_rep["geo_word_count"] = len(words)
            if not (134 <= len(words) <= 167):
                site_rep["warnings"].append(f"GEO answer block words: {len(words)} (benchmark: 134-167)")
            geo_table = geo_block.find("table")
            if not geo_table:
                site_rep["errors"].append("Missing 4-row comparative HTML table in .geo-answer-block")
            else:
                rows = geo_table.find_all("tr")
                site_rep["geo_table_rows"] = len(rows)

        # OpenGraph & Twitter
        og_tags = ["og:title", "og:description", "og:url", "og:type", "og:site_name", "og:locale"]
        for og in og_tags:
            if not soup.find("meta", attrs={"property": og}):
                site_rep["warnings"].append(f"Missing meta property={og}")
        tw_tags = ["twitter:card", "twitter:title", "twitter:description"]
        for tw in tw_tags:
            if not soup.find("meta", attrs={"name": tw}):
                site_rep["warnings"].append(f"Missing meta name={tw}")

        # Schema.org Unified @graph
        schema_scripts = soup.find_all("script", type="application/ld+json")
        schema_valid = False
        for sc in schema_scripts:
            try:
                data = json.loads(sc.string)
                if "@graph" in data:
                    types = [node.get("@type") for node in data["@graph"]]
                    site_rep["schema_types"] = types
                    schema_valid = True
                    break
            except Exception:
                pass
        if not schema_valid:
            site_rep["errors"].append("Missing or invalid Schema.org Core v30.0 unified @graph")

        # GA4 Roll-Up
        if "G-CK7NVYS1Y9" not in index_html:
            site_rep["errors"].append("Missing GA4 Measurement ID G-CK7NVYS1Y9")
        if "ai_search_traffic" not in index_html:
            site_rep["warnings"].append("Missing AI search traffic interceptor event")

        # GSC verification
        gsc_meta = soup.find("meta", attrs={"name": "google-site-verification"})
        gsc_file = [f for f in os.listdir(sp) if f.startswith("google") and f.endswith(".html")]
        site_rep["has_gsc_meta"] = bool(gsc_meta)
        site_rep["gsc_file"] = gsc_file[0] if gsc_file else None
        if not gsc_meta and not gsc_file:
            site_rep["errors"].append("Missing GSC verification meta tag and HTML file")

        # Community Links Check
        cards = soup.find_all("div", class_=re.compile(r"community-card|card"))
        card_links = []
        for c in cards:
            a = c.find("a", href=True)
            if a:
                card_links.append(a["href"])
        banned = ["telegram.com/community", "discord.com/community", "whatsapp.com/community", "reddit.com/community", "{cid}"]
        found_banned = [l for l in card_links if any(b in l.lower() for b in banned)]
        if found_banned:
            site_rep["errors"].append(f"Found banned synthetic URLs: {found_banned[:3]}")
        site_rep["community_card_count"] = len(cards)

    # 3. 5 EEAT Pages
    eeat_rep = {}
    for ep in REQUIRED_EEAT_PAGES:
        ep_path = os.path.join(sp, ep)
        if not os.path.exists(ep_path):
            site_rep["errors"].append(f"Missing EEAT page: {ep}")
            eeat_rep[ep] = {"exists": False, "words": 0}
        else:
            with open(ep_path, "r", encoding="utf-8", errors="ignore") as f:
                ep_html = f.read()
            ep_soup = BeautifulSoup(ep_html, "html.parser")
            body = ep_soup.find("main") or ep_soup.find("body")
            body_words = len(body.text.split()) if body else 0
            eeat_rep[ep] = {"exists": True, "words": body_words}
            if body_words < 400:
                site_rep["warnings"].append(f"{ep} content below 400 words ({body_words} words)")
    site_rep["eeat_pages"] = eeat_rep

    # 4. sitemap.xml & llms.txt
    sm_path = os.path.join(sp, "sitemap.xml")
    site_rep["has_sitemap"] = os.path.exists(sm_path)
    llms_path = os.path.join(sp, "llms.txt")
    site_rep["has_llms_txt"] = os.path.exists(llms_path)
    if not site_rep["has_sitemap"]:
        site_rep["errors"].append("Missing sitemap.xml")
    if not site_rep["has_llms_txt"]:
        site_rep["errors"].append("Missing llms.txt")

    report[site] = site_rep

with open(os.path.join(OUTPUT_DIR, "..", "audit_todays_sites_results.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"Audit completed for {len(report)} sites.")
for site, rep in report.items():
    err_cnt = len(rep["errors"])
    warn_cnt = len(rep["warnings"])
    print(f"{site}: errors={err_cnt}, warnings={warn_cnt}")
    if err_cnt > 0:
        for err in rep["errors"]:
            print(f"   [ERROR] {err}")
    if warn_cnt > 0:
        for warn in rep["warnings"]:
            print(f"   [WARN] {warn}")
