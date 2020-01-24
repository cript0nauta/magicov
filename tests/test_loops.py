from tests.side_effect_utils import c

for _ in c(1, []):
    removeme

c(2)

while c(3, False):
    removeme

c(4)

c.reset()

for _ in 'a':
    c(1)
    break
else:
    removeme

a = True
while a:
    c(2)
    a = False
    break
else:
    removeme
c(3)
