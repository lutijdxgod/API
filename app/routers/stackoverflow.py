from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .. import database, schemas, models
from ..config import settings
from typing import Optional, List

router = APIRouter(prefix="/stackoverflow", tags=["Local Stack Overflow"])


@router.post("/problem")
async def post_problem(
    problem_to_upload: schemas.ProblemCreate,
    tags: Optional[List[str]] = [],
    db: Session = Depends(database.get_db),
):
    new_problem = models.Problem(**problem_to_upload.dict())
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    problem_id = jsonable_encoder(new_problem)["id"]

    tags_to_upload = []
    for tag in tags:
        tag_query = db.query(models.Tags).filter(models.Tags.tag == tag)
        tag_itself = tag_query.first()
        if not tag_itself:
            tag_model = models.Tags(tag=tag)
            db.add(tag_model)
            db.commit()
            db.refresh(tag_model)
            tag_id = jsonable_encoder(tag_model)["tag_id"]
            tags_to_upload.append(tag_id)
        else:
            tag = jsonable_encoder(tag_itself)["tag_id"]
            tags_to_upload.append(tag)

    db.add(models.ProblemTags(problem_id=problem_id, tags=tags_to_upload))
    db.commit()

    return {"message": "success"}


@router.get("/problem")
async def get_problem(
    limit: int = 10, skip: int = 0, db: Session = Depends(database.get_db)
):
    problems_query = (
        db.query(models.Problem)
        .filter(models.Problem.is_solved == False)
        .limit(limit)
        .offset(skip)
    )
    if not problems_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="В данный момент нет проблем, которые нужно помочь устранить",
        )
    problem_list = []
    for problem in problems_query.all():
        problem = jsonable_encoder(problem)
        creator_id = problem["creator_id"]
        creator_query = db.query(models.User).filter(models.User.id == creator_id)
        creator = jsonable_encoder(creator_query.first())
        problem.update(
            {
                "creator_name": creator["name"] + " " + creator["surname"],
                "creator_profile_image": creator["profile_image"],
                "creator_role": creator["role"],
            }
        )
        problem.pop("is_solved")  # убрал ненужный параметр при выводе
        tags_query = db.query(models.ProblemTags).filter(
            models.ProblemTags.problem_id == problem["id"]
        )
        tags = tags_query.first()
        if not tags:
            problem.update({"tags": []})
        else:
            tag_list = []
            tag_ids = jsonable_encoder(tags)["tags"]
            for tag_id in tag_ids:
                tags_to_add_query = db.query(models.Tags).filter(
                    models.Tags.tag_id == tag_id
                )
                tags = jsonable_encoder(tags_to_add_query.all())
                for tag in tags:
                    tag = jsonable_encoder(tag)["tag"]
                    tag_list.append(tag)
                problem.update({"tags": tag_list})

        problem_list.append(problem)

    return problem_list
