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


class SessionListView(QWidget):

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
        export_xlsx_button = QPushButton("Экспорт в Excel")
        export_pdf_button = QPushButton("Экспорт в PDF")

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
            "Пользователь",
            "Дата входа",
            "Дата выхода",
            "Время в программе (сек)",
        ]
        self.refresh()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(filters)
        layout.addWidget(self.table_view)

        search_button.clicked.connect(self.refresh)
        reset_button.clicked.connect(self.reset)
        export_xlsx_button.clicked.connect(self.export_xlsx)
        export_pdf_button.clicked.connect(self.export_pdf)

    def fetch_data(self):
        keyword = self.search_input.text()
        query = sa.select(m.Session).order_by(m.Session.login)

        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.casefold(m.Session.user).contains(keyword),
                )
            )

        query = query.filter(
            sa.and_(
                m.Session.login >= self.from_date.toPyDateTime(),
                m.Session.login < self.to_date.toPyDateTime() + timedelta(days=1),
            )
        )
        results = session.scalars(query)
        return results.all()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.SessionListItem.from_obj(obj)) for obj in raw_data]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

        return len(data)

    def reset(self):
        self.search_input.clear()

        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY

        self.from_date_filter.datepicker.setDateTime(self.from_date)
        self.to_date_filter.datepicker.setDateTime(self.to_date)

        self.refresh()

    def set_from_date(self, dt: QDateTime):
        self.from_date = dt
        self.refresh()

    def set_to_date(self, dt: QDateTime):
        self.to_date = dt
        self.refresh()

    def get_export_data(self):
        raw_data = self.fetch_data()
        dumped_data = [
            s.SessionExportItem.from_obj(obj).model_dump(mode="json") for obj in raw_data
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
