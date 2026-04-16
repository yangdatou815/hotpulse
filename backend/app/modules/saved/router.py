from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.topics.schemas import TopicSummary
from app.modules.topics.service import delete_saved_topic, list_saved_topics, save_topic

router = APIRouter(prefix="/saved", tags=["saved"])


class SaveTopicRequest(BaseModel):
    topic_id: str


@router.get("", response_model=list[TopicSummary])
async def get_saved(
    lang: str = Query(default="en", regex="^(en|zh)$"),
    db: AsyncSession = Depends(get_db),
) -> list[TopicSummary]:
    return await list_saved_topics(db, lang=lang)


@router.post("", status_code=status.HTTP_201_CREATED)
async def save(req: SaveTopicRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    ok = await save_topic(db, req.topic_id)
    if not ok:
        raise HTTPException(status_code=404, detail={"error": {"code": "TOPIC_NOT_FOUND", "message": f"Topic '{req.topic_id}' not found", "details": {}}})
    return {"status": "saved"}


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(topic_id: str, db: AsyncSession = Depends(get_db)) -> Response:
    await delete_saved_topic(db, topic_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
