from struct import Struct
from time import sleep

from serial import Serial

INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2


class Arduino:
    __PIN_MODE = 0x10
    __DIGITAL_WRITE = 0x11
    __DIGITAL_READ = 0x12
    __DELAY_MS = 0x13

    def __init__(self, serial: Serial) -> None:
        self.serial = serial

        self.__bool = Struct("?")
        self.__u8 = Struct("B")
        self.__u32 = Struct("L")

    def pinMode(self, pin: int, mode: int) -> None:
        self.serial.write(self.__u8.pack(self.__PIN_MODE) + self.__u8.pack(pin) + self.__u8.pack(mode))

    def digitalWrite(self, pin: int, state: bool) -> None:
        self.serial.write(self.__u8.pack(self.__DIGITAL_WRITE) + self.__u8.pack(pin) + self.__bool.pack(state))

    def digitalRead(self, pin: int) -> bool:
        pass

    def delay(self, milliseconds: int) -> None:
        self.serial.write(self.__u8.pack(self.__DELAY_MS) + self.__u32.pack(milliseconds))
        sleep(0.001 * milliseconds)


def main() -> None:
    arduino = Arduino(Serial("COM10", 115200))

    sleep(0.5)

    arduino.pinMode(13, OUTPUT)

    for i in range(10):
        arduino.digitalWrite(13, True)
        arduino.delay(100)
        arduino.digitalWrite(13, False)
        arduino.delay(1000)

    arduino.serial.close()


if __name__ == '__main__':
    main()
