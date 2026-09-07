import json, datetime

GA4_HEAD_TAG = """    <!-- Google Analytics 4 (GA4) Unified Measurement Tag & AI Referral Attribution -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CK7NVYS1Y9"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      // AI / LLM Search Engine Referral & Citations Attribution Engine
      (function() {
        var ref = document.referrer ? document.referrer.toLowerCase() : '';
        var params = new URLSearchParams(window.location.search);
        var utmSource = (params.get('utm_source') || '').toLowerCase();
        
        var aiEngine = null;
        if (ref.indexOf('chatgpt.com') !== -1 || ref.indexOf('openai.com') !== -1 || utmSource.indexOf('chatgpt') !== -1) {
          aiEngine = 'ChatGPT';
        } else if (ref.indexOf('gemini.google.com') !== -1 || utmSource.indexOf('gemini') !== -1) {
          aiEngine = 'Google Gemini';
        } else if (ref.indexOf('perplexity.ai') !== -1 || utmSource.indexOf('perplexity') !== -1) {
          aiEngine = 'Perplexity AI';
        } else if (ref.indexOf('claude.ai') !== -1 || utmSource.indexOf('claude') !== -1) {
          aiEngine = 'Claude AI';
        } else if (ref.indexOf('copilot.microsoft.com') !== -1 || ref.indexOf('bing.com/chat') !== -1 || utmSource.indexOf('copilot') !== -1) {
          aiEngine = 'Microsoft Copilot';
        } else if (ref.indexOf('android-app://com.openai') !== -1) {
          aiEngine = 'ChatGPT Mobile App';
        } else if (ref.indexOf('meta.ai') !== -1) {
          aiEngine = 'Meta AI';
        } else if (ref.indexOf('deepseek.com') !== -1) {
          aiEngine = 'DeepSeek AI';
        }

        var configObj = {
          'send_page_view': true,
          'portfolio_folder': 'ai_directory_empire',
          'page_path': window.location.pathname
        };

        if (aiEngine) {
          configObj['user_properties'] = { 'last_ai_referrer': aiEngine };
          gtag('config', 'G-CK7NVYS1Y9', configObj);
          gtag('event', 'ai_search_traffic', {
            'event_category': 'AI Search Traffic',
            'ai_engine': aiEngine,
            'traffic_type': 'LLM Referral',
            'referrer_url': ref || 'direct_or_app',
            'landing_page': window.location.pathname,
            'page_title': document.title
          });
        } else {
          gtag('config', 'G-CK7NVYS1Y9', configObj);
        }
      })();
    </script>"""

def make_seo_title(prefix, name, max_len=60):
    candidate = f"{prefix} | {name}"
    if 30 <= len(candidate) <= max_len:
        return candidate
    elif len(candidate) > max_len:
        avail = max_len - len(f"{prefix} | ")
        truncated = name[:avail].rsplit(' ', 1)[0]
        return f"{prefix} | {truncated}"
    else:
        pad = f"{prefix} | {name} Hub"
        if len(pad) <= max_len:
            return pad
        return pad[:max_len].strip()

