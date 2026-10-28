from .add_pubs_interface import AddPubsInterface
from .ports import ViewModels
from PySide6.QtGui import QIcon
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import FluentIcon as Icon


class MainWindow(MSFluentWindow):
    def __init__(self, title: str, view_models: ViewModels,
                 icon_path: QIcon | None = None) -> None:
        super().__init__()
        self.add_pubs_interface = AddPubsInterface('Add pubs interface',
                                                   view_models.add_pubs,
                                                   self)
        self._init_navigation()
        self._init_window(title, icon_path)


    def _init_navigation(self) -> None:
        self.addSubInterface(self.add_pubs_interface, Icon.ADD, 'Add pubs')
        self.navigationInterface.setCurrentItem(
            self.add_pubs_interface.objectName())


    def _init_window(self, title: str, icon: QIcon | None) -> None:
        self.setWindowTitle(title)
        if icon is not None:
            self.setWindowIcon(icon)
        self.setMinimumSize(800, 600)
        self.showMaximized()
