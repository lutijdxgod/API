import fastapi
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = fastapi.APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = fastapi.Depends(get_db),
                    current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, 
                       func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = fastapi.Depends(get_db), current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user)):
    new_post = post.dict()
    new_post.update({"owner_id": current_user.id})
    new_post = models.Post(**new_post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = fastapi.Depends(get_db), current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()


    post = db.query(models.Post, 
                       func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f"post with id: {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise fastapi.HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN,
    #                                 detail="Not authorized to perform requested action")
    
    return post


@router.delete("/{id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = fastapi.Depends(get_db), current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user)):

    to_delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    to_delete_post = to_delete_post_query.first()

    if not to_delete_post:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")

    if to_delete_post.owner_id != current_user.id:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail="Not authorized to perform requested action")

    to_delete_post_query.delete(synchronize_session=False)
    db.commit()
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = fastapi.Depends(get_db), current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user)):

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()

    if not updated_post:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")


    if updated_post.owner_id != current_user.id:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail="Not authorized to perform requested action")

    
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post_query.first()
