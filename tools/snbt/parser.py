"""Парсер SNBT — диалект FTB Quests (см. ../METHODS.md).

Отличия диалекта от строгого SNBT: запятые между элементами
объектов и массивов могут отсутствовать (разделитель — перевод строки).

Ветка кода: parse_snbt вызывает _value; _value вызывает _object/_array/
_string/_number/_word; те вызывают _key, _skip_ws, _peek — примитивы.
"""

import re

_NUMBER = re.compile(r'[-+]?(?:\d[\d_]*\.?\d*(?:[eE][-+]?\d+)?|\.\d+)([NSLnsfdfbBI]?)')
_WORD = re.compile(r'[A-Za-z_][A-Za-z0-9_.]*')
_KEY = re.compile(r'[A-Za-z0-9_\-]+')
_COMMENT = re.compile(r'(^|\s)//[^\n]*')


def parse_snbt(text):
    """Вход: текст SNBT. Выход: объект Python (dict/list/str/число/bool)."""
    return SnbtParser(text).parse()


def _strip_comments(text):
    """Вход: текст. Выход: текст. Убрать комментарии, начинающиеся с //."""
    return _COMMENT.sub(lambda match: match.group(1), text)


class SnbtParser:
    """Рекурсивный спуск. Позиция хранится в self._pos."""

    def __init__(self, text):
        self._text = _strip_comments(text)
        self._pos = 0

    def parse(self):
        """Вход: —. Выход: корневое значение. Начать разбор."""
        return self._value()

    def _peek(self):
        """Вход: —. Выход: символ. Текущий символ ('' = конец текста)."""
        if self._pos < len(self._text):
            return self._text[self._pos]
        return ''

    def _error(self, message):
        """Вход: сообщение. Выход: никогда (raise). Контекстная ошибка."""
        context = self._text[max(0, self._pos - 30):self._pos + 30]
        raise ValueError('%s at %d: ...%s...' % (message, self._pos, context))

    def _skip_ws(self):
        """Вход: —. Выход: —. Пропустить пробелы и переводы строк."""
        while self._peek() in (' ', '\t', '\r', '\n'):
            self._pos += 1

    def _value(self):
        """Вход: —. Выход: значение. Объект/массив/строка/число/слово."""
        self._skip_ws()
        char = self._peek()
        if char == '{':
            return self._object()
        if char == '[':
            return self._array()
        if char in ('"', "'"):
            return self._string()
        match = _NUMBER.match(self._text, self._pos)
        if match:
            self._pos = match.end()
            return self._number(match.group(1), match.group(2))
        return self._word()

    def _object(self):
        """Вход: —. Выход: dict. Разбор { ключ: значение ... }."""
        self._pos += 1
        result = {}
        while True:
            self._skip_ws()
            if self._peek() == '}':
                self._pos += 1
                return result
            key = self._key()
            self._skip_ws()
            if self._peek() != ':':
                self._error("ожидалось ':'")
            self._pos += 1
            result[key] = self._value()
            self._skip_ws()
            if self._peek() == ',':
                self._pos += 1

    def _array(self):
        """Вход: —. Выход: list. Разбор [ ... ] или [I; ... ]."""
        self._pos += 1
        self._skip_ws()
        typed = re.match(r'[BILFD]\s*;', self._text[self._pos:])
        if typed:
            self._pos += typed.end()
            return self._typed_array()
        result = []
        while True:
            self._skip_ws()
            if self._peek() == ']':
                self._pos += 1
                return result
            result.append(self._value())
            self._skip_ws()
            if self._peek() == ',':
                self._pos += 1

    def _typed_array(self):
        """Вход: — (префикс [I; уже пропущен). Выход: list чисел."""
        result = []
        while True:
            self._skip_ws()
            if self._peek() == ']':
                self._pos += 1
                return result
            result.append(self._value())
            self._skip_ws()
            if self._peek() == ',':
                self._pos += 1

    def _string(self):
        """Вход: — (каемы уже видны). Выход: str. Разбор с экранированием."""
        quote = self._peek()
        self._pos += 1
        chars = []
        while self._pos < len(self._text) and self._text[self._pos] != quote:
            if self._text[self._pos] == '\\':
                escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\',
                           '"': '"', "'": "'"}
                nxt = self._text[self._pos + 1:self._pos + 2]
                chars.append(escapes.get(nxt, nxt))
                self._pos += 2
            else:
                chars.append(self._text[self._pos])
                self._pos += 1
        self._pos += 1
        return ''.join(chars)

    def _number(self, token, suffix):
        """Вход: токен и суффикс NBT. Выход: int/float. Преобразование."""
        clean = token.replace('_', '')
        if '.' in clean or 'e' in clean or 'E' in clean:
            return float(clean)
        return int(clean)

    def _word(self):
        """Вход: —. Выход: True/False/str. Разбор true/false/слова."""
        match = _WORD.match(self._text, self._pos)
        if not match:
            self._error('неожиданный символ')
        self._pos = match.end()
        word = match.group(0)
        if word == 'true':
            return True
        if word == 'false':
            return False
        return word

    def _key(self):
        """Вход: —. Выход: str. Разбор ключа объекта."""
        self._skip_ws()
        char = self._peek()
        if char in ('"', "'"):
            return self._string()
        match = _KEY.match(self._text, self._pos)
        if not match:
            self._error('неверный ключ')
        self._pos = match.end()
        return match.group(0)