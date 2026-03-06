"""
fetch_news.py — Daily IT News Generator
========================================
Fetches articles from public RSS feeds, renders index.html via Jinja2.

Run locally:
    python fetch_news.py

Output:
    index.html  (written to the same directory as this script)

Timezone note
-------------
All display timestamps are shown in Myanmar Time (MMT = UTC+6:30).
The GitHub Actions cron is set to 18:00 UTC, which equals 00:30 MMT
the following calendar day — i.e. the site refreshes at midnight-ish
in Yangon every day.
"""

import html as html_mod
import logging
import os
import re
import sys
import calendar
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests
import feedparser
from jinja2 import Environment, FileSystemLoader

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Yangon / Myanmar Time (UTC+6:30) ─────────────────────────────────────────
# We use a fixed-offset timezone because Myanmar does not observe DST.
# Python's stdlib `datetime.timezone` is sufficient — no pytz needed.
MMT = timezone(timedelta(hours=6, minutes=30), name="MMT")

# ── Feed Sources ──────────────────────────────────────────────────────────────
# Edit this list to add or remove news sources.
# Format: ("Display Name", "RSS/Atom feed URL")
FEEDS = [
    ("Hacker News",   "https://news.ycombinator.com/rss"),
    ("TechCrunch",    "https://techcrunch.com/feed/"),
    ("Ars Technica",  "https://feeds.arstechnica.com/arstechnica/index"),
    ("The Verge",     "https://www.theverge.com/rss/index.xml"),
    ("r/technology",  "https://www.reddit.com/r/technology/.rss"),
    ("r/programming", "https://www.reddit.com/r/programming/.rss"),
]

# Maximum number of articles to display (newest-first after dedup)
MAX_ARTICLES = 60

# HTTP request timeout in seconds per feed
REQUEST_TIMEOUT = 15

# Minimum excerpt length before we fall back to a default message
MIN_EXCERPT_LEN = 10

# Default message when no summary is available
NO_SUMMARY_MSG = "No summary available — click the link to read the full article."


# ── HTTP Helper ───────────────────────────────────────────────────────────────

