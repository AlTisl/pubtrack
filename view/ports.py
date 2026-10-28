from dataclasses import dataclass
from pathlib import Path
from PySide6.QtCore import QAbstractItemModel, SignalInstance
from typing import Protocol


class AddPubsProtocol(Protocol):
    @property
    def file_path(self) -> Path:
        ...

    @file_path.setter
    def file_path(self, path: Path) -> None:
        ...

    @property
    def table_model(self) -> QAbstractItemModel:
        ...
    
    def verify_file_structure(self) -> None:
        ...

    def get_publications(self) -> None:
        ...

    file_verified: SignalInstance


@dataclass(frozen=True)
class ViewModels():
    add_pubs: AddPubsProtocol