#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    geometry.py - demonstrate the use of CStruct
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

import struct
from cstruct import CStruct, CStructArray, cstructarray


class Point(CStruct):
	x = struct.Struct('b')
	y = struct.Struct('b')

	def __str__(self):
		return 'Piont(x={0.x}, y={0.y})'.format(self)


class Line(CStruct):
	p1 = Point
	p2 = Point

	def __str__(self):
		return 'Line(p1={0.p1}, p2={0.p2})'.format(self)


class Rectangle(CStruct):
	p1 = Point
	p2 = Point

	def area(self):
		return abs(self.p1.x - self.p2.x) * abs(self.p1.y - self.p2.y)

	def valid(self):
		return 0 != self.area()

	def __str__(self):
		return 'Rectangle(p1={0.p1}, p2={0.p2})'.format(self)


class Triangle(CStructArray, size=3):
	array = Point

	def __str__(self):
		return 'Triangle({0[0]!s}, {0[1]!s}, {0[2]!s})'.format(self)


Triangle2 = cstructarray(Point, 3)


def geometry(cls, buffer):
	o = cls.from_bytes(buffer)
	print(cls.__name__, o.size, o)
	assert buffer == o.to_bytes()


if __name__ == '__main__':
	geometry(Point, b'\x00\x00')
	geometry(Point, b'\x0f\x20')
	geometry(Line, b'\x00\x00\x10\x09')
	geometry(Rectangle, b'\x00\x00\xff\xff')
	geometry(Triangle, b'\x00\x00\x00\x02\x03\x00')
	geometry(Triangle2, b'\x00\x00\x00\x02\x03\x00')
	geometry(Rectangle, b'\x00\x00\x00\xff')
