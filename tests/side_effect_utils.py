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

class Counter:
    def __init__(self):
        self.count = 1

    def __call__(self, expected_count, return_value=None):
        assert self.count == expected_count, (
                "Count doesn't match: you are expecting {}, but my "
                "count is {}").format(expected_count, self.count)
        self.count += 1
        return return_value

    def reset(self):
        self.count = 1

c = Counter()
