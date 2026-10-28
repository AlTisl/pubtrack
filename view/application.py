from .main_window import MainWindow
from .ports import ViewModels
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from typing import Sequence


_main_window: MainWindow | None = None


def create_app(args: Sequence[str] | None = None) -> QApplication:
    params = args or []
    app = QApplication(params)
    return app


def create_main_window(app: QApplication, view_models: ViewModels) -> None:
    icon = QIcon(r'./resources/images/Icon.ico')
    app.setWindowIcon(icon)
    global _main_window
    _main_window = MainWindow('PubTrack', view_models, icon)
    _main_window.show()
