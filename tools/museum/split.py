"""Разбиение предметов мода на части по лимиту строк.

Закон репозитория: файл ≤ 500 строк. Музейный файл мода = шапка +
одна строка на предмет, поэтому большой мод делится на части
(modid.md, modid_part2.md, ...). Лимит предметов — с запасом на шапку.
"""

PART_LIMIT = 470


def split_parts(rows):
    """Вход: список предметов мода. Выход: [части] — списки длиной
    ≤ PART_LIMIT (каждая часть — срез исходного списка)."""
    return [rows[start:start + PART_LIMIT]
            for start in range(0, len(rows), PART_LIMIT)]


def part_filename(modid, part_no, parts):
    """Вход: modid, номер части (1-based), всего частей. Выход: имя
    файла: modid.md при одной части, иначе modid_partN.md."""
    if parts <= 1:
        return '%s.md' % modid
    return '%s_part%d.md' % (modid, part_no)


def part_title(part_no, parts):
    """Вход: номер части, всего частей. Выход: подзаголовок части
    ('' при одной части, иначе 'Часть N из M')."""
    if parts <= 1:
        return ''
    return '## Часть %d из %d' % (part_no, parts)
