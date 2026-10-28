from conftest import SCOPUS_FIELDS, WOS_FIELDS
from custom_typing import Result
import pytest
import re
from unittest.mock import PropertyMock


REAL_SCOPUS_FIELDS = ['Authors', 'Author full names', 'Author(s) ID',
                      'Title', 'Year', 'Source title', 'Volume', 'Issue',
                      'Art. No.', 'Page start', 'Page end', 'DOI', 'Link',
                      'Affiliations', 'Authors with affiliations', 'Publisher',
                      'ISSN', 'ISBN', 'CODEN', 'Language of Original Document',
                      'Document Type', 'Publication Stage', 'Source']

REAL_WOS_FIELDS = ['PT', 'AU', 'BA', 'BE', 'GP', 'AF', 'BF', 'CA', 'TI', 'SO',
                   'SE', 'BS', 'LA', 'DT', 'CT', 'CY', 'CL', 'SP', 'HO', 'DE',
                   'ID', 'AB', 'C1', 'C3', 'RP', 'EM', 'RI', 'OI', 'FU', 'FP',
                   'FX', 'CR', 'NR', 'TC', 'Z9', 'U1', 'U2', 'PU', 'PI', 'PA',
                   'SN', 'EI', 'BN', 'J9', 'JI', 'PD', 'PY', 'VL', 'IS', 'PN',
                   'SU', 'SI', 'MA', 'BP', 'EP', 'AR', 'DI', 'DL', 'D2', 'EA',
                   'PG', 'WC', 'WE', 'SC', 'GA', 'PM', 'OA', 'HC', 'HP', 'DA',
                   'UT']

# (fieldnames, is_supported) для файлов, которые не должны проходить проверку
INVALID_FILE_CASES = [(SCOPUS_FIELDS, False),
                      (SCOPUS_FIELDS[:-1], True),
                      (None, True)]


def mentions_field(text: str, field: str) -> bool:
    # `re.escape(field)` нужно для экранирования скобок в 'Author(s) ID'.
    # `(?<!\w)` и `(?!\w)` означают отсутствие \w до и после `field` соответственно
    # (замена `\b`, если `field` может начинаться или заканчиваться спецсимволом).
    return re.search(rf'(?<!\w){re.escape(field)}(?!\w)', text) is not None


@pytest.mark.us_01(criteria='1')
def test_vm_supported_file_type_read_fields(vm, reader):
    fieldnames = PropertyMock(return_value=[])
    type(reader).fieldnames = fieldnames
    reader.is_supported = True
    vm.verify_file_structure()

    # Переменная `fieldnames` нужна, т. к. без неё при вызове свойства `fieldnames`
    # будет получен не `PropertyMock`, а его возвращаемое значение.
    fieldnames.assert_called_once()


@pytest.mark.us_01(criteria='1')
def test_vm_unsupported_file_type_not_read_fields(vm, reader):
    fieldnames = PropertyMock(return_value=[])
    type(reader).fieldnames = fieldnames
    reader.is_supported = False
    vm.verify_file_structure()

    fieldnames.assert_not_called()


@pytest.mark.us_01(criteria='1')
def test_vm_unsupported_file_type_emits_error(qtbot, vm, reader):
    reader.is_supported = False
    with qtbot.waitSignal(vm.file_verified,
                          check_params_cb=lambda x, _: x.is_ok is False and x.value is None):
        vm.verify_file_structure()


@pytest.mark.us_01(criteria='2')
@pytest.mark.parametrize('fields', [SCOPUS_FIELDS, WOS_FIELDS,
                                    REAL_SCOPUS_FIELDS, REAL_WOS_FIELDS])
def test_vm_accepts_import_file_with_fields(qtbot, vm, reader, fields):
    reader.is_supported = True
    reader.fieldnames = fields
    with qtbot.waitSignal(vm.file_verified,
                           check_params_cb=lambda x, y: x.is_ok is True and y == reader.rows_count):
        vm.verify_file_structure()


