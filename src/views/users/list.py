from datetime import timedelta
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
from PyQt6.QtCore import QDateTime
from src.config import TODAY

import src.models as m
import src.schemas as s
from src.db import session
from src.views.table_model import TableModel
from src.widgets.datepicker import DatePickerWidget
from .create import UserCreateForm


# TODO: пагинация
class UserListView(QWidget):

    def __init__(self):
        super().__init__()

        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        filters_layout = QHBoxLayout()

        controls = QWidget()
        controls.setLayout(controls_layout)
        filters = QWidget()
        filters.setLayout(filters_layout)

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

        self.from_date_filter = DatePickerWidget(
            "Создан (От)", self.from_date, self.set_from_date
        )
        self.to_date_filter = DatePickerWidget(
            "Создан (До)", self.to_date, self.set_to_date
        )

        filters_layout.addWidget(self.from_date_filter)
        filters_layout.addWidget(self.to_date_filter)

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "Фамилия",
            "Имя",
            "Номер телефона",
            "Звание",
            "Дата создания",
            "Дата обновления",
        ]
        self.fetch_data()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(filters)
        layout.addWidget(self.table_view)

        search_button.clicked.connect(self.fetch_data)
        reset_button.clicked.connect(self.reset)
        add_button.clicked.connect(self.show_create_form)

    def fetch_data(self):
        keyword = self.search_input.text()
        query = sa.select(m.User).order_by(m.User.last_name)

        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.casefold(m.User.first_name).contains(keyword),
                    sa.func.casefold(m.User.last_name).contains(keyword),
                    sa.func.casefold(m.User.phone_number).contains(keyword),
                )
            )

        query = query.filter(
            sa.and_(
                m.User.created >= self.from_date.toPyDateTime(),
                m.User.created < self.to_date.toPyDateTime() + timedelta(days=1),
            )
        )
        results = session.scalars(query)
        table_model = TableModel(
            data=[list(s.UserListItem.from_obj(obj)) for obj in results],
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

    def reset(self):
        self.search_input.clear()
        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY
        self.from_date_filter.datepicker.setDateTime(self.from_date)
        self.to_date_filter.datepicker.setDateTime(self.to_date)
        self.fetch_data()

    def set_from_date(self, dt: QDateTime):
        self.from_date = dt
        self.fetch_data()

    def set_to_date(self, dt: QDateTime):
        self.to_date = dt
        self.fetch_data()

    def show_create_form(self):
        self.create_form = UserCreateForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()
