import os, re

patterns = [
    r'telegram\.com/community',
    r'discord\.com/community',
    r'whatsapp\.com/community',
    r'reddit\.com/community'
]

def scan_dir(d):
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(('.html', '.xml', '.txt', '.json')):
                fp = os.path.join(root, file)
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        c = f.read()
                    for p in patterns:
                        m = re.findall(p, c)
                        if m:
                            print(f'{fp}: {len(m)} matches of {p}')
                except Exception as e:
                    pass

scan_dir('output/fire-personal-finance-hub')
scan_dir('output/dividend-growth-investing-hub')
