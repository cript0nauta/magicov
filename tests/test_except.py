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

