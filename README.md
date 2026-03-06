# IT Pulse — Daily IT News

A zero-cost, automatically updating news site powered by free public RSS feeds.

**Updates every 24 hours** using GitHub Actions. Browse the latest articles from Hacker News, TechCrunch, Ars Technica, The Verge, and Reddit communities.

---

## Features

- ✅ **Automatic daily updates** — New articles every 24 hours (no manual work)
- ✅ **Free RSS feeds** — No API keys, no paid services
- ✅ **Lightweight design** — Clean, eye-friendly interface
- ✅ **Responsive** — Works on desktop, tablet, and mobile
- ✅ **Zero cost** — GitHub Pages + GitHub Actions (both free)
- ✅ **Privacy-focused** — No tracking, no cookies, no database

---

## News Sources

- Hacker News
- TechCrunch
- Ars Technica
- The Verge
- r/technology
- r/programming

---

## Technical Stack

- **Python** — Article fetcher & HTML renderer
- **Jinja2** — Template engine
- **GitHub Actions** — Automated daily updates
- **GitHub Pages** — Static hosting

---

## Setup (Local Testing)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/it-pulse.git
cd it-pulse

# 2. Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the fetcher
python fetch_news.py

# 4. Open index.html in your browser
```

---

## Deployment (GitHub Pages)

1. **Push to GitHub** (ensure repo is public)
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Source: Branch `main`, Folder `/root`
   - Save

3. **Done!** Your site is live at `https://YOUR_USERNAME.github.io/it-pulse/`

The workflow runs automatically every 24 hours and updates the page.

---

## Customization

### Change News Sources

Edit `fetch_news.py`, find the `FEEDS` list:

```python
FEEDS = [
    ("Hacker News",   "https://news.ycombinator.com/rss"),
    ("TechCrunch",    "https://techcrunch.com/feed/"),
    # ... add or remove sources ...
]
```

### Change Colors

Edit `template.html`, modify the `:root` CSS variables:

```css
:root {
  --bg: #f5f4f0;        /* background */
  --text: #2c2c2e;      /* text */
  --accent: #0a7ea4;    /* links, accents */
  /* ... more colors ... */
}
```

### Change Article Count

Edit `fetch_news.py`:

```python
MAX_ARTICLES = 60  # Change to desired number
```

---

## How It Works

1. **GitHub Actions** runs every day at 00:30 Yangon time (UTC+6:30)
2. **fetch_news.py** fetches articles from 6 RSS feeds
3. **Jinja2 template** renders the articles into HTML
4. **index.html** is committed and pushed back to the repository
5. **GitHub Pages** automatically serves the updated page

No manual work required — it's fully automated.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Site doesn't update | Check GitHub Actions logs in the Actions tab |
| RSS feed returns no articles | The feed may be temporarily down; it will retry next update |
| Want to update right now | Manually trigger the workflow from the Actions tab |

---

## License

MIT — Free to use and modify.

---

**Built with free tools. Zero cost. Always current.** 📰
