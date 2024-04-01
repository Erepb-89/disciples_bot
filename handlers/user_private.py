import os

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import FSInputFile
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_units
from filters.chat_types import ChatTypeFilter
from keyboards.reply import del_kbd, start_kb2, get_keyboard
from common.settings import EMPIRE_DESC, HORDES_DESC, LEGIONS_DESC, CLANS_DESC

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

PARENT_DIR = os.getcwd()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    START_KB = get_keyboard(
        "О боте",
        "Об игре",
        "Почитать описание игровых фракций",
        "Просмотр списка юнитов",
        "Скриншоты",
        placeholder="Что вас интересует?",
        sizes=(2, 2, 1),
    )
    await message.answer('Привет! Я виртуальных помощник', reply_markup=START_KB)


@user_private_router.message(or_f(Command('about'),
                                  F.text.lower().contains('бот')))
async def about_cmd(message: types.Message):
    await message.answer('Бот для просмотра информации об игре Disciples Mobile. '
                         'Здесь Вы можете просмотреть игровые скриншоты, '
                         'а также харакктеристики юнитов.')


@user_private_router.message(or_f(Command('screenshots'),
                                  F.text.lower().contains('скриншот')))
async def screenshots_cmd(message: types.Message):
    await message.answer('Вот несколько скриншотов из игры:', reply_markup=del_kbd)

    images_path = os.path.join(PARENT_DIR, 'screenshots/')
    for image in os.listdir(images_path):
        new_path = os.path.join(images_path, image)
        image = FSInputFile(new_path)

        await message.answer_photo(image)


@user_private_router.message(or_f(Command('game'),
                                  F.text.lower().contains('игр')))
async def game_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Реализовано:'),
            'Создана база существ (sqlite) с помощью парсинга с сайта Disciples Wiki с помощью scrapy, urllib, xpath, с последующим переходом на postgresql (192 активных существа с разными характеристиками и способностями, разделенные условно на 4 категории: Стрелки, Маги, Бойцы, Воины поддержки).',
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
                                  F.text.lower().contains('юнитов')))
async def units_cmd(message: types.Message, session: AsyncSession):
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
