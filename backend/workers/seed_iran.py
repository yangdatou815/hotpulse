"""Add US-Iran tension topic with rich data.

Usage: cd backend && python -m workers.seed_iran
"""
from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, ".")

from app.db.session import SessionLocal
from app.modules.topics.models import (
    Entity,
    SourceDocument,
    TimelineEvent,
    Topic,
    TopicEntity,
)
from sqlalchemy import select


async def seed_iran_topic() -> None:
    async with SessionLocal() as session:
        # Check if already exists
        existing = await session.scalar(
            select(Topic).where(Topic.slug == "us-iran-military-tensions-escalate").limit(1)
        )
        if existing:
            print("Topic already exists, skipping.")
            return

        now = datetime.now(timezone.utc)

        # ── Main Topic ──
        topic = Topic(
            id="topic_usiran_001",
            slug="us-iran-military-tensions-escalate",
            title="US-Iran Military Tensions Escalate Amid Regional Power Struggle",
            title_zh="美伊军事紧张局势在地区权力争夺中急剧升级",
            summary=(
                "US-Iran military tensions have escalated sharply. The US has deployed a carrier strike group to the Persian Gulf, "
                "while Iran responds with large-scale military exercises. The security situation in the Middle East has drawn global attention, "
                "with multiple countries engaging in diplomatic mediation to prevent escalation. "
                "Analysts note this is the most serious confrontation since 2020."
            ),
            summary_zh=(
                "美伊军事紧张局势急剧升级。美国在波斯湾部署航母战斗群，伊朗进行大规模军事演习作为回应。"
                "中东地区安全形势引发全球关注，多国介入外交斡旋以避免冲突升级。"
                "分析人士指出，当前紧张局势是自2020年以来最严重的对峙。"
            ),
            region="international",
            category="politics",
            heat_score=95,
            freshness="rising",
            source_count=28,
            updated_at=now,
        )
        session.add(topic)

        # ── Timeline Events ──
        events = [
            ("US deploys additional carrier strike group to Persian Gulf",
             "美国向波斯湾增派航母战斗群",
             now - timedelta(days=7), "Pentagon Press Briefing"),
            ("Iran conducts large-scale military exercises near Strait of Hormuz",
             "伊朗在霍尔木兹海峡附近开展大规模军事演习",
             now - timedelta(days=5), "IRNA"),
            ("UN Security Council holds emergency session on escalation",
             "联合国安理会就局势升级召开紧急会议",
             now - timedelta(days=4), "UN News"),
            ("EU mediators begin shuttle diplomacy between Washington and Tehran",
             "欧盟调解人开始在华盛顿和德黑兰之间穿梭外交",
             now - timedelta(days=3), "Reuters"),
            ("China and Russia issue joint statement calling for restraint",
             "中俄发表联合声明呼吁各方克制",
             now - timedelta(days=2), "Xinhua"),
            ("US imposes new sanctions on Iranian defense sector",
             "美国对伊朗国防部门实施新制裁",
             now - timedelta(days=1), "AP News"),
            ("Iran's IRGC conducts ballistic missile test in Gulf of Oman",
             "伊朗伊斯兰革命卫队在阿曼湾进行弹道导弹试射",
             now - timedelta(hours=18), "BBC News"),
            ("Oil prices surge 8% as markets react to escalation",
             "市场对局势升级做出反应，油价飙升 8%",
             now - timedelta(hours=12), "Bloomberg"),
            ("Pentagon confirms additional 3,000 troops deployed to region",
             "五角大楼确认向该地区增派 3000 名士兵",
             now - timedelta(hours=6), "CNN"),
            ("Iran Foreign Minister proposes conditional negotiations framework",
             "伊朗外长提出有条件谈判框架",
             now - timedelta(hours=2), "Al Jazeera"),
        ]
        for title, title_zh, ts, source in events:
            session.add(TimelineEvent(
                topic_id=topic.id,
                title=title,
                title_zh=title_zh,
                timestamp=ts,
                source=source,
            ))

        # ── Entities ──
        entities_data = [
            ("United States", "location", 45),
            ("Iran", "location", 42),
            ("Pentagon", "org", 18),
            ("Islamic Revolutionary Guard Corps", "org", 15),
            ("Persian Gulf", "location", 12),
            ("UN Security Council", "org", 10),
            ("European Union", "org", 8),
            ("Joe Biden", "person", 7),
            ("Ali Khamenei", "person", 6),
            ("China", "location", 5),
            ("Russia", "location", 4),
            ("Strait of Hormuz", "location", 8),
        ]

        for name, etype, count in entities_data:
            entity = Entity(name=name, entity_type=etype)
            session.add(entity)
            await session.flush()
            session.add(TopicEntity(
                topic_id=topic.id,
                entity_id=entity.id,
                mention_count=count,
            ))

        # ── Source Documents ──
        sources_data = [
            ("US sends additional carrier group to Persian Gulf amid tensions",
             "CNN", now - timedelta(days=7),
             "https://example.com/cnn-carrier",
             "The USS Abraham Lincoln carrier strike group has been ordered to the Persian Gulf region as tensions with Iran continue to escalate."),
            ("Iran launches military exercises in response to US naval buildup",
             "BBC News", now - timedelta(days=5),
             "https://example.com/bbc-iran-exercises",
             "Iran's Islamic Revolutionary Guard Corps commenced large-scale military exercises near the Strait of Hormuz in what officials called a defensive measure."),
            ("UN Emergency Session: Security Council debates Iran-US escalation",
             "United Nations", now - timedelta(days=4),
             "https://example.com/un-session",
             "The UN Security Council held an emergency session to address the rapidly deteriorating situation in the Persian Gulf region."),
            ("Oil prices spike as Middle East tensions rattle global markets",
             "Bloomberg", now - timedelta(hours=12),
             "https://example.com/bloomberg-oil",
             "Brent crude surged 8% to above $95/barrel as traders assessed the risk of supply disruptions from a potential conflict in the world's top oil-producing region."),
            ("Pentagon confirms troop deployment to Middle East",
             "AP News", now - timedelta(hours=6),
             "https://example.com/ap-troops",
             "The Department of Defense confirmed the deployment of an additional 3,000 troops to the Middle East region as a precautionary measure."),
            ("EU launches diplomatic initiative to de-escalate US-Iran crisis",
             "Reuters", now - timedelta(days=3),
             "https://example.com/reuters-eu",
             "European Union foreign policy chief has begun shuttle diplomacy between Washington and Tehran in an effort to prevent military confrontation."),
            ("China-Russia joint statement urges calm in Gulf standoff",
             "Xinhua", now - timedelta(days=2),
             "https://example.com/xinhua-joint",
             "China and Russia issued a joint statement calling on all parties to exercise restraint and return to diplomatic channels."),
            ("Iran proposes conditional framework for renewed negotiations",
             "Al Jazeera", now - timedelta(hours=2),
             "https://example.com/aj-negotiations",
             "Iran's Foreign Minister outlined a conditional framework for renewed negotiations, demanding sanctions relief as a precondition for talks."),
        ]
        for title, publisher, pub_time, url, snippet in sources_data:
            session.add(SourceDocument(
                topic_id=topic.id,
                title=title,
                publisher=publisher,
                publish_time=pub_time,
                url=url,
                snippet=snippet,
            ))

        # ── Additional domestic angle topic ──
        topic2 = Topic(
            id="topic_usiran_002",
            slug="global-oil-market-impact-from-us-iran-tensions",
            title="US-Iran Conflict Impacts Global Oil Markets, Prices Hit Two-Year High",
            title_zh="美伊冲突升级冲击全球石油市场 国际油价创两年新高",
            summary=(
                "Affected by the US-Iran military standoff, international crude oil prices have surged significantly, "
                "with Brent crude surpassing $95/barrel. Analysts warn that if Strait of Hormuz shipping is disrupted, "
                "global oil supply will face serious threats and prices could climb above $120. "
                "Multiple countries have begun releasing strategic petroleum reserves to stabilize markets."
            ),
            summary_zh=(
                "受美伊军事对峙影响，国际原油价格大幅上涨，布伦特原油突破95美元/桶。"
                "分析机构警告，若霍尔木兹海峡航运受阻，全球石油供应将面临严重威胁，"
                "原油价格可能进一步攀升至120美元以上。多国开始释放战略石油储备以稳定市场。"
            ),
            region="international",
            category="economy",
            heat_score=88,
            freshness="rising",
            source_count=15,
            updated_at=now,
        )
        session.add(topic2)

        session.add(TimelineEvent(
            topic_id=topic2.id,
            title="Brent crude surpasses $95/barrel on Gulf tensions",
            title_zh="波斯湾紧张局势推动布伦特原油突码95美元/桶",
            timestamp=now - timedelta(hours=12),
            source="Bloomberg",
        ))
        session.add(TimelineEvent(
            topic_id=topic2.id,
            title="Strategic petroleum reserves release announced by IEA members",
            title_zh="国际能源署成员国宣布释放战略石油储备",
            timestamp=now - timedelta(hours=6),
            source="Financial Times",
        ))
        session.add(TimelineEvent(
            topic_id=topic2.id,
            title="OPEC+ emergency meeting called to discuss supply response",
            title_zh="OPEC+召开紧急会议讨论供应对策",
            timestamp=now - timedelta(hours=3),
            source="Reuters",
        ))

        session.add(SourceDocument(
            topic_id=topic2.id,
            title="Oil prices surge on Iran-US military standoff",
            publisher="Bloomberg",
            publish_time=now - timedelta(hours=12),
            url="https://example.com/bloomberg-oil-surge",
            snippet="Global oil prices surged to their highest level in two years as military tensions between the US and Iran raised fears of supply disruptions.",
        ))
        session.add(SourceDocument(
            topic_id=topic2.id,
            title="OPEC weighs emergency output increase amid Gulf tensions",
            publisher="Financial Times",
            publish_time=now - timedelta(hours=6),
            url="https://example.com/ft-opec",
            snippet="OPEC+ members are considering an emergency meeting to discuss boosting oil output to offset potential supply disruptions from the Persian Gulf.",
        ))

        # ── Third topic: diplomatic angle ──
        topic3 = Topic(
            id="topic_usiran_003",
            slug="us-iran-diplomacy-efforts-by-global-powers",
            title="Multiple Nations Launch Diplomatic Efforts to Prevent US-Iran Conflict",
            title_zh="多国发起外交努力以防止美伊冲突",
            summary=(
                "As military tensions intensify, a wave of diplomatic activity has erupted across the globe. "
                "The EU, China, Russia, and Gulf states are all engaged in separate mediation tracks. "
                "The UN Secretary-General called for an immediate de-escalation and proposed a cooling-off framework."
            ),
            summary_zh=(
                "随着军事紧张局势加剧，全球爆发了一波外交活动浪潮。"
                "欧盟、中国、俄罗斯和海湾国家分别开展独立的调解轨道。"
                "联合国秘书长呼吁立即降级并提出了冷静期框架。"
            ),
            region="international",
            category="politics",
            heat_score=82,
            freshness="rising",
            source_count=12,
            updated_at=now,
        )
        session.add(topic3)

        session.add(TimelineEvent(
            topic_id=topic3.id,
            title="UN Secretary-General proposes de-escalation framework",
            title_zh="联合国秘书长提出降级框架",
            timestamp=now - timedelta(days=3),
            source="UN News",
        ))
        session.add(TimelineEvent(
            topic_id=topic3.id,
            title="Saudi Arabia offers to host direct US-Iran talks",
            title_zh="沙特阿拉伯提出主办美伊直接会谈",
            timestamp=now - timedelta(days=1),
            source="Al Arabiya",
        ))
        session.add(TimelineEvent(
            topic_id=topic3.id,
            title="G7 issues joint statement supporting diplomatic resolution",
            title_zh="G7发表联合声明支持外交解决",
            timestamp=now - timedelta(hours=8),
            source="Reuters",
        ))

        session.add(SourceDocument(
            topic_id=topic3.id,
            title="Global powers scramble to prevent US-Iran military confrontation",
            publisher="The Guardian",
            publish_time=now - timedelta(days=2),
            url="https://example.com/guardian-diplomacy",
            snippet="Multiple nations are engaged in frantic diplomatic efforts to prevent a military confrontation between the US and Iran.",
        ))

        await session.commit()
        print("✅ US-Iran topics seeded: 3 topics, 16 timeline events, 12 entities, 11 sources")


if __name__ == "__main__":
    asyncio.run(seed_iran_topic())
