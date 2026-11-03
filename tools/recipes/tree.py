"""Дерево производства: что нужно, чтобы собрать предмет с нуля.

Запуск из tools/:  python -m recipes.tree create:precision_mechanism
Выход: Markdown-дерево по слоям (как волны квестов): слой 1 — сам
предмет, слой 2 — его крафтимые ингредиенты, и так до сырья.
Теги показываются как теги (разрешение тегов в данных отсутствует).
"""

import sys

from recipes.load import load_all
from recipes.index import best_recipe, produce_index

MAX_DEPTH = 12
MAX_ITEMS = 250


def _item_inputs(index, item_id):
    """Вход: индекс, id. Выход: [id] — крафтимые item-ингредиенты
    лучшего рецепта (теги/жидкости/сырьё не включаются)."""
    ref = best_recipe(index, item_id)
    if not ref:
        return []
    return [target[1] for target in ref['inputs'] if target[0] == 'item']


def need_layers(index, item_id):
    """Вход: индекс, id. Выход: [(слой, [id])] — обход в ширину от
    предмета к сырью; каждый id входит ровно один раз (циклы отсечены)."""
    layers = [(0, [item_id])]
    seen = {item_id}
    frontier = [item_id]
    for depth in range(1, MAX_DEPTH + 1):
        next_ids = []
        for one in frontier:
            for need in _item_inputs(index, one):
                if need not in seen:
                    seen.add(need)
                    next_ids.append(need)
        if not next_ids:
            break
        layers.append((depth, sorted(next_ids)))
        frontier = next_ids[:MAX_ITEMS]
        if len(seen) > MAX_ITEMS * 4:
            break
    return layers


def tree_text(index, item_id):
    """Вход: индекс, id. Выход: строки Markdown-дерева потребностей."""
    lines = ['# Дерево производства: `%s`' % item_id, '']
    total = 0
    for depth, ids in need_layers(index, item_id):
        total += len(ids)
        label = 'Предмет' if depth == 0 else 'Слой %d' % depth
        lines.append('## %s — %d' % (label, len(ids)))
        for one in ids:
            ref = best_recipe(index, one)
            if ref:
                ins = ', '.join(target[1] for target in ref['inputs'])
                lines.append('- `%s` — %s (%s)' % (one, ref['machine'],
                                                   ins))
            else:
                lines.append('- `%s` — сырьё/вне данных' % one)
        lines.append('')
    lines.append('Итого узлов: %d. Теги во входах лучшего рецепта '
                 'смотри в JEI (R по предмету).' % total)
    return lines


def main(argv=None):
    """Склейка CLI: аргумент = id предмета, печать дерева."""
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print('Использование: python -m recipes.tree <modid:item>')
        raise SystemExit(2)
    index = produce_index(load_all())
    if argv[0] not in index:
        print('Нет производящего рецепта в данных: %s' % argv[0])
        print('(лут/дроп или рецепт мода вне выборки — смотри JEI)')
        raise SystemExit(1)
    print('\n'.join(tree_text(index, argv[0])))


if __name__ == '__main__':
    main()
