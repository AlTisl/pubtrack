import csv
from model.csv_reader import CsvReader
from pathlib import Path
import pytest
from typing import Iterable


TEST_FIELDS = ['Title', 'Document Type', 'Author(s) ID']

TEST_ROWS = [['Paper, one', 'Article', '123'],  # запятая добавлена для проверки экранирования
             ['Статья два', 'Book chapter', '456'],
             ['Paper three', 'Доповідь з конференції', '789']]


@pytest.fixture
def make_file(tmp_path):
    def _make(name: str, fields: Iterable[str]=TEST_FIELDS, rows: Iterable[Iterable[str]]=TEST_ROWS,
              delimiter: str=',', encoding: str='utf-8') -> Path:
        path = tmp_path / name
        with open(path, 'w', newline='', encoding=encoding) as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(fields)
            writer.writerows(rows)
        return path
    return _make


@pytest.mark.us_01(criteria='1')
@pytest.mark.parametrize('ext, expected', [('.csv', True),
                                           ('.CSV', True),
                                           ('.tsv', True),
                                           ('.txt', False),
                                           ('.xlsx', False),
                                           ('', False)])
def test_reader_supports_given_file_types(ext, expected):
    reader = CsvReader()
    reader.file_path = Path(f'sample{ext}')

    assert reader.is_supported == expected


@pytest.mark.parametrize('name, delimiter, encoding', [('data.csv', ',', 'utf-8'),
                                                       ('data.csv', ',', 'utf-8-sig'),
                                                       ('data.tsv', '\t', 'utf-8'),
                                                       ('data.tsv', '\t', 'utf-8-sig'),
                                                       ('DATA.CSV', ',', 'utf-8-sig'),
                                                       ('DATA.TSV', '\t', 'utf-8-sig')])
def test_reader_reads_fields_and_rows(make_file, name, delimiter, encoding):
    reader = CsvReader()
    reader.file_path = make_file(name, delimiter=delimiter, encoding=encoding)

    assert reader.fieldnames == TEST_FIELDS
    assert reader.rows_count == len(TEST_ROWS)
    assert list(reader.read()) == [dict(zip(TEST_FIELDS, row)) for row in TEST_ROWS]


def test_reader_empty_file(tmp_path):
    path = tmp_path / 'empty.csv'
    path.write_text('')
    reader = CsvReader()
    reader.file_path = path

    assert not reader.fieldnames
    assert reader.rows_count == 0
