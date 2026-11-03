"""Экстрактор: квесты FTB Quests из инстанса → data/chapters/*.jsonl.

Запуск из tools/:
  python -m extract.quests_from_instance "<путь к папке инстанса>"
Источник: config/ftbquests/quests/chapters/*.snbt.
Поддержаны две раскладки FTB Quests:
  A — глава-файл со списком quests: [ ... ] внутри;
  B — глава-папка, внутри которой один .snbt на каждый квест.
ВНИМАНИЕ: перезаписывает data/chapters/, _index.jsonl и meta.json.
Перед запуском закоммить текущее состояние репозитория.
"""

import os
import re

from core.files import read_text, list_files, ensure_dir
from core.jsonio import load_json, save_json, save_jsonl
from snbt.parser import parse_snbt

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
CHAPTERS_DIR = os.path.join(_ROOT, 'data', 'chapters')
META_PATH = os.path.join(_ROOT, 'data', 'meta.json')
_COUNT = re.compile(r'\sx(\d+)$')


def quests_root(instance_dir):
    """Вход: папка инстанса. Выход: путь config/ftbquests/quests."""
    return os.path.join(instance_dir, 'config', 'ftbquests', 'quests')


def parse_file(path):
    """Вход: путь к .snbt. Выход: разобранный объект (или None)."""
    try:
        return parse_snbt(read_text(path))
    except (ValueError, OSError):
        return None


def item_target(item):
    """Вход: значение item задачи. Выход: цель для строки задачи."""
    if isinstance(item, str):
        return item
    if 'tag' in item:
        return 'any#tag:%s' % item['tag']
    if 'id' in item:
        return str(item['id'])
    if 'items' in item:
        return 'any of [%s]' % ', '.join(str(one) for one in item['items'])
    return 'unknown'


def as_list(value):
    """Вход: значение SNBT. Выход: список (оборачивает одиночное)."""
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def task_line(task):
    """Вход: задача-словарь SNBT. Выход: строка задачи схемы данных."""
    kind = task.get('type', '')
    if kind == 'item':
        item = task.get('item', {})
        count = task.get('count', 0) or (
            item.get('count', 1) if isinstance(item, dict) else 1)
        return 'ITEM %s x%s' % (item_target(item), count)
    if kind == 'fluid':
        return fluid_line(task)
    if kind == 'checkmark':
        return 'CHECK'
    if kind == 'kill':
        return 'KILL %s x%s' % (task.get('mob', ''), task.get('count', 1))
    if kind == 'advancement':
        return 'ADV %s' % task.get('advancement', '')
    if kind == 'dimension':
        return 'DIM %s' % task.get('dimension', '')
    if kind == 'biome':
        return 'BIOME %s' % task.get('biome', '')
    if kind == 'structure':
        return 'STRUCT %s' % task.get('structure', '')
    if kind == 'observation':
        return 'OBSERVE %s' % task.get('structure', '')
    return '%s ?' % str(kind).upper()


def fluid_line(task):
    """Вход: задача type=fluid. Выход: строка FLUID id xN."""
    fluid = task.get('fluid', '')
    amount = task.get('amount', task.get('count', 1))
    if isinstance(fluid, dict):
        amount = fluid.get('Amount', amount)
        fluid = fluid.get('FluidName', '')
    return 'FLUID %s x%s' % (fluid, amount)


def description_of(quest):
    """Вход: квест SNBT. Выход: описание одной строкой (может быть пустой)."""
    raw = quest.get('description', '')
    lines = [str(line) for line in as_list(raw)]
    return '\n'.join(lines).strip()


def quest_row(quest):
    """Вход: квест SNBT. Выход: строка схемы data/chapters."""
    mode = quest.get('dependency_mode', 0)
    return {
        'id': str(quest.get('id', '')),
        'title': str(quest.get('title', '')),
        'deps': [str(dep) for dep in as_list(quest.get('dependencies'))],
        'dm': 'ONE' if mode == 1 else 'ALL',
        'tasks': [task_line(task) for task in as_list(quest.get('tasks'))],
        'desc': description_of(quest),
    }


