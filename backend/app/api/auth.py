from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from dotenv import load_dotenv

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.gmail_service import GmailService

import os
import secrets
import warnings

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly"
]

CODE_VERIFIER = None


@router.get("/google-login")
async def google_login():

    global CODE_VERIFIER

    CODE_VERIFIER = secrets.token_urlsafe(64)

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.code_verifier = CODE_VERIFIER

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    return {
        "success": True,
        "auth_url": authorization_url
    }


@router.get("/callback")
async def callback(
    request: Request,
    session: AsyncSession = Depends(get_db)
):

    global CODE_VERIFIER

    code = request.query_params.get("code")

    if not code:
        return {
            "success": False,
            "message": "Authorization code not found"
        }

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.code_verifier = CODE_VERIFIER

    warnings.filterwarnings("ignore")

    flow.fetch_token(code=code)

    credentials = flow.credentials

    access_token = credentials.token
    refresh_token = credentials.refresh_token

    idinfo = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        CLIENT_ID
    )

    google_id = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo.get("name", "")

    user = await UserRepository.get_by_email(
        session,
        email
    )

    if not user:

        user = await UserRepository.create_user(
            session=session,
            email=email,
            name=name,
            google_id=google_id
        )

    await UserRepository.update_tokens(
        session=session,
        user=user,
        access_token=credentials.token,
        refresh_token=credentials.refresh_token
    )

    profile = await GmailService.get_profile(
        credentials
    )

    return {
        "success": True,
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "gmail_address": profile.get("emailAddress"),
        "total_messages": profile.get("messagesTotal"),
        "gmail_connected": True,
        "token_saved": True
    }


@router.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": "google-auth"
    }