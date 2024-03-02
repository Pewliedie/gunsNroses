from datetime import datetime

import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

import src.models as m
import src.schemas as s
from src.config import DESKTOP_PATH
from src.db import session
from src.report import export_to_pdf, export_to_xlsx
from src.views.table_model import TableModel

export_headers = [
    "Пользователь",
    "Дата входа",
    "Дата выхода",
    "Время сессии",
]


class SessionListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()

        controls = QWidget()
        controls.setLayout(controls_layout)

        export_xlsx_button = QPushButton("Экспорт в Excel")
        export_pdf_button = QPushButton("Экспорт в PDF")

        controls_layout.addWidget(export_xlsx_button)
        controls_layout.addWidget(export_pdf_button)

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "Пользователь",
            "Дата входа",
            "Дата выхода",
            "Время сессии",
        ]
        self.refresh()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(controls)
        layout.addWidget(self.table_view)

        export_xlsx_button.clicked.connect(self.export_xlsx)
        export_pdf_button.clicked.connect(self.export_pdf)

    def fetch_data(self):
        query = sa.select(m.Session).order_by(m.Session.login.desc())
        results = session.scalars(query)
        return results.all()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.SessionListItem.from_obj(obj)) for obj in raw_data]

        table_model = TableModel(
            data=data,
            headers=self.headers,
            hide_first_column=False,
        )
        self.table_view.setModel(table_model)

        return len(data)

    def get_export_data(self):
        raw_data = self.fetch_data()
        dumped_data = [
            s.SessionExportItem.from_obj(obj).model_dump(mode="json")
            for obj in raw_data
        ]
        rows = [list(d.values()) for d in dumped_data]
        return rows

    def get_file_path(self, file_type: str):
        filename = f"сессии-{datetime.now().strftime('%d-%m-%Y-%H-%M')}.{file_type}"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            DESKTOP_PATH + "/" + filename,
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
