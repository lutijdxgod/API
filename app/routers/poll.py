from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from ..config import settings

router = APIRouter(prefix="/polls", tags=["Polls"])


@router.post(
    "/init",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PollResponse,
)
async def poll_initiate(
    poll: schemas.PollCreate,
    db: Session = Depends(database.get_db),
):
    new_poll = models.Poll(**poll.dict())
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)

    return new_poll


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_poll(
    questions_with_answers: schemas.PollQuestions,
    db: Session = Depends(database.get_db),
):
    for i in questions_with_answers.questions_answers:
        for question, answers in i.items():
            new_question = models.PollQuestion(
                poll_id=questions_with_answers.poll_id,
                question=question,
                answers=answers,
            )
            db.add(new_question)
            db.commit()

    return {"message": "вопрос(ы) добавлен(ы)"}


@router.get("/active")
async def get_active_polls(db: Session = Depends(database.get_db)):
    active_polls_query = db.query(models.Poll).filter(models.Poll.is_active == "True")
    if not (active_polls_query.first()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="В данный момент нет активных опросов",
        )
    # active_polls = [
    #     (jsonable_encoder(i)["id"], jsonable_encoder(i)["title"], jsonable_encoder(i)["title"])
    #     for i in active_polls_query.all()
    # ]
    active_polls_to_add = []
    active_polls = active_polls_query.all()
    for i in active_polls:
        poll = jsonable_encoder(i)
        creator_id = poll["creator_id"]
        creator = jsonable_encoder(
            db.query(models.User).filter(models.User.id == creator_id).first()
        )
        poll.update(
            {
                "creator_name": creator["name"] + " " + creator["surname"],
                "creator_profile_image": creator["profile_image"],
                "creator_role": creator["role"],
            }
        )
        #
        title_questions_query = db.query(models.PollQuestion).filter(
            models.PollQuestion.poll_id == poll["id"]
        )
        title_questions = title_questions_query.all()

        to_return_questions = []

        for entry in title_questions:
            entry = jsonable_encoder(entry)
            entry.pop("entry_id")
            to_return_questions.append(entry)

        poll.update({"polls": to_return_questions})

        active_polls_to_add.append(poll)

    # for i in active_polls_query.all():
    #     get_query = jsonable_encoder(i)
    #     active_polls.append(
    #         (get_query["id"], get_query["title"], get_query["is_anonymous"])
    #     )

    # for id, title, anonymity in active_polls:
    #     title_questions_query = db.query(models.PollQuestion).filter(
    #         models.PollQuestion.poll_id == id
    #     )
    #     title_questions = title_questions_query.all()

    #     to_return_questions = []

    #     for entry in title_questions:
    #         entry = jsonable_encoder(entry)
    #         entry.pop("entry_id")
    #         to_return_questions.append(entry)

    # return_data.append(
    #     {"name": title, "polls": to_return_questions, "is_anonymous": anonymity}
    # )  # polls это вопросы(Антоха попросил так назвать)

    return active_polls_to_add


@router.get("/{id}")
async def get_poll(id: int, db: Session = Depends(database.get_db)):
    title = db.query(models.Poll).filter(models.Poll.id == id).first()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Опроса с id {id} не существует",
        )

    poll_query = db.query(models.PollQuestion).filter(models.PollQuestion.poll_id == id)
    polls = poll_query.all()
    return polls
