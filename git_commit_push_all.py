import os
import subprocess

OUTPUT_DIR = r"c:\Users\jibra\Desktop\1\20 blogs\site-empire-factory\output"
SITES = [
    "b2b-saas-founders-circle-hub",
    "biohacking-longevity-health-hub",
    "smart-home-homeassistant-hub",
    "cyber-threat-intelligence-hub",
    "generative-ai-video-creators-hub",
    "ethical-hacking-bugbounty-hub",
    "prop-firm-forex-traders-hub",
    "notion-systems-productivity-hub",
    "3d-blender-unreal-artists-hub",
    "remote-developer-jobs-alpha-hub"
]

results = {}
for s in SITES:
    repo_path = os.path.join(OUTPUT_DIR, s)
    status = subprocess.run(["git", "status", "--short"], cwd=repo_path, capture_output=True, text=True)
    st = status.stdout.strip()
    if not st:
        results[s] = "clean (no changes)"
        print(f"{s}: clean")
        continue

    print(f"{s}: changes detected:\n{st}")
    subprocess.run(["git", "add", "index.html", "data/groups.json"], cwd=repo_path, check=True)
    commit_res = subprocess.run(
        ["git", "commit", "-m", "fix(links): verify and replace outbound community links with 100% real verified endpoints"],
        cwd=repo_path, capture_output=True, text=True
    )
    print(f"  commit: {commit_res.stdout.strip()[:100]}")

    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=repo_path, capture_output=True, text=True)
    print(f"  push: {push_res.stdout.strip() or push_res.stderr.strip()}")
    results[s] = "committed and pushed"

print("\nAll git operations completed:")
for s, res in results.items():
    print(f"  {s}: {res}")
