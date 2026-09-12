import urllib.request
import json

test_urls = [
    "https://discord.gg/programming",
    "https://discuss.kubernetes.io",
    "https://slack.k8s.io",
    "https://discuss.huggingface.co",
    "https://discord.gg/devcord",
    "https://www.biggerpockets.com/forums",
    "https://discord.gg/realestate",
    "https://github.com/langchain-ai/langchain/discussions",
    "https://discord.gg/daytrading",
    "https://discord.gg/trading",
    "https://discord.gg/tech",
    "https://discuss.pytorch.org",
    "https://users.rust-lang.org"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for u in test_urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"PASS: {u} -> {resp.status}")
    except Exception as e:
        print(f"FAIL: {u} -> {e}")
