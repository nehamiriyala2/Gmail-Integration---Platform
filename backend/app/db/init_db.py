from app.db.database import engine
from app.models.base import Base

import app.models.user
import app.models.email


async def create_tables():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )