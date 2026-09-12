import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0"}

test_urls = [
    # CNCF
    ("CNCF Community", "https://community.cncf.io/"),
    ("CNCF Slack", "https://slack.cncf.io/"),
    # GrowthHackers
    ("GrowthHackers Home", "https://growthhackers.com/"),
    ("GrowthHacking Reddit", "https://www.reddit.com/r/growthhacking/"),
    # CERN
    ("CERN Careers Home", "https://careers.cern/"),
    ("CERN Home", "https://home.cern/summer-student-programme"),
    ("CERN Students Portal", "https://careers.cern/early-career"),
    # Italy
    ("Study in Italy Esteri", "https://studyinitaly.esteri.it/"),
    ("Esteri Home", "https://www.esteri.it/en/opportunita/borse-di-studio/per-cittadini-stranieri/"),
    # Taiwan
    ("Taiwan Scholarship MOE", "https://taiwanscholarship.moe.gov.tw/"),
    ("Taiwan MOE English", "https://english.moe.gov.tw/"),
    # A*STAR SINGA
    ("A*STAR Scholarships", "https://www.a-star.edu.sg/scholarships"),
    ("A*STAR Home", "https://www.a-star.edu.sg/")
]

for name, url in test_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            print(f"[OK {resp.status}] {name}: {url}")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {name}: {url}")
    except Exception as ex:
        print(f"[ERR] {name}: {url} -> {ex}")
