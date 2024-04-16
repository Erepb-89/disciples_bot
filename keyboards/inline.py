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
    faction: Optional[int] = None


def get_user_main_btns(*, level_menu: int, sizes: Tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Все юниты 😈": "units",
        "О боте ℹ️": "about",
        "Об игре 🎮": "game",
        "Фракции 🧩": "factions",
        "Скриншоты 👓": "screenshots",
        "Категории 💪": "catalog",
    }
    for text, menu_name in btns.items():
        if menu_name == 'units':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level_menu=2,
                        menu_name=menu_name).pack()))
        elif menu_name == 'screenshots':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level_menu=4,
                        menu_name=menu_name).pack()))
        elif menu_name == 'factions':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level_menu=5,
                        menu_name=menu_name).pack()))
        elif menu_name == 'catalog':
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level_menu=1,
                        menu_name=menu_name).pack()))
        else:
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level_menu=level_menu,
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

    keyboard.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=MenuCallBack(
                level_menu=level_menu - 1,
                menu_name='main').pack()))
    keyboard.add(
        InlineKeyboardButton(
            text='Добавить в избранное ⭐',
            callback_data=MenuCallBack(
                level_menu=level_menu,
                menu_name='add_to_favs',
                unit_id=unit_id).pack()))

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


def get_screens_btns(
        *,
        level_menu: int,
        page: Optional[int] = None,
        pagination_btns: dict,
        sizes: Tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=MenuCallBack(
                level_menu=0,
                menu_name='main').pack()))

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level_menu=level_menu,
                                                menu_name=menu_name,
                                                page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level_menu=level_menu,
                                                menu_name=menu_name,
                                                page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


def get_user_catalog_btns(
        *,
        level_menu: int,
        unit_levels: list,
        sizes: Tuple[int] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=MenuCallBack(
                level_menu=level_menu - 1,
                menu_name='main').pack()))
    keyboard.add(
        InlineKeyboardButton(
            text='Избранное ⭐',
            callback_data=MenuCallBack(
                level_menu=3,
                menu_name='favourites').pack()))

    for level in unit_levels:
        keyboard.add(
            InlineKeyboardButton(
                text=level.level,
                callback_data=MenuCallBack(
                    level_menu=level_menu + 1,
                    menu_name=level.level,
                    level_unit=level.id).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_factions_btns(
        *,
        level_menu: int,
        factions: list,
        menu_name: str,
        sizes: Tuple[int] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    if level_menu == 5:
        level_menu += 1
        back_page = 0
        back_menu = 'main'
    else:
        level_menu = 6
        back_page = level_menu - 1
        back_menu = 'factions'

    for faction in factions:
        if faction.name != menu_name:
            keyboard.add(
                InlineKeyboardButton(
                    text=faction.name,
                    callback_data=MenuCallBack(
                        level_menu=level_menu,
                        menu_name=faction.name,
                        faction=faction.id).pack()))

    keyboard.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=MenuCallBack(
                level_menu=back_page,
                menu_name=back_menu).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_favourites(
        *,
        level_menu: int,
        page: Optional[int] = None,
        pagination_btns: Optional[dict] = None,
        unit_id: Optional[int] = None,
        sizes: Tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text='Удалить',
                                          callback_data=MenuCallBack(
                                              level_menu=level_menu,
                                              menu_name='delete',
                                              unit_id=unit_id,
                                              page=page).pack()))

        keyboard.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(
                                                    level_menu=level_menu,
                                                    menu_name=menu_name,
                                                    page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(
                                                    level_menu=level_menu,
                                                    menu_name=menu_name,
                                                    page=page - 1).pack()))

        keyboard.row(*row)

        row2 = [
            InlineKeyboardButton(text='На главную 🏠',
                                 callback_data=MenuCallBack(
                                     level_menu=0,
                                     menu_name='main').pack())
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(
            InlineKeyboardButton(text='На главную 🏠',
                                 callback_data=MenuCallBack(
                                     level_menu=0,
                                     menu_name='main').pack()))

        return keyboard.adjust(*sizes).as_markup()