def _safe_get(url: str) -> Optional[str]:
    """
    Download *url* and return the raw response text.
    Returns None on any network or HTTP error (logs a warning instead of
    raising), so a single broken feed never aborts the whole run.
    """
    headers = {
        # Identify ourselves politely; some feeds block generic Python UA strings.
        "User-Agent": (
            "Mozilla/5.0 (compatible; ITPulseBot/2.0; "
            "+https://github.com/your-username/it-pulse)"
        ),
        "Accept": "application/rss+xml, application/atom+xml, text/xml, */*",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.Timeout:
        log.warning("Timeout fetching %s (limit=%ds)", url, REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError as exc:
        log.warning("Connection error fetching %s — %s", url, exc)
    except requests.exceptions.HTTPError as exc:
        log.warning("HTTP %s for %s", exc.response.status_code, url)
    except requests.exceptions.RequestException as exc:
        log.warning("Request failed for %s — %s", url, exc)
    return None


# ── Date Parsing ──────────────────────────────────────────────────────────────

def _parse_date(entry) -> datetime:
    """
    Extract a timezone-aware UTC datetime from a feedparser entry.

    feedparser normalises dates into time.struct_time tuples stored in
    ``published_parsed``, ``updated_parsed``, or ``created_parsed``.
    We try each in order and fall back to *now* if none is present.
    """
    for attr in ("published_parsed", "updated_parsed", "created_parsed"):
        tup = getattr(entry, attr, None)
        if tup:
            try:
                # calendar.timegm converts a UTC struct_time → POSIX timestamp
                ts = calendar.timegm(tup)
                return datetime.fromtimestamp(ts, tz=timezone.utc)
            except (OverflowError, OSError, ValueError):
                pass  # malformed tuple — try next attribute
    # No date found; use current UTC time so the article sorts near the top
    log.debug("No date found for entry '%s'; using now(UTC)", getattr(entry, "title", "?"))
    return datetime.now(tz=timezone.utc)


# ── Excerpt Extraction ────────────────────────────────────────────────────────

def _excerpt(entry, max_len: int = 300) -> str:
    """
    Return a clean, plain-text excerpt from the feed entry.

    Strategy (in order):
      1. ``summary``  — most feeds provide this
      2. ``description`` — older RSS 2.0 feeds
      3. ``content[0].value`` — Atom feeds with full content
      4. Fall back to NO_SUMMARY_MSG if nothing useful is found

    HTML tags are stripped, entities decoded, and whitespace collapsed.
    The result is truncated to *max_len* characters at a word boundary.
    """
    raw = ""
    for attr in ("summary", "description"):
        val = getattr(entry, attr, None)
        if val and isinstance(val, str):
            raw = val
            break

    # feedparser stores Atom <content> as a list of dicts
    if not raw:
        content_list = getattr(entry, "content", None)
        if content_list and isinstance(content_list, list):
            raw = content_list[0].get("value", "")

    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", raw)
    # Collapse whitespace (newlines, tabs, multiple spaces)
    text = re.sub(r"\s+", " ", text).strip()
    # Decode HTML entities (e.g. &amp; → &, &#39; → ')
    text = html_mod.unescape(text)

    # If the cleaned text is too short or looks like boilerplate, use default
    if len(text) < MIN_EXCERPT_LEN:
        return NO_SUMMARY_MSG

    # Truncate at a word boundary to avoid cutting mid-word
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0].rstrip(".,;:") + "…"

    return text


# ── Core Fetch ────────────────────────────────────────────────────────────────

def fetch_all_articles() -> list[dict]:
    """
    Iterate over every feed in FEEDS, parse entries, deduplicate by URL,
    and return a list of article dicts sorted newest-first (capped at
    MAX_ARTICLES).

    Each dict contains:
        title      – article headline (HTML-safe via Jinja2 autoescape)
        url        – canonical link to the original article
        source     – display name of the feed
        date       – timezone-aware UTC datetime (for sorting)
        date_str   – human-readable date in Yangon time, e.g. "March 06, 2026"
        time_str   – human-readable time in Yangon time, e.g. "00:30 MMT"
        excerpt    – plain-text summary / description
    """
    all_articles: list[dict] = []
    seen_urls: set[str] = set()

    for source_name, feed_url in FEEDS:
        log.info("Fetching %-20s  %s", source_name, feed_url)
        raw = _safe_get(feed_url)
        if raw is None:
            log.warning("Skipping %s — could not retrieve feed.", source_name)
            continue

        try:
            parsed = feedparser.parse(raw)
        except Exception as exc:
            log.warning("feedparser failed on %s — %s", source_name, exc)
            continue

        if parsed.bozo and parsed.bozo_exception:
            # bozo=True means the feed is malformed but feedparser still tried
            log.debug(
                "Feed %s is malformed (%s) — continuing anyway.",
                source_name,
                type(parsed.bozo_exception).__name__,
            )

        count = 0
        for entry in parsed.entries:
            link = getattr(entry, "link", "").strip()
            if not link:
                log.debug("Entry without link in %s — skipping.", source_name)
                continue
            if link in seen_urls:
                continue  # deduplicate across feeds
            seen_urls.add(link)

            title = getattr(entry, "title", "(no title)").strip()
            if not title:
                title = "(no title)"

            pub_date_utc = _parse_date(entry)

            # Convert to Yangon time for display
            pub_date_mmt = pub_date_utc.astimezone(MMT)

            excerpt = _excerpt(entry)

            all_articles.append({
                "title":    title,
                "url":      link,
                "source":   source_name,
                "date":     pub_date_utc,          # used for sorting (UTC)
                # Readable date: "March 06, 2026"
                "date_str": pub_date_mmt.strftime("%B %d, %Y"),
                # Readable time: "00:30 MMT"
                "time_str": pub_date_mmt.strftime("%H:%M MMT"),
                "excerpt":  excerpt,
            })
            count += 1

        log.info("  → %d new articles from %s", count, source_name)

    if not all_articles:
        return []

    # Sort newest-first, then cap
    all_articles.sort(key=lambda a: a["date"], reverse=True)
    return all_articles[:MAX_ARTICLES]


# ── Render ────────────────────────────────────────────────────────────────────

def render_html(articles: list[dict], output_path: Path) -> None:
    """
    Render *articles* into index.html using the Jinja2 template.

    Template variables injected:
        articles        – list of article dicts (see fetch_all_articles)
        article_count   – int
        sources         – list of source display names
        generated_at    – "Friday, March 06, 2026 at 00:30 MMT"
        generated_at_utc– "Friday, March 06, 2026 at 18:00 UTC"
        next_update     – "Saturday, March 07, 2026 at 00:30 MMT"
    """
    # Jinja2 environment — autoescape=True prevents XSS / broken HTML from
    # feed content that contains stray < > & characters.
    src_dir = Path(__file__).parent
    env = Environment(
        loader=FileSystemLoader(str(src_dir)),
        autoescape=True,          # HTML-escape all {{ }} expressions
        trim_blocks=True,         # remove newline after block tags
        lstrip_blocks=True,       # strip leading whitespace before block tags
    )
    template = env.get_template("template.html")

    now_utc = datetime.now(tz=timezone.utc)
    now_mmt = now_utc.astimezone(MMT)

    # Next update is 24 hours from now (same local time tomorrow in MMT)
    next_update_mmt = now_mmt + timedelta(days=1)

    html_out = template.render(
        articles=articles,
        article_count=len(articles),
        sources=[name for name, _ in FEEDS],
        # e.g. "Friday, March 06, 2026 at 00:30 MMT"
        generated_at=now_mmt.strftime("%A, %B %d, %Y at %H:%M MMT"),
        # e.g. "Friday, March 06, 2026 at 18:00 UTC"
        generated_at_utc=now_utc.strftime("%A, %B %d, %Y at %H:%M UTC"),
        # e.g. "Saturday, March 07, 2026 at 00:30 MMT"
        next_update=next_update_mmt.strftime("%A, %B %d, %Y at %H:%M MMT"),
    )

    output_path.write_text(html_out, encoding="utf-8")
    log.info("Wrote %d articles → %s", len(articles), output_path)


# ── Entry Point ───────────────────────────────────────────────────────────────

def main() -> None:
    output = Path(__file__).parent / "index.html"

    log.info(
        "=== IT Pulse News Generator — %s ===",
        datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    articles = fetch_all_articles()

    if not articles:
        # Safety guard: never overwrite a working page with an empty one.
        log.error(
            "No articles were fetched from any source. "
            "index.html has NOT been overwritten."
        )
        sys.exit(1)

    render_html(articles, output)
    log.info("Done. Open %s in your browser to preview.", output)


if __name__ == "__main__":
    main()
