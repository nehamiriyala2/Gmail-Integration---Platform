from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
def dashboard_stats():

    return {
        "total_emails": 120,
        "unread_emails": 15,
        "important_emails": 8,
        "job_emails": 12,
        "interview_emails": 3
    }