from tests.side_effect_utils import c

# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 1

n = 5

def func():
    global n
    n = 1

def func2():
    global n

func()
c(n)
