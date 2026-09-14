import os, sys, json, subprocess
from PIL import Image

def generate_evidence():
    factory_dir = 'site-empire-factory'
    output_dir = os.path.join(factory_dir, 'output')

    evidence = {
        "git_gate": {},
        "quarantine_gate": {},
        "og_images_dimensions": {},
        "sample_properties": []
    }

    # 1. Git Gate
    try:
        p = subprocess.run(["git", "log", "-1", "--format=%H%n%an <%ae>%n%ad"], cwd=factory_dir, capture_output=True, text=True)
        evidence["git_gate"]["factory"] = p.stdout.strip().split("\n")
    except Exception as e:
        evidence["git_gate"]["factory"] = str(e)

    # 2. Quarantine Gate
    banned_occurrences = []
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if f.endswith(('.html', '.json', '.txt', '.xml')):
                fp = os.path.join(root, f)
                try:
                    c = open(fp, encoding='utf-8', errors='ignore').read()
                    if 'jibranpccc@gmail.com' in c:
                        banned_occurrences.append(fp)
                except Exception:
                    pass
    evidence["quarantine_gate"]["banned_found"] = len(banned_occurrences)
    evidence["quarantine_gate"]["status"] = "CLEAN (0 occurrences)" if len(banned_occurrences) == 0 else "FAIL"

    # 3. Image Dimensions Verification
    all_og_images = []
    for root, dirs, files in os.walk('.'):
        if 'og-preview.png' in files and ('output' in root or root in ['.\\developer-coding-hub', '.\\deals-loot-coupons-hub']):
            all_og_images.append(os.path.join(root, 'og-preview.png'))

    dimensions_match = 0
    for img_p in all_og_images:
        try:
            im = Image.open(img_p)
            if im.size == (1200, 630):
                dimensions_match += 1
        except Exception:
            pass

    evidence["og_images_dimensions"] = {
        "total_scanned": len(all_og_images),
        "exact_1200x630_count": dimensions_match,
        "compliance_rate": f"{(dimensions_match / len(all_og_images) * 100):.1f}%" if all_og_images else "0%"
    }

    # 4. Detailed samples from 5 diverse platforms (GitHub Pages, Netlify, Vercel)
    sample_slugs = [
        "developer-coding-hub", # Root GitHub Pages
        "no-code-automation-hub", # Output Vercel
        "rust-systems-engineering-hub", # Output Netlify
        "deals-loot-coupons-hub", # Root Flagship
        "music-production-audio-engineering-hub" # Output Netlify
    ]

    for slug in sample_slugs:
        p_dir = os.path.join(output_dir, slug)
        if not os.path.exists(p_dir):
            p_dir = os.path.join('.', slug)
        
        if os.path.exists(p_dir):
            idx = os.path.join(p_dir, 'index.html')
            c = open(idx, encoding='utf-8', errors='ignore').read()
            
            # Extract headers, canonical, og:image, details count
            has_headers_file = os.path.exists(os.path.join(p_dir, '_headers'))
            has_vercel_headers = False
            v_path = os.path.join(p_dir, 'vercel.json')
            if os.path.exists(v_path):
                v_data = json.load(open(v_path, encoding='utf-8'))
                has_vercel_headers = 'headers' in v_data
            
            details_count = c.count('<details')
            has_og_meta = 'og:image' in c
            has_tw_meta = 'twitter:image' in c
            canonical_match = "link rel=\"canonical\"" in c
            
            evidence["sample_properties"].append({
                "slug": slug,
                "path": p_dir,
                "details_faq_elements": details_count,
                "canonical_present": canonical_match,
                "og_image_meta": has_og_meta,
                "twitter_image_meta": has_tw_meta,
                "netlify_headers_file": has_headers_file,
                "vercel_json_headers": has_vercel_headers
            })

    evidence_path = os.path.join(factory_dir, 'boss_verification_evidence.json')
    with open(evidence_path, 'w', encoding='utf-8') as f:
        json.dump(evidence, f, indent=2)
    print("Boss verification evidence compiled successfully!")
    print(json.dumps(evidence, indent=2))

if __name__ == '__main__':
    generate_evidence()
