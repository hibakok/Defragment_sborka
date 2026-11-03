# Инструменты

Python 3, только стандартная библиотека. Запуск из папки tools/:

```bash
cd tools
python -m tests.selftest              # самотест всего стека (22 проверки)
python -m pipeline.order_all          # data/quest_order.jsonl
python -m pipeline.demand_all         # data/demand.jsonl + data/kills.jsonl
python -m pipeline.skeleton_all       # plan/auto/*.md (галочки сохраняются)
python -m pipeline.progress_count     # сводка прогресса по квестам
python -m pipeline.museum_all         # plan/museum/*.md (галочки сохраняются)
python -m pipeline.museum_count       # сводка прогресса по предметам
python -m pipeline.production_all     # data/production.jsonl + карта производства
python -m recipes.tree create:shaft   # дерево: что нужно для предмета с нуля
```

## Ветки кода

- core/files.py, core/jsonio.py — примитивы (кирпичики низшего уровня)
- snbt/parser.py — парсер SNBT (собран из примитивов)
- quests/* — квесты FTBQ поверх data/ (загрузка, граф, задачи, спрос)
- items/ids.py — lang-ключ → id предмета (фильтр мусора, 22 501 шт.)
- recipes/* — рецепты: загрузка, нормализация, индекс, дерево потребностей
- museum/* — отрисовка и деление музейных чек-листов
- plan/* — маршрут и отрисовка Markdown
- pipeline/* — склейки-скрипты (точки входа)
- extract/* — экстракторы данных из инстанса игры
- tests/selftest.py — регрессионная сетка

Каждый метод задокументирован в METHODS.md: вход / выход / функция.
Новый метод = сначала запись в METHODS.md, потом код.

## Экстракторы (запускает игрок на своём инстансе)

Путь инстанса — папка, где лежат `config/`, `mods/`, `saves/`
(Prism: правый клик → «Папка»; CurseForge App: ...Instances\<имя>).

```bash
cd tools
python -m extract.quests_from_instance "<путь к инстансу>"
python -m extract.mods_from_folder "<путь к инстансу>\mods"
python -m extract.items_from_mods "<путь к инстансу>\mods"
python -m extract.recipes_from_mods "<путь>\mods" create create_dd create_sa tfmg
python -m extract.kubejs_from_instance "<путь к инстансу>"
```

ВАЖНО: экстракторы перезаписывают data/ — перед запуском закоммить
текущее состояние репозитория. Порядок: сначала квесты (дадут описания),
потом остальное. После экстракторов перезапусти пайплайны (order_all,
demand_all, skeleton_all, museum_all, production_all) и selftest.
