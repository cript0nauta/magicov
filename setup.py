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

from setuptools import setup

setup(
    name='magicov',
    version='0.2',
    packages=['magicov',],
    license='GPLv3+',
    author='Matías Lang',
    url='https://github.com/cript0nauta/magicov',
    long_description=open('README.md').read(),
    install_requires=['google-pasta>=0.2.0', 'coverage<5', 'click'],
    entry_points={
        'console_scripts': [
            'magicov=magicov:main'
        ]
    },
)
