import subprocess, sys

hub17_urls = [
    'https://www.reddit.com/r/financialindependence/',
    'https://www.reddit.com/r/personalfinance/',
    'https://www.reddit.com/r/Bogleheads/',
    'https://www.reddit.com/r/leanfire/',
    'https://www.reddit.com/r/fatFIRE/',
    'https://www.reddit.com/r/FIREyFemmes/',
    'https://www.reddit.com/r/ChubbyFIRE/',
    'https://www.reddit.com/r/CoastFIRE/',
    'https://www.reddit.com/r/BaristaFIRE/',
    'https://www.reddit.com/r/PovertyFinance/',
    'https://www.reddit.com/r/frugal/',
    'https://www.reddit.com/r/FIREUK/',
    'https://www.reddit.com/r/fiaustralia/',
    'https://www.reddit.com/r/eupersonalfinance/',
    'https://www.reddit.com/r/FIRE_Ind/',
    'https://www.reddit.com/r/ETFs/',
    'https://www.reddit.com/r/MiddleClassFinance/',
    'https://www.reddit.com/r/fican/',
    'https://www.reddit.com/r/investing/',
    'https://www.reddit.com/r/stocks/',
    'https://discord.gg/personalfinance',
    'https://discord.gg/fire',
    'https://discord.gg/bogleheads',
    'https://discord.gg/investing',
    'https://discord.gg/finance',
    'https://t.me/financialindependence',
    'https://t.me/personalfinance',
    'https://t.me/bogleheads',
    'https://t.me/wealthbuilding',
    'https://t.me/passiveincome'
]

hub18_urls = [
    'https://www.reddit.com/r/dividends/',
    'https://www.reddit.com/r/dividendinvesting/',
    'https://www.reddit.com/r/passive_income/',
    'https://www.reddit.com/r/investing/',
    'https://www.reddit.com/r/stocks/',
    'https://www.reddit.com/r/ValueInvesting/',
    'https://www.reddit.com/r/incomeinvesting/',
    'https://www.reddit.com/r/qyldgang/',
    'https://www.reddit.com/r/CanadianInvestor/',
    'https://www.reddit.com/r/ukinvesting/',
    'https://www.reddit.com/r/SecurityAnalysis/',
    'https://www.reddit.com/r/reits/',
    'https://www.reddit.com/r/Bogleheads/',
    'https://www.reddit.com/r/financialindependence/',
    'https://www.reddit.com/r/ETFs/',
    'https://www.reddit.com/r/StockMarket/',
    'https://www.reddit.com/r/smallstreetbets/',
    'https://www.reddit.com/r/personalfinance/',
    'https://www.reddit.com/r/Frugal/',
    'https://www.reddit.com/r/options/',
    'https://discord.gg/dividends',
    'https://discord.gg/investing',
    'https://discord.gg/stocks',
    'https://discord.gg/valueinvesting',
    'https://discord.gg/passiveincome',
    'https://discord.gg/finance',
    'https://t.me/dividendinvestors',
    'https://t.me/valueinvesting',
    'https://t.me/passiveincome',
    'https://t.me/financialindependence'
]

def check(urls, name):
    print(f'Checking {name} ({len(urls)} URLs)...')
    for u in urls:
        p = subprocess.run(['curl.exe', '-s', '-I', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', u], capture_output=True, text=True)
        status_line = p.stdout.split('\n')[0].strip() if p.stdout else 'NO OUTPUT'
        is_404 = '404' in status_line
        status_code = status_line[:20]
        print(f'{status_code:20} -> {u}')
        if is_404:
            print(f'  >>> 404 DETECTED: {u}')

check(hub17_urls, 'Hub 17')
check(hub18_urls, 'Hub 18')