@pytest.mark.us_01(criteria='2')
@pytest.mark.parametrize('fields, missing', [(set(SCOPUS_FIELDS) - {'Link'}, {'Link'}),
                                    (set(WOS_FIELDS) - {'EI'}, {'EI'}),
                                    (set(SCOPUS_FIELDS) - {'Title', 'DOI'}, {'Title', 'DOI'}),
                                    (set(WOS_FIELDS) - {'AF', 'UT'}, {'AF', 'UT'}),
                                    (set(SCOPUS_FIELDS[:-3] + WOS_FIELDS[:3]), set(SCOPUS_FIELDS[-3:])),
                                    (set(SCOPUS_FIELDS[:3] + WOS_FIELDS[:-3]), set(WOS_FIELDS[-3:]))])
def test_error_points_out_missing_fields(qtbot, vm, reader, fields, missing):
    def check_error_msg(indexer: Result, count: int) -> bool:
        message = indexer.error_msg
        return (indexer.is_ok is False and
                message is not None and
                all(mentions_field(message, field) for field in missing) and
                # присутствующие в файле поля в сообщении упоминаться не должны
                not any(mentions_field(message, field) for field in fields))

    reader.is_supported = True
    reader.fieldnames = fields
    with qtbot.waitSignal(vm.file_verified, check_params_cb=check_error_msg):
        vm.verify_file_structure()


@pytest.mark.us_01(criteria='2')
@pytest.mark.parametrize('fields, is_supported', INVALID_FILE_CASES)
def test_vm_not_load_data_if_file_is_invalid(vm, reader, fields, is_supported):
    reader.is_supported = is_supported
    reader.fieldnames = fields
    vm.verify_file_structure()
    vm.get_publications()

    assert not vm.table_model.table_data
    reader.read.assert_not_called()


@pytest.mark.parametrize('fields, is_supported', INVALID_FILE_CASES)
def test_vm_reset_identifier_between_files_processing(qtbot, vm, reader, fields, is_supported):
    # сначала имитируем валидный файл
    reader.is_supported = True
    reader.fieldnames = SCOPUS_FIELDS
    with qtbot.waitSignal(vm.file_verified,
                          check_params_cb=lambda x, _: x.is_ok is True and x.value == 'Scopus'):
        vm.verify_file_structure()

    # После этого имитируем невалидный файл
    # и проверяем, что `identifier` сбрасывается между вызовами
    reader.is_supported = is_supported
    reader.fieldnames = fields
    with qtbot.waitSignal(vm.file_verified,
                          check_params_cb=lambda x, _: x.is_ok is False and x.value is None):
        vm.verify_file_structure()

    # и что после этого данные не загружаются
    vm.get_publications()
    assert not vm.table_model.table_data
    reader.read.assert_not_called()


@pytest.mark.us_01(criteria='3')
@pytest.mark.parametrize('fields, indexer, success', [(SCOPUS_FIELDS, 'Scopus', True),
                                                      (WOS_FIELDS, 'WoS', True),
                                                      (['a', 'b', 'c'], None, False)])
def test_vm_suggests_import_file_indexer(qtbot, vm, reader, fields, indexer, success):
    reader.is_supported = True
    reader.fieldnames = fields
    with qtbot.waitSignal(vm.file_verified, check_params_cb=lambda x, _: x.value == indexer and x.is_ok == success):
        vm.verify_file_structure()


@pytest.mark.us_01(criteria='4')
@pytest.mark.parametrize('fields', [set(SCOPUS_FIELDS) - {'Link'},
                                    set(WOS_FIELDS) - {'EI'},
                                    set(SCOPUS_FIELDS) - {'Title', 'DOI'},
                                    set(WOS_FIELDS) - {'AF', 'UT'},
                                    set(),
                                    None])
def test_vm_emits_negative_rows_count_if_missing_fields(qtbot, vm, reader, fields):
    reader.is_supported = True
    reader.fieldnames = fields

    with qtbot.waitSignal(vm.file_verified,
                          check_params_cb=lambda _, x: x < 0):
        vm.verify_file_structure()


@pytest.mark.us_01(criteria='4')
def test_vm_emits_negative_rows_count_for_unsupported_file(qtbot, vm, reader):
    reader.is_supported = False
    reader.fieldnames = SCOPUS_FIELDS

    with qtbot.waitSignal(vm.file_verified,
                          check_params_cb=lambda _, x: x < 0):
        vm.verify_file_structure()