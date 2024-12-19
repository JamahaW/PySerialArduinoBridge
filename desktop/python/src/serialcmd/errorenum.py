from __future__ import annotations

from enum import IntEnum


class ErrorEnum(IntEnum):
    """Перечисление ошибок"""

    def getOk(self) -> ErrorEnum:
        """Получить код успешного значения"""
        return self.__class__(0)
