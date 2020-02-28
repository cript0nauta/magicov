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
