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
# _magicov_expected_uncovered_lines = 2
class K(object):
    def _f1():
        if True:
            yield host_ip
            pass

    def _f2():
        pass

# Discomment when https://github.com/google/pasta/issues/76 is fixed
# _magicov_expected_uncovered_lines = 3
#     def _f3():
#         pass
