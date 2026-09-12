import os
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"

SITES_81_120 = [
    "study-in-germany-daadvise-hub",
    "study-in-japan-mext-hub",
    "tax-strategies-offshore-hub",
    "tiktok-shop-dropshipping-hub",
    "ui-ux-design-systems-hub",
    "unity-6-indie-studios-hub",
    "unreal-engine-5-creators-hub",
    "usmle-medical-residency-hub",
    "valorant-scrims-competitive-hub",
    "virtual-assistants-agency-hub",
    "youtube-automation-creators-hub",
    "algo-trading-quant-hub",
    "autonomous-ai-agents-hub",
    "biohacking-longevity-hub",
    "book-clubs-readers-lounge-hub",
    "calisthenics-street-workout-hub",
    "creative-indie-filmmakers-hub",
    "cs2-lineups-premier-hub",
    "cybersecurity-grc-compliance-hub",
    "deep-learning-nlp-transformers-hub",
    "digital-nomad-visas-tax-hub",
    "electric-vehicles-clean-energy-hub",
    "fintech-embedded-banking-hub",
    "golang-backend-cloud-hub",
    "high-ticket-closing-sales-hub",
    "homelab-selfhosted-linux-hub",
    "indie-game-marketing-steam-hub",
    "language-exchange-polyglot-hub",
    "minimalist-slow-living-hub",
    "neurotech-brain-computer-interface-hub",
    "nextjs-fullstack-react-hub",
    "prompt-engineering-tuning-hub",
    "real-estate-investing-syndicates-hub",
    "remote-vanlife-overlanding-hub",
    "rust-systems-performance-hub",
    "smart-contract-solidity-hub",
    "speedrunning-glitches-hub",
    "travel-hacking-points-hub",
    "vr-gaming-meta-quest-hub",
    "youtube-automation-cashcow-hub"
]

BANNED_PATTERNS = [
    "telegram.com/community",
    "discord.com/community",
    "whatsapp.com/community",
    "reddit.com/community",
    "vipflashloot_",
    "t.me/community",
    "discord.gg/community",
    "example.com",
    "{cid}"
]

KNOWN_BROKEN = [
    "https://discord.gg/theprogrammershangout",
    "https://discord.gg/kubernetes",
    "https://discord.gg/huggingface",
    "https://discord.gg/devops",
    "https://discord.gg/biggerpockets",
    "https://discord.gg/langchain",
    "https://discord.gg/proptrading",
    "https://discord.gg/technology",
    "https://github.com/pytorch/pytorch/discussions",
    "https://github.com/kubernetes/kubernetes/discussions",
    "https://github.com/rust-lang/rust/discussions",
    "https://research.ethdev.com",
    "https://discord.gg/dexscreener",
    "https://discord.gg/amazonsellers",
    "https://discord.gg/affiliatemarketing",
    "https://discord.gg/copywriting"
]

def analyze():
    all_urls = set()
    site_urls = {}
    url_to_sites = {}
    banned_urls_found = []
    broken_urls_found = []

    for site in SITES_81_120:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        collected = set()

        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                html = f.read()

            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if href.startswith("http://") or href.startswith("https://"):
                    collected.add(href)

            copy_matches = re.findall(r"copyInviteLink\([^,]+,\s*['\"]([^'\"]+)['\"]\)", html)
            for m in copy_matches:
                collected.add(m.strip())

            for s in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(s.string)
                    def extract(obj):
                        if isinstance(obj, dict):
                            if obj.get("@type") == "ListItem" and "url" in obj:
                                collected.add(obj["url"].strip())
                            for v in obj.values():
                                extract(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                extract(item)
                    extract(data)
                except Exception:
                    pass

        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                try:
                    gdata = json.load(gf)
                    for g in gdata:
                        u = g.get("joinUrl", "").strip()
                        if u:
                            collected.add(u)
                except Exception:
                    pass

        site_urls[site] = list(collected)
        for u in collected:
            all_urls.add(u)
            if u not in url_to_sites:
                url_to_sites[u] = []
            url_to_sites[u].append(site)

            u_low = u.lower()
            for b in BANNED_PATTERNS:
                if b in u_low:
                    banned_urls_found.append((site, u, b))
            if u in KNOWN_BROKEN:
                broken_urls_found.append((site, u))

    print(f"Total Unique URLs found across 40 sites: {len(all_urls)}")
    print(f"Total Banned Placeholders in URLs: {len(banned_urls_found)}")
    for b in banned_urls_found:
        print(f"  BANNED: {b}")

    print(f"\nTotal Known Broken URLs: {len(broken_urls_found)}")
    broken_url_map = {}
    for site, u in broken_urls_found:
        if u not in broken_url_map:
            broken_url_map[u] = []
        broken_url_map[u].append(site)

    for u, slist in broken_url_map.items():
        print(f"  BROKEN: {u} (in {len(slist)} sites: {', '.join(slist[:3])}{'...' if len(slist)>3 else ''})")

    # Save unique URLs to file
    with open(r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\fleet_3_unique_urls.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(all_urls)), f, indent=2)

    # Breakdown by domain
    domain_counts = {}
    for u in all_urls:
        p = urlparse(u).netloc
        domain_counts[p] = domain_counts.get(p, 0) + 1

    print("\nDomain breakdown of unique URLs:")
    for d, c in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {d}: {c}")

if __name__ == "__main__":
    analyze()
