"""Примитивы JSON и JSONL. Каждый метод — кирпичик (см. ../METHODS.md)."""

import json

try:  # запуск из tools/ как модуль
    from core.files import read_text, write_text
except ImportError:  # запуск файла напрямую
    from files import read_text, write_text


def load_json(path):
    """Вход: путь. Выход: объект Python. Прочитать JSON."""
    return json.loads(read_text(path))


def save_json(path, obj):
    """Вход: путь, объект. Выход: путь. Записать JSON с отступами."""
    write_text(path, json.dumps(obj, indent=1, ensure_ascii=False))
    return path


def load_jsonl(path):
    """Вход: путь. Выход: список объектов. 1 строка файла = 1 объект."""
    rows = []
    for line in read_text(path).splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def save_jsonl(path, rows):
    """Вход: путь, список объектов. Выход: путь. 1 объект = 1 строка."""
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    write_text(path, '\n'.join(lines) + '\n')
    return path