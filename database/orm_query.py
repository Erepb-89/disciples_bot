from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Units


async def orm_get_units(session: AsyncSession):
    query = select(Units)
    result = await session.scalars(query)
    return result.all()
