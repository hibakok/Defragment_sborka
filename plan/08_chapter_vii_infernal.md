# Этап 08: глава VII — инфернальный механизм

## Цель

Закрыть chapter_vii_infernal_mechanism (27/27). Цепочка мистик-угля
и ember alloy → create_dd:infernal_mechanism — предпоследняя ступень
лестницы механизмов (вход для расчётного механизма гл. IX).

## Предусловия

- Этапы 06–07: steel_mechanism на потоке, бензин есть.
- Чек-лист: plan/auto/08_chapter_vii_infernal_mechanism.md (11 волн).
- Рецепты: analysis/gating_items.md (строка 6 лестницы).

## Блок А — мистик-уголь (волны 1–4)

1. kubejs:mystic_coal — мистик-уголь: связка угля с внешним
   воздействием (JEI; связка с glow/ink). Из него:
   ingot_mystic_coal (слиток) → rod_mystic_coal (стержень) →
   mystic_coal_block (блок). Всё это — квесты + материалы.
2. minecraft:glow_ink_sac — светящиеся чернила: рыбалка/сквиды
   (ночью). ink_sac — обычные чернила: ферма сквидов в резервуаре.
3. create:cinder_flour — тухловая мука: дробление туфа/пепла.
   Ей настанет большой час в гл. IX (туф ×15000!) — начни
   копить туф уже сейчас в двойных сундуках.

## Блок Б — ember alloy и магма (волны 5–7)

1. create_dd:ember_alloy = cinder_flour + smoked_planks (копчёные
   доски create_dd) + blaze_powder, 2× за крафт
   (data/recipes/create_dd/…/ember_alloy.json).
2. create_things_and_misc:crushed_magma — дроблёная магма:
   дробление магматического блока. Магма возобновляема (лава→обсидиан
   нет, магма — да: магмовые жилы в Незере + Alex's Caves).
3. minecraft:blaze_rod/powder — ферма ифритов (спавнер из крепости
   или HNN-симулятор с этапа 05!).

## Блок В — инфернальный механизм (волны 8–11)

1. create_dd:infernal_mechanism: SA от steel_mechanism, 2 петли:
   залить бензин 25mB → деплой crushed_magma → деплой ember_alloy →
   пресс (main.js:690). Побочки с шансом 5%: стержень мистик-угля,
   дроб. магма, тухловая мука — приятный возврат.
2. Потребление: расч. механизм ×2049, plating ×43, полёт-якорь.
   Держи линию включённой до конца игры.
3. Сдай infernal_mechanism — глава IX расчётный механизм откроется
   ПОСЛЕ ракетной главы (порядок: гл. VII-инферно → гл. VII-ракета
   → гл. IX, см. progression_map.md).

## Блок Г — попутно (стратегия)

1. forbidden_arcanus: arcana-кристаллы (dust/speck) — глава 13c:
   обелиски в тёмных лесах; собирай по пути.
2. minecraft:prismarine_crystals — морской фонарь/стражи: HNN.
3. create_dd:industrial_fan — пром. вентилятор: понадобится в
   расчётной главе (обдув/охлаждение линий).

## Критерий готовности

- 27/27 в plan/auto/08_...md.
- infernal_mechanism капает с SA-линии.
- Туф копится (≥10 стаков), бензин течёт, ember alloy автоматизирован.

## Что дальше

plan/09_chapter_vii_rocket.md — ракета: посадки, плакирование, старт.
