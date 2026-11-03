"""Пайплайн: классификация производства всех предметов.

Запуск из tools/:  python -m pipeline.production_all
Выходы:
  data/production.jsonl — {id, name, modid, marker, ways, machines}
    marker: к — рецепт в данных, в — ваниль (JEI), н — лут/дроп;
  analysis/production_map.md — карта: покрытие крафта по модам;
  консоль — сводка (сколько крафтимых, топ машин).
"""

import glob
import os

from core.files import write_text, ensure_dir
from core.jsonio import load_json, save_json, save_jsonl
from items import ids
from museum.render import marker_of
from recipes.load import load_all
from recipes.index import craftable_set, machines_of, produce_index, ways_of

_TOOLS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_TOOLS, '..', '..'))
PRODUCTION_PATH = os.path.join(_ROOT, 'data', 'production.jsonl')
MAP_PATH = os.path.join(_ROOT, 'analysis', 'production_map.md')
META_PATH = os.path.join(_ROOT, 'data', 'meta.json')


def update_meta(rows):
    """Вход: строки classify_rows. Выход: —. Дополняет data/meta.json
    слоем музея: чистые предметы (после фильтра) и файлы plan/museum."""
    meta = load_json(META_PATH)
    meta['museum_items'] = len(rows)
    meta['museum_files'] = len(glob.glob(os.path.join(
        _ROOT, 'plan', 'museum', '*.md')))
    meta['production_layer_date'] = '2026-11-03'
    save_json(META_PATH, meta)


def classify_rows(index):
    """Вход: индекс производства. Выход: строки data/production.jsonl
    для каждого предмета из items.jsonl."""
    rows = []
    for row in ids.load_items():
        rows.append({'id': row['id'], 'name': row['name'],
                     'modid': row['modid'],
                     'marker': marker_of(row['id'], craftable_set(index)),
                     'ways': ways_of(index, row['id']),
                     'machines': machines_of(index, row['id'])})
    return rows


def _mod_summary(rows):
    """Вход: строки classify_rows. Выход: {modid: (всего, к, в, н)}."""
    table = {}
    for row in rows:
        stats = table.setdefault(row['modid'], [0, 0, 0, 0])
        slot = {'к': 1, 'в': 2, 'н': 3}[row['marker']]
        stats[0] += 1
        stats[slot] += 1
    return table


def map_lines(rows, index):
    """Вход: строки classify_rows, индекс. Выход: строки Markdown
    карты производства (analysis/production_map.md)."""
    lines = ['# Карта производства предметов', '',
             'Источник: data/production.jsonl (сгенерирован '
             'pipeline.production_all). Рецепты: data/recipes/*.jsonl '
             '(33 мода, 10 647) + data/kubejs/data (35 recipe-json).', '',
             'Маркеры: к — рецепт в данных (фабрика возможна); '
             'в — ванильный minecraft (рецепт в клиенте, JEI); '
             'н — нет рецепта в данных: лут, дроп мобов, данжи, '
             'торговля или мод вне выборки извлечения.', '',
             'ВАЖНО: «н» не значит «некрафтимо»: рецепты части модов '
             '(simplyswords, quark, chipped частично и др.) не '
             'извлекались — проверить в JEI (клавиша R).', '',
             '| Мод | Всего | к | в | н | Покрытие |', '| --- | --- | --- | --- | --- | --- |']
    for modid, stats in sorted(_mod_summary(rows).items(),
                               key=lambda pair: -pair[1][0]):
        share = 100 * stats[1] // stats[0] if stats[0] else 0
        lines.append('| %s | %d | %d | %d | %d | %d%% |' % (
            modid, stats[0], stats[1], stats[2], stats[3], share))
    craftable = sum(1 for row in rows if row['marker'] == 'к')
    lines.extend(['', 'Итого предметов: %d; крафтимых по данным: %d '
                 '(%.1f%%); рецептных ссылок в индексе: %d.' % (
                     len(rows), craftable, 100.0 * craftable / len(rows),
                     len(index))])
    return lines


def main():
    """Склейка: индекс → production.jsonl + production_map.md + отчёт."""
    index = produce_index(load_all())
    rows = classify_rows(index)
    save_jsonl(PRODUCTION_PATH, rows)
    ensure_dir(os.path.dirname(MAP_PATH))
    write_text(MAP_PATH, '\n'.join(map_lines(rows, index)) + '\n')
    update_meta(rows)
    craftable = sum(1 for row in rows if row['marker'] == 'к')
    print('production.jsonl: %d предметов; крафтимых к=%d, '
          'ваниль в=%d, вне данных н=%d' % (
              len(rows), craftable,
              sum(1 for row in rows if row['marker'] == 'в'),
              sum(1 for row in rows if row['marker'] == 'н')))
    print('Карта: analysis/production_map.md')


if __name__ == '__main__':
    main()
