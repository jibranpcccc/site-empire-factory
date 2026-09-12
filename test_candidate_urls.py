import urllib.request
import urllib.error
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

candidate_urls = [
    # B2B SaaS
    "https://www.reddit.com/r/SaaS/",
    "https://www.reddit.com/r/startups/",
    "https://www.reddit.com/r/Entrepreneur/",
    "https://www.reddit.com/r/IndieHackers/",
    "https://www.reddit.com/r/smallbusiness/",
    "https://www.reddit.com/r/growthhacking/",
    "https://www.reddit.com/r/marketing/",
    "https://www.reddit.com/r/sales/",
    "https://news.ycombinator.com",
    "https://www.producthunt.com",
    "https://discord.gg/entrepreneur",
    "https://discord.gg/business",

    # Biohacking
    "https://www.reddit.com/r/Biohackers/",
    "https://www.reddit.com/r/longevity/",
    "https://www.reddit.com/r/Supplements/",
    "https://www.reddit.com/r/Nootropics/",
    "https://www.reddit.com/r/intermittentfasting/",
    "https://www.reddit.com/r/HubermanLab/",
    "https://www.reddit.com/r/PeterAttia/",
    "https://www.reddit.com/r/fasting/",
    "https://www.reddit.com/r/QuantifiedSelf/",
    "https://www.reddit.com/r/science/",
    "https://www.reddit.com/r/Fitness/",
    "https://www.reddit.com/r/nutrition/",
    "https://www.reddit.com/r/sleep/",

    # Smart Home
    "https://www.reddit.com/r/homeassistant/",
    "https://www.reddit.com/r/smarthome/",
    "https://www.reddit.com/r/homelab/",
    "https://www.reddit.com/r/homeautomation/",
    "https://www.reddit.com/r/Zigbee/",
    "https://www.reddit.com/r/esp8266/",
    "https://www.reddit.com/r/esp32/",
    "https://www.reddit.com/r/raspberry_pi/",
    "https://community.home-assistant.io",
    "https://discord.gg/home-assistant",
    "https://discord.gg/homelab",

    # Cyber Threat Intel
    "https://www.reddit.com/r/threatintel/",
    "https://www.reddit.com/r/OSINT/",
    "https://www.reddit.com/r/cybersecurity/",
    "https://www.reddit.com/r/netsec/",
    "https://www.reddit.com/r/Malware/",
    "https://www.reddit.com/r/blueteamsec/",
    "https://www.reddit.com/r/reverseengineering/",
    "https://0x00sec.org",
    "https://discord.gg/security",
    "https://discord.gg/cyber",
    "https://github.com/OWASP/CheatSheetSeries/discussions",

    # AI Video
    "https://www.reddit.com/r/aivideo/",
    "https://www.reddit.com/r/Midjourney/",
    "https://www.reddit.com/r/StableDiffusion/",
    "https://www.reddit.com/r/runwayml/",
    "https://www.reddit.com/r/ComfyUI/",
    "https://www.reddit.com/r/PromptEngineering/",
    "https://discord.gg/midjourney",
    "https://discord.gg/openai",
    "https://discord.gg/anthropic",
    "https://discuss.huggingface.co",

    # Bug Bounty
    "https://www.reddit.com/r/bugbounty/",
    "https://www.reddit.com/r/ethicalhacking/",
    "https://discord.gg/bugbounty",
    "https://discord.gg/hackthebox",
    "https://discord.gg/tryhackme",
    "https://forum.hackthebox.com",

    # Notion / Productivity
    "https://www.reddit.com/r/Notion/",
    "https://www.reddit.com/r/ObsidianMD/",
    "https://www.reddit.com/r/productivity/",
    "https://www.reddit.com/r/PKMS/",
    "https://www.reddit.com/r/GetOrganized/",
    "https://www.reddit.com/r/Anki/",
    "https://forum.obsidian.md",
    "https://www.reddit.com/r/zapier/",
    "https://www.reddit.com/r/nocode/",
    "https://www.reddit.com/r/gtd/",

    # 3D Blender Unreal
    "https://www.reddit.com/r/blender/",
    "https://www.reddit.com/r/unrealengine/",
    "https://www.reddit.com/r/3Dmodeling/",
    "https://www.reddit.com/r/vfx/",
    "https://www.reddit.com/r/gamedev/",
    "https://www.reddit.com/r/unity3d/",
    "https://discord.gg/blender",
    "https://discord.gg/gamedev",
    "https://blenderartists.org",
    "https://www.reddit.com/r/Houdini/",

    # Remote Dev Jobs
    "https://www.reddit.com/r/cscareerquestions/",
    "https://www.reddit.com/r/remotework/",
    "https://www.reddit.com/r/digitalnomad/",
    "https://www.reddit.com/r/workfromhome/",
    "https://www.reddit.com/r/leetcode/",
    "https://www.reddit.com/r/ExperiencedDevs/",
    "https://www.reddit.com/r/ITCareerQuestions/",
    "https://discord.gg/programming",
    "https://nomadlist.com",
    "https://discord.gg/devcord",
    "https://www.reddit.com/r/freelance/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def check(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return url, resp.status, "ok"
    except urllib.error.HTTPError as e:
        return url, e.code, str(e)
    except Exception as ex:
        return url, "err", str(ex)

results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check, u): u for u in candidate_urls}
    for f in as_completed(futures):
        u, status, msg = f.result()
        results[u] = (status, msg)

failed = [u for u, (st, m) in results.items() if st == 404]
print(f"Tested {len(results)} candidate URLs. 404 count: {len(failed)}")
for f in failed:
    print(f"FAILED: {f}")
