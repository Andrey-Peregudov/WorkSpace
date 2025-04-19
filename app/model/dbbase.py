from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

# Подключение к базе данных SQLite
DATABASE_URL = "sqlite+aiosqlite:///./database.db"
# Создание асинхронного движока SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия для работы с БД
async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

# Базовый класс моделей SQLAlchemy
Base = declarative_base()