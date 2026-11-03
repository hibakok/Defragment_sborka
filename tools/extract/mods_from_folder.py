"""Экстрактор: папка mods инстанса → data/mods.jsonl.

Запуск из tools/:
  python -m extract.mods_from_folder "<путь к папке mods>"
Читает META-INF/mods.toml из каждого .jar (Forge 1.20.1).
"""

import os
import re
import zipfile

from core.jsonio import save_jsonl

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
OUT_PATH = os.path.join(_ROOT, 'data', 'mods.jsonl')

_FIELD = re.compile(r'^[ \t]*(modId|displayName|version)\s*=\s*"(.*)"',
                    re.MULTILINE)


def jar_files(mods_dir):
    """Вход: папка mods. Выход: отсортированный список имён .jar."""
    return [name for name in sorted(os.listdir(mods_dir))
            if name.endswith('.jar')]


def read_member(jar_path, member):
    """Вход: путь к jar, имя записи. Выход: текст записи или None."""
    try:
        with zipfile.ZipFile(jar_path) as archive:
            return archive.read(member).decode('utf-8', 'replace')
    except (KeyError, zipfile.BadZipFile, OSError):
        return None


def parse_mods_toml(text):
    """Вход: текст mods.toml. Выход: [{modid, name, version}] — все
    секции [[mods]]. Секция обрезается на [[dependencies: поля
    зависимостей (modId="forge" и пр.) не затирают поля самого мода."""
    mods = []
    for block in text.split('[[mods]]')[1:]:
        own = block.split('[[dependencies')[0]
        fields = dict(_FIELD.findall(own))
        mods.append({
            'modid': fields.get('modId', ''),
            'name': fields.get('displayName', ''),
            'version': fields.get('version', ''),
        })
    return mods


def scan_jar(jar_path):
    """Вход: путь к jar. Выход: [{file, modid, name, version}] или []."""
    text = read_member(jar_path, 'META-INF/mods.toml')
    if text is None:
        text = read_member(jar_path, 'META-INF/mods.cfg')
    if text is None:
        return []
    rows = []
    for mod in parse_mods_toml(text):
        mod['file'] = os.path.basename(jar_path)
        rows.append(mod)
    return rows


def scan_folder(mods_dir):
    """Вход: папка mods. Выход: все строки по всем jar (+ пропуски)."""
    rows, skipped = [], []
    for name in jar_files(mods_dir):
        found = scan_jar(os.path.join(mods_dir, name))
        if found:
            rows.extend(found)
        else:
            skipped.append(name)
    return rows, skipped


def main():
    """Склейка: аргумент → скан → data/mods.jsonl → отчёт."""
    if len(os.sys.argv) < 2:
        raise SystemExit('Использование: python -m extract.mods_from_folder '
                         '"<путь к папке mods>"')
    rows, skipped = scan_folder(os.sys.argv[1])
    save_jsonl(OUT_PATH, rows)
    print('mods.jsonl: %d модов из %d jar (пропущено jar: %d)'
          % (len(rows), len(jar_files(os.sys.argv[1])), len(skipped)))
    if skipped:
        print('Пропущены (нет mods.toml): %s' % ', '.join(skipped[:10]))


if __name__ == '__main__':
    main()
