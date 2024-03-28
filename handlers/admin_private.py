from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

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


@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_unit(message: types.Message):
    await message.answer("Вот список юнитов")


@admin_router.message(F.text == "Изменить юнит")
async def change_unit(message: types.Message):
    await message.answer("Вот список юнитов")


@admin_router.message(F.text == "Удалить юнит")
async def delete_unit(message: types.Message):
    await message.answer("Выберите юнит(ы) для удаления")


# Код ниже для машины состояний (FSM)

class AddUnit(StatesGroup):
    name = State()
    desc = State()
    price = State()
    image = State()

    texts = {
        'AddUnit:name': 'Введите имя заново',
        'AddUnit:desc': 'Введите описание заново',
        'AddUnit:price': 'Введите стоимость заново',
        'AddUnit:image': 'Это последний стейт'
    }


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


@admin_router.message(AddUnit.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Юнит добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


@admin_router.message(AddUnit.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, добавьте изображение юнита")
