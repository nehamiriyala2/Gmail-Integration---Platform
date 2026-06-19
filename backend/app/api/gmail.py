from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from google.oauth2.credentials import Credentials

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.gmail_service import GmailService
from app.services.gemini_service import GeminiService
from app.repositories.email_repository import EmailRepository
from datetime import datetime

import os


router = APIRouter(
    prefix="/gmail",
    tags=["Gmail"]
)

@router.get("/emails")
async def get_emails(
    session: AsyncSession = Depends(get_db)
):
    emails = await EmailRepository.get_all(session)

    return {
        "success": True,
        "count": len(emails),
        "emails": [
            {
                "id": email.id,
                "subject": email.subject,
                "sender": email.sender,
                "category": email.category,
                "priority": email.priority,
                "created_at": str(email.created_at)
            }
            for email in emails
        ]
    }
    
@router.get("/profile")
async def get_profile(
    session: AsyncSession = Depends(get_db)
):

    user = await UserRepository.get_by_email(
        session,
        "nehamiriyala2025@gmail.com"
    )

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if not user.access_token:
        return {
            "success": False,
            "message": "Gmail not connected"
        }

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    profile = await GmailService.get_profile(
        credentials
    )

    return {
        "success": True,
        "profile": profile
    }


@router.get("/analyze-emails")
async def analyze_emails():

    sample_email = """
    Dear Candidate,

    Congratulations!

    Your interview is scheduled tomorrow at 10:00 AM.

    Please join 15 minutes early.

    Regards,
    HR Team
    """

    result = await GeminiService.analyze_email(
        sample_email
    )

    return result


@router.get("/health")
async def health():

    return {
        "success": True,
        "message": "Gmail route working"
    }


@router.get("/analyze-latest")
async def analyze_latest(
    session: AsyncSession = Depends(get_db)
):

    user = await UserRepository.get_by_email(
        session,
        "nehamiriyala2025@gmail.com"
    )

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    emails = await GmailService.get_emails(
        credentials,
        max_results=1
    )

    if not emails:
        return {
            "success": False,
            "message": "No emails found"
        }

    email_text = emails[0]["snippet"]

    result = await GeminiService.analyze_email(
        email_text
    )

    return {
        "email": emails[0],
        "analysis": result
    }


@router.get("/email/{message_id}")
async def get_email(
    message_id: str,
    session: AsyncSession = Depends(get_db)
):

    user = await UserRepository.get_by_email(
        session,
        "nehamiriyala2025@gmail.com"
    )

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    email = await GmailService.get_email_by_id(
        credentials,
        message_id
    )

    return {
        "success": True,
        "email": email
    }
@router.get("/save-latest-email")
async def save_latest_email(
    session: AsyncSession = Depends(get_db)
):

    user = await UserRepository.get_by_email(
        session,
        "nehamiriyala2025@gmail.com"
    )

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    emails = await GmailService.get_emails(
        credentials=credentials,
        max_results=1
    )
    latest_email = emails[0]

    if not emails:
        return {
            "success": False,
            "message": "No emails found"
        }

    email = emails[0]

    existing = await EmailRepository.get_by_gmail_id(
        session,
        email["id"]
    )

    if existing:
        return {
            "success": True,
            "message": "Email already saved"
        }

    analysis = await GeminiService.analyze_email(
        email["snippet"]
    )

    await EmailRepository.create(
        session,
        {
            "user_id": user.id,
            "gmail_message_id": latest_email["id"],
            "subject": latest_email["subject"],
            "sender": latest_email["from"],
            "body": latest_email.get("snippet",""),
           
            "category": "Job",
            "priority": "Medium",
            "summary": str(analysis),
            "created_at":datetime.utcnow()
        }
    )

    return {
        "success": True,
        "message": "Email saved successfully"
    }

@router.get("/saved-emails")
async def get_saved_emails(
    session: AsyncSession = Depends(get_db)
):
    emails = await EmailRepository.get_all(session)

    return {
        "success": True,
        "count": len(emails),
        "emails": emails
    }
@router.get("/emails/{email_id}")
async def get_email_by_id(
    email_id: int,
    session: AsyncSession = Depends(get_db)
):
    email = await EmailRepository.get_by_id(
        session,
        email_id
    )

    if not email:
        return {
            "success": False,
            "message": "Email not found"
        }

    return {
        "success": True,
        "email": {
            "id": email.id,
            "subject": email.subject,
            "sender": email.sender,
            "category": email.category,
            "priority": email.priority,
            "summary": email.summary
        }
    }

@router.delete("/emails/{email_id}")
async def delete_email(
    email_id: int,
    session: AsyncSession = Depends(get_db)
):
    deleted = await EmailRepository.delete(
        session,
        email_id
    )

    if not deleted:
        return {
            "success": False,
            "message": "Email not found"
        }

    return {
        "success": True,
        "message": "Email deleted successfully"
    }

@router.get("/dashboard")
async def dashboard(
    session: AsyncSession = Depends(get_db)
):

    stats = await EmailRepository.get_dashboard_stats(
        session
    )

    return {
        "success": True,
        "dashboard": stats
    }

@router.get("/gmail/threads")
async def get_threads():

    return {
        "threads": [
            {
                "sender": "Amazon",
                "count": 3
            },
            {
                "sender": "Google",
                "count": 2
            }
        ]
    }