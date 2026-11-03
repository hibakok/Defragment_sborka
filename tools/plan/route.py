"""Маршрут прохождения: глава → этап (см. ../METHODS.md).

Этапы совпадают с progress/TRACKER.md. Порядок внутри этапа — порядок
в списке ROUTE (он же задаёт букву файла: 13a, 13b...).
create101 — учебник Create, идёт ПАРАЛЛЕЛЬНО этапам 02–11.
"""

ROUTE = [
    ('basics', 1),
    ('chapter_i_the_andesite_machine', 2),
    ('chapter_iii_the_cooper_machine', 3),
    ('chapter_ii_the_brass_machine', 4),
    ('storage_solutions', 4),
    ('chapter_iv_the_locomotive_machine', 5),
    ('chapter_v_steel_mechanism', 6),
    ('chapter_vi_rocket_fuel', 7),
    ('chapter_vii_infernal_mechanism', 8),
    ('chapter_vii_building_a_rocket', 9),
    ('chapter_ix_calculation_mechanism', 10),
    ('chapter_x_applied_energetics', 11),
    ('space_exploration_iii_to_mars', 12),
    ('space_exploration_ii_to_venus', 12),
    ('space_exploration_iii_to_glacio', 12),
    ('ars_nouveau', 13),
    ('irons_spells_n_spellbooks', 13),
    ('forbidden_and_arcanus', 13),
    ('the_twilight', 14),
    ('the_aether', 14),
    ('blue_skies', 14),
    ('the_end', 14),
    ('deeper_and_darker', 14),
    ('alexs_caves', 14),
    ('bosses_and_skill_points', 15),
    ('the_black_market', 15),
    ('renewable_ores', 15),
    ('artifacts', 15),
    ('simply_swords', 15),
    ('rings_of_ascension', 15),
    ('create101', 16),
]

_STAGE_NAMES = {
    1: 'basics — старт',
    2: 'глава I — андезитовая машина',
    3: 'глава III — медная машина',
    4: 'глава II — латунная машина + хранение',
    5: 'глава IV — локомотивная машина',
    6: 'глава V — стальной механизм',
    7: 'глава VI — ракетное топливо',
    8: 'глава VII — инфернальный механизм',
    9: 'глава VII — постройка ракеты',
    10: 'глава IX — расчётный механизм',
    11: 'глава X — Applied Energistics',
    12: 'космос: Марс → Венера → Гласио',
    13: 'магия',
    14: 'измерения',
    15: 'боссы, чёрный рынок, коллекции, руды',
    16: 'create101 — учебник Create (параллельно 02–11)',
}


def _stages():
    """Вход: —. Выход: {этап: [главы в порядке ROUTE]} (внутренний)."""
    table = {}
    for chapter, stage in ROUTE:
        table.setdefault(stage, []).append(chapter)
    return table


def stage_of(chapter):
    """Вход: имя главы. Выход: номер этапа (KeyError, если главы нет)."""
    for name, stage in ROUTE:
        if name == chapter:
            return stage
    raise KeyError(chapter)


def stage_name(stage):
    """Вход: номер этапа. Выход: человеческое название этапа."""
    return _STAGE_NAMES.get(stage, 'этап %d' % stage)


def auto_filename(chapter):
    """Вход: имя главы. Выход: имя файла чек-листа в plan/auto/."""
    stage = stage_of(chapter)
    siblings = _stages()[stage]
    prefix = '%02d' % stage
    if len(siblings) > 1:
        letter = chr(ord('a') + siblings.index(chapter))
        return '%s%s_%s.md' % (prefix, letter, chapter)
    return '%s_%s.md' % (prefix, chapter)
