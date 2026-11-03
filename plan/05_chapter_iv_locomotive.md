# Этап 05: глава IV — локомотивная машина

## Цель

Закрыть chapter_iv_the_locomotive_machine (34/34). Построить
kubejs:obsidian_machine («Locomotive Machine») — ключ к ж/д и главе V.
Появляется Hostile Neural Networks — «фабрика лута» (см. Блок В).

## Предусловия

- Этап 04 закрыт: brass_machine, precision_mechanism SA-конвейер работает.
- Чек-лист: plan/auto/05_chapter_iv_the_locomotive_machine.md.
- Рецепты: analysis/gating_items.md (лестница, строка 4).

## Блок А — сырьё волны 1 (12 квестов, всё по ×1)

1. Вода/лава в вёдрах, песок, гравий, глина, слизь, мёд, обсидиан —
   базовые предметы; обсидиан лучше уже лить из лавы (казан).
2. tfmg:formwork_block — опалубка TFMG (JEI: доски+прочий хлам) —
   пригодится для бетона в главе V.
3. hostilenetworks:blank_data_model, deep_learner, prediction_matrix —
   см. Блок В (это квесты-«вехи», сами предметы ниже).
4. createaddition:alternator — генератор FE (Create→электричество);
   рядом же connector (волна 2). Электросеть нужна для Create Crafts
   & Additions (аккумуляторы, тесла-катушка для overcharge-сплава).

## Блок Б — прочный лист и обсидиановая пыль (волны 2–3)

1. create:powdered_obsidian — дробление обсидиана (дробильные колёса).
2. create:sturdy_sheet — прочный лист: спекание обсидиановой пыли
   (компактор/пресс, JEI). Сразу строй линию: обсидиан → пыль → лист.
   Потребность: locomotive_mechanism (по 1 на SA), 27× в гл. VII.
3. create:limestone — известняк (жилы Create-камня; скория даёт его
   при дроблении, JEI). Известняк = источник извести для TFMG-цемента.
4. createaddition:copper_spool, connector — электрический тир.

## Блок В — Hostile Neural Networks (волна 1, параллельно)

1. deep_learner — «учебник»: вставляешь data model моба, симуляция
   даёт лут моба (кости, порох, жемчуг Эндера!) без охоты.
2. blank_data_model + сим-камера (sim_chamber): фабрика лута на
   компьютер, а не на гринд. Требует FE — подключи к alternator.
3. loot_fabricator (квест волны 1): печатаёт лут из матриц — второй
   уровень той же идеи. Рецепт заменён: precision_mechanism вместо
   незеритового слитка (main.js:449).
4. СТРАТЕГИЯ: не собирай лут руками — прокачай HNN: к этапу 15
   нужны кости ×1300 (demand.jsonl), порох, стрелы, жемчуг.

## Блок Г — арматура Alex's Caves (волна 1)

1. alexscaves:metal_rebar — арматура: резка scrap_metal камнетёсом
   Create (2× за раз, main.js:467). Scrap metal копи в пещерах
   Алекса (или жди главу 14f — но арматура нужна УЖЕ сейчас для
   locomotive_mechanism ×2 на петлю).
2. slime_ball — ферма слизи уже должна работать (этап 01).

## Блок Д — локомотивный механизм и машина (волны 4–14)

1. locomotive_mechanism: SA от precision_mechanism, 2 петли:
   прочный лист → слизь → арматура ×2 → пресс (main.js:470).
   Т.е. 1 механизм = 2× precision + 2× лист + 2× слизь + 4× арматура.
2. kubejs:obsidian_machine = 8× locomotive_mechanism +
   create:railway_casing (main.js:490). Railway casing — из латунных
   компонентов (JEI). Сдай машину — откроется глава V.
3. Машина расходуется: камнетёс даёт рельсы, станции, семафоры,
   расписания, controls (пульт машиниста) — main.js:499.

## Блок Е — железная дорога (практика, для главы IV/V)

1. Поставь 2 станции + 5–10_CHUNK рельсов между базой и шахтой:
   поезда повезут руду (unlabeled сборка: вагон + controls).
2. travel anchors: рецепт требует locomotive_mechanism (main.js:455) —
   телепорты по базе, очень удобно.
3. Заправка поездов: portable_fuel_interface + fuel_tank ( railways).

## Критерий готовности

- 34/34 в plan/auto/05_...md.
- obsidian_machine сдан; глава V видна.
- HNN-фабрика лута собрана и подключена к FE.
- Поезд ходит по маршруту база↔шахта.

## Что дальше

plan/06_chapter_v_steel.md — сталь TFMG: кокс, домны, steel_mechanism.
