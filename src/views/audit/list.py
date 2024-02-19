import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QFileDialog,
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
from src.report import export_to_xlsx
from src.views.table_model import TableModel


class AuditListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        export_xlsx_button = QPushButton("Экспорт в Excel")

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "ID объекта",
            "Таблица",
            "Название класса",
            "Действие",
            "Поля",
            "Данные",
            "Время",
            "Пользователь",
        ]
        self.refresh()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(export_xlsx_button)
        layout.addWidget(self.table_view)

        export_xlsx_button.clicked.connect(self.export_xlsx)

    def fetch_data(self):
        query = sa.select(m.AuditEntry).order_by(m.AuditEntry.created.desc())
        results = session.scalars(query)
        return results.all()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.AuditEntryListItem.from_obj(obj)) for obj in raw_data]

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
            s.AuditEntryListItem.from_obj(obj).model_dump(mode="json")
            for obj in raw_data
        ]
        rows = [list(d.values()) for d in dumped_data]
        return rows

    def get_file_path(self, file_type: str):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            DESKTOP_PATH + f"/audit.{file_type}",
            f"Файлы {file_type} (*.{file_type})",
        )
        return file_path

    def export_xlsx(self):
        file_path = self.get_file_path("xlsx")

        if not file_path:
            return

        rows = self.get_export_data()
        export_to_xlsx(headers=self.headers, rows=rows, file_path=file_path)
