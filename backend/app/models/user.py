from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    google_id: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    access_token: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    refresh_token: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )