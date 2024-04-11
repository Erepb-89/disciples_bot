import os

from aiogram import types, Router
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack

from database.orm_query import (
    orm_add_to_favs,
    orm_add_user,
)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

PARENT_DIR = os.getcwd()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(
        session, level_menu=0, menu_name="main")

    await message.answer_photo(media.media,
                               caption=media.caption,
                               reply_markup=reply_markup)


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery,
                    callback_data: MenuCallBack,
                    session: AsyncSession):
    if callback_data.menu_name == "add_to_favs":
        await add_to_favs(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level_menu=callback_data.level_menu,
        menu_name=callback_data.menu_name,
        page=callback_data.page,
        level_unit=callback_data.level_unit,
        unit_id=callback_data.unit_id,
        user_id=callback.from_user.id,
    )
    await callback.message.edit_media(media=media,
                                      reply_markup=reply_markup)
    await callback.answer()


async def add_to_favs(callback: types.CallbackQuery,
                      callback_data: MenuCallBack,
                      session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    await orm_add_to_favs(session,
                          user_id=user.id,
                          unit_id=callback_data.unit_id)
    await callback.answer("Юнит добавлен в избранное.")
