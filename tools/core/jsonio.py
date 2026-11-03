"""Примитивы JSON и JSONL. Каждый метод — кирпичик (см. ../METHODS.md)."""

import json
import re

try:  # запуск из tools/ как модуль
    from core.files import read_text, write_text
except ImportError:  # запуск файла напрямую
    from files import read_text, write_text

_COMMENT = re.compile(r'(?<!:)//.*$', re.MULTILINE)
_TAIL_COMMA = re.compile(r',\s*([}\]])')


def tolerant_json(text):
    """Вход: текст. Выход: объект или None. JSON, прощающий // и
    висячие запятые (такие lang-файлы встречаются у модов)."""
    try:
        return json.loads(text)
    except ValueError:
        cleaned = _TAIL_COMMA.sub(r'\1', _COMMENT.sub('', text))
        try:
            return json.loads(cleaned)
        except ValueError:
            return None


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
