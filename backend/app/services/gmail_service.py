from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailService:

    @staticmethod
    async def get_profile(credentials):
        try:
            service = build(
                "gmail",
                "v1",
                credentials=credentials
            )

            profile = (
                service.users()
                .getProfile(userId="me")
                .execute()
            )

            print("PROFILE =", profile)

            return profile

        except Exception as e:
            print(f"Gmail Profile Error: {e}")
            return {}

    @staticmethod
    async def get_emails(
        credentials,
        max_results=10
    ):
        try:

            service = build(
                "gmail",
                "v1",
                credentials=credentials
            )

            results = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    maxResults=max_results
                )
                .execute()
            )

            messages = results.get(
                "messages",
                []
            )

            email_list = []

            for msg in messages:

                message = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg["id"]
                    )
                    .execute()
                )

                headers = (
                    message
                    .get("payload", {})
                    .get("headers", [])
                )

                subject = ""
                sender = ""
                date = ""

                for header in headers:

                    if header["name"] == "Subject":
                        subject = header["value"]

                    elif header["name"] == "From":
                        sender = header["value"]

                    elif header["name"] == "Date":
                        date = header["value"]

                email_list.append(
                    {
                        "id": msg["id"],
                        "subject": subject,
                        "from": sender,
                        "date": date,
                        "snippet": message.get(
                            "snippet",
                            ""
                        )
                    }
                )

            return email_list

        except HttpError as e:
            print(f"Gmail API Error: {e}")
            return []

        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []

    @staticmethod
    async def get_email_by_id(
        credentials,
        message_id
    ):
        try:

            service = build(
                "gmail",
                "v1",
                credentials=credentials
            )

            message = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id
                )
                .execute()
            )

            headers = (
                message
                .get("payload", {})
                .get("headers", [])
            )

            subject = ""
            sender = ""
            date = ""

            for header in headers:

                if header["name"] == "Subject":
                    subject = header["value"]

                elif header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Date":
                    date = header["value"]

            return {
                "id": message_id,
                "subject": subject,
                "from": sender,
                "date": date,
                "snippet": message.get(
                    "snippet",
                    ""
                )
            }

        except Exception as e:

            print(f"Get Email Error: {e}")

            return {}