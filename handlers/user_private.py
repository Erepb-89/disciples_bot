from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from keyboards.reply import del_kbd, start_kb2
from common.settings import EMPIRE_DESC, HORDES_DESC, LEGIONS_DESC, CLANS_DESC

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет! Я виртуальных помощник',
                         reply_markup=start_kb2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Что вас интересует?'))


@user_private_router.message(or_f(Command('about'),
                                  F.text.lower().contains('бот')))
async def about_cmd(message: types.Message):
    await message.answer('Бот для просмотра юнитов игры Disciples Mobile')


@user_private_router.message(or_f(Command('game'),
                                  F.text.lower().contains('игр')))
async def game_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Реализовано:'),
            'Создана база существ (sqlite) с сайта Disciples Wiki с помощью scrapy, urllib, xpath, с последующим переходом на postgres (192 активных существа с разными характеристиками и способностями, разделенные условно на 4 категории: Стрелки, Маги, Бойцы, Воины поддержки).',
            'Создана фабрика юнитов при найме (на основе паттерна Абстрактная фабрика) для каждой из 4 фракций.',
            'Создан основной движок игры, методы найма, увольнения, перестановки юнитов внутри группы с изменением в БД (взаимодействие с базой с помощью sqlalchemy).',
            'Создано главное окно, окно найма юнитов, окно постройки в Столице с выбором ветвей развития юнитов, покупкой строений, с изменением в БД (применяются QtDesigner, PyQT, диалоговые окна, рекурсия, графы).',
            'Реализовано добавление и выбор пользователя.',
            'Реализовано получение уровней существами, принадлежность к фракциям. Реализована зависимость апгрейда юнитов при получении уровня от построек в Столице, в зависимости от фракции.',
            'Создан движок битвы, в котором рассчитывается очередность ходов, выбор целей, происходит обсчет урона с учетом брони, иммунитетов и защит юнитов.',
            'Парсинг GIF-анимаций большинства существ из оригинальной игры, автоматизированное переименование и распределение их по папкам для последующего обращения к ним.',
            'Создано окно битвы, взаимодействующее с движком битвы, реализован PyQT-интерфейс с полем битвы, слотами существ, выбором целей, атакой, защитой, ожиданием хода, анимацией действий персонажей на основе GIF-файлов, получения уровней существами (используются сигналы pyqtSignal и потоки QThread).',
            'Реализовано логирование каждого действия в бою (обычный менеджер контекста).',
            'Добавлены Герои 4х разных классов (в основе - Абстрактная фабрика) с возможностью получения уровней и рандомных перков/способностей.',
            'Созданы кампании для всех фракций на основе процедурной генерации (каждый уровень кампании генерируется случайно), реализованы переходы между миссиями. Всего от 4 до 5 уровней в кампании, 15 миссий на каждом уровне (применяются графы). Имеется переход по игровым дням и выбор сложности кампании.',
            'Для реализации сохранений добавлены игровые сессии. Реализовано сохранение прогресса по кампании, отстройке Столицы (1 таблица) и отряду существ с последующей возможностью загрузки (4 отдельных таблицы для каждой фракции).',
            'Реализован Автобой с автоматическим определением следующей цели (по приоритету), на ходу компьютера (ИИ) либо по желанию игрока (на ходу игрока).',
            'Проект доведен до стадии MVP. Создан exe-файл (pyinstaller).',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Не реализовано:"),
            'Протестирована часть модулей (unittest).',
            marker="❌ "
        ),
        sep="\n---------------------------\n",
    )
    await message.answer('<b>Disciples Mobile</b> - пошаговая игра в жанре Turn Base RPG, '
                         'с боями в стиле "Стенка на стенку", прокачкой существ '
                         'и отстройкой Столицы, созданная на основе известной '
                         'TBS Disciples 2')
    await message.answer(text.as_html())


@user_private_router.message(or_f(Command('factions'),
                                  F.text.lower().contains('фракци')))
async def factions_cmd(message: types.Message):
    await message.answer(f'<b>Список игровых фракций:</b>\n'
                         f'<b>Империя:</b>\n {EMPIRE_DESC}\n\n'
                         f'<b>Орды Нежити:</b>\n {HORDES_DESC}\n\n'
                         f'<b>Легионы Проклятых:</b>\n {LEGIONS_DESC}\n\n'
                         f'<b>Горные Кланы:</b>\n {CLANS_DESC}\n\n')


@user_private_router.message(or_f(Command('units'),
                                  F.text.lower().contains('юниты')))
async def units_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Юниты:"),
        "Одержимый",
        "Сквайр",
        "Боец",
        "Гном",
        marker="✅ ",
    )
    await message.answer(text.as_html(), reply_markup=del_kbd)
    # await message.answer('Юниты:', reply_markup=del_kbd)


@user_private_router.message(or_f(F.text.lower().contains('ривет'),
                                  F.text.lower().contains('hello')))
async def hello_cmd(message: types.Message):
    await message.answer('И тебе привет!')

# @user_private_router.message(F.contact)
# async def get_contact(message: types.Message):
#     await message.answer('Номер получен')
#     await message.answer(str(message.contact.phone_number))
#
#
# @user_private_router.message(F.location)
# async def get_location(message: types.Message):
#     await message.answer('Локация получена')
#     await message.answer(f'{message.location.longitude}, {message.location.latitude}')
