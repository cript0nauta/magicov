from tests.side_effect_utils import c

def f():
    a = 1
    c(2)
    return
    x = 5
    removeme

c(1)
f()
c(3)
