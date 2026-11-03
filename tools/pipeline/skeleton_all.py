"""Пайплайн: генерация чек-листов глав → plan/auto/NN_глава.md (31 файл).

Запуск из tools/:  python -m pipeline.skeleton_all
Файлы plan/auto/ — генерируемые: правки вручную запрещены (RULES.md).
"""

import os
import re

from core.files import read_text, write_text, ensure_dir
from quests import load
from quests import graph
from quests.demand import demand_rows
from quests.tasks import parse_tasks
from plan import render, route

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
AUTO_DIR = ensure_dir(os.path.join(_ROOT, 'plan', 'auto'))
_DONE_LINE = re.compile(r'^- \[x\] .*`(\w{6})`\s*$')


def waves_of(quests):
    """Вход: квесты главы с глубинами. Выход: [(глубина, [квесты])]."""
    table = {}
    for quest in quests:
        table.setdefault(quest['d'], []).append(quest)
    return sorted(table.items())


def demand_lines(quests):
    """Вход: квесты главы. Выход: строки топ-5 потребностей главы."""
    rows = demand_rows(quests)[:5]
    lines = [render.heading(2, 'Крупные потребности главы')]
    for row in rows:
        lines.append('- %s %s — всего ×%d (макс. за квест ×%d)'
                     % (row['type'], row['target'],
                        row['total'], row['max_once']))
    if not rows:
        lines.append('- (нет задач на предметы)')
    return lines


def done_ids(path):
    """Вход: путь к существующему чек-листу. Выход: множество 6-симв.
    id выполненных квестов — чтобы перегенерация не теряла галочки."""
    done = set()
    if not os.path.isfile(path):
        return done
    for line in read_text(path).splitlines():
        match = _DONE_LINE.match(line.strip())
        if match:
            done.add(match.group(1))
    return done


def chapter_lines(chapter, index_entry, path):
    """Вход: глава, запись _index, путь чек-листа. Выход: строки md."""
    done = done_ids(path)
    quests = load.load_chapter(chapter)
    graph.with_positions(quests)
    depths = graph.quest_depth(quests)
    for quest in quests:
        quest['d'] = depths[quest['id']]
    waves = waves_of(quests)
    lines = render.chapter_header(chapter, index_entry, len(quests),
                                  len(waves)).split('\n')
    for depth, group in waves:
        lines.append('')
        lines.append(render.wave_heading(depth, len(group)))
        for quest in group:
            lines.append(render.quest_line(quest, quest['id'][:6] in done))
    lines.append('')
    lines.extend(demand_lines(quests))
    lines.append('')
    lines.append(render.file_reference(chapter))
    return lines


def main():
    """Склейка: для каждой главы — файл plan/auto/<этап>_<глава>.md.
    Галочки [x] из существующих файлов переносятся в новые."""
    entries = {entry['file'][:-6]: entry for entry in load.chapter_index()}
    for chapter, _stage in route.ROUTE:
        index_entry = entries[chapter]
        name = route.auto_filename(chapter)
        path = os.path.join(AUTO_DIR, name)
        text = '\n'.join(chapter_lines(chapter, index_entry, path)) + '\n'
        write_text(path, text)
        print('%s (%d квестов)' % (name, index_entry['quests']))


if __name__ == '__main__':
    main()
