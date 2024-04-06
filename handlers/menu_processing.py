import os
from typing import Optional

from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy.ext.asyncio import AsyncSession

from common.settings import EMPIRE_DESC_SHORT, \
    LEGIONS_DESC_SHORT, CLANS_DESC_SHORT, HORDES_DESC_SHORT
from database.orm_query import (
    orm_get_units,
)
from keyboards.inline import (
    get_units_btns,
    get_user_main_btns,
    # get_screenshots_btns,
)

from utils.paginator import Paginator

PARENT_DIR = os.getcwd()


async def main_menu(level_menu):
    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), 'screenshots/Represent.png')),
        caption="Главное меню")

    kbds = get_user_main_btns(level_menu=level_menu)

    return image, kbds


def pages(paginator: Paginator):
    btns = {}
    btns["◀ Пред."] = "previous"
    btns["След. ▶"] = "next"

    return btns


async def about(level_menu):
    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), 'screenshots/Represent_02.png')),
        caption='Бот для просмотра информации об игре Disciples Mobile. '
                'Здесь Вы можете просмотреть игровые скриншоты, '
                'а также характеристики юнитов.')

    kbds = get_user_main_btns(level_menu=level_menu)

    return image, kbds


async def factions(level_menu):
    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), 'screenshots/Represent_05.png')),
        caption=f'<b>Список игровых фракций:</b>\n'
                f'<b>Империя:</b>\n{EMPIRE_DESC_SHORT}\n\n'
                f'<b>Орды Нежити:</b>\n{HORDES_DESC_SHORT}\n\n'
                f'<b>Легионы Проклятых:</b>\n{LEGIONS_DESC_SHORT}\n\n'
                f'<b>Горные Кланы:</b>\n{CLANS_DESC_SHORT}\n\n')

    kbds = get_user_main_btns(level_menu=level_menu)

    return image, kbds


async def game(level_menu):
    text = as_list(
        as_marked_section(
            Bold('Реализовано:'),
            'Создана база существ (sqlite)',
            'Создана фабрика юнитов',
            'Создан основной движок игры',
            'Создано главное окно',
            'Добавление и выбор пользователя.',
            'Получение уровней существами',
            'Создан движок битвы',
            'Парсинг GIF-анимаций',
            'Создано окно битвы',
            'Логирование',
            'Добавлены Герои',
            'Созданы кампании',
            'Добавлены игровые сессии',
            'Автобой',
            'Проект доведен до стадии MVP',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Не реализовано:"),
            'Протестирована часть модулей (unittest).',
            marker="❌ "
        ),
        sep="\n---------------------------\n",
    ).as_html()

    image = InputMediaPhoto(media=FSInputFile(
        os.path.join(os.getcwd(), 'screenshots/Represent_03.png')),
        caption=text)

    kbds = get_user_main_btns(level_menu=level_menu)

    return image, kbds


async def units(session, level_menu, page):
    units = await orm_get_units(session)

    paginator = Paginator(units, page=page)
    unit = paginator.get_page()[0]

    portraits_path = os.path.join(PARENT_DIR, 'images/portraits')
    image_path = os.path.join(portraits_path, f'{unit.name}.gif')

    image = InputMediaPhoto(
        # media=unit.image,
        media=FSInputFile(image_path),
        caption=f"<b>{unit.name}</b>\n"
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
                f"Предыдущая форма: {unit.prev_level}\n"
        ,
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


# async def screenshots(session, level_menu, page):
#     screens = os.listdir(os.path.join(PARENT_DIR, 'screenshots'))
#
#     paginator = Paginator(screens, page=page)
#     screenshot = paginator.get_page()[0]
#
#     # portraits_path = os.path.join(PARENT_DIR, 'images/portraits')
#     # image_path = os.path.join(portraits_path, f'{unit.name}.gif')
#
#     image = InputMediaPhoto(
#         media=FSInputFile(screenshot),
#         caption='1'
#     )
#
#     pagination_btns = pages(paginator)
#
#     kbds = get_screenshots_btns(
#         level_menu=level_menu,
#         page=page,
#         pagination_btns=pagination_btns,
#     )
#
#     return image, kbds


async def get_menu_content(
        session: AsyncSession,
        level_menu: int,
        menu_name: str,
        page: Optional[int] = None,
):
    if level_menu == 0 and menu_name == 'main':
        return await main_menu(level_menu)
    elif level_menu == 0 and menu_name == 'about':
        return await about(level_menu)
    elif level_menu == 0 and menu_name == 'game':
        return await game(level_menu)
    elif level_menu == 0 and menu_name == 'factions':
        return await factions(level_menu)
    elif level_menu == 1:
        return await units(session, level_menu, page)
    # elif level_menu == 2:
    #     return await screenshots(session, level_menu, page)