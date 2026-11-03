# Этап 01: basics — старт и первые 136 квестов

## Цель

Закрыть главу basics (136/136 квестов): знакомство со всеми модами,
первая база, инструменты, еда, Незер, археология. Открыть доступ ко всем
побочным главам (магия, измерения, боссы, чёрный рынок, коллекции).

## Предусловия

- Этап 00 (plan/00_setup.md): сборка 2.5.3 запускается, мир создан.
- Чек-лист квестов: plan/auto/01_basics.md (волны 1–15).
- В игре: книга квестов открывается по клавише из квеста «Keybinds».

## Как работать с этим файлом

Один блок ниже ≈ один сеанс игры (1–2 часа). После каждого блока
отмечай выполненные квесты в plan/auto/01_basics.md (строки `- [ ]` →
`- [x]`) и раз в сеанс запускай `python -m pipeline.progress_count`
(из папки tools/) — он посчитает общий прогресс для TRACKER.md.

## Блок А — первые 30 минут (волны 1–2)

1. Отметь в книге квестов: Welcome!, Talent Tree, Loot Chests, Waystones,
   Why I have less hearts?, Shaders (НЕ включай — GT 1030), Keybinds,
   Multiplayer, Your feedback, Mastering Currency.
2. Скрафти верстак (1 дерево) — квест «Always the same».
3. Прочитай описания квестов «Mastering Currency» и «Why I have less
   hearts?» — там объяснены монеты (Numismatics) и система сердец.
   Не трать монеты: всего по квестам нужно 188 spur + 70 cog.
4. Lootr: сундуки в структурах персональные — вскрывай ВСЕ, это
   безопасно и выгодно.
5. Waystones: активируй каждый встречный камень-телепорт (это сеть
   быстрого перемещения).

## Блок Б — инструменты и ночёвка (волны 2–4)

1. Деревянная кирка → каменные инструменты → печь.
2. Спальник (comforts) — спи без установки точки спавна.
3. «From ...» (6 квестов, волна 4) — ознакомительные чек-квесты авторов
   сборки: просто прочитай и отметь.
4. Первая добыча камня: 16 булыжника + печь (квест «Grab some stone»).

## Блок В — книги знаний (волны 5–7)

