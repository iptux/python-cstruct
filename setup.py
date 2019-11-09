#	setup.py - Setup Script for cstruct
#	Copyright (C) 2019  Tommy Alex <iptux7@gmail.com>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

from distutils.core import setup

setup(
	name='cstruct',
	version='0.1',
	author='Tommy Alex',
	author_email='iptux7@gmail.com',
	py_modules=['cstruct'],
	package_data={'': ['LICENSE']},

	description='Another c-struct like object support in Python',
	license='GPL-3.0+',
	platforms='any',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Software Development',
	],
)
