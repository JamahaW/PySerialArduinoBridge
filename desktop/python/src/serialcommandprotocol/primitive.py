from enum import Enum
from struct import Struct


class Primitive(Enum):
    """Примитивные типы"""

    i8 = Struct("b")
    """int8_t"""
    u8 = Struct("B")
    """uint8_t"""
    i16 = Struct("h")
    """int16_t"""
    u16 = Struct("H")
    """uint16_t"""
    i32 = Struct("l")
    """int32_t"""
    u32 = Struct("L")
    """uint32_t"""
    i64 = Struct("q")
    """int64_t"""
    u64 = Struct("Q")
    """uint64_t"""
    f32 = Struct("f")
    """float"""
    f64 = Struct("d")  # ! Не поддерживается на AVR
    """double"""

    def getSizeBytes(self) -> int:
        """Получить размер примитивного типа в байтах"""
        return self.value.size

    def pack(self, value: bool | int | float) -> bytes:
        """
        Упаковать значение в соответсвующее байтовое представление
        @param value:
        @return:
        """
        return self.value.pack(value)

    def unpack(self, buffer: bytes) -> bool | int | float:
        """
        Получить значение из соответствующего байтового представления
        @param buffer:
        @return:
        """
        return self.value.unpack(buffer)[0]

    def __getPrefix(self) -> str:
        if self in (self.f32, self.f64):
            return "f"

        if self.value.format.isupper():
            return "u"

        return "i"

    def __str__(self) -> str:
        return f"{self.__getPrefix()}{self.value.size * 8}"


if __name__ == '__main__':
    print("\n".join(map(str, Primitive)))
