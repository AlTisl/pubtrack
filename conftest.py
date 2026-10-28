import pytest
from unittest.mock import Mock
from view_model.add_pubs_view_model import AddPubsViewModel
from view_model.ports import CsvReaderProtocol


# из US-01#Обязательные поля в загружаемых файлах
SCOPUS_FIELDS = ['Title', 'Year', 'Source title', 'DOI',
                 'ISBN', 'ISSN', 'Language of Original Document',
                 'Document Type', 'Link', 'Authors', 'Author(s) ID']

WOS_FIELDS = ['TI', 'PY', 'SO', 'DI', 'SN', 'EI', 'BN',
              'LA', 'DT', 'UT', 'AF', 'RI']

@pytest.fixture
def reader():
    reader = Mock(spec=CsvReaderProtocol)
    reader.rows_count = 1
    return reader


@pytest.fixture
def vm(reader):
    return AddPubsViewModel(reader)