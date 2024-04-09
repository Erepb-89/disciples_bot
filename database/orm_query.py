from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Units, UnitLevel, Banner


async def orm_get_units(session: AsyncSession, level_id):
    if level_id is not None:
        query = select(Units).where(Units.level == int(level_id))
    else:
        query = select(Units)
    result = await session.scalars(query)
    return result.all()


async def orm_get_unit_levels(session: AsyncSession):
    query = select(UnitLevel)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_create_unit_levels(session: AsyncSession, unit_levels: list):
    query = select(UnitLevel)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([UnitLevel(level=level) for level in unit_levels])
    await session.commit()


async def orm_add_banner_description(session: AsyncSession,
                                     data: dict):
    # Добавляем новый или изменяем существующий по именам
    # пунктов меню: main, about, game, factions, screenshots, units
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return

    session.add_all([Banner(name=name,
                            description=description)
                     for name, description in data.items()])

    await session.commit()


async def orm_get_banner(session: AsyncSession, page_name: str):
    query = select(Banner).where(Banner.name == page_name)
    result = await session.scalar(query)
    return result