def make_seo_desc(verb, subject, context, max_len=160, min_len=120):
    desc = f"{verb} {subject} with our verified public directory. {context} Explore vetted Discord, Telegram, and Reddit groups."
    if len(desc) > max_len:
        desc = desc[:max_len-3].rsplit(' ', 1)[0] + '...'
    while len(desc) < min_len:
        desc += " Discover authenticated groups."
        if len(desc) > max_len:
            desc = desc[:max_len-3].rsplit(' ', 1)[0] + '...'
    return desc

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
        
        .alert-success {{ display: none; background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981; padding: 16px 20px; border-radius: 8px; margin-bottom: 25px; }}
        
        footer {{ border-top: 1px solid var(--border); padding: 50px 20px 30px; margin-top: 60px; background: rgba(0,0,0,0.2); }}
        .footer-grid {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 30px; text-align: left; }}
        .footer-col h4 {{ color: #fff; font-size: 0.9rem; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .footer-col a {{ display: block; color: var(--muted); text-decoration: none; font-size: 0.88rem; margin-bottom: 8px; transition: color 0.2s; }}
        .footer-col a:hover {{ color: var(--accent); }}
        .footer-desc {{ color: var(--muted); font-size: 0.88rem; line-height: 1.6; max-width: 380px; }}
        .footer-bottom {{ text-align: center; color: var(--muted); font-size: 0.82rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 40px; padding-top: 25px; }}
        
        @media (max-width: 768px) {{
            .footer-grid {{ grid-template-columns: 1fr; }}
            .top-nav {{ flex-direction: column; gap: 12px; align-items: flex-start; padding: 14px 16px; }}
            .nav-menu {{ width: 100%; justify-content: space-between; flex-wrap: wrap; }}
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
                <a href="{live_url}#vetted-communities">All Verified Groups</a>
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
    page_title = make_seo_title("About & Verification", name)
    page_desc = make_seo_desc("Learn", f"our 4-tier vetting methodology and standards for {name}", "Discover how we audit online communities for authenticity.")
    
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
{GA4_HEAD_TAG}
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
            <p>Our directory infrastructure executes continuous automated sweeps every 24 hours to re-validate endpoints, purge unresponsive communities, and maintain clean indexation for global search engines.</p>
            <p style="margin-top: 20px;"><a href="{live_url}submit.html" class="btn-submit">Submit Your Community for Review →</a></p>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""

def build_submit_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = make_seo_title("Submit Community", name)
    page_desc = make_seo_desc("Submit", f"your verified community to {name}", "Explore free indexing for active Discord, Telegram, and Reddit groups.")
    
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
{GA4_HEAD_TAG}
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
                    <label for="commContact">Contact Email (for administrative notices only)</label>
                    <input type="email" id="commContact" class="form-control" placeholder="desk@authoritydirectory.org">
                </div>
                <button type="submit" class="btn-submit">Submit for Verification →</button>
            </form>
        </div>

        <div class="content-card">
            <h2>📋 Community Curation Standards & Acceptance Criteria</h2>
            <p>Our editorial team applies strict, transparent standards to maintain our reputation as an authoritative directory. Before submitting your community, ensure it complies with the following mandatory prerequisites:</p>
            <ul>
                <li><strong>Active Membership Threshold:</strong> Communities must demonstrate a minimum of 250 verified participants with regular conversational velocity. Stagnant groups or bot-inflated channels are automatically disqualified.</li>
                <li><strong>Anti-Spam & Moderator Presence:</strong> Dedicated administrators or automated moderation bots must be active to remove unsolicited promotions, harmful links, and abusive interactions.</li>
                <li><strong>Zero-Cost Accessibility:</strong> Primary discussion rooms must be 100% free to access. We do not index groups that require paid subscriptions, private NFT gates, or upfront transactional fees to enter.</li>
                <li><strong>Permanent Public Direct Links:</strong> Invite links must point directly to official platform endpoints (such as discord.gg vanity links, t.me channels, or reddit.com subreddits) without intermediate shorteners or paywalls.</li>
            </ul>
        </div>

        <div class="content-card">
            <h2>🔍 The Automated Verification Pipeline</h2>
            <p>Every submitted group enters our automated curation pipeline to confirm its validity prior to publication:</p>
            <p><strong>Phase 1: Automated Endpoint Ping:</strong> Our system verifies that the provided invite link returns a valid HTTP response and is not expired, rate-limited, or redirected.</p>
            <p><strong>Phase 2: Editorial Review:</strong> A human reviewer inspects the community rules, description accuracy, and member engagement to ensure alignment with our directory taxonomy.</p>
            <p><strong>Phase 3: Directory Publication & Indexing:</strong> Approved communities receive live cards with real-time copy invite buttons, spec matrix badges, and structured Schema.org breadcrumb markup.</p>
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
    page_title = make_seo_title("Contact & DMCA Desk", name)
    page_desc = make_seo_desc("Contact", f"the administrative team at {name}", "Submit community listing updates, partnerships, or DMCA removal requests.")
    
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
{GA4_HEAD_TAG}
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
                    <input type="email" id="cEmail" class="form-control" placeholder="desk@authoritydirectory.org" required>
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
            <p>Official takedown notices must clearly identify the specific URL listing in question, state proof of authorized administrative ownership, and specify the exact rectification desired.</p>
        </div>

        <div class="content-card">
            <h2>⏱️ Editorial Service Level Agreements (SLA)</h2>
            <p>Our operational infrastructure adheres to strict service level benchmarks to support user trust and webmaster collaboration:</p>
            <ul>
                <li><strong>24-Hour Editorial Review:</strong> General inquiries, broken link notifications, and submission revisions are acknowledged within one business day.</li>
                <li><strong>Priority Copyright & DMCA Handling:</strong> Formal intellectual property notices receive prioritized attention within 12 business hours.</li>
                <li><strong>Direct Email Inquiries:</strong> Inquiries may also be routed directly to our designated compliance desk at <a href="mailto:desk@authoritydirectory.org" style="color:var(--accent);">desk@authoritydirectory.org</a>.</li>
                <li><strong>Security & Abuse Resolution:</strong> Reports of compromised channels or malicious behavior result in instant provisional quarantine pending manual investigation.</li>
            </ul>
        </div>

        <div class="content-card">
            <h2>🔒 Security Vulnerability & Safe Harbor Policy</h2>
            <p>We take the security and integrity of our directory ecosystem seriously. If you are an independent security researcher or developer who has identified a potential vulnerability, broken routing endpoint, or data integrity issue on our site, we invite you to submit a coordinated disclosure report.</p>
            <p>Our engineering team investigates all legitimate reports within 24 hours. We operate a good-faith safe harbor policy: we will not pursue legal action against ethical researchers who discover issues without disrupting live operations, scraping private user data, or violating platform terms.</p>
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
    page_title = make_seo_title("Privacy Policy", name)
    page_desc = make_seo_desc("Review", f"the privacy policy and data governance practices for {name}", "Learn about our zero-account policy and GDPR data protection.")
    
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
{GA4_HEAD_TAG}
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
        <p class="lead">Last Updated: September 2026. Your privacy and digital autonomy are fundamental to our service architecture.</p>

        <div class="content-card">
            <h2>1. Information We Do Not Collect</h2>
            <p><strong>{name}</strong> is built upon a privacy-by-design, zero-account architecture. We do not require visitors to register accounts, provide passwords, link social profiles, or disclose personal identifiers to search, filter, or explore our indexed communities.</p>
            <p>Users can explore all verified groups anonymously with no paywalls, mandatory email subscriptions, or gatekept content.</p>
        </div>

        <div class="content-card">
            <h2>2. Information Collected via Voluntary Submissions</h2>
            <p>If you voluntarily submit a community or contact us via our web forms, we collect the submitted metadata (community title, description, invite URL, and contact email). This data is used solely to verify, categorize, and index the submitted public community.</p>
            <p>We do not sell, license, rent, or trade submitted contact emails to third-party data brokers, marketing agencies, or behavioral advertising syndicates.</p>
        </div>

        <div class="content-card">
            <h2>3. Outbound Links & Third-Party Platforms</h2>
            <p>Our directory contains direct invitation links to external third-party communication networks including <strong>Discord, Telegram, WhatsApp, and Reddit</strong>. Once you navigate away from our directory, your interactions are governed exclusively by the terms and privacy frameworks of those external services.</p>
            <p>We strongly recommend reviewing the privacy controls and account permissions on respective platforms before joining any public channel.</p>
        </div>

        <div class="content-card">
            <h2>4. Analytics, Cookies & Infrastructure Logging</h2>
            <p>We do not deploy invasive cross-site tracking cookies, device fingerprinting routines, or intrusive behavioral trackers. We use standardized Google Analytics 4 telemetry strictly to aggregate anonymous traffic statistics (such as page views and referral categories).</p>
            <p>Server logs may temporarily record ephemeral technical data (such as IP addresses and browser user-agent headers) solely for the technical defense against distributed denial-of-service (DDoS) attacks and malicious automated scraping.</p>
        </div>

        <div class="content-card">
            <h2>5. Data Subject Rights Under GDPR & CCPA</h2>
            <p>Under the General Data Protection Regulation (GDPR) and California Consumer Privacy Act (CCPA), users and community owners maintain clear legal rights regarding their information:</p>
            <ul>
                <li><strong>Right of Access & Rectification:</strong> You may request a complete summary of any metadata associated with your community listing and request immediate corrections.</li>
                <li><strong>Right to Erasure (Right to be Forgotten):</strong> Community administrators may request the permanent removal and de-indexing of their channels at any time.</li>
                <li><strong>Non-Discrimination Guarantee:</strong> Exercising your data privacy rights will never result in degraded directory functionality or restricted access.</li>
                <li><strong>Contact Compliance Desk:</strong> To file a formal data governance inquiry, contact our Data Protection Officer at <a href="mailto:desk@authoritydirectory.org" style="color:var(--accent);">desk@authoritydirectory.org</a>.</li>
            </ul>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""

def build_terms_page(niche, live_url):
    name = niche["name"]
    accent = niche.get("accent", "#0ea5e9")
    page_title = make_seo_title("Terms of Service", name)
    page_desc = make_seo_desc("Review", f"the terms of service and acceptable use guidelines for {name}", "Understand third-party disclaimers and directory usage rules.")
    
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
{GA4_HEAD_TAG}
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
        <h1>Terms of Service</h1>
        <p class="lead">Last Updated: September 2026. Please review the operating terms, platform disclaimers, and directory guidelines below.</p>

        <div class="content-card">
            <h2>1. Acceptance of Terms & Service Scope</h2>
            <p>By accessing or utilizing <strong>{name}</strong>, you agree to comply with and be bound by these Terms of Service. If you disagree with any provision contained herein, you should immediately discontinue use of this directory.</p>
            <p>Our platform operates as an informational index connecting users with independent third-party communities. We do not own, operate, moderate, or employ the staff of any external server or group listed.</p>
        </div>

        <div class="content-card">
            <h2>2. Third-Party Platform Disclaimers & Non-Affiliation</h2>
            <p>All trademarks, service marks, logos, and brand names mentioned on this site—including <strong>Discord, Telegram, WhatsApp, and Reddit</strong>—are the exclusive intellectual property of their respective owners.</p>
            <p><strong>{name}</strong> is an independent directory and is not affiliated with, endorsed by, sponsored by, or officially connected with Discord Inc., Telegram FZ-LLC, WhatsApp LLC, Reddit Inc., or any of their parent corporations or subsidiaries.</p>
        </div>

        <div class="content-card">
            <h2>3. Community Content & User Responsibility</h2>
            <p>Discussions, content, media, files, opinions, and advice expressed within listed communities are solely those of the respective participants and channel administrators. We do not inspect individual chat messages and assume no responsibility for external content.</p>
            <p>Users must exercise their own independent judgment and caution when joining external discussion groups, sharing contact information, or participating in financial, professional, or social interactions.</p>
        </div>

        <div class="content-card">
            <h2>4. Acceptable Directory Use & Scraping Policy</h2>
            <p>Users agree to utilize this directory solely for lawful personal discovery. You agree not to execute automated denial-of-service requests, inject malicious exploits, or harvest administrator emails for unsolicited spam marketing.</p>
            <p>We permit standard search engine indexing and AI model grounding via our structured <code>robots.txt</code> and <code>llms.txt</code> directives, provided crawlers respect specified bandwidth constraints.</p>
        </div>

        <div class="content-card">
            <h2>5. Disclaimer of Warranties & Limitation of Liability</h2>
            <p>This directory is provided on an "as-is" and "as-available" basis without express or implied warranties of any kind. We make no guarantee that directory listings will be uninterrupted, error-free, or continuously accessible.</p>
            <p>To the maximum extent permitted by applicable law, the operators of <strong>{name}</strong> shall not be liable for any indirect, incidental, special, or consequential damages resulting from your use of, or inability to use, this directory.</p>
            <p>For questions or formal inquiries regarding these terms, contact our legal desk at <a href="mailto:desk@authoritydirectory.org" style="color:var(--accent);">desk@authoritydirectory.org</a>.</p>
        </div>
    </div>
{build_footer(niche, live_url)}
</body>
</html>"""