Скрафти и сдай (рецепты — JEI, клавиша R по предмету):
1. patchouli:guide_book — общий гайд сборки.
2. alexsmobs:animal_dictionary — зоология Alex's Mobs.
3. iceandfire:manuscript → bestiary → lectern (три квеста Ice and Fire).
4. alexscaves:cave_codex + spelunkery_table (подземелья Alex's Caves).
5. simplyswords:empowered_remnant, netherfused_gem, runefused_gem
   (вехи оружия Simply Swords).
6. quark:abacus, chalk:chalk_box + мел (картирование/разметка).
7. dummmmmmy:target_dummy — манекен для теста урона (поставь на базе).
8. camera:camera — скриншоты внутри игры.
9. toolbelt:belt — пояс с ячейками (надень).

## Блок Г — еда и выживание (волны 7–9)

1. Farmer's Delight: stove, cutting board, skillet, cooking pot —
   кухонный уголок на базе.
2. Spice of Life: Carrot Edition — food_book. КЛЮЧЕВАЯ МЕХАНИКА:
   каждые N разных съеденных продуктов дают +сердце. Ешь РАЗНОЕ с
   первого дня (веди список съеденного в food_book, он сам считает).
3. organic_compost и rich_soil ×4 — основа будущих грядок; рецепт JEI.
4. Парашют paraglider:paraglider — планирование с высоты (стамина).
5. create_sa:andesite_jetpack_chestplate — ранний полёт (Jetpack).
6. Железная броня целиком + железная кирка.
7. Аметист ×1 и подзорная труба (2 медных слитка + аметист).

## Блок Д — исследование поверхности (волны 6, 9–11)

1. STRUCT-квесты: underground_cabin (Alex's Caves), ancient_city
   (Забытые глубины — просто НАЙТИ, не зачищать!), ribbits-деревня.
2. OBSERVE: пчелиное гнездо (наблюдать через подзорную трубу? см. квест).
3. Sniffer: археология на тёплых океанских руинах — подозрительный
   песок → кисточка → sniffer_egg. Вырасти сниффера — он выкапывает
   древние растения.
4. Бронзовые/серебряные шаблоны украшений: археология руин троп.
5. Радуга корундов Quark (9 цветов): кластеры генерируются в пещерах;
   недостающие цвета — планомерно собирай при каждом спуске под землю.
6. Алмазы! («We've Struck Diamonds!») — железная кирка, глубина < 0.

## Блок Е — безопасность базы (волна 11)

1. torchmaster:megatorch — запрещает спавн мобов в радиусе (поставь
   в центре базы); dreadlamp — вариант для воды/воздуха.
2. quark:crafter — автоматический верстак (задел под автоматизацию).
3. Отметь «I want to explore new dimensions» и «The Black Market» —
   вводные к побочным главам (этапы 13–15).

## Блок Ж — Незер (волна 12–13)

1. 10 обсидиана + вход в Незер (достижение).
2. Собери: незер-нарост (грядки в адской крепости), кварц, душевный
   песок, quark:soul_bead (рецепт JEI), born_in_chaos:ethereal_spirit
   (днём/ночью охоться на духов Born in Chaos).
3. Netherite-шаблон — сундуки бастионов (осторожно, пиглины!).
4. Достижения: fast_travel (7 блоков по рельсам... см. в игре),
   create_beacon (маяк = убей Визера), respawn_anchor ×1.
5. Тотем бессмертия — выбей у призывателя (Evoker, лесной особняк
   или рейд). Один обязателен, всегда носи.

## Блок З — археология (волны 13–14)

1. minecraft:brush + betterarcheology:archeology_table.
2. fossiliferous_dirt ×4 и suspicious_red_sand ×4 — копай кисточкой
   (Better Archaeology генерирует ископаемые блоки).
3. Достижения: loot_vase_broken, artifact_shards, unidentified_artifact.

## Блок И — декор и QoL-волна (волна 13, 43 квеста)

Самая длинная волна — крафтовая. Один вечер с открытым JEI:
1. Supplementaries (15+ предметов: wrench, key, cage, sack, flags,
   notice_board, blackboard, speaker_block, turn_table, bamboo_spikes,
   redstone_illuminator, ender_watcher, feeding_trough, slime_in_a_bucket,
   glass_item_frame, obsidian_pressure_plate, золотые/незеритовые двери).
2. Chipped: 7 верстаков (alchemy_bench, mason_table, tinkering_table,
   botanist_workbench, loom_table, glassblower, carpenters_table).
3. Refurbished Furniture: workbench, light_electricity_generator.
4. McW Bridges / Additional Lights / Handcrafted — по ОДНОМУ любому
   предмету мода (квесты «любой предмет мода»).
5. dustrial_decor: sheet_metal ×3 + cardboard ×8.
6. framedblocks:framed_cube, immersive_paintings:painting,
   armor_stand (косметика статуй), supplementaries:crank («Crankonator»),
   create:tree_fertilizer, quark:seed_pouch, trowel, lodestone.

## Блок К — Dimensional Dungeons (волны 13–15)

1. block_gilded_portal ×2, portal_key, key_charger, keyhole,
   blank_build_key, secret_bell, portal_crown ×2, cfm circuit_breaker.
2. Механика: находи «позолоченные» портальные камни в подземельях,
   ключи открывают личные карманные данжи (безопасная лут-ферма).

## Критерий готовности

- plan/auto/01_basics.md: 136/136 галочек.
- База: мегафакел, спальник, кухня FD, манекен, вейстоун.
- В сундуках лежат: монеты Numismatics (не тратить!), тотем,
  netherite-шаблон, 9 корундов, sniffer_egg высижен.
- Команда `python -m pipeline.progress_count` показывает ≥136.

## Что дальше

plan/02_chapter_i_andesite.md — андезитовая машина: первый механизм
и вход в технологическую ветку Create.
