"""Нормализация рецептов: ингредиенты, результаты, машина.

Любой рецепт сборки разворачивается в списки целей. Цель — кортеж:
('item', id) | ('tag', tag) | ('fluid', id). Спец-типы без результата
(ae2:matter_cannon и пр.) результата не дают — это честно.
"""

_MACHINES = {
    'minecraft:crafting_shaped': 'Верстак (шаблон)',
    'minecraft:crafting_shapeless': 'Верстак (бессхемно)',
    'minecraft:stonecutting': 'Камнетёс',
    'minecraft:smelting': 'Печь',
    'minecraft:blasting': 'Доменная печь',
    'minecraft:smoking': 'Коптильня',
    'minecraft:campfire_cooking': 'Костёр',
    'minecraft:smithing_transform': 'Стол кузнеца',
    'create:milling': 'Мельница',
    'create:crushing': 'Дробитель',
    'create:pressing': 'Пресс',
    'create:cutting': 'Механическая пила',
    'create:mixing': 'Смеситель',
    'create:compacting': 'Компактор (пресс)',
    'create:filling': 'Наливщик',
    'create:emptying': 'Опорожнитель',
    'create:deploying': 'Деплойер',
    'create:splashing': 'Промывщик',
    'create:haunting': 'Одержимость (душа)',
    'create:sequenced_assembly': 'SA-линия (сборочная)',
    'create:mechanical_crafting': 'Механический верстак',
    'create:item_application': 'Наложение предметов',
    'createaddition:charging': 'Тесла-катушка',
    'createaddition:rolling': 'Валковый станок',
    'createaddition:liquid_burning': 'Жидкостная горелка',
    'ae2:inscriber': 'Гравировщик AE2',
    'farmersdelight:cooking': 'Котелок',
    'farmersdelight:cutting': 'Разделочная доска',
    'refurbished_furniture:workbench_constructing': 'Мебельный верстак',
    'refurbished_furniture:cutting_board_slicing': 'Разделочная доска',
    'refurbished_furniture:cutting_board_combining': 'Разделочная доска',
    'refurbished_furniture:oven_baking': 'Мебельная печь',
    'refurbished_furniture:freezer_solidifying': 'Морозильник',
    'aether:repairing': 'Починка (Эфир)',
    'forbidden_arcanus:clibano_combustion': 'Клибано',
}


def machine_name(rtype):
    """Вход: тип рецепта. Выход: человекочитаемая машина.
    Неизвестный тип → последнее слово без пространства имён."""
    if rtype in _MACHINES:
        return _MACHINES[rtype]
    return rtype.rsplit(':', 1)[-1].replace('_', ' ')


def norm_target(entry):
    """Вход: словарь/строка ингредиента. Выход: цель-кортеж или None.
    Понимает {'item': x}, {'tag': x}, {'fluid': x} и строку 'mod:id'."""
    if isinstance(entry, str):
        return ('item', entry)
    if not isinstance(entry, dict):
        return None
    for kind in ('item', 'tag', 'fluid'):
        if isinstance(entry.get(kind), str):
            return (kind, entry[kind])
    return None


def _shaped(recipe):
    """Вход: рецепт с key/pattern. Выход: цели ингредиентов шаблона."""
    targets = []
    for char in ''.join(recipe.get('pattern', [])):
        if char != ' ':
            target = norm_target(recipe.get('key', {}).get(char))
            if target:
                targets.append(target)
    return targets


def effective(recipe):
    """Вход: рецепт. Выход: [эффективные рецепты] — разворот
    forge:conditional во внутренние рецепты (рекурсивно)."""
    if recipe.get('type') == 'forge:conditional':
        inner = []
        for block in recipe.get('recipes', []):
            inner.extend(effective(block))
        return inner
    return [recipe]


def _sequence(recipe):
    """Вход: рецепт create:sequenced_assembly. Выход: цели шагов SA
    (база + деплойер-предметы; incomplete-заготовки отброшены)."""
    targets = []
    for step in recipe.get('sequence', []):
        for entry in step.get('ingredients', []):
            target = norm_target(entry)
            if target and 'incomplete' not in target[1]:
                targets.append(target)
    return targets


def ingredients(recipe):
    """Вход: рецепт. Выход: [цели] — что потребляет рецепт.
    Порядок ветки: conditional → shaped → список → одиночный → SA."""
    targets = []
    for one in effective(recipe):
        if 'key' in one and 'pattern' in one:
            targets.extend(_shaped(one))
        for field in ('ingredients', 'ingredient'):
            value = one.get(field)
            for entry in (value if isinstance(value, list) else [value]):
                target = norm_target(entry)
                if target:
                    targets.append(target)
        if one.get('type') == 'create:sequenced_assembly':
            targets.extend(_sequence(one))
    return targets


def _result_count(result):
    """Вход: словарь результата. Выход: (цель, количество) или None."""
    target = norm_target(result)
    count = result.get('count', 1) if isinstance(result, dict) else 1
    return (target, count) if target else None


def results(recipe):
    """Вход: рецепт. Выход: [(цель, количество)] — что производит.
    SA-линия отдаёт только главный продукт (остальное — лом)."""
    pairs = []
    for one in effective(recipe):
        if one.get('type') == 'create:sequenced_assembly':
            head = one.get('results', [{}])[0]
            pair = _result_count(head)
            if pair:
                pairs.append(pair)
            continue
        for field in ('result', 'results'):
            value = one.get(field)
            entries = value if isinstance(value, list) else [value]
            for entry in entries:
                pair = _result_count(entry) if entry else None
                if pair:
                    pairs.append(pair)
    return pairs
