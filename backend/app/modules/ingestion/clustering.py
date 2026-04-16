"""Heuristic topic clustering.

Groups RawArticles into topic clusters using title + snippet similarity.
Uses a simple keyword-overlap approach as the PRD specifies
"heuristic-first logic" before complex models (PRD §12, §13).
"""
from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Sequence

from app.modules.ingestion.fetcher import RawArticle

# Stop words for English and Chinese common particles
_STOP_EN = frozenset(
    "a an the and or but in on at to for of is it its this that "
    "by from with as are was were be been being have has had do does "
    "did will would shall should can could may might must not no "
    "he she they we you i my his her their our your".split()
)


def _tokenize(text: str) -> set[str]:
    """Simple word tokenizer for clustering."""
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)  # strip HTML
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = text.split()
    return {t for t in tokens if len(t) > 1 and t not in _STOP_EN}


def _similarity(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass
class TopicCluster:
    """A group of related articles forming one topic."""

    cluster_id: str
    title: str
    summary: str
    region: str
    category: str
    articles: list[RawArticle] = field(default_factory=list)
    heat_score: int = 0
    freshness: str = "stable"

    def compute_heat(self) -> None:
        """Estimate heat from article count and recency."""
        count = len(self.articles)
        # Base heat from article volume
        self.heat_score = min(100, count * 12 + 10)

        now = datetime.now(timezone.utc)
        if self.articles:
            newest = max(a.publish_time for a in self.articles)
            age_hours = (now - newest).total_seconds() / 3600
            if age_hours < 6:
                self.freshness = "rising"
            elif age_hours < 48:
                self.freshness = "stable"
            else:
                self.freshness = "fading"


def cluster_articles(
    articles: Sequence[RawArticle],
    similarity_threshold: float = 0.2,
) -> list[TopicCluster]:
    """Cluster articles into topics using greedy keyword-overlap."""
    if not articles:
        return []

    # Pre-tokenize
    token_cache: list[tuple[RawArticle, set[str]]] = [
        (a, _tokenize(a.raw_text)) for a in articles
    ]

    clusters: list[list[int]] = []
    assigned: set[int] = set()

    for i, (art_i, tok_i) in enumerate(token_cache):
        if i in assigned:
            continue
        group = [i]
        assigned.add(i)

        for j, (art_j, tok_j) in enumerate(token_cache):
            if j in assigned:
                continue
            if _similarity(tok_i, tok_j) >= similarity_threshold:
                group.append(j)
                assigned.add(j)

        clusters.append(group)

    # Build TopicCluster objects
    result: list[TopicCluster] = []
    for group_indices in clusters:
        group_articles = [token_cache[k][0] for k in group_indices]
        if not group_articles:
            continue

        # Pick the article with the longest title as representative
        rep = max(group_articles, key=lambda a: len(a.title))

        # Determine dominant region and category
        region_counts: dict[str, int] = defaultdict(int)
        cat_counts: dict[str, int] = defaultdict(int)
        for a in group_articles:
            region_counts[a.region] += 1
            cat_counts[a.category] += 1

        region = max(region_counts, key=region_counts.get)  # type: ignore[arg-type]
        category = max(cat_counts, key=cat_counts.get)  # type: ignore[arg-type]

        # Generate slug from title
        slug_base = re.sub(r"[^\w\s-]", "", rep.title.lower())
        slug_base = re.sub(r"[\s]+", "-", slug_base.strip())[:80]
        cluster_id = hashlib.md5(slug_base.encode()).hexdigest()[:12]

        tc = TopicCluster(
            cluster_id=f"topic_{cluster_id}",
            title=rep.title,
            summary=rep.snippet[:300] if rep.snippet else rep.title,
            region=region,
            category=category,
            articles=group_articles,
        )
        tc.compute_heat()
        result.append(tc)

    # Sort by heat descending
    result.sort(key=lambda c: c.heat_score, reverse=True)
    return result
