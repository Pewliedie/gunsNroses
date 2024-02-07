from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from .table_model import TableModel
import src.models as m
from src.db import session
import sqlalchemy as sa
import src.schemas as s
from .create import CaseFormWidget

class CaseListView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        controls = QWidget()
        controls.setLayout(controls_layout)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Введите ключевое слово для поиска...")

        add_button = QPushButton("Добавить")
        search_button = QPushButton("Поиск")

        controls_layout.addWidget(search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(add_button)

        self.table_view = QTableView()

        self.headers = [
            "Следователь",
            "Дата создания",
            "Дата обновления",
        ]

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.fetch_data()

        layout.addWidget(controls)
        layout.addWidget(self.table_view)

        add_button.clicked.connect(self.show_create_form)

    def fetch_data(self):
        query = sa.select(m.Case).order_by(m.Case.created.desc())
        results = session.scalars(query)
        out_table_data =  [list(s.CaseOut.from_obj(obj)) for obj in results]
        table_model = TableModel(data=out_table_data, headers=self.headers)
        self.table_view.setModel(table_model)

    def show_create_form(self):
        self.create_form = CaseFormWidget()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()