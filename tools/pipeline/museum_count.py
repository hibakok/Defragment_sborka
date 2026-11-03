"""Пайплайн: подсчёт музейного прогресса по plan/museum/*.md.

Запуск из tools/:  python -m pipeline.museum_count
Считает галочки '- [x]'/'- [ ]' по каждому файлу, выводит таблицу
модов и итог. Итог пишется в TRACKER игроком вручную.
"""

import glob
import os

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
MUSEUM_GLOB = os.path.join(_ROOT, 'plan', 'museum', '*.md')


def count_file(path):
    """Вход: путь музейного файла. Выход: (сделано, всего) — подсчёт
    строк '- [x]' и '- [ ]' в файле."""
    done = total = 0
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith('- [x]'):
                done += 1
                total += 1
            elif stripped.startswith('- [ ]'):
                total += 1
    return done, total


def mod_rows():
    """Вход: —. Выход: [(modid, сделано, всего)] — по всем файлам
    музея, сгруппировано по modid (части одного мода суммируются)."""
    table = {}
    for path in sorted(glob.glob(MUSEUM_GLOB)):
        base = os.path.basename(path)[:-3]
        modid = base.split('_part')[0]
        done, total = count_file(path)
        if not total:  # служебные файлы (README) без галочек
            continue
        row = table.setdefault(modid, [0, 0])
        row[0] += done
        row[1] += total
    return sorted(table.items())


def main():
    """Склейка: таблица модов + итог для progress/TRACKER.md."""
    rows = mod_rows()
    done_sum = sum(row[1][0] for row in rows)
    total_sum = sum(row[1][1] for row in rows)
    print('%-24s %10s %8s' % ('мод', 'получено', 'всего'))
    for modid, (done, total) in rows:
        print('%-24s %6d/%-6d' % (modid, done, total))
    print('\nИТОГО предметов: %d / %d' % (done_sum, total_sum))
    if total_sum:
        print('Готовность: %.1f%%' % (100.0 * done_sum / total_sum))
    print('Строку «Предметов получено» в progress/TRACKER.md обнови.')


if __name__ == '__main__':
    main()
