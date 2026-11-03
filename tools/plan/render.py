"""Кирпичики разметки Markdown для генерации чек-листов (см. ../METHODS.md).

Ветка кода: heading/bullet/quest_line — однострочные примитивы;
chapter_header собирает их в шапку файла главы.
"""

from quests.tasks import display_title, parse_tasks, task_text
from plan.route import auto_filename, stage_name, stage_of

_AUTO_DIR_NOTE = ('> Файл сгенерирован инструментом (tools/pipeline/skeleton_all.py).'
                  '\n> Руками не редактировать: перегенерация сотрёт правки.'
                  '\n> Порядок квестов — топологический: зависимости всегда выше.'
                  '\n> Волна = глубина в графе зависимостей; внутри волны порядок главы.')


def heading(level, text):
    """Вход: уровень 1–6, текст. Выход: строка-заголовок Markdown."""
    return '%s %s' % ('#' * level, text)


def bullet(checkbox, text):
    """Вход: галочка (True/False), текст. Выход: строка списка."""
    mark = 'x' if checkbox else ' '
    return '- [%s] %s' % (mark, text)


def quest_line(quest, done=False):
    """Вход: квест, флаг выполнения. Выход: строка чек-листа."""
    title = display_title(quest)
    parts = [task_text(task) for task in parse_tasks(quest)]
    body = ' · '.join(parts) if parts else 'нет задач'
    return bullet(done, '**%s** — %s `%s`' % (title, body, quest['id'][:6]))


def chapter_header(chapter, index_entry, count, waves):
    """Вход: глава, запись _index, число квестов, число волн. Выход: шапка."""
    lines = [
        heading(1, 'Чек-лист: %s' % chapter),
        '',
        '*Этап %d (%s) · группа: %s · квестов: %d · волн: %d*'
        % (stage_of(chapter), stage_name(stage_of(chapter)),
           index_entry.get('group', '?'), count, waves),
        '',
        _AUTO_DIR_NOTE,
        '',
        '*Легенда: «сдать» — задача ITEM (предмет изымается); ×N — количество;'
        ' `id` — первые 6 символов id квеста (для поиска в data/chapters).*',
        '',
    ]
    return '\n'.join(lines)


def plural(count, one, few, many):
    """Вход: число, формы (1, 2-4, 5+). Выход: правильная форма."""
    if count % 10 == 1 and count % 100 != 11:
        return '%d %s' % (count, one)
    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return '%d %s' % (count, few)
    return '%d %s' % (count, many)


def wave_heading(depth, count):
    """Вход: глубина, число квестов. Выход: заголовок волны."""
    return heading(2, 'Волна %d — %s' % (depth, plural(count, 'квест',
                                                      'квеста', 'квестов')))


def file_reference(chapter):
    """Вход: имя главы. Выход: строка со ссылками на источники."""
    return 'Источник: `data/chapters/%s.jsonl` · чек-лист: `plan/auto/%s`' % (
        chapter, auto_filename(chapter))
