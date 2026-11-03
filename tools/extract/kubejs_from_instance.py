"""Экстрактор: скрипты KubeJS инстанса → data/kubejs/ (+ реестр _files.jsonl).

Запуск из tools/:
  python -m extract.kubejs_from_instance "<путь к папке инстанса>"
Кастомные рецепты сборки (гейтинг-машины kubejs:*) живут в kubejs/.
Это следующий шаг данных после квестов: точные рецепты кастомных предметов.
"""

import os

from core.files import ensure_dir, read_text, write_text
from core.jsonio import save_jsonl

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
KUBEJS_OUT = ensure_dir(os.path.join(_ROOT, 'data', 'kubejs'))
_EXT = ('.js', '.json')


def kubejs_files(instance_dir):
    """Вход: папка инстанса. Выход: [(относительный путь, полный путь)]."""
    source = os.path.join(instance_dir, 'kubejs')
    found = []
    for folder, _dirs, names in os.walk(source):
        for name in sorted(names):
            if name.endswith(_EXT):
                full = os.path.join(folder, name)
                found.append((os.path.relpath(full, source), full))
    return sorted(found)


def copy_one(rel, full):
    """Вход: пути. Выход: (строки, байты). Прочитать и скопировать в data."""
    text = read_text(full)
    write_text(os.path.join(KUBEJS_OUT, rel.replace(os.sep, '/')), text)
    return {'path': rel.replace(os.sep, '/'), 'lines': text.count('\n') + 1}


def main():
    """Склейка: аргумент → копия kubejs → data/kubejs/ + _files.jsonl."""
    if len(os.sys.argv) < 2:
        raise SystemExit('Использование: python -m extract.kubejs_from_instance'
                         ' "<путь к папке инстанса>"')
    files = kubejs_files(os.sys.argv[1])
    rows = [copy_one(rel, full) for rel, full in files]
    save_jsonl(os.path.join(KUBEJS_OUT, '_files.jsonl'), rows)
    print('kubejs: скопировано %d файлов (.js/.json) в data/kubejs/'
          % len(rows))


if __name__ == '__main__':
    main()
