from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLayout, QVBoxLayout, QWidget
from qfluentwidgets import ElevatedCardWidget
from qfluentwidgets import FluentLabelBase, BodyLabel, StrongBodyLabel, TitleLabel

class StatCard(ElevatedCardWidget):
    _statuses = {
        'active': 'Режим активен',
        'inactive': 'Кликните, чтобы показать'
    }
    def __init__(self, title: str | None = None, description: str | None = None,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        card_layout = QVBoxLayout()
        self._title_label = StrongBodyLabel(self)
        self._count_label = TitleLabel(self)
        self._description_label = BodyLabel(self)
        self._status_label = StrongBodyLabel(self)
        self._init_label(self._title_label, card_layout, title.upper() if title else None, True)
        self._init_label(self._count_label,  card_layout)
        self._init_label(self._description_label, card_layout, description, True)
        self._init_label(self._status_label, card_layout, None, True)
        self.set_count(-1)
        self._is_active = False
        self._set_status(False)

        self.setLayout(card_layout)

        self.status_changed.connect(self._set_status)


    def _init_label(self, label: FluentLabelBase, layout: QLayout,
                    text: str | None = None, wrap: bool = False) -> None:
        if text is not None:
            label.setText(text)
        label.setWordWrap(wrap)
        layout.addWidget(label)


    status_changed = Signal(bool)


    def set_count(self, count: int):
        self._count_label.setText(str(count) if count >= 0 else '---')

    def _set_status(self, status: bool):
        status_str = 'active' if status else 'inactive'
        self._status_label.setText(self._statuses[status_str])


    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        if self._is_active != value:
            self._is_active = value
            self.status_changed.emit(self._is_active)
