with open("community_database.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. URL replacements
url_map = {
    "https://discord.gg/theprogrammershangout": "https://discord.gg/programming",
    "https://github.com/rust-lang/rust/discussions": "https://users.rust-lang.org",
    "https://discord.gg/huggingface": "https://discuss.huggingface.co",
    "https://discord.gg/langchain": "https://github.com/langchain-ai/langchain/discussions",
    "https://github.com/pytorch/pytorch/discussions": "https://discuss.pytorch.org",
    "https://discord.gg/devops": "https://discord.gg/devcord",
    "https://discord.gg/kubernetes": "https://discuss.kubernetes.io",
    "https://github.com/kubernetes/kubernetes/discussions": "https://discuss.kubernetes.io",
    "https://research.ethdev.com": "https://ethresear.ch",
    "https://discord.gg/biggerpockets": "https://www.biggerpockets.com/forums",
    "https://discord.gg/technology": "https://discord.gg/tech",
    "https://discord.gg/proptrading": "https://discord.gg/trading"
}

for old_u, new_u in url_map.items():
    code = code.replace(old_u, new_u)

# 2. Add to RELATED_CATEGORIES
rel_anchor = '    "general_tech": ["coding", "ai", "cloud_devops"]\n}'
new_rel = '''    "general_tech": ["coding", "ai", "cloud_devops"],
    "b2b_saas": ["marketing_growth", "coding", "general_tech"],
    "biohacking_longevity": ["general_tech", "finance_investing"],
    "smart_home_iot": ["cloud_devops", "coding", "general_tech"],
    "cyber_threat_intelligence": ["cybersecurity", "cloud_devops", "general_tech"],
    "ai_video_creators": ["ai", "gaming_3d", "general_tech"],
    "bug_bounty_hacking": ["cybersecurity", "coding", "general_tech"],
    "notion_productivity": ["productivity_automation", "coding", "general_tech"],
    "3d_blender_unreal": ["gaming_3d", "coding", "general_tech"],
    "remote_developer_jobs": ["remote_work_careers", "coding", "general_tech"]
}'''

if rel_anchor in code:
    code = code.replace(rel_anchor, new_rel)
else:
    print("WARNING: rel_anchor not found!")

# 3. Add precision mappings
prec_anchor = '    # Precision niche mappings\n'
new_prec = '''    # Precision niche mappings
    # Sites 71-80 Precision Mappings
    if any(k in combined for k in ["b2b saas", "saas founders", "cold email", "plg funnels", "stripe mrr", "churn"]):
        return "b2b_saas"
    if any(k in combined for k in ["biohack", "longevity", "human optimization", "cgm data", "cold exposure", "zone 2 cardio"]):
        return "biohacking_longevity"
    if any(k in combined for k in ["home assistant", "smart home", "zigbee2mqtt", "esphome", "matter protocol"]):
        return "smart_home_iot"
    if any(k in combined for k in ["threat intelligence", "cyber threat", "dark web monitoring", "yara rules", "soc alerts"]):
        return "cyber_threat_intelligence"
    if any(k in combined for k in ["video creator", "virtual production", "runway gen", "luma dream", "kling ai", "ai cinematography"]):
        return "ai_video_creators"
    if any(k in combined for k in ["bug bounty", "ethical hacking", "hackerone", "burp suite", "ssrf exploit", "idor detection"]):
        return "bug_bounty_hacking"
    if any(k in combined for k in ["prop firm", "ftmo", "prop trader", "funded trader"]):
        return "prop_trading"
    if any(k in combined for k in ["notion", "second brain", "para framework", "formula 2.0"]):
        return "notion_productivity"
    if any(k in combined for k in ["blender", "unreal engine", "geometry nodes", "nanite rendering", "hard surface modeling"]):
        return "3d_blender_unreal"
    if any(k in combined for k in ["remote tech", "global compensation", "tech salaries from abroad", "remote developer", "stock grant negotiation"]):
        return "remote_developer_jobs"
'''

if prec_anchor in code:
    code = code.replace(prec_anchor, new_prec)
else:
    print("WARNING: prec_anchor not found!")

with open("community_database.py", "w", encoding="utf-8") as f:
    f.write(code)

print("community_database.py updated successfully!")
