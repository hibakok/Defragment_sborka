"""Пайплайн: генерация музейных чек-листов → plan/museum/<modid>.md.

Запуск из tools/:  python -m pipeline.museum_all
Один мод = один файл (большие делятся на части ≤ 470 предметов).
Галочки [x] из существующих файлов переносятся в новые (как в
plan/auto): перегенерация прогресс не теряет.
"""

import os
import re

from core.files import write_text, ensure_dir
from items import ids
from museum import render, split
from recipes.load import load_all
from recipes.index import craftable_set, produce_index

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
MUSEUM_DIR = ensure_dir(os.path.join(_ROOT, 'plan', 'museum'))
_DONE_LINE = re.compile(r'^- \[x\] .*`([\w.:/]+)`')


def done_ids(path):
    """Вход: путь музейного файла. Выход: {id} отмеченных предметов —
    чтобы перегенерация не теряла галочки."""
    done = set()
    if not os.path.isfile(path):
        return done
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            match = _DONE_LINE.match(line.strip())
            if match:
                done.add(match.group(1))
    return done


def mod_stats(rows, craftable):
    """Вход: предметы мода, множество крафтимых. Выход: (всего,
    крафтимых) — числа для шапки музейного файла."""
    craftable_n = sum(1 for row in rows if row['id'] in craftable)
    return len(rows), craftable_n


def write_part(modid, name, rows, stats, part_no, parts, craftable):
    """Вход: мод, его строки, (всего, крафтимых), номер части, сколько
    частей, множество крафтимых. Выход: —. Пишет один файл части."""
    filename = split.part_filename(modid, part_no, parts)
    path = os.path.join(MUSEUM_DIR, filename)
    part_rows = split.split_parts(rows)[part_no - 1]
    done = done_ids(path)
    lines = render.mod_header(modid, name, stats[0], stats[1], parts)
    title = split.part_title(part_no, parts)
    if title:
        lines.extend([title, ''])
    lines.append('*В части: %d предметов.*' % len(part_rows))
    lines.append('')
    for row in part_rows:
        marker = render.marker_of(row['id'], craftable)
        lines.append(render.item_line(row, marker, row['id'] in done))
    lines.extend(render.footer())
    write_text(path, '\n'.join(lines) + '\n')


def main():
    """Склейка: все моды → plan/museum/. Печать: файл (предметов)."""
    craftable = craftable_set(produce_index(load_all()))
    table = ids.by_mod()
    names = ids.mod_names()
    for modid in sorted(table):
        rows = table[modid]
        stats = mod_stats(rows, craftable)
        parts = len(split.split_parts(rows))
        for part_no in range(1, parts + 1):
            write_part(modid, names.get(modid, modid), rows, stats,
                       part_no, parts, craftable)
        print('%s — %d файл. (%d предм., к=%d)' % (
            modid, parts, stats[0], stats[1]))


if __name__ == '__main__':
    main()
