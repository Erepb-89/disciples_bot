from typing import Tuple

from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: Tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона"
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='О боте'),
            KeyboardButton(text='Об игре'),
        ],
        [
            KeyboardButton(text='Почитать описание игровых фракций'),
            KeyboardButton(text='Просмотр списка юнитов'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)

del_kbd = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='О боте'),
    KeyboardButton(text='Об игре'),
    KeyboardButton(text='Почитать описание игровых фракций'),
    KeyboardButton(text='Просмотр списка юнитов'),
)
start_kb2.adjust(2, 2)

test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать опрос', request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text='Отправить номер', request_contact=True),
            KeyboardButton(text='Отправить локацию', request_location=True),
        ],
    ],
    resize_keyboard=True,
)
