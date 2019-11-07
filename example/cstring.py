#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    cstring.py - demonstrate use of CString
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

from cstruct import CString, cstring

class String(CString, size=5):
	ENCODING = 'ascii'

if __name__ == '__main__':
	s = String.from_bytes(b'\x31\x32\x33\x34\x35')
	print(s)
	assert s == '12345'
	scls = cstring(4)
	s2 = scls.from_bytes(b'\x41\x42\x43\x44')
	print(s2)
	assert s2 == 'ABCD'
