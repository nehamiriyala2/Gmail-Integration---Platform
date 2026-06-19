from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.models.base import Base


class Token(Base):

    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    access_token = Column(
        String,
        nullable=False
    )

    refresh_token = Column(
        String,
        nullable=True
    )