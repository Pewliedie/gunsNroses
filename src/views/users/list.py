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


class UserListView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.create_form = CaseFormWidget()

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

        headers = [
            "Идентификатор",
            "Имя",
            "Фамилия",
            "Номер телефона",
            "Звание",
            "Создан",
            "Обновлен",
        ]

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        data = self.list_users()
        table_model = TableModel(data=data, headers=headers)
        table.setModel(table_model)

        layout.addWidget(controls)
        layout.addWidget(table)

        add_button.clicked.connect(self.show_create_form)

    def list_users(self):
        query = sa.select(m.User).order_by(m.User.first_name)
        results = session.scalars(query)
        return [list(s.UserOut.from_obj(obj)) for obj in results]

    def show_create_form(self):
        self.create_form.show()
