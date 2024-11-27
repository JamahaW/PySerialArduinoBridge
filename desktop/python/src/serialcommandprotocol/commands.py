from dataclasses import dataclass
from enum import IntEnum
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type

from serial.serialutil import SerialBase

from serialcommandprotocol.primitive import Primitive


@dataclass(frozen=True)
class Result[T: IntEnum]:
    enum_type: Type[T]
    ok_code: T
    primitive_type: Primitive

    def read(self, serial: SerialBase) -> T:
        return self.enum_type(self.primitive_type.unpack(serial.read(self.primitive_type.getSizeBytes())))

    def __repr__(self) -> str:
        return f"{self.enum_type.__name__}<{self.primitive_type}>"


@dataclass(frozen=True)
class Command[ReturnType: (int, bool, float), ResultType: IntEnum]:
    """
    Команда, отсылаемая в порт
    """

    result: Result[ResultType]
    code: bytes
    signature: Optional[Sequence[Primitive]]
    return_type: Optional[Primitive]

    def pack(self, *args) -> bytes:
        """
        Скомпилировать команду в набор байт
        :param args: аргументы команды. (Их столько же, и такого же типа, что и сигнатура команды)
        :return:
        """
        if self.signature is None:
            return self.code

        return self.code + b"".join(primitive.pack(arg) for primitive, arg in zip(self.signature, args))

    def unpack(self, buffer: bytes) -> ReturnType:
        return self.return_type.unpack(buffer)

    def send(self, serial: SerialBase, *args) -> Tuple[ResultType, Optional[ReturnType]]:
        serial.write(self.pack(args))
        result_code = self.result.read(serial)

        if result_code != self.result.ok_code or self.return_type is None:
            return result_code, None

        return result_code, self.unpack(serial.read(self.return_type.getSizeBytes()))

    def __getSignatureString(self) -> str:
        return "" if self.signature is None else ", ".join(map(str, self.signature))

    def __getResultTypeString(self) -> str:
        return f"({self.result}, {self.return_type})"

    def __str__(self) -> str:
        return f"command<0x{self.code.hex()}>({self.__getSignatureString()}) -> {self.__getResultTypeString()}"


if __name__ == '__main__':
    class ExampleResult(IntEnum):
        OK = 0x00


    print(Command(
        Result(ExampleResult, ExampleResult.OK, Primitive.u8),
        Primitive.u8.pack(0x69),
        (Primitive.u8, Primitive.f32),
        Primitive.u32
    ))
