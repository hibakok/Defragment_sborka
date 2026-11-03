Карта прогрессии сборки
Источник: data/meta.json, data/chapters/_index.jsonl, data/chapters/*.jsonl.Метод: построен граф зависимостей квестов (поле deps); рёбра между разнымиглавами дают истинный порядок (номера в названиях файлов глав обманчивы).

Входная точка
Единственная глава без входящих зависимостей: basics (136 квестов).Квест "Welcome!" (id 1F6BC8C2A5B8F9B2) — корень всего дерева.

Главная ветка (группа Progression, порядок по зависимостям)
basics — 136 квестов — старт: инструменты, руда, Незер, чёрный рынок
Глава I «Андезитовая машина» — 17 — дерево→доски→андезит→сплав→kubejs:rotation_mechanism→kubejs:andesite_machine
Глава III «Медная машина» — 11 — медь, стекло, ремни→create_sa:hydraulic_engine→kubejs:copper_machine
Глава II «Латунная машина» — 42 — кварц AE2, электронные лампы, латунь→create:precision_mechanism→kubejs:brass_machine, Tom's Storage, Building Gadgets 2, Pipez
Глава IV «Локомотивная машина» — 34 — поезда
Глава V «Стальной механизм» — 49 — сталь (TFMG)
Глава VI «Ракетное топливо» — 31
Глава VII «Инфернальный механизм» — 27
Глава VII «Постройка ракеты» — 20 — Ad Astra
Глава IX «Расчётный механизм» — 100 — большая глава Create
Глава X «Applied Energistics» — 58 — финальная технология
Космос: Марс (10) → Венера (11) → Гласио (11)
Внимание: III идёт ПЕРЕД II (11 рёбер III→II против 3 рёбер I→III).Подтверждение: квест главы II "ITEM minecraft:redstone" зависит от646C119DC7AC80AB (hydraulic_engine, глава III).

Побочные ветки (открываются от basics)
Магия (3): ars_nouveau (265!), irons_spells_n_spellbooks (68), forbidden_and_arcanus (50)
Исследования (6): alexs_caves (71), blue_skies (36), the_aether (36), the_twilight (45), the_end (27), deeper_and_darker (8)
Без группы (5): bosses_and_skill_points (73), renewable_ores (77), storage_solutions (63), the_black_market (88), basics
Коллекции (3): artifacts (45), simply_swords (46), rings_of_ascension (25)
Progression-спутник: create101 (247) — учебник по Create, идёт параллельно главным главам
Сильные связи между главами (топ рёбер графа)
Откуда	Куда	Рёбер
basics	bosses_and_skill_points	72
basics	the_black_market	64
basics	artifacts	43
basics	simply_swords	39
VII-ракета	IX-расчётный	27
basics	rings_of_ascension	24
II-латунь	IV-локомотив	12
VII-инферно	VII-ракета	12
III-медь	II-латунь	11
VI-топливо	VII-инферно	10
Выводы для маршрута
Стратегия: идти по главной ветке, параллельно закрывая basics(он питает все побочные главы).
create101 (247 квестов) — «учебник Create»: выполнять по мерепрохождения главных глав, он не блокирует прогрессию.
ars_nouveau — крупнейшая побочная глава (265): разбить на сессии.
Полное 100%: 1827 квестов; порядок см. TRACKER.
Легенда полей data/chapters/*.jsonl
id: HEX-идентификатор квеста (для ссылок deps)
title: название (пусто = без заголовка; &-коды = цвета Minecraft)
deps: список id квестов-предусловий
dm: ONE (нужно любое условие) / ALL (нужны все)
tasks: список задач:
"ITEM xN" — сдать предмет
"ITEM any#tag:<тег> xN" — любой предмет с тегом
"ITEM any@mod: xN" — любой предмет мода (? = не распознано, проверить в игре)
"ITEM any of [..] xN" — один из списка ([] = пустой список в данных, проверить в игре)
"KILL xN" — убить моба
"ADV " — получить достижение
"CHECK" — отметить вручную
"STRUCT " — найти структуру
"BIOME " / "DIM " — посетить биом/измерение
"OBSERVE ?" / "FLUID ?" — редкие типы, уточняется в игре