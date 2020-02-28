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

_magicov_expected_uncovered_lines = 1
try:
    [][1]
except c(2, RuntimeError):
    pass
except ZeroDivisionError:
    removeme
except c(3, IndexError):
    pass

c(4)

try:
    x=1
except:
    removeme

try:
    1/0
except ZeroDivisionError:
    pass
else:
    removeme

try:
    c(5)
except RuntimeError:
    removeme
else:
    c(6)

c(7)

def f():
    """Based on faraday/server/__init__.py"""
    def r():
        x=0
        try:
            a=1
        except:
            removeme
    r()

f()


c.reset()
try:
    1/0
except ZeroDivisionError:
    try:
        assert 0
    except AssertionError:
        c(1)
    except Exception:
        removeme
c(2)


c.reset()
try:
    try:
        1/0
    except ZeroDivisionError:
        c(1)
    except Exception:
        removeme
except RuntimeError:
    pass
c(2)

c.reset()
try:
    c(1)
except c(2, RuntimeError):
    pass
c(2)

c.reset()
def f():
    try:
        1/0
    except ZeroDivisionError:
        c(1)
        if False:
            removeme

f()
c(2)

c.reset()
def f():
    try:
        pass
    except (RuntimeError, AssertionError):
        removeme
    else:
        if False:
            removeme
        c(1)

f()
c(2)
