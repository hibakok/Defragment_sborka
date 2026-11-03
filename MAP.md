# Карта репозитория

Правило: меняешь/добавляешь файл — обнови эту карту и INDEX.md.
Файл больше 500 строк — дели на части.

## Корень

| Файл | Назначение |
| --- | --- |
| README.md | Точка входа, миссия, словарь |
| MAP.md | Эта карта |
| RULES.md | Законы репозитория (обязательны для людей и ИИ) |
| INDEX.md | Реестр всех файлов: путь → назначение → статус |

## tools/ — инструменты (Python 3, только stdlib)

| Путь | Назначение |
| --- | --- |
| tools/README.md | Как запускать инструменты |
| tools/METHODS.md | Документация каждого метода: вход / выход / функция |
| tools/core/files.py | Примитивы файлов: чтение, запись, список |
| tools/core/jsonio.py | Примитивы JSON и JSONL |
| tools/snbt/parser.py | Парсер SNBT (диалект FTB Quests) |
| tools/quests/load.py | Загрузка глав и квестов из data/chapters |
| tools/quests/tasks.py | Разбор строк задач и титулов |
| tools/quests/graph.py | Граф зависимостей, глубины, топологический порядок |
| tools/quests/demand.py | Агрегация потребностей (предметы, мобы) |
| tools/plan/route.py | Маршрут: глава → этап (согласован с TRACKER) |
| tools/plan/render.py | Кирпичики Markdown для чек-листов |
| tools/pipeline/order_all.py | Скрипт: data/quest_order.jsonl |
| tools/pipeline/demand_all.py | Скрипт: data/demand.jsonl + data/kills.jsonl |
| tools/pipeline/skeleton_all.py | Скрипт: plan/auto/*.md (31 чек-лист) |
| tools/pipeline/progress_count.py | Скрипт: подсчёт галочек прогресса |
| tools/extract/quests_from_instance.py | FTB Quests инстанса → data/chapters (перегенерация данных) |
| tools/extract/mods_from_folder.py | папка mods → data/mods.jsonl |
| tools/extract/items_from_mods.py | jar-моды → data/items.jsonl (все предметы) |
| tools/extract/recipes_from_mods.py | jar-моды → data/recipes/<modid>.jsonl |
| tools/extract/kubejs_from_instance.py | kubejs инстанса → data/kubejs/ |
| tools/tests/selftest.py | Самотест: 17 проверок всего стека |

## data/ — факты о сборке (только данные, без мнений)

| Путь | Назначение |
| --- | --- |
| data/meta.json | Версия сборки, счётчики, типы задач |
| data/chapters/_index.jsonl | Реестр 31 главы: файл, группа, порядок, число квестов |
| data/chapters/<глава>.jsonl | Квесты главы: id, title, deps, dm, tasks, desc |
| data/quest_order.jsonl | Все 1827 квестов в топологическом порядке |
| data/demand.jsonl | Суммарные потребности в предметах/жидкостях |
| data/kills.jsonl | Мобы: кого и сколько убить |
| data/mods.jsonl | (после экстракции) 295 модов |
| data/items.jsonl | (после экстракции) все предметы сборки |
| data/recipes/*.jsonl | (после экстракции) рецепты выбранных модов |
| data/kubejs/ | (после экстракции) кастомные рецепты сборки |

## analysis/ — выводы (каждое утверждение ссылается на data/)

| Путь | Назначение |
| --- | --- |
| analysis/progression_map.md | Карта прогрессии: порядок глав, граф зависимостей |
| analysis/demand_top.md | Крупные потребности → что строить в фабриках |
| analysis/gating_items.md | Гейтинговые машины: цепочка открытия глав |

## plan/ — ГЛАВНЫЙ ПРОДУКТ (план прохождения)

| Путь | Назначение |
| --- | --- |
| plan/README.md | Как читать план, структура файлов плана |
| plan/00_setup.md | Установка и оптимизация под слабое железо |
| plan/01_basics.md | Этап 01: basics (стратегия) |
| plan/02_chapter_i_andesite.md | Этап 02: глава I (стратегия) |
| plan/03_chapter_iii_copper.md | Этап 03: глава III (стратегия) |
| plan/04_chapter_ii_brass_storage.md | Этап 04: глава II + хранение (стратегия) |
| plan/auto/*.md | Чек-листы всех 31 главы (генерируются, 1827 квестов) |

## progress/ — жизнь проекта

| Путь | Назначение |
| --- | --- |
| progress/TRACKER.md | Чек-лист выполнения (ведёт игрок) |