def chapter_from_file(path):
    """Вход: .snbt главы (раскладка A). Выход: (имя, запись _index, квесты)."""
    root = parse_file(path)
    if root is None or 'quests' not in root:
        return None
    name = str(root.get('filename',
                        os.path.splitext(os.path.basename(path))[0]))
    quests = [quest_row(quest) for quest in as_list(root.get('quests'))]
    entry = {'file': name + '.jsonl', 'group': str(root.get('group', '')),
             'order': root.get('order', 0), 'quests': len(quests)}
    return name, entry, quests


def chapter_from_dir(path):
    """Вход: папка главы (раскладка B). Выход: (имя, запись, квесты) или None."""
    quests = []
    for name in list_files(path, '.snbt'):
        quest = parse_file(os.path.join(path, name))
        if quest and 'tasks' in quest:
            quests.append(quest_row(quest))
    if not quests:
        return None
    chapter = os.path.basename(path)
    meta_path = os.path.join(os.path.dirname(path), chapter + '.snbt')
    meta = parse_file(meta_path) if os.path.isfile(meta_path) else None
    entry = {'file': chapter + '.jsonl',
             'group': str(meta.get('group', '')) if meta else '',
             'order': meta.get('order', 0) if meta else 0,
             'quests': len(quests)}
    return chapter, entry, quests


def collect_chapters(instance_dir):
    """Вход: папка инстанса. Выход: [(имя, запись _index, квесты)]."""
    chapters_dir = os.path.join(quests_root(instance_dir), 'chapters')
    found = []
    if not os.path.isdir(chapters_dir):
        return found
    for name in sorted(os.listdir(chapters_dir)):
        full = os.path.join(chapters_dir, name)
        if os.path.isfile(full) and name.endswith('.snbt'):
            chapter = chapter_from_file(full)
            if chapter:
                found.append(chapter)
        elif os.path.isdir(full):
            chapter = chapter_from_dir(full)
            if chapter:
                found.append(chapter)
    return found


def task_type_counts(chapters):
    """Вход: собранные главы. Выход: {тип задачи: число} для meta.json."""
    table = {}
    for _name, _entry, quests in chapters:
        for quest in quests:
            for line in quest['tasks']:
                kind = _COUNT.sub('', line).split(' ', 1)[0].lower()
                table[kind] = table.get(kind, 0) + 1
    return dict(sorted(table.items(), key=lambda row: -row[1]))


def write_chapters(chapters):
    """Вход: собранные главы. Выход: —. Пишет jsonl + _index.jsonl."""
    ensure_dir(CHAPTERS_DIR)
    entries = []
    for name, entry, quests in chapters:
        save_jsonl(os.path.join(CHAPTERS_DIR, name + '.jsonl'), quests)
        entries.append(entry)
    entries.sort(key=lambda row: (row['group'], row['order'], row['file']))
    save_jsonl(os.path.join(CHAPTERS_DIR, '_index.jsonl'), entries)


def update_meta(chapters):
    """Вход: собранные главы. Выход: —. Обновляет счётчики meta.json."""
    meta = load_json(META_PATH)
    total = sum(entry['quests'] for _n, entry, _q in chapters)
    meta['total_quests'] = total
    meta['chapters'] = len(chapters)
    meta['quest_task_types'] = task_type_counts(chapters)
    meta['quest_extraction'] = 'quests_from_instance.py'
    save_json(META_PATH, meta)


def main():
    """Склейка: собрать главы → записать данные → отчёт."""
    if len(os.sys.argv) < 2:
        raise SystemExit('Использование: python -m extract.quests_from_instance'
                         ' "<путь к папке инстанса>"')
    chapters = collect_chapters(os.sys.argv[1])
    if not chapters:
        raise SystemExit('Не найдено глав в config/ftbquests/quests/chapters —'
                         ' проверь путь к инстансу.')
    write_chapters(chapters)
    update_meta(chapters)
    total = sum(entry['quests'] for _n, entry, _q in chapters)
    print('Глав: %d; квестов: %d (было: см. старый meta.json до перезаписи)'
          % (len(chapters), total))
    print('Описания квестов сохранены в поле desc каждой строки.')


if __name__ == '__main__':
    main()
