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

if False:
    removeme

c(3)

class Klass(object):
    def __init__(self):
        x = 5
        if False:
            removeme
        else:
            a = 5
Klass()


class Klass(object):
    def m(self):
        try:
            x=1
        except ValueError:
            if False:
                x=3
            x=2
Klass().m()

# Test what happens when the if body is not a list
x = 1 if True else False

if False:
    removeme
else:
    if False:
        removeme
    c(4)
c(5)
