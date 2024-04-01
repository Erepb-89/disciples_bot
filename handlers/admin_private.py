import os

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_units
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

PARENT_DIR = os.getcwd()

ADMIN_KB = get_keyboard(
    "Добавить юнит",
    "Изменить юнит",
    "Удалить юнит",
    "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def add_unit(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


class AddUnit(StatesGroup):
    # Шаги состояний
    name = State()
    desc = State()
    price = State()
    photo = State()

    product_for_change = None

    texts = {
        "AddUnit:name": "Введите название заново:",
        "AddUnit:description": "Введите описание заново:",
        "AddUnit:price": "Введите стоимость заново:",
        "AddUnit:photo": "Этот стейт последний, поэтому...",
    }


@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_unit(message: types.Message, session: AsyncSession):
    portraits_path = os.path.join(PARENT_DIR, 'images/portraits')

    for unit in await orm_get_units(session):
        image_path = os.path.join(portraits_path, f'{unit.name}.gif')
        portrait = FSInputFile(image_path)

        await message.answer_photo(
            portrait,
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
            # reply_markup=get_callback_btns(
            #     btns={
            #         "Удалить": f"delete_{unit.id}",
            #         "Изменить": f"change_{unit.id}",
            #     }
            # ),
        )

    await message.answer("ОК, вот список юнитов ⏫")


@admin_router.message(F.text == "Удалить юнит")
async def delete_unit(message: types.Message):
    await message.answer("Выберите юнит(ы) для удаления")


# Код ниже для машины состояний (FSM)


@admin_router.message(StateFilter(None), F.text == "Добавить юнит")
async def add_unit(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите имя юнита", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddUnit.name)


@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddUnit.name:
        await message.answer(f'Предыдущего шага нет. Введите имя юнита или напишите "отмена"')
        return

    previous = None
    for step in AddUnit.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу\n{AddUnit.texts[previous.state]}")
            return

        previous = step


@admin_router.message(AddUnit.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание юнита")
    await state.set_state(AddUnit.desc)


@admin_router.message(AddUnit.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст имени юнита")


@admin_router.message(AddUnit.desc, F.text)
async def add_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("Введите стоимость юнита")
    await state.set_state(AddUnit.price)


@admin_router.message(AddUnit.desc)
async def add_desc(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст описания юнита")


@admin_router.message(AddUnit.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение юнита")
    await state.set_state(AddUnit.image)


@admin_router.message(AddUnit.price)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст стоимости юнита")


@admin_router.message(AddUnit.photo, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Юнит добавлен", reply_markup=ADMIN_KB)

    data = await state.get_data()

    # await orm_add_unit(session, data)

    await message.answer(str(data))
    await state.clear()


@admin_router.message(AddUnit.photo)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, добавьте изображение юнита")
