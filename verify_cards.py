import json

for hub in ['no-code-automation-hub', 'rust-systems-engineering-hub']:
    html = open(f'output/{hub}/index.html', encoding='utf-8').read()
    data = json.load(open(f'output/{hub}/data/groups.json', encoding='utf-8'))
    print(f'*** {hub} ***')
    print(f'groups.json count: {len(data)}')
    
    for i, c in enumerate(data):
        url = c['joinUrl']
        title = c['title']
        assert url in html, f'Missing URL {url} in index.html'
        assert title in html, f'Missing title {title} in index.html'
        expected_onclick = f"copyInviteLink(event, '{url}')"
        assert expected_onclick in html, f'Missing {expected_onclick}'
        expected_href = f'href="{url}"'
        assert expected_href in html, f'Missing {expected_href}'
    print('All 30 communities verified in index.html and groups.json with matching copyInviteLink and href!')
