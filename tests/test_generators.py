from tests.side_effect_utils import c

def f():
    c(1)
    1/0
    yield 2
    removeme

f()

try:
    list(f())
except ZeroDivisionError:
    pass
c(2)

c.reset()

def f():
    c(1)
    if False:
        yield 2
        removeme

f()

list(f())
c(2)


c.reset()

def f():
    def g():
        yield 5
    c(1)

f()
c(2)
