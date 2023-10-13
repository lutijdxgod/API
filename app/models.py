from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey  # , JSON
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, server_default="")
    surname = Column(String, nullable=False, server_default="")
    role = Column(String, server_default="-")
    age = Column(Integer, nullable=False, server_default="1")
    sex = Column(String, nullable=False, server_default="N")
    verification_code = Column(Integer, unique=True)
    password = Column(String, nullable=False)
    profile_image = Column(
        String,
        nullable=False,
        server_default="https://mykaleidoscope.ru/x/uploads/posts/2023-05/1684818829_mykaleidoscope-ru-p-strizhka-stasa-pekhi-pinterest-69.jpg",
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default="True", nullable=False)
    title = Column(String, nullable=False)
    is_anonymous = Column(Boolean, server_default="False", nullable=False)
    # retractable_choices = Column(Boolean, server_default="True", nullable=False)
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
        ARRAY(String, dimensions=1, zero_indexes=True),
        nullable=False,
        server_default="{}",
    )
    min_responses = Column(Integer, server_default="1", nullable=False)
    max_responses = Column(Integer, server_default="1", nullable=False)


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
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    images = Column(
        ARRAY(String, dimensions=1, zero_indexes=True),
        nullable=True,
        server_default="{}",
    )
    is_solved = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class ProblemAnswers(Base):
    __tablename__ = "problem_answers"

    entry_id = Column(Integer, primary_key=True, nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"))
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    content = Column(String, nullable=False)
    images = Column(
        ARRAY(String, dimensions=1, zero_indexes=True),
        nullable=True,
        server_default="{}",
    )
    comments = Column(
        ARRAY(Integer, dimensions=1, zero_indexes=True),
        nullable=True,
        server_default="{}",
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class ProblemAnswersComments(Base):
    __tablename__ = "problem_answers_comments"

    entry_id = Column(Integer, primary_key=True, nullable=False)
    problem_answer_id = Column(
        Integer, ForeignKey("problem_answers.entry_id"), nullable=False
    )
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="NO ACTION"))
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Tags(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, nullable=False, unique=True)
    info = Column(String, nullable=True)


class ProblemTags(Base):
    __tablename__ = "problem_tags"

    problem_id = Column(
        Integer, ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True
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


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, nullable=False)
    creator_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(String, nullable=False)
    images = Column(ARRAY(String, dimensions=1, zero_indexes=True), server_default="{}")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
