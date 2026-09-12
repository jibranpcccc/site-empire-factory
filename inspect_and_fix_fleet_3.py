import os
import json
import re
from bs4 import BeautifulSoup

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

REPLACEMENTS = {
    "https://discord.gg/theprogrammershangout": {
        "new_url": "https://discord.gg/programming",
        "title": "The Programmer's Hangout Discord",
        "platform": "Discord"
    },
    "https://github.com/rust-lang/rust/discussions": {
        "new_url": "https://users.rust-lang.org",
        "title": "Rust Users Official Community Forum",
        "platform": "Forum"
    },
    "https://discord.gg/huggingface": {
        "new_url": "https://discuss.huggingface.co",
        "title": "Hugging Face Community Forum",
        "platform": "Forum"
    },
    "https://discord.gg/langchain": {
        "new_url": "https://github.com/langchain-ai/langchain/discussions",
        "title": "LangChain Community Discussions",
        "platform": "GitHub"
    },
    "https://github.com/pytorch/pytorch/discussions": {
        "new_url": "https://discuss.pytorch.org",
        "title": "PyTorch Official Community Forum",
        "platform": "Forum"
    },
    "https://discord.gg/devops": {
        "new_url": "https://discord.gg/devcord",
        "title": "Devcord Developer & DevOps Community",
        "platform": "Discord"
    },
    "https://discord.gg/kubernetes": {
        "new_url": "https://discuss.kubernetes.io",
        "title": "Kubernetes Official Community Forum",
        "platform": "Forum"
    },
    "https://github.com/kubernetes/kubernetes/discussions": {
        "new_url": "https://discuss.kubernetes.io",
        "title": "Kubernetes Community Forum",
        "platform": "Forum"
    },
    "https://discord.gg/biggerpockets": {
        "new_url": "https://www.biggerpockets.com/forums",
        "title": "BiggerPockets Real Estate Community Forums",
        "platform": "Forum"
    },
    "https://discord.gg/technology": {
        "new_url": "https://discord.gg/tech",
        "title": "Tech Community Discord",
        "platform": "Discord"
    }
}

def inspect_and_fix():
    print("=== INSPECTING AND FIXING BROKEN LINKS IN FLEET PART 3 ===")
    
    total_sites_modified = 0
    total_replacements_html = 0
    total_replacements_groups = 0

    for site in SITES_81_120:
        site_path = os.path.join(OUTPUT_DIR, site)
        index_path = os.path.join(site_path, "index.html")
        groups_path = os.path.join(site_path, "data", "groups.json")

        site_modified = False

        # Fix groups.json
        if os.path.exists(groups_path):
            with open(groups_path, "r", encoding="utf-8") as gf:
                groups_data = json.load(gf)

            groups_changed = False
            for g in groups_data:
                u = g.get("joinUrl", "")
                if u in REPLACEMENTS:
                    rep = REPLACEMENTS[u]
                    g["joinUrl"] = rep["new_url"]
                    # If platform was previously discord or github and now forum, update platform if appropriate
                    if "platform" in rep:
                        g["platform"] = rep["platform"]
                    groups_changed = True
                    total_replacements_groups += 1
                    print(f"[{site}] groups.json: {u} -> {rep['new_url']}")

            if groups_changed:
                with open(groups_path, "w", encoding="utf-8") as gf:
                    json.dump(groups_data, gf, indent=2)
                site_modified = True

        # Fix index.html
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as inf:
                html_content = inf.read()

            html_changed = False
            for old_url, rep in REPLACEMENTS.items():
                if old_url in html_content:
                    count = html_content.count(old_url)
                    html_content = html_content.replace(old_url, rep["new_url"])
                    html_changed = True
                    total_replacements_html += count
                    print(f"[{site}] index.html: replaced {count} instances of {old_url} -> {rep['new_url']}")

            if html_changed:
                with open(index_path, "w", encoding="utf-8") as outf:
                    outf.write(html_content)
                site_modified = True

        if site_modified:
            total_sites_modified += 1

    print("\n=== SUMMARY OF REPLACEMENTS ===")
    print(f"Total Sites Modified: {total_sites_modified}")
    print(f"Total HTML Link Replacements: {total_replacements_html}")
    print(f"Total Groups.json Link Replacements: {total_replacements_groups}")

if __name__ == "__main__":
    inspect_and_fix()
