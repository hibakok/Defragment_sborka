# Крупные потребности сборки (для фабрик)

Источник: `data/demand.jsonl`, `data/kills.jsonl` (агрегация всех задач
1827 квестов; инструмент `tools/pipeline/demand_all.py`).
Каждое число ниже сверено с данными, а не по памяти.

## Итоги агрегации

Целей (чего требует сдать): 1801 — из них предметов 1745, тегов 27,
«любой из списка» 28, жидкостей 1. Мобов: 59 видов, суммарно 71 убийство.

## Валюта

Сборка использует монеты Numismatics — они требуются квестами сами по себе:

| Монета | Всего нужно | Квестов |
| --- | --- | --- |
| numismatics:spur | 188 | 10 |
| numismatics:cog | 70 | 13 |

Вывод: не продавай и не трать монеты до закрытия квестов главы
the_black_market; способ чеканки монет — см. JEI и квест «Mastering Currency».

## Лестница массового производства (главный вывод)

Сборка устроена как лестница «механизмов»: каждый этап требует сдать
ключевой механизм во всё большем количестве (степени двойки и округления).
Это и есть каркас фабрик этапа 17 (см. TRACKER):

| Механизм/машина | Всего | Макс. за квест | Квестов | Глава-владелец |
| --- | --- | --- | --- | --- |
| create_dd:sealed_mechanism | 3001 | 3000 | 2 | black market |
| create_things_and_misc:vibration_mechanism | 3001 | 3000 | 2 | black market |
| ad_astra:cryo_fuel (жидкость) | 100000 mB | 100000 | 1 | black market |
| create_dd:calculation_mechanism | 2049 | 2048 | 2 | IX, black market |
| create:precision_mechanism | 1026 | 1024 | 3 | II, IX |
| create_sa:hydraulic_engine | 1026 | 1024 | 3 | III, black market |
| kubejs:locomotive_mechanism | 1026 | 1024 | 3 | IV |
| tfmg:steel_mechanism | 1025 | 1024 | 2 | V |
| kubejs:rotation_mechanism | 514 | 512 | 3 | I |
| ae2:engineering_processor | 257 | 256 | 2 | X |
| create_sa:steam_engine | 201 | 200 | 2 | black market |

Вывод: к этапу «чёрный рынок» каждая фабрика механизмов должна выдавать
тысячи штук — закладывай масштаб сразу (см. plan/README.md, этап 17).

## Гейтинговые машины (по одной на главу)

kubejs:andesite_machine (2), kubejs:copper_machine (2), kubejs:brass_machine (2),
kubejs:obsidian_machine (2) — каждый сдают дважды (квест главы + чёрный рынок).
Это «ключи» глав: I → III → II → ... — подробности в analysis/gating_items.md.

## Еда — вторая по масштабу статья расходов

Чёрный рынок массово забирает еду (×200–500 за квест): жареные цыплята,
пироги Farmer's Delight, шоколад create_confectionery, молочные коктейли
create_dd, ягоды Blue Skies. Итог: к этапу 15 нужны автоматические фермы
пшеницы/ягод/молока/каково. Полный список — data/demand.jsonl
(фильтр по `create_confectionery`, `farmersdelight`, `create_dd`).

## Сырьё-рекордсмены

| Предмет | Всего | Комментарий |
| --- | --- | --- |
| minecraft:tuff | 15000 | главный IX ( Create-переработка туфа) |
| minecraft:copper_ingot | 2052 | медь нужна всю игру |
| create:brass_ingot | 2049 | латунь = медь + цинк |
| minecraft:enchanted_golden_apple | 2000 | чёрный рынок (дорого! золото ×8/шт) |
| minecraft:bone | 1300 | скелет-ферма окупится |
| minecraft:wheat_seeds | 1250 | фермы пшеницы |
| create:andesite_alloy | 1033 | андезит + самородки железа |
| ad_astra:fuel_bucket | 1026 | ракетное топливо |
| minecraft:emerald | 64+ | торговцы/варп-пыль |

## Мобы

71 убийство суммарно, 59 видов: драконы (iceandfire:lightning_dragon ×2),
Варден ×2, Эндер-дракон ×2, боссы Alex's Caves, Bosses of Mass Destruction,
L_Ender's Cataclysm и другие. Полный список: data/kills.jsonl.
Массовых «гриндовых» целей нет — все боссы одиночные, кроме
born_in_chaos_v1:nightmare_stalker ×5.

## Что это значит для плана

1. Порядок фабрик = порядок лестницы механизмов (этапы 02–11).
2. Заранее строить: ферму деревьев/андезита (гл. I), меди (гл. III),
   цинка+меди (гл. II), стали (гл. V, TFMG), еды (этап 15).
3. Монеты Numismatics и enchanted_golden_apple — копить с ранней игры.
4. Точные рецепты механизмов (кастомные kubejs:*) дадут данные
   data/kubejs/ после запуска tools/extract/kubejs_from_instance.py.
