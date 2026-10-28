from typing import Literal


type Identifier = Literal['Scopus', 'WoS']


class Result:
    def __init__(self) -> None:
        self._is_ok = False
        self._value: Identifier | None = None
        self._error_msg: str | None = ''


    def set_value(self, value: Identifier) -> None:
        self._is_ok = True
        self._value = value
        self._error_msg = None


    def set_error(self, msg: str) -> None:
        self._is_ok = False
        self._value = None
        self._error_msg = msg


    @property
    def is_ok(self) -> bool:
        return self._is_ok


    @property
    def value(self) -> Identifier | None:
        return self._value


    @property
    def error_msg(self) -> str | None:
        return self._error_msg
