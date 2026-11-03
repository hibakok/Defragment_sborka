"""Пайплайн: подсчёт прогресса по галочкам в plan/auto/*.md.

Запуск из tools/:  python -m pipeline.progress_count
Считает '- [ ]' (не сделано) и '- [x]' (сделано) в каждом файле
и печатает сводку для переноса в progress/TRACKER.md.
"""

import os

from core.files import list_files, read_text

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
AUTO_DIR = os.path.join(_ROOT, 'plan', 'auto')


def count_file(path):
    """Вход: путь к md-файлу. Выход: (сделано, всего) по строкам '- ['."""
    done = total = 0
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith('- [x]'):
            done += 1
            total += 1
        elif stripped.startswith('- [ ]'):
            total += 1
    return done, total


def main():
    """Склейка: обойти plan/auto → напечатать сводку прогресса."""
    grand_done = grand_total = 0
    for name in list_files(AUTO_DIR, '.md'):
        done, total = count_file(os.path.join(AUTO_DIR, name))
        grand_done += done
        grand_total += total
        print('%-45s %4d / %4d' % (name, done, total))
    percent = 100.0 * grand_done / grand_total if grand_total else 0.0
    print('ИТОГО: %d / %d квестов (%.1f%%)'
          % (grand_done, grand_total, percent))


if __name__ == '__main__':
    main()
