from model.csv_reader import CsvReader
from view.application import create_app, create_main_window
from view.ports import ViewModels
from view_model.add_pubs_view_model import AddPubsViewModel


def main() -> None:
    app = create_app()
    vm = ViewModels(add_pubs=AddPubsViewModel(file_reader=CsvReader())) # pyright: ignore[reportArgumentType]
    create_main_window(app, view_models=vm)
    app.exec()


if __name__ == '__main__':
    main()
