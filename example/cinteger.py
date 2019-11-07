#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    cinteger.py - demonstrate use of CInteger
#    Copyright (C) 2019  Tommy Alex
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numbers
from cstruct import CInteger


class SmallInteger(CInteger, size=3):
	'''3-byte integer in big-endian'''
	BYTE_ORDER = 'big'


if __name__ == '__main__':
	k1 = SmallInteger.from_bytes(b'\x01\x02\x03')
	k2 = SmallInteger(1)
	print(k1, k2)
	print(isinstance(k1, int), isinstance(k2, int))
	print(isinstance(k1, numbers.Integral), isinstance(k2, numbers.Integral))
	print(k1 & 0x1)
	print(k1 ^ k2)
	assert k1 == 0x010203
	assert k2 == (k1 & k2)
