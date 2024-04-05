from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Units


async def orm_get_units(session: AsyncSession):
    query = select(Units)
    result = await session.scalars(query)
    return result.all()


# async def orm_add_banner_description(session: AsyncSession,
#                                      data: dict):
#     # Добавляем новый или изменяем существующий по именам
#     # пунктов меню: main, about, game, factions, screenshots, units
#     query = select(Banner)
#     result = await session.execute(query)
#     if result.first():
#         return
#
#     session.add_all([Banner(name=name,
#                             description=description)
#                      for name, description in data.items()])
#     await session.commit()
#
#
# async def orm_get_banner(session: AsyncSession, page_name: str):
#     query = select(Banner).where(Banner.name == page_name)
#     result = await session.scalar(query)
#     return result
