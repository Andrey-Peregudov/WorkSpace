from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./database.db"
engine = create_async_engine(DATABASE_URL, echo=True)

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

Base = declarative_base()