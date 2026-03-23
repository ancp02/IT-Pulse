# IT Pulse

IT Pulse is a static news dashboard that aggregates public tech RSS feeds and publishes a refreshed [index.html](index.html) every 24 hours.

Live site: https://ancp02.github.io/IT-Pulse/

## How updates work

- [update-news workflow](.github/workflows/update-news.yml) runs daily.
- It fetches the latest feeds using [fetch_news.py](fetch_news.py).
- It commits only [index.html](index.html) when content changes.
- [deploy workflow](.github/workflows/deploy.yml) publishes only public website files to GitHub Pages.

## Local run

```bash
python -m pip install -r requirements.txt
python fetch_news.py
```

## Security notes

- No API keys are required.
- The site is generated from public RSS feeds.
- Deployment artifact contains only public web files.
Click the link to read IT news: https://ancp02.github.io/IT-Pulse/

News is updated daily. 
I warmly welcome your comments and suggestions for improvements.
