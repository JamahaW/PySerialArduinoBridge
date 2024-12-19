from dataclasses import dataclass
from typing import BinaryIO

from serialcmd.streams.abc import Stream


@dataclass
class MockStream(Stream):
    """Реализация-Затычка для тестов"""

    input: BinaryIO
    """Входной поток"""
    output: BinaryIO
    """Выходной поток"""

    def write(self, data: bytes) -> None:
        self.output.write(data)

    def read(self, size: int = 1) -> bytes:
        return self.input.read(size)
