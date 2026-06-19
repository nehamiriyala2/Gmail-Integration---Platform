from sqlalchemy import select
from sqlalchemy import select, func
from app.models.email import Email


class EmailRepository:

    @staticmethod
    async def get_by_gmail_id(
        session,
        gmail_message_id
    ):
        result = await session.execute(
            select(Email).where(
                Email.gmail_message_id == gmail_message_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        session,
        data
    ):
        email = Email(**data)

        session.add(email)

        await session.commit()

        await session.refresh(email)

        return email

    @staticmethod
    async def get_all(
        session
    ):
        result = await session.execute(
            select(Email)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        session,
        email_id: int
    ):
        result = await session.execute(
            select(Email).where(
                Email.id == email_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        session,
        email_id: int
    ):
        email = await EmailRepository.get_by_id(
            session,
            email_id
        )

        if not email:
            return False

        await session.delete(email)

        await session.commit()

        return True
    
    @staticmethod
    async def delete(session, email_id: int):
        email = await EmailRepository.get_by_id(
        session,
        email_id
        )

        if not email:
            return False

        await session.delete(email)
        await session.commit()

        return True
    @staticmethod
    async def get_dashboard_stats(session):

        result = await session.execute(
        select(Email)
        )

        emails = result.scalars().all()

        print("TOTAL EMAILS =", len(emails))

        return {
            "total_emails": len(emails),
            "job_emails": len(
            [e for e in emails if e.category == "Job"]
            ),
            "high_priority": len(
            [e for e in emails if e.priority == "High"]
            ),
            "latest_email": (
            emails[-1].subject
            if emails else None
            )
        }