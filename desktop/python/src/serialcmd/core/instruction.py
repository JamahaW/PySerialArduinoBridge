from dataclasses import dataclass
from typing import Optional

from serialcmd.serializers import Serializable
from serialcmd.serializers import Serializer
from serialcmd.streams.abc import Stream


@dataclass(frozen=True)
class Instruction[T: Serializable]:
    """Инструкция"""

    code: bytes
    """Уникальный идентификатор инструкции"""
    signature: Optional[Serializer[T]]
    """Сигнатура входных аргументов инструкции"""
    name: str
    """Имя команды для отладки"""

    def send(self, stream: Stream, value: T) -> None:
        """Отправить инструкцию в поток"""
        stream.write(self.code)

        if self.signature is not None:
            self.signature.write(stream, value)

    def __str__(self) -> str:
        return f"{self.name}<{self.code.hex().upper()}>({self.signature})"


def _test():
    from serialcmd.serializers import Struct, u32, f32
    from serialcmd.streams.mock import MockStream
    from io import BytesIO

    v = Struct((u32, f32))
    i = Instruction[tuple[int, float]](b"", v, "test")

    b = BytesIO()
    s = MockStream(BytesIO(), b)

    i.send(s, (123456, 123.456))

    print(b.getvalue().hex())
    print(v.unpack(b.getvalue()))

    return


if __name__ == '__main__':
    _test()
