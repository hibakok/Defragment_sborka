"""Самотест инфраструктуры: парсер, данные, граф, маршрут, экстракторы.

Запуск из tools/:  python -m tests.selftest
Выход: список проверок OK/FAIL и итог. Код возврата 1 при любом FAIL.
Экстракторы проверяются на синтетическом jar (создаётся во временной папке).
"""

import json
import os
import tempfile
import zipfile

from snbt.parser import parse_snbt
from core.jsonio import load_jsonl, save_jsonl
from quests import load
from quests.tasks import clean_title, parse_task
from plan import route

_CHECKS = []


def check(name):
    """Декоратор: регистрирует проверку в _CHECKS."""
    def wrap(func):
        _CHECKS.append((name, func))
        return func
    return wrap


@check('SNBT: объекты, массивы, типизированные массивы')
def snbt_structures():
    value = parse_snbt('{ a: [1 2 3], b: [I; 4 5], c: [B; 1B] }')
    assert value['a'] == [1, 2, 3] and value['b'] == [4, 5]
    assert value['c'] == [1]


@check('SNBT: числа с суффиксами NBT')
def snbt_numbers():
    value = parse_snbt('{ b: 1B, d: 2.5d, l: 100L, n: 1_000, f: .5 }')
    assert value['b'] == 1 and value['d'] == 2.5 and value['l'] == 100
    assert value['n'] == 1000 and value['f'] == 0.5


@check('SNBT: строки, экранирование, слова, комментарии')
def snbt_strings():
    value = parse_snbt('{ s: "a\\"b", t: true, f: false, w: bare } // хвост')
    assert value['s'] == 'a"b' and value['t'] is True
    assert value['f'] is False and value['w'] == 'bare'


@check('JSONL: запись и чтение дают одинаковые данные')
def jsonl_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'x.jsonl')
        rows = [{'a': 1}, {'b': 'ж'}]
        save_jsonl(path, rows)
        assert load_jsonl(path) == rows


@check('ДАННЫЕ: количество квестов сходится с meta.json')
def data_total():
    meta = json.load(open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..',
        'data', 'meta.json'), encoding='utf-8'))
    quests = load.load_all()
    assert len(quests) == meta['total_quests'] == 1827


@check('ДАННЫЕ: id уникальны, все deps существуют')
def data_integrity():
    quests = load.load_all()
    ids = {quest['id'] for quest in quests}
    assert len(ids) == len(quests)
    for quest in quests:
        for dep in quest.get('deps', []):
            assert dep in ids, dep


@check('ЗАДАЧИ: разбор строк ITEM/KILL/FLUID/CHECK/ADV/DIM')
def tasks_parse():
    task = parse_task('ITEM minecraft:crafting_table x1')
    assert task == {'type': 'item', 'target': 'minecraft:crafting_table',
                    'count': 1}
    assert parse_task('KILL cataclysm:x x2')['type'] == 'kill'
    assert parse_task('FLUID ad_astra:cryo_fuel x100000')['count'] == 100000
    assert parse_task('CHECK')['type'] == 'check'
    assert parse_task('ADV minecraft:story/root')['type'] == 'adv'
    assert parse_task('DIM minecraft:the_nether')['type'] == 'dim'


@check('ТИТУЛЫ: коды цветов убираются')
def titles_clean():
    assert clean_title('&9Welcome!') == 'Welcome!'
    assert clean_title('&2Overworld&f: текст') == 'Overworld: текст'


@check('МАРШРУТ: 31 глава, все ровно один раз, без лишних')
def route_complete():
    names = load.chapter_names()
    planned = [chapter for chapter, _stage in route.ROUTE]
    assert sorted(names) == sorted(planned)
    assert len(planned) == len(set(planned)) == 31


@check('ГРАФ: глубины посчитаны для всех, порядок топологический')
def graph_order():
    from quests import graph
    from pipeline.order_all import ordered_quests
    quests = load.load_all()
    depths = graph.quest_depth(quests)
    assert len(depths) == 1827
    ordered = ordered_quests()
    place = {quest['id']: number for number, quest in enumerate(ordered)}
    for quest in ordered:
        for dep in quest.get('deps', []):
            assert place[dep] < place[quest['id']], quest['id']


def make_fake_jar(tmp):
    """Вход: временная папка. Выход: путь к синтетическому jar-моду."""
    mods_toml = ('modLoader="javafml"\nloaderVersion="[47,)"\n[[mods]]\n'
                 'modId="fake"\nversion="1.0"\ndisplayName="Fake Mod"\n')
    lang = json.dumps({'item.fake.gear': 'Gear', 'block.fake.machine':
                       'Machine', 'gui.fake.x': 'y'})
    recipe = json.dumps({'type': 'create:mixing',
                         'ingredients': [{'item': 'minecraft:iron'}],
                         'results': [{'item': 'fake:gear'}]})
    path = os.path.join(tmp, 'fake-1.0.jar')
    with zipfile.ZipFile(path, 'w') as archive:
        archive.writestr('META-INF/mods.toml', mods_toml)
        archive.writestr('assets/fake/lang/en_us.json', lang)
        archive.writestr('data/fake/recipes/mixing/gear.json', recipe)
    return path


