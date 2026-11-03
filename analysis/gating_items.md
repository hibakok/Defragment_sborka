# Гейтинговые машины и механизмы

Источник: `data/demand.jsonl`, `data/chapters/*.jsonl`.
Гейтинг — постепенное открытие контента сборки через кастомные
предметы-«машины». Ниже — вся цепочка, извлечённая из квестов.

## Машины-ключи глав

Каждая машина сдаётся в квесте главы и ОБЯЗАТЕЛЬНА для продолжения:

| Машина | Где сдают | Что открывает |
| --- | --- | --- |
| kubejs:rotation_mechanism (×1) | глава I, волна 7 | доступ к andesite_machine |
| kubejs:andesite_machine (×1) | глава I, волна 8 | главу III (медный век) |
| create_sa:hydraulic_engine (×1) | глава III, волна 3 | главу II (латунный век) |
| kubejs:copper_machine (×1) | глава III, волна 4 | главу II |
| create:precision_mechanism (×1) | глава II | chapter IV, IX |
| kubejs:brass_machine (×1) | глава II | главу IV (поезда) |
| kubejs:locomotive_mechanism | глава IV | главу V |
| tfmg:steel_mechanism | глава V (сталь, TFMG) | главу VI |
| kubejs:obsidian_machine | глава VII (инферно) | ракету, главу IX |
| create_dd:calculation_mechanism | глава IX | главу X (AE2) |

Важно: эти же машины/механизмы потом требуются ЧЕРЕЗ ТЫСЯЧИ штук
(см. analysis/demand_top.md) — фабрика каждой нужна на века.

## Откуда берутся рецепты

Все kubejs:* и часть кастомных механизмов — пользовательские рецепты
сборки (KubeJS). В текущих данных их НЕТ — рецепты появятся после
запуска `tools/extract/kubejs_from_instance.py` (папка инстанса) и
коммита `data/kubejs/`. До этого источник рецепта — JEI в игре
(R по предмету).

## Как играть в гейтинг (стратегия)

1. Машина-ключ сдаётся В ЕДИНИЧНОМ экземпляре на квест главы — сначала
   руками, фабрику отложить.
2. Сразу после сдачи — проверь открывшиеся квесты следующей главы
   (чек-листы plan/auto/ по порядку этапов).
3. Каждый механизм из таблицы выше — будущий «завод»: не выбрасывай
   производственную цепочку, из которой он собран, а расширяй её.
4. Механизмы create_sa/create_dd/tfmg — из модов-аддонов Create:
   hydraulic/steam engine (create_sa: Stuff Additions),
   sealed/calculation mechanism (create_dd), steel mechanism (tfmg:
   The Factory Must Grow). Их цепочки — в JEI по имени предмета.
