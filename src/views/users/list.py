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
import src.schemas as s
from src.db import session
from src.views.table_model import TableModel
from .create import UserCreateForm


# TODO: Фильтрация, пагинация
class UserListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        controls = QWidget()
        controls.setLayout(controls_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите ключевое слово для поиска...")
        self.search_input.setClearButtonEnabled(True)

        search_button = QPushButton("Поиск")
        reset_button = QPushButton("Сбросить")
        add_button = QPushButton("Добавить")

        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(reset_button)
        controls_layout.addWidget(add_button)

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "Фамилия",
            "Имя",
            "Номер телефона",
            "Пароль",
            "Звание",
            "Дата создания",
            "Дата обновления",
        ]
        self.fetch_data()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(self.table_view)

        search_button.clicked.connect(self.search)
        reset_button.clicked.connect(self.reset)
        add_button.clicked.connect(self.show_create_form)

    def fetch_data(self, keyword: str | None = None):
        query = sa.select(m.User).order_by(m.User.last_name)
        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.lower(m.User.first_name).contains(keyword),
                    sa.func.lower(m.User.last_name).contains(keyword),
                    sa.func.lower(m.User.phone_number).contains(keyword),
                )
            )
        results = session.scalars(query)
        table_model = TableModel(
            data=[list(s.UserListItem.from_obj(obj)) for obj in results],
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

    def search(self):
        keyword = self.search_input.text()
        if keyword:
            self.fetch_data(keyword)

    def reset(self):
        self.search_input.clear()
        self.fetch_data()

    def show_create_form(self):
        self.create_form = UserCreateForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()
