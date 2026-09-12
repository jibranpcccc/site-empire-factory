import urllib.request
import json

candidates = [
    "tph", "programming", "hugging-face", "huggingface-community",
    "cloud-native", "devops-community",
    "proptraders", "tech", "langchain-ai", "langchaincommunity",
    "cncf", "cloudnative", "homelab", "homeassistant", "home-assistant",
    "infosec", "cyber", "osint", "security", "bugbounty", "bugcrowd",
    "hackthebox", "tryhackme", "blender", "unreal", "unrealengine", "gamedev",
    "notion", "obsidian", "pkm"
]
headers = {'User-Agent': 'Mozilla/5.0'}
for c in candidates:
    try:
        req = urllib.request.Request(f'https://discord.com/api/v9/invites/{c}', headers=headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            print(f"MATCH: discord.gg/{c} -> {data.get('guild', {}).get('name')}")
    except Exception:
        pass
