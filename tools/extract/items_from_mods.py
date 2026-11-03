"""Экстрактор: предметы из jar-модов → data/items.jsonl.

Запуск из tools/:
  python -m extract.items_from_mods "<путь к папке mods>"
Читает assets/<modid>/lang/en_us.json каждого jar: ключи item.* и block.*
дают полный список предметов/блоков для цели «все предметы хотя бы по разу».
"""

import json
import os
import re
import zipfile

from core.jsonio import save_jsonl

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
OUT_PATH = os.path.join(_ROOT, 'data', 'items.jsonl')

_LANG = re.compile(r'^assets/([a-z0-9_]+)/lang/en_us\.json$')


def lang_members(archive):
    """Вход: открытый ZipFile. Выход: [(modid, имя записи)] для en_us.json."""
    found = []
    for name in archive.namelist():
        match = _LANG.match(name)
        if match:
            found.append((match.group(1), name))
    return found


def item_keys(table):
    """Вход: словарь lang. Выход: [(ключ, имя)] только item.* и block.*."""
    pairs = []
    for key, value in sorted(table.items()):
        if key.startswith('item.') or key.startswith('block.'):
            pairs.append((key, value))
    return pairs


def scan_jar(jar_path):
    """Вход: путь к jar. Выход: [{modid, key, name}] или [] при ошибке."""
    rows = []
    try:
        with zipfile.ZipFile(jar_path) as archive:
            for modid, member in lang_members(archive):
                table = json.loads(archive.read(member).decode('utf-8',
                                                                'replace'))
                for key, name in item_keys(table):
                    rows.append({'modid': modid, 'key': key, 'name': name})
    except (zipfile.BadZipFile, OSError, ValueError):
        return []
    return rows


def scan_folder(mods_dir):
    """Вход: папка mods. Выход: (все строки, число обработанных jar)."""
    rows, jars = [], 0
    for name in sorted(os.listdir(mods_dir)):
        if not name.endswith('.jar'):
            continue
        jars += 1
        rows.extend(scan_jar(os.path.join(mods_dir, name)))
    return rows, jars


def main():
    """Склейка: аргумент → скан → data/items.jsonl → отчёт."""
    if len(os.sys.argv) < 2:
        raise SystemExit('Использование: python -m extract.items_from_mods '
                         '"<путь к папке mods>"')
    rows, jars = scan_folder(os.sys.argv[1])
    save_jsonl(OUT_PATH, rows)
    print('items.jsonl: %d записей item./block. из %d jar' % (len(rows), jars))


if __name__ == '__main__':
    main()
