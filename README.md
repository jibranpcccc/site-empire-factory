# 🏭 Autonomous Site Empire Factory

A 100% cloud-native, autonomous web empire builder.

## 🎯 Architecture
- **Schedule:** Runs daily at 06:00 UTC via GitHub Actions cron (`0 6 * * *`).
- **Quota Rule:** Strictly limits deployments to **exactly 3 websites per day** (never more, even if days were missed).
- **AI Research:** Curates 30+ verified niche communities per site via Google Gemini 2.5 Flash API.
- **Web Assets:** Produces responsive HTML5/CSS/JS with live instant search, platform filters, `.geo-answer-block` for AI Overviews, Schema.org JSON-LD, `sitemap.xml`, `feed.xml`, and `robots.txt`.
- **Search Engine Setup:** Embeds universal Google Search Console verification token and pings IndexNow API (`api.indexnow.org`) for instant Bing & Yandex indexing.

## 📊 Niche Queue
- 60+ pre-researched, high-RPM niches tracked in `niches.json`.
- Completed deployments tracked in `PORTFOLIO.md`.
