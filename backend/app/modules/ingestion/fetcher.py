"""RSS / news feed source definitions.

Each source has a URL, region, default category, and publisher name.
The fetcher pulls articles from these sources and normalises them
into a common RawArticle format.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import feedparser
import httpx


@dataclass
class RawArticle:
    """Normalised article coming out of any source."""

    title: str
    url: str
    snippet: str
    publisher: str
    publish_time: datetime
    region: str          # "domestic" | "international"
    category: str        # best-effort from source
    raw_text: str = ""   # full text for clustering / entity extraction


@dataclass
class FeedSource:
    url: str
    publisher: str
    region: str          # "domestic" | "international"
    category: str        # default category
    language: str = "en"


# ── Curated RSS sources ──────────────────────────────────────────────
SOURCES: list[FeedSource] = [
    # International — general
    FeedSource(
        url="https://feeds.bbci.co.uk/news/world/rss.xml",
        publisher="BBC News",
        region="international",
        category="politics",
    ),
    FeedSource(
        url="https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        publisher="New York Times",
        region="international",
        category="politics",
    ),
    # International — tech
    FeedSource(
        url="https://feeds.arstechnica.com/arstechnica/index",
        publisher="Ars Technica",
        region="international",
        category="technology",
    ),
    # International — economy
    FeedSource(
        url="https://feeds.reuters.com/reuters/businessNews",
        publisher="Reuters",
        region="international",
        category="economy",
    ),
    # Domestic — general
    FeedSource(
        url="https://feedx.net/rss/people.xml",
        publisher="人民网",
        region="domestic",
        category="politics",
        language="zh",
    ),
    FeedSource(
        url="https://feedx.net/rss/xinhua.xml",
        publisher="新华网",
        region="domestic",
        category="politics",
        language="zh",
    ),
    # Domestic — tech
    FeedSource(
        url="https://feedx.net/rss/36kr.xml",
        publisher="36氪",
        region="domestic",
        category="technology",
        language="zh",
    ),
]


async def fetch_articles(
    sources: list[FeedSource] | None = None,
    timeout: float = 15.0,
) -> list[RawArticle]:
    """Fetch and normalise articles from all configured RSS sources."""
    sources = sources or SOURCES
    articles: list[RawArticle] = []

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": "HotPulse/0.1 (RSS reader)"},
    ) as client:
        for source in sources:
            try:
                resp = await client.get(source.url)
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)

                for entry in feed.entries[:30]:  # cap per source
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "").strip()
                    if not title or not link:
                        continue

                    # Extract snippet / summary
                    snippet = ""
                    if entry.get("summary"):
                        snippet = entry.summary[:500]
                    elif entry.get("description"):
                        snippet = entry.description[:500]

                    # Parse publish time
                    pub_time = datetime.now(timezone.utc)
                    if entry.get("published_parsed"):
                        try:
                            from time import mktime
                            pub_time = datetime.fromtimestamp(
                                mktime(entry.published_parsed), tz=timezone.utc
                            )
                        except (ValueError, OverflowError):
                            pass

                    articles.append(
                        RawArticle(
                            title=title,
                            url=link,
                            snippet=snippet,
                            publisher=source.publisher,
                            publish_time=pub_time,
                            region=source.region,
                            category=source.category,
                            raw_text=f"{title}. {snippet}",
                        )
                    )

            except Exception as exc:
                # Graceful degradation: skip failing sources (PRD §11)
                print(f"[ingestion] skip {source.publisher}: {exc}")

    return articles
