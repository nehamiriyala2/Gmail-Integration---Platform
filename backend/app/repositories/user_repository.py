from sqlalchemy import select

from app.models.user import User


class UserRepository:

    @staticmethod
    async def get_by_email(
        session,
        email
    ):
        result = await session.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(
        session,
        user_id
    ):
        result = await session.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        session,
        email,
        name,
        google_id
    ):
        user = User(
            email=email,
            name=name,
            google_id=google_id
        )

        session.add(user)

        await session.commit()

        await session.refresh(user)

        return user

    @staticmethod
    async def update_tokens(
        session,
        user,
        access_token,
        refresh_token
    ):
        user.access_token = access_token
        user.refresh_token = refresh_token

        await session.commit()

        await session.refresh(user)

        return user

    @staticmethod
    async def get_user_with_tokens(
        session,
        email
    ):
        result = await session.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()