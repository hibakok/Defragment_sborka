"""Загрузка всех рецептов сборки в единой схеме.

Источники: data/recipes/<modid>.jsonl (33 мода, ~10 600 рецептов) и
data/kubejs/data/**/recipes/*.json (кастомные рецепты сборки).
Выход каждой записи: {source, file, type, json}.
"""

import glob
import os

try:  # запуск из tools/ как модуль
    from core.files import read_text
    from core.jsonio import load_jsonl, tolerant_json
except ImportError:  # запуск файла напрямую
    from files import read_text
    from jsonio import load_jsonl, tolerant_json

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
RECIPES_DIR = os.path.join(_ROOT, 'data', 'recipes')
KUBEJS_DATA = os.path.join(_ROOT, 'data', 'kubejs', 'data')


def recipe_rows():
    """Вход: —. Выход: строки рецептов из data/recipes/*.jsonl,
    каждая дополнена полем source (modid из имени файла)."""
    rows = []
    for path in sorted(glob.glob(os.path.join(RECIPES_DIR, '*.jsonl'))):
        source = os.path.basename(path)[:-6]
        for row in load_jsonl(path):
            row['source'] = source
            rows.append(row)
    return rows


def kubejs_paths():
    """Вход: —. Выход: отсортированные пути recipe-json из data/kubejs."""
    pattern = os.path.join(KUBEJS_DATA, '**', 'recipes', '**', '*.json')
    return sorted(glob.glob(pattern, recursive=True))


def kubejs_rows():
    """Вход: —. Выход: строки рецептов KubeJS (source='kubejs').
    Файлы без поля type (не рецепты) пропускаются."""
    rows = []
    root_len = len(_ROOT) + 1
    for path in kubejs_paths():
        data = tolerant_json(read_text(path))
        if not data or 'type' not in data:
            continue
        rows.append({'source': 'kubejs', 'file': path[root_len:],
                     'type': data['type'], 'json': data})
    return rows


def load_all():
    """Вход: —. Выход: ВСЕ рецепты сборки (моды + KubeJS) одним списком."""
    return recipe_rows() + kubejs_rows()
