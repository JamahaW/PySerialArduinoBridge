"""
Примитивные типы
"""
import struct
from abc import ABC
from abc import abstractmethod
from itertools import chain
from typing import Final
from typing import Iterable
from typing import Sequence


class _FormatHelper:
    I8: Final[str] = "<b"
    I16: Final[str] = "<h"
    I32: Final[str] = "<l"
    I64: Final[str] = "<q"

    U8: Final[str] = "<B"
    U16: Final[str] = "<H"
    U32: Final[str] = "<L"
    U64: Final[str] = "<Q"

    F32: Final[str] = "<f"
    F64: Final[str] = "<d"

    @classmethod
    def getSigned(cls) -> Iterable[str]:
        """Все знаковые форматы"""
        return cls.I8, cls.I16, cls.I32, cls.I64

    @classmethod
    def getUnsigned(cls) -> Iterable[str]:
        """Все форматы без знака"""
        return cls.U8, cls.U16, cls.U32, cls.U64

    @classmethod
    def getExponential(cls) -> Iterable[str]:
        """Все экспоненциальные форматы"""
        return cls.F32, cls.F64

    @classmethod
    def getAll(cls) -> Iterable[str]:
        """Все типы"""
        return chain(cls.getExponential(), cls.getSigned(), cls.getUnsigned())

    @classmethod
    def matchPrefix(cls, fmt: str) -> str:
        """Подобрать префикс"""
        match fmt:
            case _ if fmt in cls.getExponential():
                return "f"

            case _ if fmt in cls.getSigned():
                return "i"

            case _ if fmt in cls.getUnsigned():
                return "u"

        raise ValueError(fmt)


class Binary[T](ABC):
    """Двоичные данные"""

    @abstractmethod
    def pack(self, value: T) -> bytes:
        """Упаковать значение в соответсвующее байтовое представление"""

    @abstractmethod
    def unpack(self, buffer: bytes) -> T:
        """Получить значение из соответствующего байтового представления"""

    @abstractmethod
    def getSize(self) -> int:
        """Получить размер данных в байтах"""

    @abstractmethod
    def getFormat(self) -> str:
        """Получить спецификатор формата"""


class Primitive[T: (int | float | bool)](Binary[T]):
    """Примитивные типы"""

    def __init__(self, pack_format: str) -> None:
        self._struct = struct.Struct(pack_format)

    def getFormat(self) -> str:
        return self._struct.format

    def getSize(self) -> int:
        return self._struct.size

    def pack(self, value: T) -> bytes:
        return self._struct.pack(value)

    def unpack(self, buffer: bytes) -> T:
        return self._struct.unpack(buffer)[0]

    def __str__(self) -> str:
        return f"{_FormatHelper.matchPrefix(self.getFormat())}{self.getSize() * 8}"


class Struct(Binary[tuple]):
    """Структура"""

    def __init__(self, fields: Sequence[Primitive]) -> None:
        self._fields = fields
        self._packer = struct.Struct(f"<{''.join(map(lambda f: f.getFormat().replace("<", ""), fields))}")

    def unpack(self, buffer: bytes) -> tuple:
        return self._packer.unpack(buffer)

    def pack(self, fields: tuple) -> bytes:
        return self._packer.pack(*fields)

    def getSize(self) -> int:
        return self._packer.size

    def getFormat(self) -> str:
        return self._packer.format

    def __str__(self) -> str:
        return f"{{{', '.join(map(str, self._fields))}}}"


u8 = Primitive[int | bool](_FormatHelper.U8)
u16 = Primitive[int](_FormatHelper.U16)
u32 = Primitive[int](_FormatHelper.U32)
u64 = Primitive[int](_FormatHelper.U64)

i8 = Primitive[int](_FormatHelper.I8)
i16 = Primitive[int](_FormatHelper.I16)
i32 = Primitive[int](_FormatHelper.I32)
i64 = Primitive[int](_FormatHelper.I64)

f32 = Primitive[float](_FormatHelper.F32)
f64 = Primitive[float](_FormatHelper.F64)


def main():
    s = Struct((u32, u16, u8))
    print(f"{s=!s}")

    v = bytes((0xA4, 0xA3, 0xA2, 0xA1, 0xB2, 0xB1, 0x69,))

    m = s.unpack(v)
    print(", ".join(map(hex, m)))
    v1 = s.pack(m)

    print(", ".join(map(hex, v1)))


if __name__ == '__main__':
    main()
