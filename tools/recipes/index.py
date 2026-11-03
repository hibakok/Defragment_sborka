"""Индекс производства: предмет → рецепты, которые его делают.

Вход: строки recipes/load.load_all(). Выход: {item_id: [ссылки]},
ссылка = {machine, source, count, inputs}. Теги и жидкости в ключ
не попадают: индекс отвечает только за предметы.
"""

from recipes.parse import ingredients, machine_name, results


def produce_index(rows):
    """Вход: рецепты load_all(). Выход: {item_id: [ссылки рецептов]}.
    Одна ссылка на рецепт: машина, источник, выход, входы."""
    index = {}
    for row in rows:
        inputs = ingredients(row['json'])
        for target, count in results(row['json']):
            if target[0] != 'item':
                continue
            index.setdefault(target[1], []).append(
                {'machine': machine_name(row['type']),
                 'source': row['source'], 'count': count,
                 'inputs': inputs})
    return index


def craftable_set(index):
    """Вход: индекс. Выход: множество id крафтимых предметов."""
    return set(index)


def ways_of(index, item_id):
    """Вход: индекс, id. Выход: число способов производства (0 если нет)."""
    return len(index.get(item_id, []))


def machines_of(index, item_id):
    """Вход: индекс, id. Выход: отсортированный список машин."""
    return sorted({ref['machine'] for ref in index.get(item_id, [])})


def best_recipe(index, item_id):
    """Вход: индекс, id. Выход: ссылка-рецепт или None. Выбор для
    дерева потребностей: меньше входов — проще объяснить."""
    refs = index.get(item_id)
    return min(refs, key=lambda ref: len(ref['inputs'])) if refs else None
