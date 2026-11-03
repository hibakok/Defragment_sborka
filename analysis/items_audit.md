# Аудит предметов (цель «все предметы хотя бы по разу»)

Источник: `data/items.jsonl` (26 500 записей), `data/items_stats.jsonl`,
`data/demand.jsonl`, `data/mods.jsonl` (283 мода).
Инструмент: `tools/pipeline/items_audit.py` (запуск из tools/).

## Итоги экстракции (2026-11-03)

- Извлечено 26 500 предметов/блоков из 115 пространств имён
  (285 jar: 283 мода + ванильный клиент 1.20.1 + lang-файлы kubejs).
- Покрытие целей квестов: 1744/1745 (99.9%) по modid.
- Единственный пробел: `toolbelt:belt` (jar мода недоступен для
  скачивания; предмет есть в игре — получить в игре, JEI).

## Топ-мод по числу предметов (items_stats.jsonl, топ-10)

| modid | предметов | комментарий |
| --- | --- | --- |
| chipped | 6967 | вариации блоков — «музей» из чиппеда |
| minecraft | 2255 | ваниль (из client.jar) |
| railways | 1060 | Steam'n'Rails (кондукторы/вагоны) |
| simplyswords | 955 | мечи — глава коллекций |
| quark | 918 | |
| twilightforest | 842 | трофеи/лут |
| iceandfire | 836 | драконье |
| create | 823 | + компоненты через машины |
| blue_skies | 748 | |
| alexscaves | 659 | |

## Стратегия «музея»

1. Крафтимые (~90%): МЭ-автокрафт (план 11/17) — заказ по
   паре каждого; рецепты: data/recipes/*.jsonl (33 мода, ~10 200
   рецептов) + JEI.
2. Некрафтимые: HNN-симуляции (мобы), лут-маршруты структур,
   данжи измерений (план 14), боссы (план 15).
3. Кастомные kubejs:*: рецепты — data/kubejs/server_scripts/main.js;
   имена — data/kubejs/assets/kubejs/lang/en_us.json (41 предмет).

## Ограничения данных

- Ванильные рецепты НЕ извлечены (в 1.20.1 их нет в server.jar):
  смотреть в игре JEI. Предметы ванили — есть (client.jar).
- 8 jar недоступны для скачивания (403 CurseForge/Modrinth):
  Yung's ×3, ftb-library/xmod, cupboard, ToolBelt, Lionfish API,
  CerbonsBetterBeacons — библиотеки/мировой ген без предметов
  (кроме toolbelt:belt).
- Рецепты illageandspillage, molten_vents: 0 JSON-рецептов в jar
  (генерируются кодом) — JEI в игре.
