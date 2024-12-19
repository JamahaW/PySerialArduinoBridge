from abc import ABC
from abc import abstractmethod


class Stream(ABC):
    """Абстрактный стрим ввода-вывода"""

    @abstractmethod
    def write(self, data: bytes) -> None:
        """Записать данные в поток вывода"""

    @abstractmethod
    def read(self, size: int = 1) -> bytes:
        """Считать данные из потока ввода"""
