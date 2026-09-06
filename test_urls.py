import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://www.reddit.com/r/financialindependence/',
    'https://www.reddit.com/r/FIREyFemmes/',
    'https://www.reddit.com/r/leanfire/',
    'https://www.reddit.com/r/fatFIRE/',
    'https://www.reddit.com/r/personalfinance/',
    'https://www.reddit.com/r/Bogleheads/',
    'https://www.reddit.com/r/PovertyFinance/',
    'https://www.reddit.com/r/ChubbyFIRE/',
    'https://www.reddit.com/r/CoastFIRE/',
    'https://www.reddit.com/r/BaristaFIRE/',
    'https://www.reddit.com/r/frugal/',
    'https://www.reddit.com/r/FIREUK/',
    'https://www.reddit.com/r/fiaustralia/',
    'https://www.reddit.com/r/eupersonalfinance/',
    'https://www.reddit.com/r/FIRE_Ind/',
    'https://www.reddit.com/r/ETFs/',
    'https://www.reddit.com/r/MiddleClassFinance/',
    'https://www.reddit.com/r/fican/',
    'https://discord.gg/personalfinance',
    'https://discord.gg/fire',
    'https://discord.gg/bogleheads',
    'https://discord.gg/investing',
    'https://discord.gg/finance',
    'https://t.me/financialindependence',
    'https://t.me/personalfinance',
    'https://t.me/bogleheads',
    'https://t.me/dividendinvestors',
    'https://t.me/wealthbuilding',
    'https://t.me/passiveincome',
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            print(f'OK {resp.status}: {u}')
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {u}')
    except Exception as e:
        print(f'ERR {e}: {u}')
