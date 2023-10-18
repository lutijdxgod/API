from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .. import database, schemas, models
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
    problem = jsonable_encoder(new_problem).copy()
    problem_id = problem["id"]

    tags_to_upload = []
    tags_themselves = []
    for tag in tags:
        tags_themselves.append(tag)
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

    creator_id = problem["creator_id"]
    creator = jsonable_encoder(
        db.query(models.User).filter(models.User.id == creator_id).first()
    )
    problem.update(
        {
            "tags": tags_themselves,
            "creator_name": creator["name"] + " " + creator["surname"],
            "creator_profile_image": creator["profile_image"],
            "creator_role": creator["role"],
        }
    )

    return problem


@router.get("/problem")
async def get_problem(
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(database.get_db),
):
    problems_query = (
        db.query(models.Problem)
        .filter(
            or_(
                models.Problem.content.contains(search),
                models.Problem.title.contains(search),
            )
        )
        .limit(limit)
        .offset(skip)
    )
    if not problems_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подходящие проблемы не найдены",
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


@router.get("/problem_answers")
async def get_problem_answers(problem_id: int, db: Session = Depends(database.get_db)):
    problem_answers_query = db.query(models.ProblemAnswers).filter(
        models.ProblemAnswers.problem_id == problem_id
    )

    if not problem_answers_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ответов пока нет"
        )
    else:
        problem_answers = problem_answers_query.all()
        answers_to_return = []
        for answer in problem_answers:
            answer = jsonable_encoder(answer)
            comment_ids = answer.pop("comments")
            creator_id = answer["creator_id"]
            creator = jsonable_encoder(
                db.query(models.User).filter(models.User.id == creator_id).first()
            )

            if not creator:
                answer.update(
                    {
                        "creator_name": "",
                    }
                )
            else:
                answer.update(
                    {
                        "creator_name": creator["name"] + " " + creator["surname"],
                        "profile_image": creator["profile_image"],
                        "creator_role": creator["role"],
                    }
                )

            comments_to_add = []
            for comment_id in comment_ids:
                comment = jsonable_encoder(
                    db.query(models.ProblemAnswersComments)
                    .filter(models.ProblemAnswersComments.entry_id == comment_id)
                    .first()
                )
                comment.pop("entry_id")
                creator = jsonable_encoder(
                    db.query(models.User)
                    .filter(models.User.id == comment["creator_id"])
                    .first()
                )
                if not creator:
                    answer.update(
                        {
                            "creator_name": "",
                        }
                    )
                else:
                    comment.update(
                        {
                            "creator_name": creator["name"] + " " + creator["surname"],
                            # "creator_role": creator["role"],
                        }
                    )

                comments_to_add.append(comment)
            answer.update({"comments": comments_to_add})
            answers_to_return.append(answer)

    return answers_to_return


@router.post("/problem_answers")
async def post_answer(
    problem_answer: schemas.ProblemAnswerCreate, db: Session = Depends(database.get_db)
):
    problem_answer = models.ProblemAnswers(**problem_answer.dict())
    db.add(problem_answer)
    db.commit()
    db.refresh(problem_answer)

    return problem_answer


@router.post("/problem_answer_comments")
async def create_answer_comment(
    answer_comment: schemas.ProblemAnswerCommentCreate,
    db: Session = Depends(database.get_db),
):
    answer_id = answer_comment.dict()["problem_answer_id"]
    answer_comment = models.ProblemAnswersComments(**answer_comment.dict())

    db.add(answer_comment)
    db.commit()
    db.refresh(answer_comment)
    comment_to_return = jsonable_encoder(answer_comment).copy()

    answer_query = db.query(models.ProblemAnswers).filter(
        models.ProblemAnswers.entry_id == answer_id
    )
    answer = jsonable_encoder(answer_query.first())
    current_comments = answer["comments"]
    current_comments.append(jsonable_encoder(answer_comment)["entry_id"])
    answer.update({"comments": current_comments})

    answer_query.update(answer, synchronize_session=False)
    db.commit()

    return comment_to_return


@router.get("/problem_answer_comments")
async def get_answer_comments(
    problem_answer_id: int, db: Session = Depends(database.get_db)
):
    answer_comments_query = db.query(models.ProblemAnswersComments).filter(
        models.ProblemAnswersComments.problem_answer_id == problem_answer_id
    )
    comments = answer_comments_query.all()
    comments_to_return = []
    for comment in comments:
        comment = jsonable_encoder(comment)
        comment.pop("problem_answer_id")
        comments_to_return.append(comment)

    return comments_to_return
