"""Разбор строк задач квестов и титулов (см. ../METHODS.md).

Ветка кода: parse_task — один кирпичик (регулярка + split);
clean_title и task_text используют только parse-результаты.
"""

import re

_COUNT = re.compile(r'\sx(\d+)$')
_COLOR = re.compile(r'[&§][0-9a-fk-orA-FK-OR]')

_KINDS = {
    'item': 'сдать',
    'kill': 'убить',
    'fluid': 'сдать жидкость',
    'adv': 'достижение',
    'struct': 'найти структуру',
    'biome': 'побывать в биоме',
    'dim': 'побывать в измерении',
    'observe': 'наблюдение',
    'check': 'отметить вручную',
}


def parse_task(text):
    """Вход: строка задачи ('ITEM create:shaft x3'). Выход: dict
    {type, target, count}. Типы (как в данных): item/check/kill/adv/
    dim/struct/biome/observe/fluid."""
    count = 1
    match = _COUNT.search(text)
    if match:
        count = int(match.group(1))
        text = text[:match.start()]
    parts = text.split(' ', 1)
    kind = parts[0].lower()
    target = parts[1] if len(parts) > 1 else ''
    return {'type': kind, 'target': target, 'count': count}


def parse_tasks(quest):
    """Вход: квест (dict с полем tasks). Выход: список разобранных задач."""
    return [parse_task(text) for text in quest.get('tasks', [])]


def clean_title(title):
    """Вход: титул с кодами цветов (&9, §c...). Выход: чистый текст."""
    return _COLOR.sub('', title or '').strip()


def display_title(quest):
    """Вход: квест. Выход: титул для показа (пусто → первый таргет)."""
    title = clean_title(quest.get('title', ''))
    if title:
        return title
    parsed = parse_tasks(quest)
    if parsed:
        target = parsed[0]['target']
        if target.startswith('any of'):
            return '(%s)' % any_of_summary(target)
        return '(%s)' % target
    return '(без задач)'


def any_of_summary(target):
    """Вход: строка 'any of [a, b, c]'. Выход: 'a / b (+ещё N)'.
    Устойчива к отсутствию скобок и вложенным 'any of'."""
    body = target
    if '[' in body:
        body = body[body.find('[') + 1:]
    if ']' in body:
        body = body[:body.rfind(']')]
    items = [item.strip() for item in body.split(',')
             if item.strip() and 'any of' not in item]
    if not items:
        return 'любой из (список в игре)'
    head = ' / '.join(items[:2])
    rest = len(items) - 2
    if rest > 0:
        head += ' (+ещё %d)' % rest
    return 'любой из: ' + head


def task_text(task):
    """Вход: разобранная задача (dict). Выход: человекочитаемая строка."""
    kind = _KINDS.get(task['type'], task['type'])
    if task['type'] == 'check':
        return kind
    target = task['target']
    if target.startswith('any of'):
        return '%s: %s ×%d' % (kind, any_of_summary(target), task['count'])
    if target.startswith('any@mod:'):
        return '%s: любой предмет мода %s ×%d' % (
            kind, target[len('any@mod:'):], task['count'])
    return '%s: %s ×%d' % (kind, target, task['count'])
