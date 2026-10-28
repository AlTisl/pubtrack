from abc import ABC, abstractmethod
from typing import Dict


class Publication(ABC):
    _required_fields: set[str]

    @classmethod
    def required_fields(cls) -> set[str]:
        return cls._required_fields


    @staticmethod
    @abstractmethod
    def merge_identifiers(record: Dict[str, str]) -> Dict[str, str]:
        pass


class ScopusPublication(Publication):
    _required_fields = {'Title', 'Year', 'Source title', 'DOI', 'ISSN', 'ISBN',
                       'Language of Original Document', 'Document Type',
                       'Link', 'Authors', 'Author(s) ID'}

    def __init__(self, record: Dict[str, str]):
        self.authors = record['Authors']
        self.title = record['Title']
        self.p_type = record['Document Type']
        self.doi = record.get('DOI')
        self.source = record['Source title']
        self.identifiers = self.merge_identifiers(record)
        self.year = int(record['Year'])
        self.lang = record.get('Language of Original Document')


    @staticmethod
    def merge_identifiers(record: Dict[str, str]) -> Dict[str, str]:
            result = {}
            for key in ('ISBN', 'ISSN', 'eISSN'):
                value = record.get(key, '')
                if value != '':
                    result[key] = value
            return result


class WosPublication(Publication):
    _required_fields = {'TI', 'PY', 'SO', 'DI', 'SN', 'EI', 'BN',
                       'LA', 'DT', 'UT', 'AF', 'RI'}

    def __init__(self, record: Dict[str, str]):
        self.authors = record['AF']
        self.title = record['TI']
        self.p_type = record['DT']
        self.doi = record.get('DI')
        self.source = record['SO']
        self.identifiers = self.merge_identifiers(record)
        self.year = int(record['PY'])
        self.lang = record.get('LA')
        self.indexer = record['UT'].split(':')[0]


    @staticmethod
    def merge_identifiers(record: Dict[str, str]) -> Dict[str, str]:
            result = {}
            categories = {'BN': 'ISBN', 'SN': 'ISSN', 'EI': 'eISSN'}
            for key in categories.keys():
                value = record.get(key, '')
                if value != '':
                    result[categories[key]] = value
            return result
