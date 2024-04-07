from typing import Tuple, Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix="menu"):
    level_menu: int
    menu_name: str
    level_unit: Optional[int] = None
    page: int = 1
    unit_id: Optional[int] = None


def get_user_main_btns(*, level_menu: int, sizes: Tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Юниты 😈": "units",
        "О боте ℹ️": "about",
        "Об игре 🎮": "game",
        "О фракциях 🧩": "factions",
        # "Скриншоты 👓": "screenshots",
        "Категории 🧻": "catalog",
    }
    for text, menu_name in btns.items():
        if menu_name == 'units':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level_menu=2,
                                                                         menu_name=menu_name).pack()))
        elif menu_name == 'catalog':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level_menu=1,
                                                                         menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level_menu=level_menu,
                                                                         menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_units_btns(
        *,
        level_menu: int,
        level_unit: int,
        page: int,
        pagination_btns: dict,
        unit_id: int,
        sizes: Tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level_menu=0,
                                                                 menu_name='main').pack()))

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level_menu=level_menu,
                                                menu_name=menu_name,
                                                level_unit=level_unit,
                                                page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level_menu=level_menu,
                                                menu_name=menu_name,
                                                level_unit=level_unit,
                                                page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


def get_user_catalog_btns(*, level_menu: int, unit_levels: list, sizes: Tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level_menu=level_menu - 1,
                                                                 menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='Избранное ⭐',
                                      callback_data=MenuCallBack(level_menu=3,
                                                                 menu_name='favourites').pack()))

    for level in unit_levels:
        keyboard.add(InlineKeyboardButton(text=level.level,
                                          callback_data=MenuCallBack(level_menu=level_menu + 1,
                                                                     menu_name=level.level,
                                                                     level_unit=level.id).pack()))

    return keyboard.adjust(*sizes).as_markup()
