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

# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 1

n = 1

def deco(n):
    def deco2(f):
        c(n)
        return f
    return deco2

@deco(1)
def unused():
    removeme
    removeme
    return 8

@deco(2)
def used():
    return 42

used()


def test_return_multiline():
    return (
        1+1
    )

assert test_return_multiline() == 2


# based on https://github.com/marshmallow-code/marshmallow/blob/2.18.1/src/marshmallow/utils.py#L58
def is_iterable_but_not_string(obj):
    """Return True if ``obj`` is an iterable object that isn't a string."""
    # TODO cambiar por lo anterior
    x = (
        (isinstance(obj, object) and not hasattr(obj, "strip")) or False
    )
    return x

assert is_iterable_but_not_string({})
assert is_iterable_but_not_string([])
assert not is_iterable_but_not_string("")
