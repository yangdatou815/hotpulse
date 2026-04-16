"""Lightweight entity extraction.

Uses regex-based heuristics to extract people, organizations, and locations
from article text. PRD §13: "Heuristic-first implementation before heavier
ML or LLM dependencies."
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class ExtractedEntity:
    name: str
    entity_type: str  # "person" | "org" | "location"
    count: int = 1


# ── Pattern-based extractors ──

# Capitalized multi-word names (English)
_NAME_PATTERN = re.compile(
    r"\b([A-Z][a-z]{1,20}(?:\s+[A-Z][a-z]{1,20}){1,3})\b"
)

# Common org suffixes
_ORG_SUFFIXES = re.compile(
    r"\b([\w\s]{3,40}(?:Inc|Corp|Ltd|LLC|Group|Foundation|Commission|Agency|Ministry|Department|Bureau|Council|Committee|Association|Institute|University|Bank|Fund))\b",
    re.IGNORECASE,
)

# Well-known location keywords
_LOCATION_KEYWORDS = frozenset({
    "washington", "beijing", "london", "paris", "tokyo", "moscow",
    "brussels", "berlin", "new york", "shanghai", "hong kong", "singapore",
    "sydney", "mumbai", "delhi", "taipei", "seoul", "bangkok",
    "europe", "asia", "africa", "middle east", "united states", "china",
    "russia", "japan", "india", "germany", "france", "uk", "brazil",
    "canada", "australia", "iran", "israel", "ukraine", "taiwan",
    "california", "texas", "florida",
})

# Common noise words that look like names
_NAME_BLACKLIST = frozenset({
    "The", "This", "That", "These", "Those", "There", "They",
    "What", "When", "Where", "Which", "While", "Since", "After",
    "Before", "During", "About", "Other", "Under", "According",
    "Read More", "Click Here", "Sign Up", "Last Updated",
    "Published", "Updated", "Photo", "Image", "Video",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday", "January", "February", "March",
    "April", "May", "June", "July", "August", "September",
    "October", "November", "December",
})


def extract_entities(texts: list[str], max_entities: int = 15) -> list[ExtractedEntity]:
    """Extract entities from a list of text snippets."""
    name_counter: Counter[str] = Counter()
    org_counter: Counter[str] = Counter()
    loc_counter: Counter[str] = Counter()

    combined = " ".join(texts)

    # Extract organisations
    for match in _ORG_SUFFIXES.finditer(combined):
        name = match.group(1).strip()
        if len(name) > 4:
            org_counter[name] += 1

    # Extract potential names
    for match in _NAME_PATTERN.finditer(combined):
        name = match.group(1).strip()
        if name.split()[0] in _NAME_BLACKLIST:
            continue
        if name in org_counter:
            continue

        # Check if it's a location
        if name.lower() in _LOCATION_KEYWORDS:
            loc_counter[name] += 1
        else:
            name_counter[name] += 1

    # Also scan for known locations
    lower_combined = combined.lower()
    for loc in _LOCATION_KEYWORDS:
        count = lower_combined.count(loc)
        if count > 0:
            nice_name = loc.title()
            loc_counter[nice_name] = max(loc_counter.get(nice_name, 0), count)

    # Merge and rank
    entities: list[ExtractedEntity] = []
    for name, count in org_counter.most_common(5):
        entities.append(ExtractedEntity(name=name, entity_type="org", count=count))
    for name, count in name_counter.most_common(5):
        entities.append(ExtractedEntity(name=name, entity_type="person", count=count))
    for name, count in loc_counter.most_common(5):
        entities.append(ExtractedEntity(name=name, entity_type="location", count=count))

    entities.sort(key=lambda e: e.count, reverse=True)
    return entities[:max_entities]
