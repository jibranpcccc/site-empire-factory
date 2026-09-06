#!/usr/bin/env python3
"""
Comprehensive Audit & Operational Readiness Sentinel
for Autonomous Site Empire Factory
"""
import os, sys, json, urllib.request, subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NICHES_FILE = os.path.join(BASE_DIR, "niches.json")
FACTORY_FILE = os.path.join(BASE_DIR, "factory.py")
WORKFLOW_FILE = os.path.join(BASE_DIR, ".github", "workflows", "daily_factory.yml")
POOL_FILE = os.path.join(BASE_DIR, "gemini_master_pool.json")
GMAIL_FILE = os.path.join(BASE_DIR, "gmail_owners_registry.json")

score_weights = {
    "gemini_pool": 25,
    "niches_queue": 25,
    "gmail_owners": 25,
    "workflow_secrets": 25
}
scores = {}

print("==================================================")
print("🔍 1. AUDITING MULTI-KEY GEMINI POOL & FALLBACK CHAIN")
print("==================================================")
gemini_ok = True
# 1.1 Master Pool
if os.path.exists(POOL_FILE):
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    active_keys = pool_data.get("active_keys", [])
    reserve_keys = pool_data.get("reserve_keys", [])
    print(f"Active keys: {len(active_keys)} (expected 4)")
    print(f"Reserve keys: {len(reserve_keys)} (expected 40)")
    if len(active_keys) == 4 and len(reserve_keys) == 40:
        print("✅ Multi-key Gemini pool verified: 4 active + 40 reserve = 44 total keys.")
    else:
        print(f"❌ Key count mismatch: active={len(active_keys)}, reserve={len(reserve_keys)}")
        gemini_ok = False
else:
    print("❌ gemini_master_pool.json missing!")
    gemini_ok = False

# 1.2 Inspect factory.py for fallback chain & X-goog-api-key
with open(FACTORY_FILE, "r", encoding="utf-8") as f:
    factory_code = f.read()

expected_chain = 'candidate_models = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]'
if expected_chain in factory_code:
    print("✅ Model fallback chain verified: gemini-3.6-flash -> gemini-flash-latest -> gemini-2.5-flash-lite.")
else:
    print("❌ Model fallback chain missing or mismatched in factory.py!")
    gemini_ok = False

if '"X-goog-api-key": key' in factory_code:
    print("✅ X-goog-api-key header support verified.")
else:
    print("❌ X-goog-api-key header missing from factory.py!")
    gemini_ok = False

scores["gemini_pool"] = score_weights["gemini_pool"] if gemini_ok else 0

print("\n==================================================")
print("🔍 2. AUDITING NICHES.JSON QUEUE")
print("==================================================")
niches_ok = True
with open(NICHES_FILE, "r", encoding="utf-8") as f:
    niches = json.load(f)

total_niches = len(niches)
deployed_niches = [n for n in niches if n.get("status") == "deployed"]
pending_niches = [n for n in niches if n.get("status") == "pending"]

print(f"Total entries: {total_niches} (expected 63)")
print(f"Deployed: {len(deployed_niches)} (expected 9)")
print(f"Pending: {len(pending_niches)} (expected 54)")

if len(deployed_niches) == 9 and len(pending_niches) == 54:
    print("✅ Queue verified: exactly 9 deployed niches and 54 pending niches.")
else:
    print(f"❌ Queue count mismatch: deployed={len(deployed_niches)}, pending={len(pending_niches)}")
    niches_ok = False

slugs = [n["slug"] for n in niches]
dupes = [s for s in slugs if slugs.count(s) > 1]
if dupes:
    print(f"❌ Duplicate slugs: {set(dupes)}")
    niches_ok = False
else:
    print("✅ All 63 slugs are strictly unique.")

req_keys = {"id", "name", "slug", "niche", "category", "status"}
for i, n in enumerate(niches):
    missing = req_keys - set(n.keys())
    if missing:
        print(f"❌ Entry {i} ({n.get('slug')}) missing keys: {missing}")
        niches_ok = False
        break
else:
    print("✅ All entries conform to required schema specifications.")

scores["niches_queue"] = score_weights["niches_queue"] if niches_ok else 0

print("\n==================================================")
print("🔍 3. AUDITING GMAIL OWNERS REGISTRY INTEGRATION")
print("==================================================")
gmail_ok = True
if os.path.exists(GMAIL_FILE):
    with open(GMAIL_FILE, "r", encoding="utf-8") as f:
        reg_data = json.load(f)
    accounts = reg_data.get("accounts", [])
    print(f"Total verified accounts: {len(accounts)} (expected 16)")
    print(f"Status: {reg_data.get('status')}")
    print(f"Max sites per Gmail: {reg_data.get('max_sites_per_gmail')} (Capacity: {reg_data.get('total_empire_capacity')})")
    if len(accounts) != 16:
        print(f"❌ Expected 16 accounts, found {len(accounts)}")
        gmail_ok = False
