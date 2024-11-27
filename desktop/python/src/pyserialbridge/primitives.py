from enum import Enum
from struct import Struct


class Primitives(Enum):
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
    I64 = Struct("Q")
    """uint64_t"""
    f32 = Struct("f")
    """float"""
    f64 = Struct("d")  # ! Не поддерживается на Arduino
    """double"""

    def pack(self, value: bool | int | float) -> bytes:
        return self.value.pack(value)

    def unpack(self, buffer: bytes) -> bool | int | float:
        return self.value.unpack(buffer)[0]
