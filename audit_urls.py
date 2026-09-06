import json, re

def audit_file(path):
    print('--- Auditing ' + path + ' ---')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fake_patterns = [
        r'telegram\.com/community',
        r'discord\.com/community',
        r'whatsapp\.com/community',
        r'reddit\.com/community',
    ]
    total = 0
    for pat in fake_patterns:
        matches = re.findall(pat, content)
        print('  Pattern ' + pat + ': ' + str(len(matches)) + ' occurrences')
        total += len(matches)
    print('  Total fake occurrences: ' + str(total))

audit_file('output/fire-personal-finance-hub/index.html')
audit_file('output/fire-personal-finance-hub/data/groups.json')
audit_file('output/dividend-growth-investing-hub/index.html')
audit_file('output/dividend-growth-investing-hub/data/groups.json')
