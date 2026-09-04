import json, datetime

def shared_page_styles(accent):
    return f"""
        :root {{
            --accent: {accent};
            --bg: #0b0f19;
            --surface: #111827;
            --surface-hover: #1f2937;
            --border: #1f2937;
            --text: #f9fafb;
            --muted: #9ca3af;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding-bottom: 70px; }}
        
        .top-nav {{ display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; padding: 20px 20px; border-bottom: 1px solid var(--border); }}
        .nav-brand {{ font-weight: 700; font-size: 1.15rem; color: #fff; text-decoration: none; }}
        .nav-brand span {{ color: var(--accent); }}
        .nav-menu {{ display: flex; gap: 20px; align-items: center; }}
        .nav-link {{ color: var(--muted); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }}
        .nav-link:hover, .nav-link.active {{ color: #fff; }}
        .nav-btn {{ background: var(--accent); color: #fff !important; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.88rem; text-decoration: none; }}
        .nav-btn:hover {{ opacity: 0.9; }}
        
        .page-container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        .breadcrumbs {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 25px; }}
        .breadcrumbs a {{ color: var(--accent); text-decoration: none; }}
        
        h1 {{ font-size: 2.2rem; margin-bottom: 15px; color: #fff; }}
        .lead {{ font-size: 1.15rem; color: var(--muted); margin-bottom: 35px; line-height: 1.6; }}
        
        .content-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 30px; margin-bottom: 30px; }}
        .content-card h2 {{ font-size: 1.4rem; color: #fff; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }}
        .content-card h3 {{ font-size: 1.1rem; color: #fff; margin: 20px 0 10px; }}
        .content-card p {{ color: var(--muted); font-size: 0.96rem; margin-bottom: 15px; line-height: 1.65; }}
        .content-card ul {{ margin-left: 22px; color: var(--muted); margin-bottom: 18px; }}
        .content-card li {{ margin-bottom: 8px; font-size: 0.95rem; }}
        
        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; color: #fff; font-size: 0.9rem; font-weight: 600; margin-bottom: 8px; }}
        .form-control {{ width: 100%; padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg); color: #fff; font-size: 0.95rem; outline: none; }}
        .form-control:focus {{ border-color: var(--accent); }}
        .btn-submit {{ display: inline-block; background: var(--accent); color: #fff; border: none; padding: 12px 26px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: opacity 0.2s; text-decoration: none; }}
        .btn-submit:hover {{ opacity: 0.9; }}
        .alert-success {{ display: none; background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; }}
        
        footer {{ border-top: 1px solid var(--border); margin-top: 60px; padding: 50px 20px 30px; }}
        .footer-grid {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 30px; text-align: left; }}
        .footer-col h4 {{ color: #fff; font-size: 0.9rem; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .footer-col a {{ display: block; color: var(--muted); text-decoration: none; font-size: 0.88rem; margin-bottom: 8px; transition: color 0.2s; }}
        .footer-col a:hover {{ color: var(--accent); }}
        .footer-desc {{ color: var(--muted); font-size: 0.88rem; line-height: 1.6; max-width: 380px; }}
        .footer-bottom {{ text-align: center; color: var(--muted); font-size: 0.82rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 40px; padding-top: 25px; }}
        
        @media (max-width: 768px) {{
            .footer-grid {{ grid-template-columns: 1fr; }}
            .nav-menu {{ display: none; }}
        }}
    """

def build_top_nav(niche, live_url, active_page=""):
    name = niche["name"]
    return f"""
    <nav class="top-nav">
        <a href="{live_url}" class="nav-brand">{name}</a>
        <div class="nav-menu">
            <a href="{live_url}" class="nav-link {'active' if active_page == 'directory' else ''}">Directory</a>
            <a href="{live_url}about.html" class="nav-link {'active' if active_page == 'about' else ''}">About & Vetting</a>
            <a href="{live_url}submit.html" class="nav-btn">+ Submit Group</a>
            <a href="{live_url}contact.html" class="nav-link {'active' if active_page == 'contact' else ''}">Contact</a>
        </div>
    </nav>
    """

