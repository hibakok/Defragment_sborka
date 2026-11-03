"""Пайплайн: аудит предметов → data/items_stats.jsonl + отчёт.

Запуск из tools/:
  python -m pipeline.items_audit
Считает предметы по модам (items.jsonl), проверяет покрытие целей
квестов (demand.jsonl) и выдаёт отчёт для цели «все предметы».
"""

from collections import Counter

from core.jsonio import load_jsonl, save_jsonl

_TOOLS = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
_ROOT = __import__('os').path.abspath(__import__('os').path.join(_TOOLS, '..', '..'))
ITEMS_PATH = __import__('os').path.join(_ROOT, 'data', 'items.jsonl')
DEMAND_PATH = __import__('os').path.join(_ROOT, 'data', 'demand.jsonl')
STATS_PATH = __import__('os').path.join(_ROOT, 'data', 'items_stats.jsonl')


def item_rows():
    """Вход: —. Выход: строки items.jsonl."""
    return load_jsonl(ITEMS_PATH)


def per_mod(rows):
    """Вход: строки предметов. Выход: Counter modid → число записей."""
    return Counter(row['modid'] for row in rows)


def demand_targets():
    """Вход: —. Выход: список предметных целей demand.jsonl."""
    return [row['target'] for row in load_jsonl(DEMAND_PATH)
            if row['type'] == 'item']


def modids_of(rows):
    """Вход: строки предметов. Выход: множество modid."""
    return {row['modid'] for row in rows}


def split_target(target):
    """Вход: цель вида mod:item или mod:item{...}. Выход: (modid, item)."""
    body = target.split('{')[0].split('[')
    head = body[0]
    if ':' in head:
        return head.split(':', 1)
    return 'minecraft', head


def covered(targets, mods):
    """Вход: цели, множество modid. Выход: (покрытые, пропавшие)."""
    ok, miss = [], []
    for target in targets:
        modid, _item = split_target(target)
        (ok if modid in mods else miss).append(target)
    return ok, miss


def update_meta(items, namespaces):
    """Вход: счётчики. Выход: —. Дополнить meta.json слоем данных."""
    meta_path = __import__('os').path.join(_ROOT, 'data', 'meta.json')
    meta = __import__('json').load(open(meta_path, encoding='utf-8'))
    meta['items'] = items
    meta['item_namespaces'] = namespaces
    meta['data_layer_date'] = __import__('datetime').date.today().isoformat()
    open(meta_path, 'w', encoding='utf-8', newline='\n').write(
        __import__('json').dumps(meta, indent=1, ensure_ascii=False) + '\n')


def main():
    """Склейка: данные → счётчики → items_stats.jsonl + meta + отчёт."""
    rows = item_rows()
    counts = per_mod(rows)
    mods = set(counts)
    stats = [{'modid': modid, 'items': counts[modid]}
             for modid in sorted(counts, key=counts.get, reverse=True)]
    save_jsonl(STATS_PATH, stats)
    update_meta(len(rows), len(mods))
    targets = demand_targets()
    ok, miss = covered(targets, mods)
    print('предметов/блоков в items.jsonl: %d (%d модов-пространств имён)'
          % (len(rows), len(mods)))
    print('целей-предметов в demand.jsonl: %d; покрытие modid: %d (%.1f%%)'
          % (len(targets), len(ok), 100.0 * len(ok) / max(1, len(targets))))
    if miss:
        print('цели с модом, которого нет в items.jsonl (проверить в игре):')
        for target in miss[:20]:
            print('  ', target)
    print('топ-10 модов по числу предметов:')
    for row in stats[:10]:
        print('  %-22s %5d' % (row['modid'], row['items']))


if __name__ == '__main__':
    main()
