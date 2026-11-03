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
| tools/core/files.py | Примитивы файлов: чтение, запись, список, папки |
| tools/core/jsonio.py | Примитивы JSON/JSONL + толерантный парсер |
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
| tools/pipeline/items_audit.py | Скрипт: аудит предметов + meta.json + отчёт |
| tools/extract/quests_from_instance.py | FTB Quests инстанса → data/chapters |
| tools/extract/mods_from_folder.py | папка mods → data/mods.jsonl |
| tools/extract/items_from_mods.py | jar + lang-файлы → data/items.jsonl |
| tools/extract/recipes_from_mods.py | jar-моды → data/recipes/<modid>.jsonl |
| tools/extract/kubejs_from_instance.py | kubejs инстанса → data/kubejs/ (только полезное) |
| tools/tests/selftest.py | Самотест: 17 проверок всего стека |

## data/ — факты о сборке (только данные, без мнений)

| Путь | Назначение |
| --- | --- |
| data/meta.json | Версия сборки, счётчики всех слоёв данных |
| data/chapters/_index.jsonl | Реестр 31 главы: файл, группа, порядок, число квестов |
| data/chapters/<глава>.jsonl | Квесты главы: id, title, deps, dm, tasks, desc |
| data/quest_order.jsonl | Все 1827 квестов в топологическом порядке |
| data/demand.jsonl | Суммарные потребности в предметах/жидкостях |
| data/kills.jsonl | Мобы: кого и сколько убить |
| data/mods.jsonl | 283 мода из jar (modid, имя, версия, файл) |
| data/items.jsonl | 26 500 предметов/блоков всех модов + ваниль + kubejs |
| data/items_stats.jsonl | Число предметов по modid (отчёт items_audit) |
| data/recipes/<modid>.jsonl | Рецепты 33 контентных модов (~10 200) |
| data/kubejs/ | Кастомные рецепты/скрипты сборки (60 файлов) |

## analysis/ — выводы (каждое утверждение ссылается на data/)

| Путь | Назначение |
| --- | --- |
| analysis/progression_map.md | Карта прогрессии: порядок глав, граф зависимостей |
| analysis/demand_top.md | Крупные потребности → что строить в фабриках |
| analysis/gating_items.md | Лестница механизмов: точные рецепты всех ступеней |
| analysis/items_audit.md | Аудит предметов: покрытие, топ модов, пробелы |

## plan/ — ГЛАВНЫЙ ПРОДУКТ (план прохождения)

| Путь | Назначение |
| --- | --- |
| plan/README.md | Как читать план, маршрут, статус этапов |
| plan/00_setup.md | Установка и оптимизация под слабое железо |
| plan/01_basics.md … plan/18_final.md | Стратегии всех 19 этапов |
| plan/auto/*.md | Чек-листы всех 31 главы (генерируются, 1827 квестов) |

## progress/ — жизнь проекта

| Путь | Назначение |
| --- | --- |
| progress/TRACKER.md | Чек-лист выполнения (ведёт игрок) |
