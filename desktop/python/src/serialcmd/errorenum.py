from __future__ import annotations

from enum import IntEnum


class ErrorEnum(IntEnum):
    """Перечисление ошибок"""

    @classmethod
    def getOk(cls) -> ErrorEnum:
        """Получить код успешного значения"""
        return cls(0)
