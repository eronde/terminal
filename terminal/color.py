#!/usr/bin/env python
import os
import sys

codes = {}


def is_color_support():
    "Find out if your terminal environment supports color."
    # shinx.util.console
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    if 'COLORTERM' in os.environ:
        return True
    term = os.environ.get('TERM', 'dumb').lower()
    return term in ('xterm', 'linux') or 'color' in term


def colorize(name, text):
    if not is_color_support():
        return text
    code = codes.get(name, None)
    if not code:
        return text
    return code[0] + text + code[1]


def create_color_func(name):
    def inner(text):
        return colorize(name, text)
    globals()[name] = inner


def _esc(*codes):
    return "\x1b[%sm" % (";".join([str(c) for c in codes]))

_styles = {
    'bold': (1, 22),
    'italic': (3, 23),
    'underline': (4, 24),
    'blink': (5, 25),
    'flip': (7, 27),
    'strike': (9, 29),
}
for _name in _styles:
    _code = _styles[_name]
    codes[_name] = (_esc(_code[0]), _esc(_code[1]))


_colors = [
    'black', 'red', 'green', 'yellow',
    'blue', 'magenta', 'cyan', 'white'
]

for i, _name in enumerate(_colors):
    codes[_name] = (_esc(i + 30), _esc(39))

for _name in codes:
    create_color_func(_name)
