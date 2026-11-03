"""Пайплайн: все квесты → data/quest_order.jsonl (глобальный порядок).

Запуск из tools/:  python -m pipeline.order_all
Порядок — топологический (deps всегда раньше), внутри волны — по этапу
маршрута и позиции в файле главы.
"""

import os

from core.jsonio import save_jsonl
from quests import load
from quests import graph
from quests.tasks import clean_title, parse_tasks
from plan.route import stage_of

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
OUT_PATH = os.path.join(_ROOT, 'data', 'quest_order.jsonl')


def build_rows(quests):
    """Вход: квесты с глубинами и pos. Выход: компактные строки порядка."""
    rows = []
    for quest in quests:
        rows.append({
            'id': quest['id'],
            'ch': quest['chapter'],
            'd': quest['d'],
            'pos': quest['pos'],
            'title': clean_title(quest.get('title', '')),
            'tasks': [[task['type'], task['target'], task['count']]
                      for task in parse_tasks(quest)],
        })
    return rows


def ordered_quests():
    """Вход: —. Выход: квесты, готовые к сортировке (с d и pos)."""
    quests = load.load_all()
    graph.with_positions(quests)
    depths = graph.quest_depth(quests)
    for quest in quests:
        quest['d'] = depths[quest['id']]
    return graph.order_rows(quests, depths, stage_of)


def main():
    """Склейка: загрузить → отсортировать → сохранить → отчёт."""
    rows = build_rows(ordered_quests())
    save_jsonl(OUT_PATH, rows)
    print('quest_order.jsonl: %d квестов, макс. глубина %d'
          % (len(rows), max(row['d'] for row in rows)))


if __name__ == '__main__':
    main()
