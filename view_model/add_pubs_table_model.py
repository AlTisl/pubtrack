from model.structures import ScopusPublication
from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt, QAbstractTableModel
from typing import Any, Iterable, Sequence


class AddPubsTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self._data = []
        self._headers = ['Authors', 'Title', 'Type', 'DOI', 'Source', 'Identifiers', 'Language']


    @property
    def table_data(self) -> Sequence:
        return self._data


    @table_data.setter
    def table_data(self, data: Iterable[ScopusPublication]) -> None:
        self.beginResetModel()
        self._data = [self._transform_record(item) for item in data]
        self.endResetModel()


    def _transform_record(self, record: ScopusPublication) -> Sequence:
        return (record.authors, record.title, record.p_type, record.doi, record.source,
                '; '.join([f'{key}: {value}' for key, value in record.identifiers.items()]),
                record.lang)


    def rowCount(self, /, parent: QModelIndex | QPersistentModelIndex =QModelIndex()) -> int:
        return len(self._data)


    def columnCount(self, /, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._data[0]) if self._data else 0


    def data(self, index: QModelIndex | QPersistentModelIndex, /, role: int=Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
    

    def headerData(self, section: int, orientation: Qt.Orientation, /, role: int=Qt.ItemDataRole.DisplayRole) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            return str(section + 1)
