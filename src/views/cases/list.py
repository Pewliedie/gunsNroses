from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .table_model import TableModel
import src.models as m
from src.db import session
import sqlalchemy as sa
import src.schemas as s


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

        table = QTableView()
        data = self.list_cases()
        table_model = TableModel(data)
        table.setModel(table_model)

        layout.addWidget(controls)
        layout.addWidget(table)

    def list_cases(self):
        query = sa.select(m.Case).order_by(m.Case.created.desc())
        results = session.scalars(query)
        return [s.CaseOut.from_obj(obj) for obj in results]
