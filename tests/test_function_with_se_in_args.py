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
# _magicov_expected_uncovered_lines = 2

def removemybody(a=c(1), b=c(2)):
    removeme

class Klass:
    def removemybody_method(self, a=c(3), b=c(4)):
        removeme

c(5)
