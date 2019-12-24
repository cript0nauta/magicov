from tests.side_effect_utils import c

try:
    1/0
except ZeroDivisionError:
    a=1
except AttributeError:
    removeme

c(1)

try:
    1/2
except ZeroDivisionError:
    removeme

_magicov_expected_uncovered_lines = 1
try:
    [][1]
except c(2, RuntimeError):
    pass
except ZeroDivisionError:
    removeme
except c(3, IndexError):
    pass

c(4)

try:
    x=1
except:
    removeme

try:
    1/0
except ZeroDivisionError:
    pass
else:
    removeme

try:
    c(5)
except RuntimeError:
    removeme
else:
    c(6)

c(7)

def f():
    """Based on faraday/server/__init__.py"""
    def r():
        x=0
        try:
            a=1
        except:
            removeme
    r()

f()