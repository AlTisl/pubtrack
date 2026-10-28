from .add_pubs_table_model import AddPubsTableModel
from .ports import CsvReaderProtocol
from custom_typing import Result
from model.structures import ScopusPublication, WosPublication
from pathlib import Path
from PySide6.QtCore import QObject, Signal


class AddPubsViewModel(QObject):
    def __init__(self, file_reader: CsvReaderProtocol, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._file_reader = file_reader
        self._indexer = Result()
        self._table_model = AddPubsTableModel()


    @property
    def file_path(self) -> Path:
        if self._file_reader.file_path is None:
            raise Exception('File should be given.')
        return self._file_reader.file_path

    @file_path.setter
    def file_path(self, path: Path) -> None:
        self._file_reader.file_path = path
        self._table_model.table_data = []


    @property
    def table_model(self) -> AddPubsTableModel:
        return self._table_model


    def _supported_file_type(self) -> bool:
        supported = self._file_reader.is_supported
        if not supported:
            self._indexer.set_error('File of this type is not supported.')
            self.file_verified.emit(self._indexer, -1)
        return supported


    def verify_file_structure(self) -> None:
        if not self._supported_file_type():
            return
        fieldnames = self._file_reader.fieldnames or []
        scopus_diff = ScopusPublication.required_fields() - set(fieldnames)
        wos_diff = WosPublication.required_fields() - set(fieldnames)
        difference = wos_diff if len(wos_diff) < len(scopus_diff) else scopus_diff
        if len(difference) > 0:
            self._indexer.set_error(f'Fields are missed: {", ".join(difference)}.')
            self.file_verified.emit(self._indexer, -1)
        else:
            self._indexer.set_value('WoS' if len(wos_diff) == 0 else 'Scopus')
            self.file_verified.emit(self._indexer, self._file_reader.rows_count)


    def get_publications(self) -> None:
        pub_class = {'Scopus': ScopusPublication, 'WoS': WosPublication}
        if self._indexer.value is not None:
            data = self._file_reader.read()
            self.table_model.table_data = (pub_class[self._indexer.value](record) for record in data)


    file_verified = Signal(object, int)
