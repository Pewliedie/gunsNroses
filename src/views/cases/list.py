import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

import src.models as m
from src.db import session
from src.schemas import CaseListItem
from src.views.table_model import TableModel
from .create import CaseCreateForm


# TODO: Фильтрация, поиск, пагинация
class CaseListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        controls = QWidget()
        controls.setLayout(controls_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите ключевое слово для поиска...")

        add_button = QPushButton("Добавить")
        search_button = QPushButton("Поиск")

        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(add_button)

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "Наименование",
            "Следователь",
            "Дата создания",
            "Дата обновления",
        ]
        self.fetch_data()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(self.table_view)

        add_button.clicked.connect(self.show_create_form)

    def fetch_data(self):
        query = sa.select(m.Case).order_by(m.Case.created.desc())
        results = session.scalars(query)
        table_model = TableModel(
            data=[list(CaseListItem.from_obj(obj)) for obj in results],
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

    def show_create_form(self):
        self.create_form = CaseCreateForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()
