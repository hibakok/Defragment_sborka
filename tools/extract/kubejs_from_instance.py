"""Экстрактор: скрипты KubeJS инстанса → data/kubejs/ (+ реестр _files.jsonl).

Запуск из tools/:
  python -m extract.kubejs_from_instance "<путь к папке инстанса>"
Кастомные рецепты сборки (гейтинг-машины kubejs:*) живут в kubejs/.
Копируется только ПОЛЕЗНОЕ (useful_rel), иначе 500+ файлов мусора
(текстуры, модели, worldgen) забьют репозиторий:
  server_scripts/** и startup_scripts/** и client_scripts/** (.js)
  assets/*/lang/*.json (имена кастомных предметов)
  data/**/recipes/*.json и data/chronicles/** (кастомные рецепты/данные)
"""

import os

from core.files import ensure_dir, ensure_parent, read_text, write_text
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


def useful_rel(rel):
    """Вход: относительный путь. Выход: bool. Полезен ли файл для плана."""
    rel = rel.replace(os.sep, '/')
    parts = rel.split('/')
    if len(parts) < 2:
        return False
    if parts[0] in ('server_scripts', 'startup_scripts', 'client_scripts'):
        return rel.endswith('.js')
    if parts[0] == 'assets':
        return (len(parts) == 4 and parts[2] == 'lang'
                and rel.endswith('.json'))
    if parts[0] == 'data':
        if parts[1] == 'chronicles':
            return rel.endswith('.json')
        return 'recipes' in parts and rel.endswith('.json')
    return False


def copy_one(rel, full):
    """Вход: пути. Выход: строка реестра. Прочитать и скопировать в data."""
    text = read_text(full)
    out = os.path.join(KUBEJS_OUT, rel.replace(os.sep, '/'))
    ensure_parent(out)
    write_text(out, text)
    return {'path': rel.replace(os.sep, '/'), 'lines': text.count('\n') + 1}


def main():
    """Склейка: аргумент → фильтр → копия → data/kubejs/ + _files.jsonl."""
    if len(os.sys.argv) < 2:
        raise SystemExit('Использование: python -m extract.kubejs_from_instance'
                         ' "<путь к папке инстанса>"')
    files = [pair for pair in kubejs_files(os.sys.argv[1])
             if useful_rel(pair[0])]
    rows = [copy_one(rel, full) for rel, full in files]
    save_jsonl(os.path.join(KUBEJS_OUT, '_files.jsonl'), rows)
    print('kubejs: скопировано %d полезных файлов в data/kubejs/' % len(rows))


if __name__ == '__main__':
    main()
