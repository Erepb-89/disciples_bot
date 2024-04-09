import os
from typing import Optional

from aiogram.types import InputMediaPhoto, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_get_units,
    orm_get_unit_levels,
    orm_get_banner,
)
from keyboards.inline import (
    get_units_btns,
    get_user_main_btns, get_user_catalog_btns,
)

from utils.paginator import Paginator

PARENT_DIR = os.getcwd()


async def main_menu(session, level_menu, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), f'screenshots/{banner.image}')),
        caption=banner.description)

    kbds = get_user_main_btns(level_menu=level_menu)

    return image, kbds


def pages_all(paginator: Paginator):
    btns = {}
    btns["◀ Пред."] = "previous"
    btns["След. ▶"] = "next"

    return btns


def pages(paginator: Paginator):
    btns = {}
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def units(session, level_menu, page, level_unit):
    units_list = await orm_get_units(session, level_id=level_unit)

    paginator = Paginator(units_list, page=page)
    unit = paginator.get_page()[0]

    portraits_path = os.path.join(PARENT_DIR, 'images/portraits')
    image_path = os.path.join(portraits_path, f'{unit.name}.gif')

    image = InputMediaPhoto(
        media=FSInputFile(image_path),
        caption=f"<b>{unit.name}</b>\n\n"
                f"{unit.desc}\n"
                f"Уровень: {unit.level}\n"
                f"Размер: {unit.size}\n"
                f"Стоимость: {unit.price}\n"
                f"Опыт: {unit.exp}\n"
                f"Опыт за убийство: {unit.exp_per_kill}\n"
                f"Здоровье: {unit.health}\n"
                f"Броня: {unit.armor}\n"
                f"Иммунитет: {unit.immune}\n"
                f"Защита: {unit.ward}\n"
                f"Атака: {unit.attack_type}\n"
                f"Шанс попадания: {unit.attack_chance}\n"
                f"Урон: {unit.attack_dmg}\n"
                f"Периодический урон: {unit.dot_dmg}\n"
                f"Источник атаки: {unit.attack_source}\n"
                f"Инициатива: {unit.attack_ini}\n"
                f"Радиус: {unit.attack_radius}\n"
                f"Цели: {unit.attack_purpose}\n"
                f"Атакует дважды: {unit.attack_twice}\n"
                f"Предыдущая форма: {unit.prev_level}\n",
    )

    pagination_btns = pages(paginator)

    kbds = get_units_btns(
        level_menu=level_menu,
        page=page,
        pagination_btns=pagination_btns,
        unit_id=unit.id,
        level_unit=unit.level,
    )

    return image, kbds


async def catalog(session, level_menu, menu_name):
    banner = await orm_get_banner(session, menu_name)

    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), f'screenshots/{banner.image}')))

    unit_levels = await orm_get_unit_levels(session)
    kbds = get_user_catalog_btns(
        level_menu=level_menu,
        unit_levels=unit_levels)

    return image, kbds


async def get_menu_content(
        session: AsyncSession,
        level_menu: int,
        menu_name: str,
        page: Optional[int] = None,
        level_unit: int = None
):
    if level_menu == 0:
        return await main_menu(session, level_menu, menu_name)
    if level_menu == 1:
        return await catalog(session, level_menu, menu_name)
    if level_menu == 2:
        return await units(session, level_menu, page, level_unit)
