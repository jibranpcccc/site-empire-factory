import urllib.request
import urllib.error
import ssl
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

replacements = {
    'https://discord.gg/airtable': 'https://community.airtable.com',
    'https://discord.gg/audioengineering': 'https://gearspace.com/board/',
    'https://discord.gg/biggerpockets': 'https://www.biggerpockets.com/forums',
    'https://discord.gg/bogleheads': 'https://www.bogleheads.org/forum/',
    'https://discord.gg/bubble': 'https://forum.bubble.io',
    'https://discord.gg/devops': 'https://discord.gg/devcord',
    'https://discord.gg/dexscreener': 'https://discord.gg/raydium',
    'https://discord.gg/dividends': 'https://www.reddit.com/r/dividends/',
    'https://discord.gg/edmproduction': 'https://discord.gg/flstudio',
    'https://discord.gg/ethereum': 'https://discord.gg/solana',
    'https://discord.gg/fire': 'https://forum.mrmoneymustache.com',
    'https://discord.gg/flutterflow': 'https://discord.gg/flutter',
    'https://discord.gg/huggingface': 'https://discuss.huggingface.co',
    'https://discord.gg/kotlin': 'https://discord.gg/android',
    'https://discord.gg/kubernetes': 'https://discuss.kubernetes.io',
    'https://discord.gg/langchain': 'https://github.com/langchain-ai/langchain/discussions',
    'https://discord.gg/llvm': 'https://discourse.llvm.org',
    'https://discord.gg/makinghiphop': 'https://discord.gg/flstudio',
    'https://discord.gg/marketing': 'https://discord.gg/agency',
    'https://discord.gg/mediabuyers': 'https://discord.gg/ecommerce',
    'https://discord.gg/nocode': 'https://community.make.com',
    'https://discord.gg/notion': 'https://forum.obsidian.md',
    'https://discord.gg/personalfinance': 'https://discord.gg/wealth',
    'https://discord.gg/podcasting': 'https://podcastmovement.com',
    'https://discord.gg/proptrading': 'https://discord.gg/trading',
    'https://discord.gg/technology': 'https://discord.gg/tech',
    'https://discord.gg/techseo': 'https://discord.gg/seo',
    'https://discord.gg/theprogrammershangout': 'https://discord.gg/programming',
    'https://discord.gg/thetagang': 'https://discord.gg/options',
    'https://discord.gg/tiktokads': 'https://discord.gg/dropshipping',
    'https://discord.gg/webdev': 'https://discord.gg/code',
    'https://discord.gg/webflow': 'https://discourse.webflow.com',
    'https://discord.gg/zapier': 'https://community.zapier.com',
    'https://github.com/kubernetes/kubernetes/discussions': 'https://discuss.kubernetes.io',
    'https://github.com/pytorch/pytorch/discussions': 'https://discuss.pytorch.org',
    'https://github.com/rust-lang/rust/discussions': 'https://users.rust-lang.org',
    'https://forum.thegradcafe.com': 'https://www.reddit.com/r/GradSchool/'
}

def check_replacement(old_u, new_u):
    if 'discord.gg' in new_u:
        code = new_u.split('/')[-1]
        api_url = f'https://discord.com/api/v9/invites/{code}'
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=4, context=ctx) as r:
                d = json.loads(r.read().decode())
                return old_u, new_u, True, f"Discord 200: {d.get('guild', {}).get('name')}"
        except Exception as ex:
            return old_u, new_u, False, f"Discord err: {ex}"
    else:
        try:
            req = urllib.request.Request(new_u, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
                return old_u, new_u, True, f"HTTP {r.status}"
        except urllib.error.HTTPError as e:
            if e.code in [403, 429]:
                return old_u, new_u, True, f"HTTP {e.code} (WAF protected active site)"
            return old_u, new_u, False, f"HTTP err {e.code}"
        except Exception as ex:
            return old_u, new_u, False, f"HTTP ex: {ex}"

results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_replacement, o, n): (o, n) for o, n in replacements.items()}
    for f in as_completed(futures):
        old_u, new_u, ok, msg = f.result()
        results[old_u] = {"new": new_u, "ok": ok, "msg": msg}
        print(f"[{'PASS' if ok else 'FAIL'}] {old_u} -> {new_u} ({msg})")

with open("replacements_verified.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

print(f"\nAll replacements checked. Total: {len(results)}, Passed: {sum(1 for r in results.values() if r['ok'])}, Failed: {sum(1 for r in results.values() if not r['ok'])}")
