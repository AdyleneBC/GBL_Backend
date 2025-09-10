from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/tu_db"
)

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
