from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .. import database, schemas, models
from typing import Optional, List

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/create")
async def create_some_news(
    news_to_add: schemas.NewsCreate, db: Session = Depends(database.get_db)
):
    news_to_add = news_to_add.dict()
    creator_id = news_to_add["creator_id"]
    news = models.News(**news_to_add)
    db.add(news)
    db.commit()
    db.refresh(news)
    news_to_return = jsonable_encoder(news)

    creator = jsonable_encoder(
        db.query(models.User).filter(models.User.id == creator_id).first()
    )
    news_to_return.update(
        {
            "creator_name": creator["name"] + " " + creator["surname"],
            "creator_profile_image": creator["profile_image"],
            "creator_role": creator["role"],
        }
    )

    return news_to_return


@router.get("/get")
async def get_news(db: Session = Depends(database.get_db)):
    news_query = db.query(models.News).order_by(models.News.created_at.desc())

    if not news_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Никаких новостей в данный момент",
        )

    news_to_return = []
    news = news_query.all()
    for entry in news:
        entry = jsonable_encoder(entry)
        creator_id = entry["creator_id"]
        # entry.pop("creator_id")  ## спорно, удалять или нет
        creator = jsonable_encoder(
            db.query(models.User).filter(models.User.id == creator_id).first()
        )
        entry.update(
            {
                "creator_name": creator["name"] + " " + creator["surname"],
                "creator_profile_image": creator["profile_image"],
                "creator_role": creator["role"],
            }
        )
    news_to_return.append(entry)

    return news_to_return
