from custom_typing import Result
from pathlib import Path
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout, QFileDialog
from qfluentwidgets import FluentLabelBase, BodyLabel, TitleLabel, CardWidget

class FileSelectCard(CardWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self._file_name: Path | None = None
        self._file_name_label = BodyLabel('Файл не выбран', self)
        self._file_size_label = BodyLabel(self)
        self._identifier_label = TitleLabel(self)
        self._error_label = BodyLabel(self)
        self._error_label.setTextColor(QColor(255, 0, 0), QColor(255, 0, 0))
        self._error_label.setWordWrap(True)
        prompt = BodyLabel('Кликните, чтобы выбрать файл', self)
        card_layout = QVBoxLayout()
        file_info_layout = QHBoxLayout()
        file_info_layout.addWidget(self._file_name_label, stretch=1)
        file_info_layout.addWidget(self._file_size_label, stretch=0)
        self._status_layout = QStackedLayout()
        self._status_layout.addWidget(self._identifier_label)
        self._status_layout.addWidget(self._error_label)
        card_layout.addLayout(file_info_layout, stretch=1)
        card_layout.addLayout(self._status_layout, stretch=1)
        card_layout.addWidget(prompt, stretch=0)
        self.setLayout(card_layout)
        self._dialog = QFileDialog(self.parentWidget(),
                                  'Выбрать файл',
                                  filter='CSV файлы (*.csv *.tsv)',
                                  fileMode=QFileDialog.FileMode.ExistingFile)

        self.clicked.connect(self._dialog.exec)
        self._dialog.fileSelected.connect(self.set_file_name)
        self.file_selected.connect(self.show_file_info)


    @property
    def status_text(self) -> str:
        label = self._status_layout.currentWidget()
        assert isinstance(label, FluentLabelBase)
        return label.text()


    file_selected = Signal(Path)


    def set_file_name(self, path: str) -> None:
        self._file_name = Path(path)
        self.file_selected.emit(self._file_name)


    def show_file_info(self, path: Path):
        file_size = path.stat().st_size
        units = 'bytes'
        if file_size >= 1024:
            file_size = round(file_size / 1024)
            units = 'kbytes'
        self._file_name_label.setText(path.name)
        self._file_size_label.setText(f'{file_size} {units}')


    def set_status(self, status: Result):
        match status.is_ok:
            case True:
                assert status.value is not None
                self._identifier_label.setText(status.value)
                self._status_layout.setCurrentWidget(self._identifier_label)
            case False:
                assert status.error_msg is not None
                self._error_label.setText(status.error_msg)
                self._status_layout.setCurrentWidget(self._error_label)
