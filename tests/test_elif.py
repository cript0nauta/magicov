from tests.side_effect_utils import c

if c(1):
    removeme
elif c(2, True):
    c(3)

c(4)
c.reset()

if c(1):
    removeme
else:
    if c(2, True):
        c(3)

c(4)


def f():
    if False:
        removeme
    elif True:
        a=1
    else:
        a=3
f()

if True:
    if True:
        c(5)
    else:
        removeme


c.reset()
def f(b):
    if False:
        removeme
    elif b:
        c(1)
    else:
        c(2)

f(True)
f(False)
c(3)

c.reset()
def f(b):
    if False:
        removeme
    else:
        if b:
            c(1)
        else:
            c(2)

f(True)
f(False)
c(3)
