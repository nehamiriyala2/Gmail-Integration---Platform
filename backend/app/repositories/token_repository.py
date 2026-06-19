from sqlalchemy import select

from app.models.token import Token


class TokenRepository:

    @staticmethod
    async def get_user_token(
        session,
        user_id
    ):

        result = await session.execute(
            select(Token).where(
                Token.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create_token(
        session,
        user_id,
        access_token,
        refresh_token
    ):

        token = Token(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )

        session.add(token)

        await session.commit()

        await session.refresh(token)

        return token