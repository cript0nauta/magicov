from tests.side_effect_utils import c

if True:
    a = 1
else:
    removeme

if False:
    removeme
else:
    a = 2

if False:
    removeme

if c(1):
    a = 1

if c(2):
    a = 1
else:
    a = 2

c(3)

class Klass(object):
    def __init__(self):
        x = 5
        if False:
            removeme
        else:
            a = 5
Klass()
