import re

def verify_site(slug):
    path = f"output/{slug}/index.html"
    print(f"=== Verifying {slug} ===")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    cards = re.findall(r'<div id="community-card-\d+"', html)
    print(f"Cards count: {len(cards)}")
    assert len(cards) == 30, f"Expected 30 cards, got {len(cards)}"

    copy_links = re.findall(r'onclick="copyInviteLink\(event, \'([^\']+)\'\)"', html)
    print(f"Copy links count: {len(copy_links)}")
    assert len(copy_links) == 30, f"Expected 30 copy links, got {len(copy_links)}"

    join_links = re.findall(r'<a href="([^"]+)" target="_blank" rel="noopener noreferrer" class="btn-join">', html)
    print(f"Join links count: {len(join_links)}")
    assert len(join_links) == 30, f"Expected 30 join links, got {len(join_links)}"

    for i in range(30):
        assert copy_links[i] == join_links[i], f"Mismatch at {i}: {copy_links[i]} vs {join_links[i]}"
        u = copy_links[i]
        assert u.startswith(("https://www.reddit.com/r/", "https://discord.gg/", "https://t.me/")), f"Invalid domain: {u}"
        assert not any(b in u for b in ["community/", "example", "placeholder", "{", "}"]), f"Fake pattern in {u}"
        print(f"  Card {i+1:2d}: {u}")

    print(f">>> ALL 30 CARDS IN {slug} VERIFIED PERFECTLY! <<<\n")

verify_site("fire-personal-finance-hub")
verify_site("dividend-growth-investing-hub")
