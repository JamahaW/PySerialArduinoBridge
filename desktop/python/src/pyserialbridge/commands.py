from typing import Final

from pyserialbridge.primitives import Primitives


class Command:
    """
    Команда по порту

    Имеет свой код (Должен совпадать на slave устройстве)
    Сигнатуру аргументов (Должна совпадать на устройстве)
    """

    def __init__(self, code: int, signature: tuple[Primitives, ...]) -> None:
        self.header: Final[bytes] = Primitives.u8.pack(code)
        self.signature = signature

    def pack(self, *args) -> bytes:
        """
        Скомпилировать команду в набор байт
        :param args: аргументы команды. (Их столько же, и такого же типа, что и сигнатура команды)
        :return:
        """
        return self.header + b"".join(primitive.pack(arg) for primitive, arg in zip(self.signature, args))


class CacheableCommand(Command):

    def __init__(self, code: int, signature: tuple[Primitives, ...]):
        super().__init__(code, signature)
        self.__cache = dict[tuple, bytes]()

    def pack(self, *args) -> bytes:
        if (cached_command := self.__cache.get(args)) is not None:
            return cached_command

        self.__cache[args] = cached_command = super().pack(*args)
        return cached_command
