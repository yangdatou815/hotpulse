"""Tag existing US-Iran topics.

Usage: cd backend && DATABASE_URL="sqlite+aiosqlite:///./hotpulse_dev.db" python -m workers.tag_iran
"""
from __future__ import annotations

import asyncio
import sys

sys.path.insert(0, ".")

from sqlalchemy import select, update
from app.db.session import SessionLocal
from app.modules.topics.models import Topic


async def tag_topics() -> None:
    async with SessionLocal() as session:
        # Tag all US-Iran related topics
        slugs = [
            "us-iran-military-tensions-escalate",
            "global-oil-market-impact-from-us-iran-tensions",
            "us-iran-diplomacy-efforts-by-global-powers",
        ]
        for slug in slugs:
            topic = await session.scalar(
                select(Topic).where(Topic.slug == slug).limit(1)
            )
            if topic:
                topic.tags = "us-iran-conflict,middle-east"
                print(f"  Tagged: {slug}")

        await session.commit()
        print("✅ US-Iran topics tagged")


if __name__ == "__main__":
    asyncio.run(tag_topics())
