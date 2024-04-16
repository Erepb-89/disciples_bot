from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.settings import DESCRIPTIONS, LEVELS, FACTIONS
from database.models import Base

from database.orm_query import orm_add_banner_description, orm_create_factions

# from .env file:
from database.orm_query import orm_create_unit_levels

DB_LITE = "sqlite+aiosqlite:///disc2.db"
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name

engine = create_async_engine(DB_LITE, echo=True)

# engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await orm_add_banner_description(session, DESCRIPTIONS)

    async with session_maker() as session:
        await orm_create_unit_levels(session, LEVELS)

    async with session_maker() as session:
        await orm_create_factions(session, FACTIONS)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
