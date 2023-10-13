from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    role: str
    age: int
    sex: str
    profile_image: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserVerifyEmail(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    password: str
    verification_code: int


# class CheckValidity(BaseModel):
#     email: EmailStr
#     code: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# class Vote(BaseModel):
#     post_id: int
#     dir: conint(le=1)


class PollCreate(BaseModel):
    title: str
    creator_id: int
    is_anonymous: Optional[bool] = False
    is_active: Optional[bool] = True


class PollResponse(BaseModel):
    id: int
    title: str
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PollQuestions(BaseModel):
    poll_id: int
    questions_answers: list


class ProblemCreate(BaseModel):
    creator_id: int
    title: str
    content: str
    images: Optional[List[str]] = []


class ProblemAnswerCreate(BaseModel):
    problem_id: int
    creator_id: int
    content: str
    images: Optional[List[str]] = []


class ProblemAnswerCommentCreate(BaseModel):
    problem_answer_id: int
    creator_id: int
    content: str


class NewsCreate(BaseModel):
    creator_id: int
    content: str
    images: Optional[List[str]] = []
