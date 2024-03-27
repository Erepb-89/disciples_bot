from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
