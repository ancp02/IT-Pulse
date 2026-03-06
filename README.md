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
