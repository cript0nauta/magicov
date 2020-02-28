# Copyright (C) 2020  Matías Lang

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

c.reset()
def f(b):
    c.reset()
    if c(1):
        removeme
    elif c(2):
        removeme
    elif b:
        x=1
    else:
        c(3)
f(False)
f(True)

if False:
    removeme
elif True:
    if False:
        removeme
