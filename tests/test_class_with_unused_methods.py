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

# This is commented because of the added pragma: nocov
# _magicov_expected_uncovered_lines = 3

class Test:
    def method1(self):
        removeme

    def method2(self):
        removeme

    def method3(self):
        removeme

    def unused_generator(self):
        # This function is not covered at first because it has a yield,
        # but will be covered after being rewritten.
        n=1
        removeme
        yield 1

    def used_generator(self):
        yield 1

Test().unused_generator()
next(Test().used_generator())
