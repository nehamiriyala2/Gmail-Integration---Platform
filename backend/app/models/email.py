from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    gmail_message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    sender: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    priority: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )