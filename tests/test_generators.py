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

c.reset()
# https://github.com/google/pasta/issues/82
class C:
    def s(self):
        c(1)
        1/0
        yield 1

try:
    list(C().s())
except ZeroDivisionError:
    pass
c(2)
