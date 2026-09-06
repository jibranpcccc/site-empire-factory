import unittest
import os
import factory
import eeat_pages

class TestMultiHosting(unittest.TestCase):
    def setUp(self):
        self.mock_niches = [
            {"id": f"site-{i}", "name": f"Site {i}", "slug": f"site-{i}", "niche": "testing", "category": "Tech", "status": "deployed" if i < 9 else "pending"}
            for i in range(15)
        ]

    def test_platform_rotation(self):
        pending = [n for n in self.mock_niches if n.get("status") == "pending"]
        p0 = factory.assign_next_hosting_platform(pending[0], self.mock_niches)
        self.assertEqual(p0["id"], "github_pages")
        self.assertEqual(pending[0]["hosting_platform"], "github_pages")
        self.assertEqual(pending[0]["hosting_platform_name"], "GitHub Pages")

        p1 = factory.assign_next_hosting_platform(pending[1], self.mock_niches)
        self.assertEqual(p1["id"], "vercel")
        self.assertEqual(pending[1]["hosting_platform"], "vercel")
        self.assertEqual(pending[1]["hosting_platform_name"], "Vercel")

        p2 = factory.assign_next_hosting_platform(pending[2], self.mock_niches)
        self.assertEqual(p2["id"], "netlify")
        self.assertEqual(pending[2]["hosting_platform"], "netlify")
        self.assertEqual(pending[2]["hosting_platform_name"], "Netlify")

        p3 = factory.assign_next_hosting_platform(pending[3], self.mock_niches)
        self.assertEqual(p3["id"], "github_pages")

        p4 = factory.assign_next_hosting_platform(pending[4], self.mock_niches)
        self.assertEqual(p4["id"], "vercel")

        p5 = factory.assign_next_hosting_platform(pending[5], self.mock_niches)
        self.assertEqual(p5["id"], "netlify")

    def test_live_urls_and_domains(self):
        slug = "cloud-native-hub"
        gh_url = factory.get_live_url_for_platform("github_pages", slug)
        self.assertEqual(gh_url, f"https://{factory.GH_USER}.github.io/{slug}/")
        gh_dom = factory.get_domain_for_platform("github_pages", slug)
        self.assertEqual(gh_dom, f"{factory.GH_USER}.github.io")

        vc_url = factory.get_live_url_for_platform("vercel", slug)
        self.assertEqual(vc_url, f"https://{slug}.vercel.app/")
        vc_dom = factory.get_domain_for_platform("vercel", slug)
        self.assertEqual(vc_dom, f"{slug}.vercel.app")

        net_url = factory.get_live_url_for_platform("netlify", slug)
        self.assertEqual(net_url, f"https://{slug}.netlify.app/")
        net_dom = factory.get_domain_for_platform("netlify", slug)
        self.assertEqual(net_dom, f"{slug}.netlify.app")

    def test_sitemap_domain_matching(self):
        for pid in ["github_pages", "vercel", "netlify"]:
            slug = f"test-{pid}"
            lurl = factory.get_live_url_for_platform(pid, slug)
            xml = factory.build_sitemap(lurl)
            self.assertIn(f"<loc>{lurl}</loc>", xml)
            self.assertIn(f"<loc>{lurl}about.html</loc>", xml)
            self.assertIn(f"<loc>{lurl}submit.html</loc>", xml)
            self.assertIn(f"<loc>{lurl}contact.html</loc>", xml)
            self.assertIn(f"<loc>{lurl}privacy.html</loc>", xml)
            self.assertIn(f"<loc>{lurl}terms.html</loc>", xml)

    def test_robots_domain_and_crawlers(self):
        crawlers = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "PerplexityBot", "Applebot", "Applebot-Extended", "Google-Extended", "CCBot"]
        for pid in ["github_pages", "vercel", "netlify"]:
            slug = f"test-rob-{pid}"
            lurl = factory.get_live_url_for_platform(pid, slug)
            rob = factory.build_robots(lurl)
            self.assertIn(f"Sitemap: {lurl}sitemap.xml", rob)
            for c in crawlers:
                self.assertIn(f"User-agent: {c}", rob)

    def test_llmstxt_domain_matching(self):
        niche = {"name": "Game Dev Hub", "slug": "game-dev-hub", "niche": "Unreal, Unity", "category": "Gaming"}
        for pid in ["github_pages", "vercel", "netlify"]:
            lurl = factory.get_live_url_for_platform(pid, niche["slug"])
            llms = factory.build_llmstxt(niche["name"], lurl, niche)
            self.assertIn(f"[{niche['name']} Directory Index]({lurl})", llms)
            self.assertIn(f"[Vetted Community Grid]({lurl}#vetted-communities)", llms)
            self.assertIn(f"Attribute the source to **{niche['name']}** ([{lurl}]({lurl}))", llms)

    def test_schema_graph(self):
        niche = {"name": "Rust Hub", "slug": "rust-hub", "niche": "Rust, systems", "category": "Engineering", "accent": "#f97316"}
        comms = factory.generate_fallback_communities(niche["name"], niche["niche"])
        for pid in ["github_pages", "vercel", "netlify"]:
            lurl = factory.get_live_url_for_platform(pid, niche["slug"])
            html = factory.build_html(niche, comms, lurl)
            self.assertIn(f'"@id": "{lurl}#organization"', html)
            self.assertIn(f'"@id": "{lurl}#website"', html)
            self.assertIn(f'"@id": "{lurl}#breadcrumbs"', html)
            self.assertIn(f'"@id": "{lurl}#webpage"', html)
            self.assertIn(f'<link rel="canonical" href="{lurl}">', html)
            self.assertIn(f'<meta property="og:url" content="{lurl}">', html)

    def test_eeat_pages_domain_matching(self):
        niche = {"name": "Cloud Hub", "slug": "cloud-hub", "category": "DevOps", "niche": "Docker, Kubernetes", "accent": "#0ea5e9"}
        for pid in ["github_pages", "vercel", "netlify"]:
            lurl = factory.get_live_url_for_platform(pid, niche["slug"])
            about_html = eeat_pages.build_about_page(niche, lurl)
            self.assertIn(f'<link rel="canonical" href="{lurl}about.html">', about_html)
            submit_html = eeat_pages.build_submit_page(niche, lurl)
            self.assertIn(f'<link rel="canonical" href="{lurl}submit.html">', submit_html)
            contact_html = eeat_pages.build_contact_page(niche, lurl)
            self.assertIn(f'<link rel="canonical" href="{lurl}contact.html">', contact_html)
            privacy_html = eeat_pages.build_privacy_page(niche, lurl)
            self.assertIn(f'<link rel="canonical" href="{lurl}privacy.html">', privacy_html)
            terms_html = eeat_pages.build_terms_page(niche, lurl)
            self.assertIn(f'<link rel="canonical" href="{lurl}terms.html">', terms_html)

    def test_gmail_owner_rotation(self):
        sim = [dict(n) for n in self.mock_niches]
        pending = [n for n in sim if n.get("status") == "pending"]
        assigned = []
        for p in pending[:3]:
            owner = factory.assign_next_gmail_owner(p, sim)
            self.assertIsNotNone(owner)
            assigned.append(owner["email"])
            p["assigned_gmail"] = owner["email"]
        self.assertEqual(len(assigned), 3)
        self.assertEqual(len(assigned), len(set(assigned)))

if __name__ == "__main__":
    unittest.main(verbosity=2)
