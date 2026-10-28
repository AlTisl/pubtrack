import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Iterable, Sequence


class CsvReader:
    def __init__(self) -> None:
        self._file_path: Path | None = None


    @property
    def file_path(self) -> Path:
        if self._file_path is None:
            raise Exception('File should be given.')
        return self._file_path

    @file_path.setter
    def file_path(self, path: Path) -> None:
        self._file_path = path


    @property
    def is_supported(self) -> bool:
        return self.file_path.suffix.lower() in ('.csv', '.tsv')


    @property
    def fieldnames(self) -> Sequence[str] | None:
        with open(self.file_path, newline='', encoding='utf-8-sig') as file:
            reader = self._create_reader(file)
            fieldnames = reader.fieldnames
        return fieldnames


    @property
    def rows_count(self) -> int:
        with open(self.file_path, newline='', encoding='utf-8-sig') as file:
            reader = self._create_reader(file)
            total_rows = sum(1 for _ in reader)
        return total_rows


    def _create_reader(self, file: TextIOWrapper) -> csv.DictReader[str]:
        if self.file_path.suffix.lower() == '.tsv':
            delimiter = '\t'
            return csv.DictReader(file, delimiter=delimiter)
        return csv.DictReader(file)


    def read(self) -> Iterable[Dict[str, str]]:
        with open(self.file_path, newline='', encoding='utf-8-sig') as file:
            reader = self._create_reader(file)
            rows = [row for row in reader]
        return rows