@check('ЭКСТРАКТОР: mods.toml читается из jar')
def extractor_mods():
    from extract.mods_from_folder import scan_jar
    with tempfile.TemporaryDirectory() as tmp:
        rows = scan_jar(make_fake_jar(tmp))
        assert rows and rows[0]['modid'] == 'fake'
        assert rows[0]['name'] == 'Fake Mod'


@check('ЭКСТРАКТОР: item./block. извлекаются, прочее отбрасывается')
def extractor_items():
    from extract.items_from_mods import scan_jar
    with tempfile.TemporaryDirectory() as tmp:
        rows = scan_jar(make_fake_jar(tmp))
        keys = sorted(row['key'] for row in rows)
        assert keys == ['block.fake.machine', 'item.fake.gear']


@check('ЭКСТРАКТОР: рецепты мода читаются из jar')
def extractor_recipes():
    from extract.recipes_from_mods import scan_jar
    with tempfile.TemporaryDirectory() as tmp:
        rows = scan_jar(make_fake_jar(tmp), 'fake')
        assert len(rows) == 1 and rows[0]['type'] == 'create:mixing'
        assert rows[0]['json']['results'][0]['item'] == 'fake:gear'


@check('ЭКСТРАКТОР: kubejs-файлы находятся в инстансе')
def extractor_kubejs():
    from extract.kubejs_from_instance import kubejs_files
    with tempfile.TemporaryDirectory() as tmp:
        scripts = os.path.join(tmp, 'kubejs', 'server_scripts')
        os.makedirs(scripts)
        open(os.path.join(scripts, 'recipes.js'), 'w').write('// пусто\n')
        found = kubejs_files(tmp)
        assert [row[0] for row in found] == ['server_scripts/recipes.js']


@check('SNBT: слова-HEX без кавычек не ломают числа')
def snbt_hex_words():
    value = parse_snbt('{ id: 072DA448D144179C, flag: 1abc, n: 2.5d }')
    assert value['id'] == '072DA448D144179C'
    assert value['flag'] == '1abc' and value['n'] == 2.5


def write(path, text):
    """Вход: путь, текст. Выход: путь. Записать файл (для фикстур)."""
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)
    return path


@check('ЭКСТРАКТОР КВЕСТОВ: раскладка A (глава-файл)')
def quests_layout_a():
    from extract import quests_from_instance as extractor
    chapter = (
        '{\n group: "Progression"\n order: 1\n filename: "fake"\n'
        ' quests: [\n  {\n   id: "AA11"\n   title: "&9T"\n'
        '   dependencies: []\n   tasks: [ { type: "checkmark" } ]\n'
        '   description: ["строка 1" "строка 2"]\n  }\n  {\n'
        '   id: "BB22"\n   title: "Second"\n   dependency_mode: 1\n'
        '   dependencies: ["AA11"]\n   tasks: [\n'
        '    { type: "item" item: { count: 3L id: "mod:item" } }\n'
        '    { type: "kill" mob: "mod:mob" count: 2L }\n   ]\n  }\n ]\n}\n')
    with tempfile.TemporaryDirectory() as tmp:
        chapters_dir = os.path.join(tmp, 'config', 'ftbquests', 'quests',
                                    'chapters')
        os.makedirs(chapters_dir)
        write(os.path.join(chapters_dir, 'fake.snbt'), chapter)
        found = extractor.collect_chapters(tmp)
        assert len(found) == 1
        name, entry, quests = found[0]
        assert name == 'fake' and entry['group'] == 'Progression'
        assert quests[0]['desc'] == 'строка 1\nстрока 2'
        assert quests[1]['tasks'] == ['ITEM mod:item x3', 'KILL mod:mob x2']
        assert quests[1]['dm'] == 'ONE'


@check('ЭКСТРАКТОР КВЕСТОВ: раскладка B (папка на главу)')
def quests_layout_b():
    from extract import quests_from_instance as extractor
    quest = ('{\n id: "CC33"\n title: "Q"\n dependencies: []\n'
             ' tasks: [ { type: "item" item: { tag: "minecraft:logs" } } ]\n}\n')
    with tempfile.TemporaryDirectory() as tmp:
        chapter_dir = os.path.join(tmp, 'config', 'ftbquests', 'quests',
                                   'chapters', 'side')
        os.makedirs(chapter_dir)
        write(os.path.join(chapter_dir, 'CC33.snbt'), quest)
        found = extractor.collect_chapters(tmp)
        assert len(found) == 1
        name, entry, quests = found[0]
        assert name == 'side' and quests[0]['tasks'] == [
            'ITEM any#tag:minecraft:logs x1']


def main():
    """Склейка: выполнить все проверки, напечатать итог."""
    failures = []
    for name, func in _CHECKS:
        try:
            func()
            print('OK   %s' % name)
        except AssertionError as error:
            failures.append(name)
            print('FAIL %s (%s)' % (name, error))
    print('\n%d/%d проверок пройдено' % (len(_CHECKS) - len(failures),
                                         len(_CHECKS)))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
