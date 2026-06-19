import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiService:

    MODEL_NAME = "models/gemini-2.5-flash"

    @staticmethod
    async def summarize_email(text: str):

        try:
            model = genai.GenerativeModel(
                GeminiService.MODEL_NAME
            )

            response = model.generate_content(
                f"""
                Summarize the following email in 3-5 concise points.

                Email:
                {text}
                """
            )

            return {
                "success": True,
                "summary": response.text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def classify_email(text: str):

        try:
            model = genai.GenerativeModel(
                GeminiService.MODEL_NAME
            )

            prompt = f"""
            Classify this email into ONLY ONE category.

            Categories:
            - Job
            - Interview
            - Promotion
            - Finance
            - Personal
            - Spam
            - General

            Email:
            {text}

            Return only the category name.
            """

            response = model.generate_content(prompt)

            return {
                "success": True,
                "category": response.text.strip()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def summarize_and_classify(text: str):

        summary = await GeminiService.summarize_email(text)

        classification = await GeminiService.classify_email(text)

        return {
            "success": True,
            "summary": summary,
            "classification": classification
        }

    @staticmethod
    async def analyze_email(text: str):

        try:
            model = genai.GenerativeModel(
                GeminiService.MODEL_NAME
            )

            prompt = f"""
Analyze this email.

Return JSON only:

{{
    "category": "",
    "priority": "",
    "summary": ""
}}

Categories:
- Job
- Interview
- Promotion
- Finance
- Personal
- Spam
- General

Priority:
- High
- Medium
- Low

Email:
{text}
"""

            response = model.generate_content(prompt)

            return {
                "success": True,
                "analysis": response.text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }