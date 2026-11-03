"""Загрузка квестов из data/chapters (см. ../METHODS.md).

Ветка кода: chapter_index / load_chapter используют примитивы core/jsonio.py;
load_all_quests собирает все главы в один плоский список с полем chapter.
"""

import os

from core.jsonio import load_jsonl

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
CHAPTERS_DIR = os.path.join(_ROOT, 'data', 'chapters')


def chapter_index():
    """Вход: —. Выход: список записей _index.jsonl (реестр глав)."""
    return load_jsonl(os.path.join(CHAPTERS_DIR, '_index.jsonl'))


def chapter_names():
    """Вход: —. Выход: имена глав (без .jsonl), кроме _index."""
    names = []
    for entry in chapter_index():
        names.append(entry['file'][:-6])
    return names


def chapter_path(name):
    """Вход: имя главы. Выход: полный путь к её jsonl-файлу."""
    return os.path.join(CHAPTERS_DIR, name + '.jsonl')


def load_chapter(name):
    """Вход: имя главы. Выход: квесты главы, каждому добавлен chapter."""
    quests = load_jsonl(chapter_path(name))
    for quest in quests:
        quest['chapter'] = name
    return quests


def load_all():
    """Вход: —. Выход: все квесты всех глав одним списком."""
    quests = []
    for name in chapter_names():
        quests.extend(load_chapter(name))
    return quests


def quest_map(quests):
    """Вход: список квестов. Выход: словарь {id: квест}."""
    return {quest['id']: quest for quest in quests}
