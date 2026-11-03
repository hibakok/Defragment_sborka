"""Примитивы работы с файлами. Каждый метод — кирпичик (см. ../METHODS.md)."""

import os


def read_text(path):
    """Вход: путь. Выход: текст. Прочитать текстовый файл целиком."""
    with open(path, 'r', encoding='utf-8') as handle:
        return handle.read()


def write_text(path, text):
    """Вход: путь, текст. Выход: путь. Записать текст (перезапись)."""
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


def ensure_dir(path):
    """Вход: путь. Выход: путь. Создать директорию, если её нет."""
    os.makedirs(path, exist_ok=True)
    return path


def list_files(folder, suffix=''):
    """Вход: папка, суффикс. Выход: список имён. Только файлы подпапки."""
    names = []
    for name in sorted(os.listdir(folder)):
        full = os.path.join(folder, name)
        if os.path.isfile(full) and name.endswith(suffix):
            names.append(name)
    return names