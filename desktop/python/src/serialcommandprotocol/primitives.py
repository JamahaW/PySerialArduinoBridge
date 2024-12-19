"""
Примитивные типы
"""
import struct
from abc import ABC
from abc import abstractmethod
from itertools import chain
from typing import Final
from typing import Iterable
from typing import NamedTuple
from typing import Sequence
from typing import Type
from typing import TypedDict
from typing import get_type_hints


class _Format:
    I8: Final[str] = "b"
    I16: Final[str] = "h"
    I32: Final[str] = "l"
    I64: Final[str] = "q"

    U8: Final[str] = "B"
    U16: Final[str] = "H"
    U32: Final[str] = "L"
    U64: Final[str] = "Q"

    F32: Final[str] = "f"
    F64: Final[str] = "d"

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

    def __init__(self, _format: str) -> None:
        self._struct = struct.Struct(f"<{_format}")

    @abstractmethod
    def pack(self, value: T) -> bytes:
        """Упаковать значение в соответсвующее байтовое представление"""

    @abstractmethod
    def unpack(self, buffer: bytes) -> T:
        """Получить значение из соответствующего байтового представления"""

    def getSize(self) -> int:
        """Получить размер данных в байтах"""
        return self._struct.size

    def getFormat(self) -> str:
        """Получить спецификатор формата"""
        return self._struct.format.strip("<").strip(">")


class Primitive[T: (int | float | bool)](Binary[T]):
    """Примитивные типы"""

    def pack(self, value: T) -> bytes:
        return self._struct.pack(value)

    def unpack(self, buffer: bytes) -> T:
        return self._struct.unpack(buffer)[0]

    def __str__(self) -> str:
        return f"{_Format.matchPrefix(self.getFormat())}{self.getSize() * 8}"


class Struct[T: TypedDict](Binary[T]):
    """Объединение нескольких примитивов"""

    def __init__(self, fields: Sequence[Primitive]) -> None:
        super().__init__(''.join(map(lambda f: f.getFormat(), fields)))
        self._fields = fields

    def unpack(self, buffer: bytes) -> T:
        return self._struct.unpack(buffer)

    def pack(self, fields: T) -> bytes:
        return self._struct.pack(*fields)

    def __str__(self) -> str:
        return f"{{{', '.join(map(str, self._fields))}}}"


class Struct2[T: NamedTuple](Binary[T]):
    """Объединение нескольких примитивов для работы с NamedTuple."""

    def __init__(self, cls: type[T]) -> None:
        """
        cls: NamedTuple, описывающий структуру.
        """
        if not issubclass(cls, NamedTuple):
            raise TypeError(f"{cls.__name__} должен быть подклассом NamedTuple.")

        self.cls = cls

        self._fields = self._create_primitives(cls)

        super().__init__(''.join(field.getFormat() for field in self._fields))

    @staticmethod
    def _check_primitive(name: str, p: Primitive) -> Primitive:
        if not isinstance(p, Primitive):
            raise ValueError(f"Тип {p} не поддерживается для {name}")

        return p

    def _create_primitives(self, cls: type[T]) -> Sequence[Primitive]:
        """Создает список примитивов на основе аннотаций NamedTuple."""
        return [
            self._check_primitive(name, _type)
            for name, _type in get_type_hints(cls).items()
        ]

    def pack(self, value: T) -> bytes:
        """Упаковывает экземпляр NamedTuple в байты."""
        if not isinstance(value, self.cls):
            raise TypeError(f"Ожидался объект типа {self.cls.__name__}, получен {type(value).__name__}")

        # Используем _fields из NamedTuple
        # noinspection PyProtectedMember
        values = tuple(getattr(value, field) for field in self.cls._fields)
        return self._struct.pack(*values)

    def unpack(self, buffer: bytes) -> T:
        """Распаковывает байты в экземпляр NamedTuple."""
        return self.cls(*(self._struct.unpack(buffer)))

    @classmethod
    def from_namedtuple(cls, namedtuple_cls: Type[T]):
        """Создаёт Struct на основе NamedTuple."""
        return cls(namedtuple_cls)


u8 = Primitive[int | bool](_Format.U8)
u16 = Primitive[int](_Format.U16)
u32 = Primitive[int](_Format.U32)
u64 = Primitive[int](_Format.U64)

i8 = Primitive[int](_Format.I8)
i16 = Primitive[int](_Format.I16)
i32 = Primitive[int](_Format.I32)
i64 = Primitive[int](_Format.I64)

f32 = Primitive[float](_Format.F32)
f64 = Primitive[float](_Format.F64)


def _test():

    class MyStruct(NamedTuple):
        a: u32
        b: u16
        c: u8

    s = Struct2(MyStruct)

    v = bytes((0xA4, 0xA3, 0xA2, 0xA1, 0xB2, 0xB1, 0x69,))
    r = s.unpack(v)
    print(r)

    # print(f"{s=!s}")
    #
    #
    # m = s.unpack(v)
    # print(", ".join(map(hex, m)))
    # v1 = s.pack(m)
    #
    # print(", ".join(map(hex, v1)))


if __name__ == '__main__':
    _test()
