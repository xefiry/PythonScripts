# Source : https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

from enum import StrEnum


def _escape(value: int) -> str:
    return f"\033[{value}m"


CLEAR = _escape(0)


class FG(StrEnum):
    """Foreground colors"""

    BLACK = _escape(30)
    RED = _escape(31)
    GREEN = _escape(32)
    YELLOW = _escape(33)
    BLUE = _escape(34)
    MAGENTA = _escape(35)
    CYAN = _escape(36)
    WHITE = _escape(37)
    CLEAR = _escape(39)
    GRAY = _escape(90)  # same as bright black


class FGB(StrEnum):
    """Foreground colors - bright"""

    BLACK = _escape(90)
    RED = _escape(91)
    GREEN = _escape(92)
    YELLOW = _escape(93)
    BLUE = _escape(94)
    MAGENTA = _escape(95)
    CYAN = _escape(96)
    WHITE = _escape(97)
    CLEAR = _escape(39)


class BG(StrEnum):
    """Background colors"""

    BLACK = _escape(40)
    RED = _escape(41)
    GREEN = _escape(42)
    YELLOW = _escape(43)
    BLUE = _escape(44)
    MAGENTA = _escape(45)
    CYAN = _escape(46)
    WHITE = _escape(47)
    CLEAR = _escape(49)
    GRAY = _escape(100)  # same as bright black


class BGB(StrEnum):
    """Background colors - bright"""

    BLACK = _escape(100)
    RED = _escape(101)
    GREEN = _escape(102)
    YELLOW = _escape(103)
    BLUE = _escape(104)
    MAGENTA = _escape(105)
    CYAN = _escape(106)
    WHITE = _escape(107)
    CLEAR = _escape(49)
