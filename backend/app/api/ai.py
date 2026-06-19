from fastapi import APIRouter

from app.services.gemini_service import GeminiService

router = APIRouter(
   
    tags=["AI"]
)


@router.post("/summarize")
async def summarize(data: dict):

    email_text = data.get("email")

    if not email_text:
        return {
            "success": False,
            "message": "email field is required"
        }

    result = await GeminiService.summarize_email(
        email_text
    )

    return result


@router.post("/classify")
async def classify(data: dict):

    email_text = data.get("email")

    if not email_text:
        return {
            "success": False,
            "message": "email field is required"
        }

    result = await GeminiService.classify_email(
        email_text
    )

    return result


@router.get("/test")
async def test():

    sample_email = """
    Dear Candidate,

    Congratulations!

    Your interview is scheduled for tomorrow at 10:00 AM.

    Regards,
    HR Team
    """

    summary = await GeminiService.summarize_email(
        sample_email
    )

    classification = await GeminiService.classify_email(
        sample_email
    )

    return {
        "success": True,
        "summary": summary,
        "classification": classification
    }
  
@router.post("/analyze")
async def analyze(data: dict):

    email_text = data.get("email")

    if not email_text:
        return {
            "success": False,
            "message": "email field is required"
        }

    result = await GeminiService.analyze_email(
        email_text
    )

    return result