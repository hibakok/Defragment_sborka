"""Пайплайн: агрегация потребностей → data/demand.jsonl + data/kills.jsonl.

Запуск из tools/:  python -m pipeline.demand_all
Печатает топ потребностей (для analysis/demand_top.md) и топ мобов.
"""

import os

from core.jsonio import save_jsonl
from quests import load
from quests.demand import demand_rows, kill_rows

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
DEMAND_PATH = os.path.join(_ROOT, 'data', 'demand.jsonl')
KILLS_PATH = os.path.join(_ROOT, 'data', 'kills.jsonl')


def save_demand(rows):
    """Вход: строки потребностей. Выход: путь. Сохранить demand.jsonl."""
    return save_jsonl(DEMAND_PATH, rows)


def save_kills(rows):
    """Вход: строки мобов. Выход: путь. Сохранить kills.jsonl."""
    return save_jsonl(KILLS_PATH, rows)


def top_report(rows, limit):
    """Вход: строки, лимит. Выход: текстовый топ для консоли."""
    lines = []
    for row in rows[:limit]:
        lines.append('%(type)s %(target)s — всего %(total)d '
                     '(макс. за квест %(max_once)d, квестов %(n_quests)d)'
                     % row)
    return '\n'.join(lines)


def kills_report(rows, limit):
    """Вход: строки мобов, лимит. Выход: текстовый топ для консоли."""
    lines = []
    for row in rows[:limit]:
        lines.append('%(mob)s — всего %(total)d (квестов %(n_quests)d)' % row)
    return '\n'.join(lines)


def main():
    """Склейка: загрузить → агрегировать → сохранить → отчёт."""
    quests = load.load_all()
    demand = demand_rows(quests)
    kills = kill_rows(quests)
    save_demand(demand)
    save_kills(kills)
    print('demand.jsonl: %d целей; kills.jsonl: %d мобов'
          % (len(demand), len(kills)))
    print('\nТОП-40 потребностей:\n' + top_report(demand, 40))
    print('\nТОП-20 мобов:\n' + kills_report(kills, 20))


if __name__ == '__main__':
    main()
