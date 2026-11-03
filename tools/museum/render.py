"""Кирпичики Markdown для музейных чек-листов (plan/museum/).

Маркер предмета — способ добычи:
  к — рецепт есть в данных (data/recipes + kubejs) → автокрафт/фабрика;
  в — ванильный minecraft (рецепты в клиенте игры, смотри JEI);
  н — нет рецепта в данных → лут, дроп, данж, торговля.
"""

import re

_DONE = re.compile(r'^- \[x\] .*`([\w.:/]+)`')
GEN_NOTE = ('> Файл сгенерирован (tools/pipeline/museum_all.py). Руками '
            'менять ТОЛЬКО галочки `- [ ]` → `- [x]`: перегенерация '
            'сохраняет галочки, остальное перезаписывает.')


def marker_of(item_id, craftable):
    """Вход: id предмета, множество крафтимых. Выход: 'к' | 'в' | 'н'."""
    if item_id in craftable:
        return 'к'
    if item_id.startswith('minecraft:'):
        return 'в'
    return 'н'


def item_line(row, marker, done):
    """Вход: строка предмета, маркер, галочка. Выход: строка чек-листа
    вида: - [ ] **Имя** — `modid:path` · к"""
    box = 'x' if done else ' '
    return '- [%s] **%s** — `%s` · %s' % (box, row['name'], row['id'],
                                          marker)


def mod_header(modid, name, total, craftable_n, parts):
    """Вход: мод, имя, всего/крафтимых предметов, всего частей.
    Выход: строки шапки музейного файла мода."""
    share = 100 * craftable_n // total if total else 0
    lines = ['# Музей: %s (%s)' % (name, modid), '']
    lines.append('Предметов: %d · крафтимых по данным: %d (%d%%) · '
                 'файлов: %d' % (total, craftable_n, share, parts))
    lines.append('')
    lines.append(GEN_NOTE)
    lines.append('')
    lines.append('Маркер: · к — рецепт в данных (фабрика возможна); '
                 '· в — ваниль (JEI); · н — лут/дроп/данж.')
    lines.append('')
    return lines


def footer():
    """Вход: —. Выход: строки подвала со ссылкой на источник."""
    return ['', '---', 'Источник имён: data/items.jsonl; рецептов: '
            'data/recipes/*.jsonl + data/kubejs/.']
