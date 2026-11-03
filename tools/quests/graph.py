"""Граф зависимостей квестов (см. ../METHODS.md).

Ветка кода: deps_map/dependents_map — примитивы графа; quest_depth
считает глубину итеративно; order_rows сортирует по (глубина, этап,
позиция в файле) — это корректный топологический порядок, потому что
глубина предка всегда строго меньше глубины потомка.
"""

from quests import tasks as qtasks


def deps_map(quests):
    """Вход: список квестов. Выход: {id: [id зависимостей]}."""
    return {quest['id']: list(quest.get('deps', [])) for quest in quests}


def dependents_map(quests):
    """Вход: список квестов. Выход: {id: [id зависящих]}."""
    result = {}
    for quest in quests:
        for dep in quest.get('deps', []):
            result.setdefault(dep, []).append(quest['id'])
    return result


def _ready(quest, depths, known):
    """Вход: квест, глубины, множество известных id. Выход: bool.
    Зависимости вне известного множества считаются выполненными."""
    for dep in quest.get('deps', []):
        if dep in known and dep not in depths:
            return False
    return True


def _max_dep(quest, depths):
    """Вход: квест, глубины. Выход: максимум глубины deps (0 если нет)."""
    best = 0
    for dep in quest.get('deps', []):
        if dep in depths:
            best = max(best, depths[dep])
    return best


def quest_depth(quests):
    """Вход: список квестов. Выход: {id: глубина}. Глубина = длина самого
    длинного пути от корня; корень (без deps внутри списка) = 1. Зависимости
    вне списка (другие главы) считаются выполненными."""
    known = {quest['id'] for quest in quests}
    depths = {}
    pending = list(quests)
    while pending:
        rest = []
        for quest in pending:
            if _ready(quest, depths, known):
                depths[quest['id']] = _max_dep(quest, depths) + 1
            else:
                rest.append(quest)
        if len(rest) == len(pending):
            raise ValueError('цикл в зависимостях квестов')
        pending = rest
    return depths


def order_rows(quests, depths, stage_of):
    """Вход: квесты, глубины, функция этапа главы. Выход: квесты,
    отсортированные топологически (deps всегда раньше)."""
    def key(quest):
        return (depths[quest['id']], stage_of(quest['chapter']), quest['pos'])
    return sorted(quests, key=key)


def with_positions(quests):
    """Вход: список квестов. Выход: тот же список, каждому добавлен pos
    (номер строки в файле главы, для стабильного порядка)."""
    for number, quest in enumerate(quests):
        quest['pos'] = number
    return quests
