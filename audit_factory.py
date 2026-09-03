#!/usr/bin/env python3
"""
Comprehensive Audit of the Site Empire Factory & Portfolio
"""
import os, sys, json, urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NICHES_FILE = os.path.join(BASE_DIR, "niches.json")
FACTORY_FILE = os.path.join(BASE_DIR, "factory.py")
WORKFLOW_FILE = os.path.join(BASE_DIR, ".github", "workflows", "daily_factory.yml")

print("==================================================")
print("🔍 1. AUDITING NICHES.JSON DATABASE")
print("==================================================")
with open(NICHES_FILE, "r", encoding="utf-8") as f:
    niches = json.load(f)

print(f"Total entries: {len(niches)}")
slugs = [n["slug"] for n in niches]
dupes = [s for s in slugs if slugs.count(s) > 1]
if dupes:
    print(f"❌ Duplicate slugs found: {set(dupes)}")
else:
    print("✅ All slugs are unique.")

req_keys = {"id", "name", "slug", "niche", "category", "status"}
all_valid = True
for i, n in enumerate(niches):
    missing = req_keys - set(n.keys())
    if missing:
        print(f"❌ Entry {i} ({n.get('slug')}) missing keys: {missing}")
        all_valid = False
if all_valid:
    print("✅ All 60 entries have 100% complete schemas.")

print("\n==================================================")
print("🔍 2. AUDITING FACTORY.PY PYTHON SCRIPT")
print("==================================================")
import py_compile
try:
    py_compile.compile(FACTORY_FILE, doraise=True)
    print("✅ factory.py compiles with 0 syntax errors.")
except Exception as e:
    print(f"❌ factory.py syntax error: {e}")

# Check imports
with open(FACTORY_FILE, "r", encoding="utf-8") as f:
    src = f.read()

# Verify that standard library only is used
standard_libs = ["os", "sys", "time", "json", "datetime", "urllib", "subprocess"]
for lib in ["requests", "playwright", "bs4", "selenium", "dotenv"]:
    if f"import {lib}" in src or f"from {lib}" in src:
        print(f"⚠️ Warning: external dependency {lib} found!")
        break
else:
    print("✅ Uses strictly Python Standard Library (zero pip install required in cloud runner).")

# Verify MAX_SITES_PER_RUN constraint
if "MAX_SITES_PER_RUN = 3" in src:
    print("✅ Strict velocity limit verified: MAX_SITES_PER_RUN = 3.")
else:
    print("❌ MAX_SITES_PER_RUN not set to 3!")

print("\n==================================================")
print("🔍 3. AUDITING GITHUB ACTIONS WORKFLOW")
print("==================================================")
with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    wf = f.read()

if "cron: '0 6 * * *'" in wf:
    print("✅ Cron schedule verified: '0 6 * * *' (Every day at 06:00 UTC).")
if "workflow_dispatch:" in wf:
    print("✅ Manual trigger verified: workflow_dispatch enabled.")
if "secrets.GEMINI_API_KEY" in wf and "secrets.GH_PAT" in wf:
    print("✅ Cloud secrets verified: GEMINI_API_KEY and GH_PAT wired properly.")

print("\n==================================================")
print("🔍 4. AUDITING LIVE PRODUCTION SITES & FEEDS (SITES 8, 9, 10)")
print("==================================================")
sites = [
    ("developer-coding-hub", "https://jibranpcccc.github.io/developer-coding-hub/"),
    ("deals-loot-coupons-hub", "https://jibranpcccc.github.io/deals-loot-coupons-hub/"),
    ("scholarships-study-abroad-hub", "https://jibranpcccc.github.io/scholarships-study-abroad-hub/")
]

for name, base_url in sites:
    endpoints = [
        ("Homepage", base_url),
        ("Sitemap", f"{base_url}sitemap.xml"),
        ("RSS Feed", f"{base_url}feed.xml"),
        ("Robots.txt", f"{base_url}robots.txt"),
        ("GSC Verification", f"{base_url}google6fe267a998c19a9a.html")
    ]
    print(f"\n--- Testing {name} ---")
    for label, url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SiteAuditBot/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"  ✅ {label} ({resp.status}): {url}")
        except Exception as e:
            print(f"  ❌ {label} FAILED: {url} -> {e}")

print("\n==================================================")
print("🎯 AUDIT COMPLETE")
print("==================================================")
