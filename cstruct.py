# -*- coding: utf-8 -*-
#
#    python-cstruct - another C-struct in Python effort
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


import inspect
import struct
import collections


def unpack_from(format, buffer, offset):
	value = format.unpack_from(buffer, offset)
	return value[0] if isinstance(value, tuple) and 1 == len(value) else value


class CStructBase(object):
	'''CStruct base class that support struct.Struct interface'''

	@classmethod
	def pack(cls, *values):
		buffer = bytearray(cls.size)
		cls.pack_into(buffer, 0, *values)
		return buffer

	@classmethod
	def pack_into(cls, buffer, offset, *values):
		raise NotImplementedError

	@classmethod
	def unpack(cls, buffer):
		assert cls.size == len(buffer), 'buffer size mismatch'
		return cls.unpack_from(buffer)

	@classmethod
	def unpack_from(cls, buffer, offset=0):
		raise NotImplementedError

	@classmethod
	def iter_unpack(cls, buffer):
		assert 0 == len(buffer) % cls.size
		for offset in range(0, len(buffer), cls.size):
			yield unpack_from(cls, buffer, offset)

	@classmethod
	def from_bytes(cls, bytes):
		return cls.unpack(bytes)

	def to_bytes(self):
		return self.pack(self)


def is_struct_member(value):
	'''return True if VALUE can be used in CStruct'''
	return isinstance(value, struct.Struct) or (inspect.isclass(value) and issubclass(value, CStructBase))


class CStructBaseType(type):
	'''base metaclass for CStruct, set the SIZE attribute for CStruct class'''

	NAME_SIZE = 'size'

	def __new__(cls, name, bases, namespace, **kwds):
		if cls.NAME_SIZE in namespace:
			raise TypeError('"{}" is reserved in {}'.format(cls.NAME_SIZE, cls.__name__))
		namespace[cls.NAME_SIZE] = int(cls.calcsize(namespace, **kwds))
		return super().__new__(cls, name, bases, namespace)

	@classmethod
	def calcsize(cls, namespace, **kwds):
		'''return size from CBigInteger class definition'''
		if cls.NAME_SIZE in kwds and isinstance(kwds[cls.NAME_SIZE], int):
			return kwds[cls.NAME_SIZE]
		raise TypeError('"{}" not defined'.format(cls.NAME_SIZE))


class CStructType(CStructBaseType, type(collections.abc.Mapping)):
	'''metaclass for CStruct, collect all members for struct'''

	NAME_MEMBERS = 'members'

	def __new__(cls, name, bases, namespace, **kwds):
		if cls.NAME_MEMBERS in namespace:
			raise TypeError('"{}" is reserved in {}'.format(cls.NAME_MEMBERS, cls.__name__))
		members = collections.OrderedDict((key, value) for key, value in namespace.items() if is_struct_member(value))
		namespace[cls.NAME_MEMBERS] = members
		return super().__new__(cls, name, bases, namespace, **kwds)

	@classmethod
	def calcsize(cls, namespace, **kwds):
		return sum(member.size for member in namespace[cls.NAME_MEMBERS].values())


class CStruct(CStructBase, collections.abc.Mapping, metaclass=CStructType):
	'''define a struct using CStruct'''

	@classmethod
	def unpack_from(cls, buffer, offset=0):
		assert len(buffer) >= offset + cls.size, 'buffer too small'
		obj = cls()
		for member, format in cls.members.items():
			value = unpack_from(format, buffer, offset)
			setattr(obj, member, value)
			offset += format.size
		return obj

	@classmethod
	def pack_into(cls, buffer, offset, *values):
		assert len(buffer) >= offset + cls.size, 'buffer too small'
		obj = values[0]
		for member, format in cls.members.items():
			value = getattr(obj, member)
			if not isinstance(value, tuple):
				value = (value,)
			format.pack_into(buffer, offset, *value)
			offset += format.size

	def __getitem__(self, key):
		if not key in self.__class__.members:
			raise KeyError(key)
		return getattr(self, key)

	def __iter__(self):
		return iter(self.__class__.members)

	def __len__(self):
		return len(self.__class__.members)


class CStructArrayType(CStructBaseType, type(collections.abc.Sequence)):
	'''array type for CStruct'''

	NAME_ARRAY = 'array'

	@classmethod
	def calcsize(cls, namespace, **kwds):
		if not cls.NAME_ARRAY in namespace:
			raise TypeError('"{}" not defined for array'.format(cls.NAME_ARRAY))
		if not is_struct_member(namespace[cls.NAME_ARRAY]):
			raise TypeError('unsupportted value of "{}"'.format(cls.NAME_ARRAY))

		count = super().calcsize(namespace, **kwds)
		return namespace[cls.NAME_ARRAY].size * count


class CStructArray(CStructBase, collections.abc.Sequence, metaclass=CStructArrayType, size=0):
	'''array support for CStruct'''
	array = CStruct

	def __getitem__(self, key):
		return self.array[key]

	def __len__(self):
		return len(self.array)

	@classmethod
	def unpack_from(cls, buffer, offset=0):
		assert len(buffer) >= offset + cls.size, 'buffer too small'
		obj = cls()
		array = tuple(unpack_from(cls.array, buffer, i) for i in range(offset, offset + cls.size, cls.array.size))
		setattr(obj, CStructArrayType.NAME_ARRAY, array)
		return obj

	@classmethod
	def pack_into(cls, buffer, offset, *values):
		assert len(buffer) >= offset + cls.size, 'buffer too small'
		obj = values[0]
		for o in obj:
			cls.array.pack_into(buffer, offset, o)
			offset += cls.array.size


class CInteger(CStructBase, int, metaclass=CStructBaseType, size=0):
	'''integer with specific size'''

	BYTE_ORDER = 'little'
	SIGNED = True

	@classmethod
	def unpack_from(cls, buffer, offset=0):
		assert len(buffer) >= offset + cls.size, 'buffer too small'

		integer = int.from_bytes(buffer[offset:offset + cls.size], cls.BYTE_ORDER, signed=cls.SIGNED)
		return cls(integer)

	@classmethod
	def pack_into(cls, buffer, offset, *values):
		assert len(buffer) >= offset + cls.size, 'buffer too small'

		obj = values[0]
		bytes = obj.to_bytes(cls.size, cls.BYTE_ORDER, signed=cls.SIGNED)
		buffer[offset:offset + cls.size] = bytes


class CString(CStructBase, str, metaclass=CStructBaseType, size=0):
	'''string with specific size'''

	ENCODING = 'utf-8'

	@classmethod
	def unpack_from(cls, buffer, offset=0):
		assert len(buffer) >= offset + cls.size, 'buffer too small'
		return cls(buffer[offset:offset + cls.size], encoding=cls.ENCODING)

	@classmethod
	def pack_into(cls, buffer, offset, *values):
		assert len(buffer) >= offset + cls.size, 'buffer too small'

		obj = values[0]
		bytes = obj.encode(encoding=cls.ENCODING)
		if len(bytes) > cls.size:
			raise ValueError('data too big')
		fmt = b'%-0%db' % cls.size
		buffer[offset:offset + cls.size] = fmt % bytes


def cstructarray(item, size):
	return type('', (CStructArray, ), {'array': item}, size=size)

def cinteger(size, byteorder, signed=False):
	return type('', (CInteger, ), {'BYTE_ORDER': byteorder, 'SIGNED': signed}, size=size)

def cstring(size, encoding='utf-8'):
	return type('', (CString, ), {'ENCODING': encoding}, size=size)
