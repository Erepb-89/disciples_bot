from aiogram.utils.formatting import Bold, as_list, as_marked_section

LEVELS = [1, 2, 3, 4, 5, 6, 7, 8]

EMPIRE_DESC_SHORT = 'Государство человеческой расы, охраняемое силами людей и ангелами Верховного Отца, в том числе Мизраэлем, охраняющем столицу. Раса титанов находится в союзе с Империей и в войнах выступает на её стороне. Магия людей направлена на восстановление и улучшение способностей.'
HORDES_DESC_SHORT = 'Нежить, созданная Мортис из жителей королевства Алкмаар (позже к Ордам присоединялись другие трупы, а также некоторые люди и драконы). Главным жрецом алкмаарцев был Ашган, Мортис превратила его в чудовище и сделала охранником столицы Орд.'
LEGIONS_DESC_SHORT = 'Чудовища, созданные падшим ангелом Бетрезеном, и люди-демонопоклонники, цель которых — освобождение Бетрезена из шеститысячелетнего заточения в ядре Невендаара. Бетрезен назначил Ашкаэля командиром Легионов.'
CLANS_DESC_SHORT = 'Народ гномов, несколько королевств, объединённых под властью верховного короля. Великаны воспринимают гномов как родичей и сражаются на их стороне. Столица гномов охраняется Витаром — полубожеством из свиты Вотана.'

DESCRIPTIONS = {
    'empire': 'Империя (англ. The Empire) — государство человеческой расы, охраняемое силами людей и ангелами Верховного Отца, в том числе Мизраэлем, охраняющем столицу. Раса титанов находится в союзе с Империей и в войнах выступает на её стороне. Правитель Империи во время событий первых двух игр серии — император Демосфен, потерявший в Первой Великой войне жену и единственного наследника — Утера. Во время событий дополнения «Гвардия света» трон Империи пустует, к началу событий «Восстания Эльфов» его занимают барон Эмри Абриссельский и леди Амбриэль Верциллинская. Магия людей основана на мане жизни и направлена на восстановление и улучшение способностей; единственная стихия боевой магии — воздух.',
    'hordes': 'Орды Нежити (англ. Undead Hordes) — нежить, созданная Мортис из жителей королевства Алкмаар (позже к Ордам присоединялись другие трупы, а также некоторые люди и драконы). Главным жрецом алкмаарцев был Ашган, Мортис превратила его в чудовище и сделала охранником столицы Орд. У нежити нет никакого государственного строя, все они подчинены воле своей богини. Магия нежити основана на мане смерти, и направлена на ухудшение способностей противника и поражение магией смерти.',
    'legions': 'Легионы Проклятых (англ. Legions of the Damned) — чудовища, созданные падшим ангелом Бетрезеном, и люди-демонопоклонники, цель которых — освобождение Бетрезена из шеститысячелетнего заточения в ядре Невендаара. Бетрезен назначил Ашкаэля командиром Легионов. В отличие от остальных игровых рас демоны не имеют централизованного государства. Магия демонов основана на мане ада, направлена на разрушение и ухудшение способностей противника; основная стихия боевой магии — огонь.',
    'clans': 'Горные Кланы (англ. Mountain Clans) — народ гномов, несколько королевств, объединённых под властью верховного короля. Верховным королём во время событий первой игры серии был Стурмир Громобой, но он был убит воинами Мортис. К событиям Disciples II королём стал Морок. Великаны воспринимают гномов как родичей и сражаются на их стороне. Столица гномов охраняется Витаром — полубожеством из свиты Вотана. Во время Первой Великой войны (Disciples: Sacred Lands) Кланы и Империя были союзниками, но этот союз был нарушен. Магия гномов основана на мане рун, направлена на восстановление и улучшение способностей; в боевой магии используются все четыре стихии.',
    "main": "Добро пожаловать!",
    'about': 'Бот для просмотра информации об игре Disciples Mobile. '
             'Здесь Вы можете просмотреть игровые скриншоты, '
             'а также характеристики юнитов.',
    'catalog': 'Категории',
    'favourites': 'Избранное',
    'factions': f'<b>Список игровых фракций:</b>\n'
                f'<b>Империя:</b>\n{EMPIRE_DESC_SHORT}\n\n'
                f'<b>Орды Нежити:</b>\n{HORDES_DESC_SHORT}\n\n'
                f'<b>Легионы Проклятых:</b>\n{LEGIONS_DESC_SHORT}\n\n'
                f'<b>Горные Кланы:</b>\n{CLANS_DESC_SHORT}\n\n',
    'game': as_list(
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
    ).as_html(),
}

IMAGES = {
    'empire': 'Represent_16.png',
    'hordes': 'Represent_17.png',
    'legions': 'Represent_18.png',
    'clans': 'Represent_19.png',
    'main': 'Represent.png',
    'about': 'Represent_02.png',
    'catalog': 'Represent_04.png',
    'factions': 'Represent_05.png',
    'game': 'Represent_03.png',
    'favourites': 'Represent_09.png',
}
