from tests.side_effect_utils import c

# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 1

n = 1

def deco(n):
    def deco2(f):
        c(n)
        return f
    return deco2

@deco(1)
def unused():
    removeme
    removeme
    return 8

@deco(2)
def used():
    return 42

used()
