import timeit
from typing import Callable

from arduino import ArduinoProtocol
from arduino import LED_BUILTIN
from arduino import OUTPUT
from serialcmd.streams.serials import Serial


def _launch() -> str:
    ports = Serial.getPorts()
    print(f"{ports=}")

    if len(ports) == 0:
        return "Нет доступных портов"

    arduino = ArduinoProtocol(Serial(ports[0], 115200))

    # print("\n".join(map(str, arduino.getCommands())))

    startup = arduino.begin()

    if startup != 0x01:
        return f"Недействительный код инициализации {startup=}"

    print(f"Пакет ответа инициализации ведомого устройства: {startup=}")

    #

    arduino.pinMode(LED_BUILTIN, OUTPUT)

    def _blink():
        arduino.digitalWrite(LED_BUILTIN, True)
        arduino.digitalWrite(LED_BUILTIN, False)

    def _test():
        # arduino.delay(500)

        print(arduino.millis())

        return

    def calc(f: Callable[[], None], n: int = 1000) -> float:
        return timeit.timeit(f, number=n) / n

    # t = calc(_blink)
    t = calc(_test, 10)
    print(f"{t * 1000.0} ms ({1 / t})")

    return "Успешное завершение"


if __name__ == '__main__':
    print(_launch())
