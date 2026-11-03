"""Экстрактор: рецепты из jar-модов → data/recipes/<modid>.jsonl.

Запуск из tools/:
  python -m extract.recipes_from_mods "<путь к папке mods>" <modid> [modid...]
Без modid — только create. Рецепты Create (mixing, crushing, ...) лежат
в data/create/recipes/**.json внутри jar. Это основа планирования фабрик.
"""

import json
import os
import zipfile

from core.jsonio import save_jsonl
from core.files import ensure_dir

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
RECIPES_DIR = ensure_dir(os.path.join(_ROOT, 'data', 'recipes'))


def recipe_members(archive, modid):
    """Вход: ZipFile, modid. Выход: [(путь, тип)] рецептов мода."""
    prefix = 'data/%s/recipes/' % modid
    found = []
    for name in archive.namelist():
        if name.startswith(prefix) and name.endswith('.json'):
            found.append((name, None))
    return found


def load_recipe(archive, member):
    """Вход: ZipFile, имя записи. Выход: (json, тип) или (None, None)."""
    try:
        parsed = json.loads(archive.read(member).decode('utf-8', 'replace'))
    except (ValueError, KeyError):
        return None, None
    return parsed, parsed.get('type', '')


def scan_jar(jar_path, modid):
    """Вход: путь к jar, modid. Выход: [{file, type, json}] или []."""
    rows = []
    try:
        with zipfile.ZipFile(jar_path) as archive:
            for member, _kind in recipe_members(archive, modid):
                parsed, kind = load_recipe(archive, member)
                if parsed is not None:
                    rows.append({'file': member, 'type': kind, 'json': parsed})
    except (zipfile.BadZipFile, OSError):
        return []
    return rows


def scan_folder(mods_dir, modid):
    """Вход: папка mods, modid. Выход: строки рецептов по всем jar."""
    rows = []
    for name in sorted(os.listdir(mods_dir)):
        if name.endswith('.jar'):
            rows.extend(scan_jar(os.path.join(mods_dir, name), modid))
    return rows


def main():
    """Склейка: аргументы → скан по каждому modid → файл в data/recipes/."""
    argv = os.sys.argv
    if len(argv) < 2:
        raise SystemExit('Использование: python -m extract.recipes_from_mods '
                         '"<путь к папке mods>" [modid ...]')
    mods_dir = argv[1]
    modids = argv[2:] or ['create']
    for modid in modids:
        rows = scan_folder(mods_dir, modid)
        out = os.path.join(RECIPES_DIR, modid + '.jsonl')
        save_jsonl(out, rows)
        print('recipes/%s.jsonl: %d рецептов' % (modid, len(rows)))


if __name__ == '__main__':
    main()