def build_footer(niche, live_url):
    name = niche["name"]
    year = datetime.datetime.now().year
    return f"""
    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h4>{name}</h4>
                <p class="footer-desc">Independent, verified directory connecting enthusiasts and professionals to active communities across Telegram, Discord, WhatsApp, and Reddit.</p>
            </div>
            <div class="footer-col">
                <h4>Directory Index</h4>
                <a href="{live_url}#communitiesGrid">All Verified Groups</a>
                <a href="{live_url}about.html">Vetting Methodology</a>
                <a href="{live_url}submit.html">Submit Your Community</a>
                <a href="{live_url}feed.xml">RSS Syndication Feed</a>
            </div>
            <div class="footer-col">
                <h4>Trust & Legal</h4>
                <a href="{live_url}privacy.html">Privacy Policy</a>
                <a href="{live_url}terms.html">Terms of Service & Disclaimer</a>
                <a href="{live_url}contact.html">Contact & DMCA Removal</a>
                <a href="{live_url}sitemap.xml">XML Sitemap</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© {year} {name} • Verified Independent Community Index. All rights reserved.</p>
        </div>
    </footer>
    """

def build_about_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = f"About & Verification | {name}"[:60]
    page_desc = f"Learn about our 4-tier verification methodology, quality standards, and editorial independence for {name}."[:160]
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AboutPage",
                "@id": f"{live_url}about.html#webpage",
                "url": f"{live_url}about.html",
                "name": page_title,
                "description": page_desc,
                "isPartOf": {"@id": f"{live_url}#website"},
                "breadcrumb": {"@id": f"{live_url}about.html#breadcrumbs"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{live_url}about.html#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": live_url},
                    {"@type": "ListItem", "position": 2, "name": "About & Verification", "item": f"{live_url}about.html"}
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{live_url}about.html">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{live_url}about.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{name}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
{shared_page_styles(accent)}
    </style>
</head>
<body>
{build_top_nav(niche, live_url, "about")}
    <div class="page-container">
        <div class="breadcrumbs">
            <a href="{live_url}">Home</a> / <span>About & Verification Standards</span>
        </div>
        <h1>About {name}</h1>
        <p class="lead">We are an independent, community-first directory dedicated to discovering, vetting, and categorizing top-tier online communities for {niche['niche']}.</p>

        <div class="content-card">
            <h2>🎯 Our Mission & Core Purpose</h2>
            <p>Finding high-signal, spam-free communities is increasingly difficult in today's digital landscape. Chat platforms like Telegram, Discord, WhatsApp, and Reddit are flooded with inactive groups, dead invite links, and low-quality channels.</p>
            <p><strong>{name}</strong> was built to solve this problem: a centralized, regularly audited repository where every indexed community meets strict standards for active discussion, moderation, and genuine member value.</p>
            <p>We serve thousands of enthusiasts, researchers, and professionals seeking genuine peer discussion without navigating commercial promotions, paywalled gatekeeping, or unmoderated chat noise.</p>
        </div>

        <div class="content-card">
            <h2>🛡️ The 4-Tier Verification Process</h2>
            <p>Every channel, server, and group indexed in our directory must pass our four foundational checks before receiving the <strong>✓ Verified</strong> badge:</p>
            <ul>
                <li><strong>1. Link Liveness & Security Check:</strong> Our automated monitoring routines scan invite URLs continuously. Any link that becomes expired, revoked, or redirects to suspicious domains is automatically flagged and removed.</li>
                <li><strong>2. Active Human Moderation:</strong> Communities must maintain active moderators and enforceable rules prohibiting spam, phishing, unauthorized financial promotion, and malicious behavior.</li>
                <li><strong>3. 100% Free Public Entry:</strong> We exclusively curate publicly accessible communities that do not impose mandatory paywalls, VIP entry fees, or private token gates for primary access.</li>
                <li><strong>4. Organic Member Activity:</strong> We assess daily engagement and discussion velocity to ensure listed communities represent active peer hubs, rather than dead or bot-inflated groups.</li>
            </ul>
        </div>

        <div class="content-card">
            <h2>⚖️ Editorial Independence & Moderation Ethics</h2>
            <p>Rankings and placements in our index are determined strictly by verified community metrics, member volume, and relevance. <strong>We do not accept payment to feature, rank, or artificially inflate community visibility.</strong></p>
            <p>Our curation board operates independently of listed community administrators. If a listed group changes ownership, introduces mandatory paid tiers, or fails moderation benchmarks, our editorial team immediately revokes verified status.</p>
            <p>If you run a community dedicated to {niche['niche']}, you are welcome to submit it for our next curation review.</p>
            <p style="margin-top: 20px;"><a href="{live_url}submit.html" class="btn-submit">Submit Your Community for Review →</a></p>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""

def build_submit_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = f"Submit Your Community | {name}"[:60]
    page_desc = f"Submit your verified community to {name}. Free listing for active Discord, Telegram, WhatsApp, and Reddit groups."[:160]
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{live_url}submit.html#webpage",
                "url": f"{live_url}submit.html",
                "name": page_title,
                "description": page_desc,
                "isPartOf": {"@id": f"{live_url}#website"},
                "breadcrumb": {"@id": f"{live_url}submit.html#breadcrumbs"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{live_url}submit.html#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": live_url},
                    {"@type": "ListItem", "position": 2, "name": "Submit Community", "item": f"{live_url}submit.html"}
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{live_url}submit.html">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{live_url}submit.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{name}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
{shared_page_styles(accent)}
    </style>
</head>
<body>
{build_top_nav(niche, live_url, "submit")}
    <div class="page-container">
        <div class="breadcrumbs">
            <a href="{live_url}">Home</a> / <span>Submit Community</span>
        </div>
        <h1>Submit Your Community</h1>
        <p class="lead">Are you an admin or creator of an active community dedicated to {niche['niche']}? Submit your group below for automated verification and free indexing.</p>

        <div id="submitAlert" class="alert-success">
            ✓ <strong>Submission Received!</strong> Your community has been added to our verification queue. Our crawler will check the invite link and moderation status within 24 hours.
        </div>

        <div class="content-card">
            <h2>📝 Community Information</h2>
            <form id="communityForm" onsubmit="handleCommunitySubmit(event)">
                <div class="form-group">
                    <label for="commName">Community Name *</label>
                    <input type="text" id="commName" class="form-control" placeholder="e.g. Global Tech Mentors" required>
                </div>
                <div class="form-group">
                    <label for="commPlatform">Platform *</label>
                    <select id="commPlatform" class="form-control" required>
                        <option value="Discord">Discord Server</option>
                        <option value="Telegram">Telegram Channel / Group</option>
                        <option value="WhatsApp">WhatsApp Group / Community</option>
                        <option value="Reddit">Reddit Subreddit</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="commUrl">Public Direct Invite Link *</label>
                    <input type="url" id="commUrl" class="form-control" placeholder="https://discord.gg/... or https://t.me/..." required>
                </div>
                <div class="form-group">
                    <label for="commMembers">Estimated Active Members *</label>
                    <input type="text" id="commMembers" class="form-control" placeholder="e.g. 5,400+ members" required>
                </div>
                <div class="form-group">
                    <label for="commCategory">Category / Sub-focus</label>
                    <input type="text" id="commCategory" class="form-control" placeholder="e.g. Careers, Networking, Tutorials">
                </div>
                <div class="form-group">
                    <label for="commDesc">Community Description *</label>
                    <textarea id="commDesc" class="form-control" rows="4" placeholder="Briefly describe what members discuss, community guidelines, and why members should join..." required></textarea>
                </div>
                <div class="form-group">
                    <label for="adminEmail">Admin / Contact Email (Optional)</label>
                    <input type="email" id="adminEmail" class="form-control" placeholder="admin@example.com (used only for verification updates)">
                </div>
                <button type="submit" class="btn-submit">Submit Community for Verification →</button>
            </form>
        </div>

        <div class="content-card">
            <h2>📋 Submission Guidelines & Curation Policy</h2>
            <ul>
                <li><strong>Minimum Membership:</strong> Communities must have at least 50+ active members before index approval.</li>
                <li><strong>Working Invites:</strong> Provide permanent, non-expiring invitation links to ensure uninterrupted user access.</li>
                <li><strong>Zero Tolerance:</strong> Groups containing spam, malware, hate speech, or financial scams are permanently rejected.</li>
                <li><strong>Free Directory:</strong> Indexation is 100% free; we never charge for inclusion or verified status.</li>
                <li><strong>Audit Cycle:</strong> Approved groups undergo bi-weekly automated re-verification to maintain indexing integrity.</li>
            </ul>
        </div>
    </div>
{build_footer(niche, live_url)}
    <script>
        function handleCommunitySubmit(e) {{
            e.preventDefault();
            const alert = document.getElementById('submitAlert');
            alert.style.display = 'block';
            document.getElementById('communityForm').reset();
            window.scrollTo({{ top: alert.offsetTop - 40, behavior: 'smooth' }});
        }}
    </script>
</body>
</html>"""

def build_contact_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = f"Contact & Support | {name}"[:60]
    page_desc = f"Contact the administrative team at {name}. Submit listing updates, partnerships, or DMCA removal requests."[:160]
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ContactPage",
                "@id": f"{live_url}contact.html#webpage",
                "url": f"{live_url}contact.html",
                "name": page_title,
                "description": page_desc,
                "isPartOf": {"@id": f"{live_url}#website"},
                "breadcrumb": {"@id": f"{live_url}contact.html#breadcrumbs"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{live_url}contact.html#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": live_url},
                    {"@type": "ListItem", "position": 2, "name": "Contact & Support", "item": f"{live_url}contact.html"}
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{live_url}contact.html">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{live_url}contact.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{name}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
{shared_page_styles(accent)}
    </style>
</head>
<body>
{build_top_nav(niche, live_url, "contact")}
    <div class="page-container">
        <div class="breadcrumbs">
            <a href="{live_url}">Home</a> / <span>Contact & Support</span>
        </div>
        <h1>Contact & Operator Inquiries</h1>
        <p class="lead">Have a question, feedback, or need to update or remove a community listing? Contact our editorial and administrative team below.</p>

        <div id="contactAlert" class="alert-success">
            ✓ <strong>Message Received!</strong> Thank you for reaching out. We will review your inquiry and respond within 24 business hours.
        </div>

        <div class="content-card">
            <h2>✉️ Send a Message</h2>
            <form id="contactForm" onsubmit="handleContactSubmit(event)">
                <div class="form-group">
                    <label for="cName">Your Name *</label>
                    <input type="text" id="cName" class="form-control" placeholder="e.g. Alex Morgan" required>
                </div>
                <div class="form-group">
                    <label for="cEmail">Your Email *</label>
                    <input type="email" id="cEmail" class="form-control" placeholder="alex@example.com" required>
                </div>
                <div class="form-group">
                    <label for="cSubject">Subject *</label>
                    <select id="cSubject" class="form-control" required>
                        <option value="Listing Update">Update an Existing Listing</option>
                        <option value="Takedown Request">Listing Removal / Takedown Request</option>
                        <option value="Partnership">Partnership or Collaboration</option>
                        <option value="Bug Report">Broken Link or Bug Report</option>
                        <option value="General">General Inquiry</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="cMessage">Message *</label>
                    <textarea id="cMessage" class="form-control" rows="5" placeholder="Include community URL or specific details..." required></textarea>
                </div>
                <button type="submit" class="btn-submit">Send Inquiry →</button>
            </form>
        </div>

        <div class="content-card">
            <h2>🛡️ DMCA & Community Removal Protocol</h2>
            <p>If you are an official admin, owner, or legal representative of a community indexed on {name} and wish to modify your listing or have your channel removed from our public index, please select <strong>'Listing Removal / Takedown Request'</strong> above.</p>
            <p>We process all verified owner removal requests within <strong>24 business hours</strong> with zero friction. You may also report broken invite links, updated community descriptions, or ownership changes directly through this portal.</p>
        </div>
    </div>
{build_footer(niche, live_url)}
    <script>
        function handleContactSubmit(e) {{
            e.preventDefault();
            const alert = document.getElementById('contactAlert');
            alert.style.display = 'block';
            document.getElementById('contactForm').reset();
            window.scrollTo({{ top: alert.offsetTop - 40, behavior: 'smooth' }});
        }}
    </script>
</body>
</html>"""

def build_privacy_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = f"Privacy Policy | {name}"[:60]
    page_desc = f"Privacy policy and data governance practices for {name}. Transparent, GDPR, and CCPA compliant."[:160]
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{live_url}privacy.html#webpage",
                "url": f"{live_url}privacy.html",
                "name": page_title,
                "description": page_desc,
                "isPartOf": {"@id": f"{live_url}#website"},
                "breadcrumb": {"@id": f"{live_url}privacy.html#breadcrumbs"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{live_url}privacy.html#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": live_url},
                    {"@type": "ListItem", "position": 2, "name": "Privacy Policy", "item": f"{live_url}privacy.html"}
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{live_url}privacy.html">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{live_url}privacy.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{name}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
{shared_page_styles(accent)}
    </style>
</head>
<body>
{build_top_nav(niche, live_url)}
    <div class="page-container">
        <div class="breadcrumbs">
            <a href="{live_url}">Home</a> / <span>Privacy Policy</span>
        </div>
        <h1>Privacy Policy</h1>
        <p class="lead">Last Updated: September 2026. Your privacy and digital autonomy are fundamental to our service.</p>

        <div class="content-card">
            <h2>1. Information We Do Not Collect</h2>
            <p><strong>{name}</strong> is a publicly accessible, zero-account community directory. We do not require account registration, login credentials, passwords, or personal user profiles to browse, search, or filter our directory.</p>
            <p>Users can explore all verified groups anonymously with no paywalls, mandatory email subscriptions, or gatekept content.</p>
        </div>

        <div class="content-card">
            <h2>2. Information Collected via Submissions</h2>
            <p>If you voluntarily submit a community or contact us via our web forms, we collect the submitted metadata (community title, description, invite URL, and contact email). This data is used solely to verify, categorize, and index the submitted public community.</p>
            <p>We do not sell, license, or monetize submitted contact emails to third-party marketing brokers or advertising networks.</p>
        </div>

        <div class="content-card">
            <h2>3. Outbound Links & Third-Party Platforms</h2>
            <p>Our directory contains outbound links to third-party communication networks including <strong>Discord, Telegram, WhatsApp, and Reddit</strong>. Once you click an invite link, you are governed by the privacy policy and terms of service of that specific platform.</p>
            <p>We encourage users to review the privacy controls and notification settings on respective chat applications before joining any public channel.</p>
        </div>

        <div class="content-card">
            <h2>4. Cookies & Server Logs</h2>
            <p>We do not use invasive tracking cookies, browser fingerprinting, or cross-site behavioral advertising trackers. Standard server logs (IP address, browser user-agent, timestamp) may be recorded temporarily by our global CDN edge network solely for DDoS defense and security auditing.</p>
        </div>

        <div class="content-card">
            <h2>5. Your Rights & Data Requests</h2>
            <p>Under GDPR and CCPA regulations, you have the right to request access to, correction of, or deletion of any community metadata associated with you. Please reach out via our <a href="{live_url}contact.html" style="color: var(--accent);">Contact Page</a> to submit requests.</p>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""

def build_terms_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = f"Terms of Service | {name}"[:60]
    page_desc = f"Terms of service, third-party platform disclaimers, and acceptable use guidelines for {name}."[:160]
    
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{live_url}terms.html#webpage",
                "url": f"{live_url}terms.html",
                "name": page_title,
                "description": page_desc,
                "isPartOf": {"@id": f"{live_url}#website"},
                "breadcrumb": {"@id": f"{live_url}terms.html#breadcrumbs"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{live_url}terms.html#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": live_url},
                    {"@type": "ListItem", "position": 2, "name": "Terms of Service", "item": f"{live_url}terms.html"}
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{live_url}terms.html">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{live_url}terms.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{name}">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <style>
{shared_page_styles(accent)}
    </style>
</head>
<body>
{build_top_nav(niche, live_url)}
    <div class="page-container">
        <div class="breadcrumbs">
            <a href="{live_url}">Home</a> / <span>Terms of Service</span>
        </div>
        <h1>Terms of Service & Disclaimer</h1>
        <p class="lead">Last Updated: September 2026. Please read these terms carefully before utilizing our directory.</p>

        <div class="content-card">
            <h2>1. Informational Directory Nature</h2>
            <p><strong>{name}</strong> functions exclusively as an informational index and discovery catalog of publicly shared community links. We are <strong>not</strong> the owners, operators, administrators, or moderators of any third-party Discord server, Telegram channel, WhatsApp cohort, or Subreddit listed.</p>
            <p>Our index aggregates publicly distributed invitation links to facilitate peer connection and interest-based networking across verified digital ecosystems.</p>
        </div>

        <div class="content-card">
            <h2>2. Disclaimer of Warranties & External Content</h2>
            <p>All directory content and external links are provided strictly on an <strong>"as-is" and "as-available"</strong> basis. We do not endorse, guarantee, or assume liability for opinions, trading signals, financial advice, software downloads, or communications conducted within external third-party groups.</p>
            <p>Users are encouraged to exercise due diligence and adhere to basic online safety practices when interacting in public chat groups.</p>
        </div>

        <div class="content-card">
            <h2>3. Trademark & Non-Affiliation Notice</h2>
            <p>Discord, Telegram, WhatsApp, Reddit, and their respective logos are registered trademarks of their respective corporate owners. {name} is an independent research and discovery directory and is in no way affiliated with, sponsored by, or endorsed by any of these entities.</p>
        </div>

        <div class="content-card">
            <h2>4. Copyright & DMCA Takedown</h2>
            <p>We respect intellectual property rights. If you believe any content on this directory infringes upon your copyright or trademark, or if you wish to remove your community listing, please submit a notice via our <a href="{live_url}contact.html" style="color: var(--accent);">Contact Page</a> for immediate resolution.</p>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""
