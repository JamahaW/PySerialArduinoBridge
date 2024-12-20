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
    startup = arduino.begin()

    print(f"Пакет ответа инициализации ведомого устройства: {startup=}")

    if not startup:
        return "Недействительный код инициализации"

    arduino.pinMode(LED_BUILTIN, OUTPUT)

    for i in range(20):
        arduino.digitalWrite(LED_BUILTIN, i % 2 == 0)
        arduino.delay(500)

    return "Успешное завершение"


if __name__ == '__main__':
    print(_launch())
