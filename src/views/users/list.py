from datetime import timedelta

import sqlalchemy as sa
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

import src.models as m
import src.schemas as s
from src.config import DESKTOP_PATH, TODAY
from src.db import session
from src.report import export_to_pdf, export_to_xlsx
from src.views.table_model import TableModel
from src.widgets.datepicker import DatePickerWidget

from .create import UserCreateForm
from .edit import UserEditForm

export_headers = [
    "ID",
    "Фамилия",
    "Имя",
    "Номер телефона",
    "Звание",
    "Количество дел",
    "Дата создания",
    "Дата обновления",
    "Активен",
]


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
        export_xlsx_button = QPushButton("Экспорт в Excel")
        export_pdf_button = QPushButton("Экспорт в PDF")

        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(reset_button)
        controls_layout.addWidget(add_button)
        controls_layout.addWidget(export_xlsx_button)
        controls_layout.addWidget(export_pdf_button)

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
            "",
            "Фамилия",
            "Имя",
            "Номер телефона",
            "Звание",
            "Дата создания",
            "Дата обновления",
        ]
        self.refresh_table()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(filters)
        layout.addWidget(self.table_view)

        search_button.clicked.connect(self.refresh_table)
        reset_button.clicked.connect(self.reset)
        add_button.clicked.connect(self.show_create_form)
        export_xlsx_button.clicked.connect(self.export_xlsx)
        export_pdf_button.clicked.connect(self.export_pdf)

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
        return results.all()

    def refresh_table(self):
        raw_data = self.fetch_data()
        data = [list(s.UserListItem.from_obj(obj)) for obj in raw_data]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

        for i in range(len(data)):
            user_id = data[i][0][1]
            button = QPushButton("✏️")
            button.clicked.connect(lambda: self.show_edit_form(user_id))
            self.table_view.setIndexWidget(table_model.index(i, 0), button)

    def reset(self):
        self.search_input.clear()

        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY

        self.from_date_filter.datepicker.setDateTime(self.from_date)
        self.to_date_filter.datepicker.setDateTime(self.to_date)

        self.refresh_table()

    def set_from_date(self, dt: QDateTime):
        self.from_date = dt
        self.refresh_table()

    def set_to_date(self, dt: QDateTime):
        self.to_date = dt
        self.refresh_table()

    def show_create_form(self):
        self.create_form = UserCreateForm()
        self.create_form.on_save.connect(self.refresh_table)
        self.create_form.show()

    def show_edit_form(self, user_id: int):
        self.edit_form = UserEditForm(user_id)
        self.edit_form.on_save.connect(self.refresh_table)
        self.edit_form.show()

    def get_export_data(self):
        raw_data = self.fetch_data()
        dumped_data = [
            s.UserExportItem.from_obj(obj).model_dump(mode="json") for obj in raw_data
        ]
        rows = [list(d.values()) for d in dumped_data]
        return rows

    def get_file_path(self, file_type: str):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            DESKTOP_PATH + f"/users.{file_type}",
            f"Файлы {file_type} (*.{file_type})",
        )
        return file_path

    def export_xlsx(self):
        file_path = self.get_file_path("xlsx")

        if not file_path:
            return

        rows = self.get_export_data()
        export_to_xlsx(headers=export_headers, rows=rows, file_path=file_path)

    def export_pdf(self):
        file_path = self.get_file_path("pdf")

        if not file_path:
            return

        rows = self.get_export_data()
        export_to_pdf(headers=export_headers, rows=rows, file_path=file_path)
