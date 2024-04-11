from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import (
    Units,
    UnitLevel,
    Banner,
    User,
    Favourites,
)


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


async def orm_add_user(
        session: AsyncSession,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id,
                 first_name=first_name,
                 last_name=last_name)
        )
        await session.commit()


async def orm_add_to_favs(session: AsyncSession,
                          user_id: int,
                          unit_id: int):
    query = select(Favourites).where(
        Favourites.user_id == user_id,
        Favourites.unit_id == unit_id)
    favs = await session.execute(query)
    favs = favs.scalar()
    if favs:
        return favs
    else:
        session.add(Favourites(user_id=user_id,
                               unit_id=unit_id))
        await session.commit()


async def orm_get_user_favs(session: AsyncSession, user_id):
    query = select(Favourites).filter(
        Favourites.user_id == user_id).options(
        joinedload(Favourites.unit))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_from_favs(session: AsyncSession,
                               user_id: int,
                               unit_id: int):
    query = delete(Favourites).where(
        Favourites.user_id == user_id,
        Favourites.unit_id == unit_id)
    await session.execute(query)
    await session.commit()
