from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.ai import router as ai_router
from app.api.gmail import router as gmail_router

from app.db.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating database tables...")

    await create_tables()

    print("Database ready.")

    yield

    print("Application shutdown.")


app = FastAPI(
    title="Gmail Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)

app.include_router(
    gmail_router
)

@app.get("/")
async def root():

    return {
        "message": "Gmail Intelligence Platform Running",
        "status": "healthy"
    }