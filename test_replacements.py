import urllib.request
import urllib.error
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0"}

candidates = [
    # Ansible
    ("Ansible Reddit", "https://www.reddit.com/r/ansible/"),
    ("Ansible Forum", "https://forum.ansible.com/"),
    # Award Travel
    ("Award Travel Reddit", "https://www.reddit.com/r/awardtravel/"),
    # Bogleheads
    ("Bogleheads Reddit", "https://www.reddit.com/r/Bogleheads/"),
    ("Bogleheads Forum", "https://www.bogleheads.org/forum/"),
    # BuildAPCSales
    ("BuildAPCSales Reddit", "https://www.reddit.com/r/buildapcsales/"),
    ("BAPCS Discord", "https://discord.com/api/v9/invites/bapcs"),
    # Build In Public
    ("Build In Public Reddit", "https://www.reddit.com/r/buildinpublic/"),
    ("Indie Hackers", "https://www.indiehackers.com/"),
    # Confluent / Kafka
    ("Kafka Reddit", "https://www.reddit.com/r/apachekafka/"),
    ("Confluent Forum", "https://forum.confluent.io/")
]

for name, url in candidates:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            print(f"[OK] {name}: {url} -> {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {name}: {url}")
    except Exception as ex:
        print(f"[ERR] {name}: {url} -> {ex}")
