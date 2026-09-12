import json
from urllib.parse import urlparse

with open("fleet1_audit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

urls = data["unique_community_urls"]
print(f"Total Unique Community URLs: {len(urls)}")

domains = {}
for u in urls:
    p = urlparse(u)
    domain = p.netloc.lower()
    domains[domain] = domains.get(domain, 0) + 1

print("\n--- Domain Distribution ---")
for dom, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
    print(f"  {dom}: {count}")

# Check any suspicious or strange URLs
suspicious = []
for u in urls:
    u_low = u.lower()
    if any(k in u_low for k in ["example", "placeholder", "test", "dummy", "fake", "temp", "foo", "bar", "127.0.0.1", "localhost"]):
        suspicious.append(u)

print(f"\nSuspicious URLs found: {len(suspicious)}")
for s in suspicious:
    print(f"  {s}")
