"""Кирпичики предметов: lang-ключ → id предмета.

Источник: data/items.jsonl (26 500 строк из lang-файлов модов).
Фильтр is_item_key отделяет настоящие предметы/блоки от тултипов,
описаний, зелье-вариантов и мусорных ключей без modid. Путь с точкой
легален только для everycomp (реальные id с '/', см. WoodGood#759)
и для id, подтверждённых рецептами/квестами (toms_storage:ts.*).
"""

import glob
import os
import re

try:  # запуск из tools/ как модуль
    from core.files import read_text
    from core.jsonio import load_jsonl
except ImportError:  # запуск файла напрямую
    from files import read_text
    from jsonio import load_jsonl

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
ITEMS_PATH = os.path.join(_ROOT, 'data', 'items.jsonl')
MODS_PATH = os.path.join(_ROOT, 'data', 'mods.jsonl')

_BAD_TAILS = ('tooltip', 'desc', 'info', 'details', 'name')
_JUNK_PREFIX = ('tooltip', 'behaviour', 'condition', 'desc')
_JUNK_EXACT = {'summary', 'text', 'mode', 'info', 'details'}


def _bad_segment(seg):
    """Вход: сегмент пути ключа (после modid). Выход: bool. Мусорный
    сегмент тултипов/описаний: tooltip, behaviour1, condition2, summary,
    цифра-номер строки и т.п."""
    low = seg.lower()
    if low.isdigit() or low in _JUNK_EXACT:
        return True
    return low.startswith(_JUNK_PREFIX)


def is_item_key(key):
    """Вход: lang-ключ. Выход: bool. Ключ настоящего предмета/блока?
    Отбрасываются: тултипы (.tooltip*), описания (.desc/.info), хвост
    .name, зелье-варианты (.effect.), ключи без modid (item.canBreak)
    и тултипные вставки (.tooltip.behaviour1, .text.0)."""
    parts = key.split('.')
    if parts[0] not in ('item', 'block') or len(parts) < 3:
        return False
    if '.effect.' in key:
        return False
    tail = parts[-1].lower()
    if tail.startswith('tooltip') or tail in _BAD_TAILS:
        return False
    return not any(_bad_segment(seg) for seg in parts[2:])


def key_to_id(key):
    """Вход: lang-ключ. Выход: 'modid:path' или None.
    Пример: item.ae2things.disk_drive_16k → ae2things:disk_drive_16k."""
    if not is_item_key(key):
        return None
    parts = key.split('.')
    return parts[1] + ':' + '.'.join(parts[2:])


def row_id(row):
    """Вход: строка items.jsonl {modid, key, name}. Выход: id или None.
    Дополнительно к is_item_key: modid внутри ключа должен совпадать с
    modid источника — отсекает звуковые субтитры и чужие ключи."""
    parts = row['key'].split('.')
    if len(parts) < 3 or parts[1] != row['modid']:
        return None
    if not is_item_key(row['key']):
        return None
    path = '.'.join(parts[2:])
    if '.' in path:
        return _dotted_id(row['modid'], path)
    return row['modid'] + ':' + path


_REF_ITEM = re.compile(r'"(?:item|fluid)":\s*"([\w.]+:[\w./]+)"')
_REF_TASK = re.compile(r'\b(?:ITEM|FLUID) ([\w.]+:[\w./]+)')
_REFS = None


def known_refs():
    """Вход: —. Выход: {id} — предметные ссылки из рецептов и квестов
    (авторитет для легализации редких id с точкой в пути). Кэш."""
    global _REFS
    if _REFS is None:
        _REFS = _scan_refs()
    return _REFS


def _scan_refs():
    """Вход: —. Выход: {id}. Сканирует data/recipes и data/chapters
    регэкспами по двум форматам: JSON-поля и строки задач FTBQ."""
    refs = set()
    for pattern in (os.path.join(_ROOT, 'data', 'recipes', '*.jsonl'),
                    os.path.join(_ROOT, 'data', 'chapters', '*.jsonl')):
        for path in glob.glob(pattern):
            text = read_text(path)
            refs.update(_REF_ITEM.findall(text))
            refs.update(_REF_TASK.findall(text))
    return refs


def _dotted_id(modid, path):
    """Вход: modid, путь с точкой. Выход: id или None. Точка в пути —
    почти всегда тултип/вариант (banner.base.black, biome_map.badlands).
    Легальны: everycomp (id с '/', WoodGood#759) и ссылки из рецептов."""
    if modid == 'everycomp':
        return modid + ':' + path.replace('.', '/')
    candidate = modid + ':' + path
    return candidate if candidate in known_refs() else None


def mod_of(item_id):
    """Вход: 'modid:path'. Выход: modid (часть до двоеточия)."""
    return item_id.split(':', 1)[0]


def load_items():
    """Вход: —. Выход: [{id, name, modid}] — настоящие предметы без
    дубликатов id (побеждает первое имя; item./block. коллизии склеены)."""
    seen = {}
    for row in load_jsonl(ITEMS_PATH):
        item_id = row_id(row)
        if item_id and item_id not in seen:
            seen[item_id] = {'id': item_id, 'name': row['name'],
                             'modid': mod_of(item_id)}
    return list(seen.values())


def by_mod(items=None):
    """Вход: список load_items (None → загрузить). Выход: {modid:
    [строки предметов]}, внутри каждого мода сортировка по id."""
    if items is None:
        items = load_items()
    table = {}
    for row in items:
        table.setdefault(row['modid'], []).append(row)
    for modid in table:
        table[modid].sort(key=lambda row: row['id'])
    return table


def mod_names():
    """Вход: —. Выход: {modid: человекочитаемое имя мода} из mods.jsonl."""
    names = {}
    for row in load_jsonl(MODS_PATH):
        names[row['modid']] = row['name']
    return names
