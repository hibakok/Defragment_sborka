"""Агрегация требований квестов: предметы, жидкости, мобы (см. ../METHODS.md).

Ветка кода: demand_key/task_type — примитивы классификации; demand_rows
и kill_rows собирают агрегаты поверх parse_task из quests/tasks.py.
"""

from quests.tasks import parse_tasks


def demand_key(task):
    """Вход: разобранная задача item/fluid. Выход: (тип, цель) для группировки.

    item → 'item'; 'any#tag:x' → 'tag:x'; прочие any → 'any'."""
    target = task['target']
    if task['type'] == 'fluid':
        return ('fluid', target)
    if target.startswith('any#tag:'):
        return ('tag', target[len('any#tag:'):])
    if target.startswith('any'):
        return ('any', target)
    return ('item', target)


def demand_rows(quests):
    """Вход: квесты. Выход: [{type, target, total, max_once, n_quests}]
    — суммарная потребность в предметах/жидкостях, по убыванию total."""
    table = {}
    for quest in quests:
        for task in parse_tasks(quest):
            if task['type'] not in ('item', 'fluid'):
                continue
            kind, target = demand_key(task)
            row = table.setdefault(
                (kind, target),
                {'type': kind, 'target': target,
                 'total': 0, 'max_once': 0, 'n_quests': 0})
            row['total'] += task['count']
            row['max_once'] = max(row['max_once'], task['count'])
            row['n_quests'] += 1
    rows = list(table.values())
    rows.sort(key=lambda row: (-row['total'], row['target']))
    return rows


def kill_rows(quests):
    """Вход: квесты. Выход: [{mob, total, n_quests}] — кого и сколько
    убить, по убыванию total."""
    table = {}
    for quest in quests:
        for task in parse_tasks(quest):
            if task['type'] != 'kill':
                continue
            row = table.setdefault(
                task['target'],
                {'mob': task['target'], 'total': 0, 'n_quests': 0})
            row['total'] += task['count']
            row['n_quests'] += 1
    rows = list(table.values())
    rows.sort(key=lambda row: (-row['total'], row['mob']))
    return rows
