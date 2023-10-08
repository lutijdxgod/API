from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey  # , JSON
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship
from .database import Base


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, server_default="True", nullable=False)
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
#     owner_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )

#     owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, server_default="")
    surname = Column(String, nullable=False, server_default="")
    role = Column(String)
    age = Column(Integer)
    sex = Column(String)
    verification_code = Column(Integer, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    is_anonymous = Column(Boolean, server_default="False", nullable=False)
    retractable_choices = Column(Boolean, server_default="True", nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class PollQuestion(Base):
    __tablename__ = "poll_questions"

    entry_id = Column(Integer, primary_key=True, nullable=False)
    poll_id = Column(
        Integer,
        ForeignKey("polls.id", ondelete="CASCADE"),
        nullable=False,
    )
    question = Column(String, nullable=False)
    answers = Column(
        ARRAY(String, dimensions=1, zero_indexes=True), nullable=False
    )  # JSON


# ----------------2version----------------


# class PollQuestion(Base):
#     __tablename__ = "poll_questions"

#     poll_id = Column(
#         Integer,
#         ForeignKey("polls.id", ondelete="CASCADE"),
#         nullable=False
#     )
#     question = Column(String, nullable=False, unique=True)

# ----------------2version----------------


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # photos
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Tags(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, nullable=False, unique=True)


class ProblemTags(Base):
    __tablename__ = "problem_tags"

    problem_id = Column(
        Integer, ForeignKey("problems.id", ondelete="SET NULL"), primary_key=True
    )
    tags = Column(ARRAY(Integer, dimensions=1, zero_indexes=True), server_default="{}")


# class Vote(Base):
#     __tablename__ = "votes"

#     post_id = Column(
#         Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
#     )
#     user_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
#     )
