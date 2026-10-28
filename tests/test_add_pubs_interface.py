from custom_typing import Result
import pytest
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QStandardItemModel
from unittest.mock import Mock
from view.add_pubs_interface import AddPubsInterface


class FakeViewModel(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.table_model = QStandardItemModel()
        self.verify_file_structure = Mock()
        self.get_publications = Mock()
        self.file_path = None

    file_verified = Signal(object, int)


@pytest.fixture
def fake_vm():
    return FakeViewModel()

@pytest.fixture
def interface(qtbot, fake_vm):
    widget = AddPubsInterface('Add pubs', fake_vm)
    qtbot.addWidget(widget)
    return widget


@pytest.mark.us_01(criteria='2')
@pytest.mark.parametrize('msg, is_ok', [('Error description', False),
                                        ('Scopus', True)])
def test_fs_card_shows_correct_status_text(interface, msg, is_ok):
    indexer = Result()
    if is_ok:
        indexer.set_value(msg)
    else:
        indexer.set_error(msg)

    assert not interface.file_select.status_text
    interface.view_model.file_verified.emit(indexer, 0)
    assert interface.file_select.status_text == msg


def test_file_selected_event_passes_path_to_vm(tmp_path, interface, fake_vm):
    path = tmp_path / 'sample.csv'
    path.write_text('')
    path_at_verification = []
    fake_vm.verify_file_structure.side_effect = lambda: path_at_verification.append(fake_vm.file_path)
    interface.file_select.file_selected.emit(path)

    # Проверяем, что `verify_file_structure()` вызывается один раз (в массиве будет один элемент)
    # и на момент этого вызова `file_path` уже содержит значение `path`
    assert path_at_verification == [path]


def test_fs_card_switches_between_indexer_and_error(interface):
    indexer = Result()
    data = ((indexer.set_value, 'Scopus'),
            (indexer.set_error, 'Some error occured.'),
            (indexer.set_value, 'WoS'))
    # имитируем валидный файл -> невалидный -> валидный
    for method, arg in data:
        method(arg) # type: ignore
        interface.view_model.file_verified.emit(indexer, 0)
        assert interface.file_select.status_text == arg


@pytest.mark.us_01(criteria='4')
@pytest.mark.parametrize('count, text', [(10, '10'), (0, '0'), (-1, '---')])
def test_total_card_shows_rows_count(interface, count, text):
    interface.view_model.file_verified.emit(Result(), count)
    assert interface.total_card._count_label.text() == text


def test_total_card_click_calls_vm_method(qtbot, interface, fake_vm):
    qtbot.mouseClick(interface.total_card, Qt.MouseButton.LeftButton)
    fake_vm.get_publications.assert_called_once()
