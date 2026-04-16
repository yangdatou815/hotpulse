"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "topics",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("region", sa.String(length=32), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("heat_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("freshness", sa.String(length=16), nullable=False, server_default="stable"),
        sa.Column("source_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_topics_slug", "topics", ["slug"], unique=True)
    op.create_index("ix_topics_region", "topics", ["region"], unique=False)
    op.create_index("ix_topics_category", "topics", ["category"], unique=False)

    op.create_table(
        "timeline_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("topic_id", sa.String(length=64), sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_timeline_events_topic_id", "timeline_events", ["topic_id"], unique=False)

    op.create_table(
        "entities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=False),
    )
    op.create_index("ix_entities_name", "entities", ["name"], unique=False)

    op.create_table(
        "topic_entities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("topic_id", sa.String(length=64), sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mention_count", sa.Integer(), nullable=False, server_default="1"),
    )
    op.create_index("ix_topic_entities_topic_id", "topic_entities", ["topic_id"], unique=False)
    op.create_index("ix_topic_entities_entity_id", "topic_entities", ["entity_id"], unique=False)

    op.create_table(
        "source_documents",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("topic_id", sa.String(length=64), sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("publisher", sa.String(length=255), nullable=False),
        sa.Column("publish_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("snippet", sa.Text(), nullable=False),
    )
    op.create_index("ix_source_documents_topic_id", "source_documents", ["topic_id"], unique=False)

    op.create_table(
        "saved_topics",
        sa.Column("topic_id", sa.String(length=64), sa.ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("saved_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("saved_topics")
    op.drop_index("ix_source_documents_topic_id", table_name="source_documents")
    op.drop_table("source_documents")
    op.drop_index("ix_topic_entities_entity_id", table_name="topic_entities")
    op.drop_index("ix_topic_entities_topic_id", table_name="topic_entities")
    op.drop_table("topic_entities")
    op.drop_index("ix_entities_name", table_name="entities")
    op.drop_table("entities")
    op.drop_index("ix_timeline_events_topic_id", table_name="timeline_events")
    op.drop_table("timeline_events")
    op.drop_index("ix_topics_category", table_name="topics")
    op.drop_index("ix_topics_region", table_name="topics")
    op.drop_index("ix_topics_slug", table_name="topics")
    op.drop_table("topics")
