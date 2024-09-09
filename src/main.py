from enum import Enum
from struct import Struct
from time import sleep
from typing import Final

from serial import Serial

INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
LED_BUILTIN = 13


class Primitives(Enum):
    """Примитивные типы"""

    i8 = Struct("b")
    u8 = Struct("B")

    i16 = Struct("h")
    u16 = Struct("H")

    i32 = Struct("l")
    u32 = Struct("L")

    i64 = Struct("q")
    I64 = Struct("Q")

    f32 = Struct("f")
    f64 = Struct("d")  # ! Не поддерживается на Arduino

    def pack(self, value: bool | int | float) -> bytes:
        return self.value.pack(value)

    def unpack(self, buffer: bytes) -> bool | int | float:
        return self.value.unpack(buffer)[0]


class Command:
    def __init__(self, code: int, signature: tuple[Primitives, ...]) -> None:
        self.__header: Final[bytes] = Primitives.u8.pack(code)
        self.__signature = signature

    def pack(self, *args) -> bytes:
        return self.__header + b"".join(primitive.pack(arg) for primitive, arg in zip(self.__signature, args))


class ArduinoConnection:

    def __init__(self, serial: Serial) -> None:
        self.serial = serial

        self.__pin_mode = Command(0x10, (Primitives.u8, Primitives.u8))
        self.__digital_write = Command(0x11, (Primitives.u8, Primitives.u8))
        self.__digital_read = Command(0x12, (Primitives.u8,))
        self.__delay_ms = Command(0x13, (Primitives.u32,))

    def pinMode(self, pin: int, mode: int) -> None:
        self.serial.write(self.__pin_mode.pack(pin, mode))

    def digitalWrite(self, pin: int, state: bool | int) -> None:
        self.serial.write(self.__digital_write.pack(pin, state))

    def digitalRead(self, pin: int) -> bool:
        self.serial.write(self.__digital_read.pack(pin))
        return Primitives.u8.unpack(self.serial.read())

    def delay(self, milliseconds: int) -> None:
        self.serial.write(self.__delay_ms.pack(milliseconds))
        sleep(0.001 * milliseconds)


def main() -> None:
    arduino = ArduinoConnection(Serial("COM10", 115200, timeout=10))

    sleep(2)

    arduino.digitalWrite(LED_BUILTIN, 1)
    arduino.delay(1000)
    arduino.digitalWrite(LED_BUILTIN, 0)
    arduino.delay(1000)

    arduino.serial.close()


if __name__ == '__main__':
    main()
