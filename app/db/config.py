import reflex as rx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+aiomysql://user:password@host/db_name"


class DBConfig:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


db_config = DBConfig()
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with db_config.SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()