# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 1

def identity(f):
    return f

def afunction():
    removeme

identity(afunction)
