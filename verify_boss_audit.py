import os

def verify_all_properties():
    factory_dir = 'site-empire-factory'
    output_dir = os.path.join(factory_dir, 'output')
    
    all_dirs = []
    for d in os.listdir('.'):
        p = os.path.join('.', d)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'index.html')) and os.path.exists(os.path.join(p, 'feed.xml')):
            all_dirs.append(p)
    if os.path.exists(output_dir):
        for d in os.listdir(output_dir):
            p = os.path.join(output_dir, d)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, 'index.html')):
                all_dirs.append(p)

    total = len(all_dirs)
    faq_ok = 0
    og_img_ok = 0
    headers_ok = 0
    vercel_ok = 0
    fake_links = 0
    banned_email = 0

    for site_p in all_dirs:
        idx_p = os.path.join(site_p, 'index.html')
        content = open(idx_p, encoding='utf-8', errors='ignore').read()
        if 'id="faq"' in content and 'class="faq-section"' in content:
            faq_ok += 1
        else:
            print(f"Missing FAQ in: {site_p}")
        
        og_p = os.path.join(site_p, 'og-preview.png')
        if os.path.exists(og_p) and os.path.getsize(og_p) > 2000:
            og_img_ok += 1
            
        h_p = os.path.join(site_p, '_headers')
        if os.path.exists(h_p) and 'Strict-Transport-Security' in open(h_p, encoding='utf-8').read():
            headers_ok += 1
            
        v_p = os.path.join(site_p, 'vercel.json')
        if os.path.exists(v_p) and 'headers' in open(v_p, encoding='utf-8').read():
            vercel_ok += 1
            
        for banned in ['telegram.com/community', 'discord.com/community', 'whatsapp.com/community', 'reddit.com/community']:
            if banned in content:
                fake_links += 1
                
        if 'jibranpccc@gmail.com' in content:
            banned_email += 1

    print("=======================================================")
    print("👑 AUDIT RESULTS: BOSS DEEPSEEK DIRECTIVES")
    print("=======================================================")
    print(f"Total Site Directories Audited: {total}")
    print(f"1. Physical FAQ Accordions Active: {faq_ok}/{total} ({(faq_ok/total)*100:.1f}%)")
    print(f"2. High-Contrast Social Previews (og-preview.png): {og_img_ok}/{total} ({(og_img_ok/total)*100:.1f}%)")
    print(f"3. Netlify/Cloudflare Security _headers Deployed: {headers_ok}/{total} ({(headers_ok/total)*100:.1f}%)")
    print(f"4. Vercel Security Headers Configured: {vercel_ok}/{total} ({(vercel_ok/total)*100:.1f}%)")
    print(f"5. Synthetic / Fake Links Detected: {fake_links}")
    print(f"6. Banned Email Occurrences: {banned_email}")
    print("=======================================================")

if __name__ == '__main__':
    verify_all_properties()