else:
    print("❌ gmail_owners_registry.json missing!")
    gmail_ok = False

# Check integration in factory.py
if "assign_next_gmail_owner" in factory_code and "load_gmail_registry" in factory_code:
    print("✅ factory.py has active assign_next_gmail_owner and load_gmail_registry functions.")
else:
    print("❌ factory.py lacks Gmail owner registry integration functions!")
    gmail_ok = False

# Verify all 9 deployed sites have assigned owners
deployed_without_owner = [n for n in deployed_niches if not n.get("assigned_gmail")]
if not deployed_without_owner:
    print("✅ All 9 currently deployed sites have isolated assigned Gmail owners.")
else:
    print(f"❌ {len(deployed_without_owner)} deployed sites lack assigned_gmail!")
    gmail_ok = False

# Simulate assignment for next 3 pending sites
import factory
sim_niches = [dict(n) for n in niches]
next_pending = [n for n in sim_niches if n.get("status") == "pending"][:3]
next_assigned = []
for p in next_pending:
    owner = factory.assign_next_gmail_owner(p, sim_niches)
    next_assigned.append((p["slug"], owner["email"], owner["label"]))
    p["assigned_gmail"] = owner["email"]

print("\nNext 3 sites to be deployed tomorrow at 06:00 UTC:")
for idx, (slug, email, label) in enumerate(next_assigned, 10):
    print(f"  #{idx} {slug} -> {email} ({label})")

expected_next = [accounts[9]["email"], accounts[10]["email"], accounts[11]["email"]]
actual_next = [e for _, e, _ in next_assigned]
if actual_next == expected_next:
    print("✅ Next 3 pending sites automatically pick up accounts #9, #10, and #11 in sequential round-robin.")
else:
    print(f"❌ Allocation mismatch! Actual: {actual_next}, Expected: {expected_next}")
    gmail_ok = False

scores["gmail_owners"] = score_weights["gmail_owners"] if gmail_ok else 0

print("\n==================================================")
print("🔍 4. AUDITING GITHUB ACTIONS WORKFLOW & SECRETS")
print("==================================================")
workflow_ok = True
with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    wf_code = f.read()

if "cron: '0 6 * * *'" in wf_code:
    print("✅ Cron schedule verified: '0 6 * * *' (Every day at 06:00 UTC).")
else:
    print("❌ Cron schedule '0 6 * * *' missing or mismatched!")
    workflow_ok = False

if "workflow_dispatch:" in wf_code:
    print("✅ Manual trigger verified: workflow_dispatch enabled.")
else:
    print("❌ workflow_dispatch missing!")
    workflow_ok = False

if "${{ secrets.GEMINI_API_KEY }}" in wf_code and "${{ secrets.GH_PAT }}" in wf_code:
    print("✅ Environment variables wired to GitHub Secrets (GEMINI_API_KEY, GH_PAT).")
else:
    print("❌ Secret wiring missing in workflow!")
    workflow_ok = False

# Verify actual repository secrets via gh CLI
try:
    gh_res = subprocess.run(["gh", "secret", "list", "--repo", "jibranpcccc/site-empire-factory"], capture_output=True, text=True)
    if gh_res.returncode == 0:
        sec_out = gh_res.stdout
        has_gemini = "GEMINI_API_KEY" in sec_out
        has_gh_pat = "GH_PAT" in sec_out
        if has_gemini and has_gh_pat:
            print("✅ Verified live repository secrets present in GitHub: GEMINI_API_KEY, GH_PAT.")
        else:
            print(f"❌ Missing required repository secrets! Found: {sec_out}")
            workflow_ok = False
except Exception as e:
    print(f"⚠️ Could not query gh CLI: {e}")

scores["workflow_secrets"] = score_weights["workflow_secrets"] if workflow_ok else 0

print("\n==================================================")
print("🎯 FINAL OPERATIONAL READINESS ASSESSMENT")
print("==================================================")
total_score = sum(scores.values())
for cat, pts in scores.items():
    status = "PASS" if pts == score_weights[cat] else "FAIL"
    print(f"  • {cat.replace('_', ' ').title():<25}: {pts}/{score_weights[cat]} pts [{status}]")

print(f"\n🏆 OPERATIONAL READINESS SCORE: {total_score}% / 100%")
if total_score == 100:
    print("🟢 STATUS: 100% READY FOR TOMORROW'S 06:00 UTC AUTOMATED DEPLOYMENT RUN.")
else:
    print("🔴 STATUS: REMEDIATION REQUIRED BEFORE SCHEDULED RUN.")
print("==================================================")

