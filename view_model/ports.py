from pathlib import Path
from typing import Dict, Iterable, Protocol, Sequence


class CsvReaderProtocol(Protocol):
    @property
    def file_path(self) -> Path:
        ...

    @file_path.setter
    def file_path(self, path: Path) -> None:
        ...

    @property
    def is_supported(self) -> bool:
        ...

    @property
    def fieldnames(self) -> Sequence[str] | None:
        ...

    @property
    def rows_count(self) -> int:
        ...

    def read(self) -> Iterable[Dict[str, str]]:
        ...