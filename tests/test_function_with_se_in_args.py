from tests.side_effect_utils import c

_magicov_expected_uncovered_lines = 2

def removemybody(a=c(1), b=c(2)):
    removeme

class Klass:
    def removemybody_method(self, a=c(3), b=c(4)):
        removeme

c(5)
