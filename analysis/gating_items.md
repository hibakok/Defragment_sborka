# Гейтинговые машины и лестница механизмов

Источник: `data/kubejs/server_scripts/main.js` (точные рецепты, номера
строк), `data/recipes/create_dd.jsonl`, `data/recipes/create_things_and_misc.jsonl`,
`data/demand.jsonl`, `data/chapters/*.jsonl`.
Гейтинг — постепенное открытие контента через кастомные механизмы и
«машины». Здесь полная цепочка со ВСЕМИ промежуточными рецептами.

## Как устроен гейтинг (главный принцип сборки)

1. **Механизм** (rotation → hydraulic → precision → …) собирается
   Sequenced Assembly (SA) из механизма ПОРОМ НИЖЕ.
2. **Машина** = 8 механизмов текущего уровня + кожух (casing), рецепт 3×3.
3. Машина — РАСХОДНЫЙ материал: камнетёс (multicut) или бесс Shapeless
   (машина + предмет) превращают её в компоненты Create, а оригинальные
   рецепты компонентов УДАЛЕНЫ (remove.js). 1 машина = 1 компонент!
   Пример: `brass_machine + алмазный блок → механический пресс`
   (main.js:182–192). Поэтому механизмов нужно ТЫСЯЧИ (demand.jsonl).

## Лестница механизмов (точные SA-рецепты)

| # | Механизм | Вход SA | Шаги (deploy/fill/press) | Петли | Файл |
| --- | --- | --- | --- | --- | --- |
| 1 | kubejs:rotation_mechanism | любая дерев. плита | андезитовый сплав ×2 → молот Ad Astra | 1 | main.js:108 |
| 2 | create_sa:hydraulic_engine | rotation_mechanism | медный лист → #forge:glass → гаечный ключ (supplementaries) → пресс | 1 | main.js:204 |
| 3 | create:precision_mechanism | hydraulic_engine | латунный лист → электронная лампа → шестерня → пресс | 2 | main.js:353 |
| 4 | kubejs:locomotive_mechanism | precision_mechanism | прочный лист → слизь → арматура Alex's Caves ×2 → пресс | 2 | main.js:470 |
| 5 | tfmg:steel_mechanism | locomotive_mechanism | тяж. пластина TFMG → сталь → алюминий → винт → отвёртка | 2 | main.js:552 |
| 6 | create_dd:infernal_mechanism | steel_mechanism | бензин 25mB → дроб. магма → ember alloy → пресс | 2 | main.js:690 |
| 7 | create_dd:calculation_mechanism | infernal_mechanism | лист сияния → олов. лист → медная катушка → оптич. прибор (create_optical) → пресс | 2 | main.js:1015 |
| 8 | create_dd:integrated_circuit | calculation_mechanism | лист перегруз. сплава → control chip → светопыль → резистор → конденсатор | 1 | main.js:1032 |
| 9 | create_dd:sealed_mechanism | резина (create_dd:rubber) | шестерня → суш. ламинария → медный лист → стекло | 4 | recipes/create_dd |
| 10 | create_things_and_misc:vibration_mechanism | (см. data/recipes/create_things_and_misc.jsonl) | — | — | recipes |

Параллельные цепочки (не «лестница», но нужны в тысячах):
- tfmg:steel_mechanism — гл. V; sealed/vibration — чёрный рынок (по 3001 шт).
- kubejs:tier_1..4_plating — ракеты: SA от infernal_mechanism:
  пыль мундабитур ×2 → пыль коррупти ×2 → тяж. пластина → пресс (t1,
  main.js:745); t2–t4 — аналогично дальше по main.js.

## Машины-ключи глав (8 механизлов + кожух, 3×3)

| Машина | Механизмов ×8 | Кожух | Что открывает | Глава |
| --- | --- | --- | --- | --- |
| kubejs:andesite_machine («Rotation Machine») | rotation_mechanism | create:andesite_casing | компоненты Create 1-го тира | I (main.js:137) |
| kubejs:copper_machine («Valve Machine») | hydraulic_engine | create:copper_casing | жидкостные компоненты | III (main.js:218) |
| kubejs:brass_machine («Precision Machine») | precision_mechanism | create:brass_casing | умные компоненты, крафтеры | II (main.js:369) |
| kubejs:obsidian_machine («Locomotive Machine») | locomotive_mechanism | create:railway_casing | ж/д компоненты, рельсы Steam'n'Rails | IV (main.js:490) |

Имена машин — из `data/kubejs/assets/kubejs/lang/en_us.json`.

## Что даёт каждая машина (примеры, main.js)

- andesite_machine: 32 компонента камнетёсом (вод. колеса, воронки,
  поршни, депо, лопасти…) + 7 «shapeless-форм» (пресс = машина +
  алмазный блок и т.п.), main.js:147–192.
- copper_machine: трубы ×12, помпы, паровой двигатель, чаны,
  опрыскиватель, медный джетпак (pyrope из Blue Skies!) main.js:227–248.
- brass_machine: 34 компонента (мех. руки, крафтеры ×3 от верстака!,
  вентили, nixie-трубки, ролик из колеса дробления) main.js:378–427.
- obsidian_machine: рельсы-компоненты, семафоры, станции,
  расписание, пульт управления поездом main.js:499–514.

## Ключевые промежуточные цепочки (для фабрик)

- Электронная лампа: деплой железный лист + полир. розовый кварц
  (main.js:301). Розовый кварц: SA — кристалл-certus + дестабилизир.
  красный камень 50mB ×3 петли (main.js:342); дестаб. красный камень:
  смешивание 3× redstone + 4× адский нарост, нагрев (main.js:340).
- Certus-кварц (AE2): смешивание вода 100mB + песок + сахар ×2 + кварц
  → мал. бутон (main.js:309); рост бутона → кластера: SA с заливкой
  воды 100mB ×3 петли на каждый тир (main.js:311–336); кластер →
  фрезеровка = 3 кристалла (main.js:338). ПОЛНОСТЬЮ автоматизируемо.
- Chromatic compound (create_dd): смешивание 4× обсидиановая пыль +
  полир. розовый кварц + полир. спектр. рубин, superheated → ×2
  (recipes/create_dd) ИЛИ полир. рубин + matter ball (AE2) + хроматич.
  сток 500mB → ×2 (main.js:1008).
- Спектральный рубин: аметист + 7× светящаяся пыль (shapeless);
  полировка наждаком. Сияние (refined_radiance): сундуки деревень
  ЛУНЫ ×10 (loot.js:386–403) и лут боссов; лист сияния — прессование.
- Сталь TFMG: кокс. печь (кокс из угля) → дом. печь TFMG; разлив
  112mB жидкой стали в изложницу (main.js:545).
- Бокситы: 4× тухловая мука + красный песок (мех. крафт, main.js:536) —
  возобновляемый алюминий.

## Как играть в гейтинг (стратегия)

1. Первую машину-ключ каждого тира сдай ЕДИНИЧНО на квест главы.
2. Далее строишь SA-конвейер (депо + деплоеры + пресс) механизмов —
   это завод №1 (см. plan/17_factories.md, «Лестница»).
3. Камнетёс ставь рядом с запасом машин: bulk-конверсия в компоненты.
4. Открытие новой главы = новый SA-конвейер поверх старого (вход =
   выход предыдущего). НЕ ломай старые линии — они нужны для чёрного
   рынка (3000+ шт sealed/vibration, 1024+ механизмов каждой ступени).
5. Точные рецепты компонентов — JEI (R по предмету) и
   data/recipes/*.jsonl; кастомные — data/kubejs/server_scripts/main.js.
