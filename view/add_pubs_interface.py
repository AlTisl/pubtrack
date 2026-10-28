from custom_typing import Result
from pathlib import Path
from PySide6.QtWidgets import QFrame, QGridLayout, QWidget
from qfluentwidgets import TableView
from .file_select_card import FileSelectCard
from .ports import AddPubsProtocol
from .stat_card import StatCard


class AddPubsInterface(QFrame):
    def __init__(self, text: str, view_model: AddPubsProtocol, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.view_model = view_model
        self.file_select = FileSelectCard()
        self.total_card = StatCard(title='Всего публикаций в файле',
                                   description='Общее количество распознанных записей '\
                                               'из загруженного файла'
                                   )
        self.new_card = StatCard(title='Новые публикации',
                                 description='Записи, отсутствующие в текущей базе данных'
                                 )
        self.complement_card = StatCard(title='Дополнения',
                                        description='Добавление нового индексатора '\
                                        'для существующих записей')
        self.table = self._init_table()
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.file_select, 0, 0)
        grid_layout.addWidget(self.total_card, 0, 1)
        grid_layout.addWidget(self.new_card, 0, 2)
        grid_layout.addWidget(self.complement_card, 0, 3)
        grid_layout.addWidget(self.table, 1, 0, 1, 4)
        grid_layout.setRowStretch(0, 0)     # высота строки 0 - по содержимому
        grid_layout.setRowStretch(1, 1)     # строка 1 занимает всё оставшееся пространство по вертикали
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setColumnStretch(3, 1)
        grid_layout.setVerticalSpacing(20)
        self.setLayout(grid_layout)

        self.file_select.file_selected.connect(self.validate_file)
        self.view_model.file_verified.connect(self.show_validating_results)
        self.total_card.clicked.connect(self.view_model.get_publications)

        self.setObjectName(f'altis1024@gmail.com/{text.replace(" ", "-")}')


    def _init_table(self) -> TableView:
        table = TableView()
        table.setShowGrid(True)
        table.setModel(self.view_model.table_model)
        table.horizontalHeader().setStretchLastSection(True)
        return table


    def validate_file(self, path: Path):
        self.view_model.file_path = path
        self.view_model.verify_file_structure()


    def show_validating_results(self, status: Result, rows_count: int):
        self.file_select.set_status(status)
        self.total_card.set_count(rows_count)
