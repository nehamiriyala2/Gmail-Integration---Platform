from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    REDIRECT_URI: str

    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()