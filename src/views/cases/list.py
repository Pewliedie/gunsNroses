from datetime import datetime, timedelta

import sqlalchemy as sa
from PyQt6.QtCore import QDateTime, QEvent, Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMessageBox,
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
from src.utils import get_current_user
from src.views.cases.edit import CaseEditForm
from src.views.material_evidences.create import MaterialEvidenceCreateForm
from src.views.table_model import TableModel
from src.widgets import DatePickerWidget, FilterWidget, QRDialog

from .create import CaseCreateForm

export_headers = [
    "ID",
    "Наименование",
    "Следователь",
    "Вещ.доказательства",
    "Дата создания",
    "Дата обновления",
    "Активно",
]


class CaseListView(QWidget):

    def __init__(self):
        super().__init__()

        self.current_user = get_current_user()
        self.investigator_id = None
        self.barcode = ""

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
        add_material_evidence_button = QPushButton("Добавить вещ.док")
        search_by_qr_button = QPushButton("Найти по QR")
        export_xlsx_button = QPushButton("Экспорт в Excel")
        export_pdf_button = QPushButton("Экспорт в PDF")

        self.qr_dialog = QRDialog(self.handle_scan)

        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(reset_button)
        controls_layout.addWidget(add_button)
        controls_layout.addWidget(add_material_evidence_button)
        controls_layout.addWidget(search_by_qr_button)
        controls_layout.addWidget(export_xlsx_button)
        controls_layout.addWidget(export_pdf_button)

        self.investigator_filter = FilterWidget(
            "Следователь", m.User, s.UserSelectItem, self.set_investigator
        )

        self.from_date_filter = DatePickerWidget(
            "Создан (От)", self.from_date, self.set_from_date
        )
        self.to_date_filter = DatePickerWidget(
            "Создан (До)", self.to_date, self.set_to_date
        )

        if self.current_user.is_superuser:
            filters_layout.addWidget(self.investigator_filter)

        filters_layout.addWidget(self.from_date_filter)
        filters_layout.addWidget(self.to_date_filter)

        self.table_view = QTableView()
        self.headers = [
            "",
            "Наименование",
            "Следователь",
            "Дата создания",
            "Дата обновления",
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
        add_button.clicked.connect(self.show_create_form)
        add_material_evidence_button.clicked.connect(
            self.show_create_material_evidence_form
        )
        search_by_qr_button.clicked.connect(self.search_by_qr)
        export_xlsx_button.clicked.connect(self.export_xlsx)
        export_pdf_button.clicked.connect(self.export_pdf)

    def fetch_data(self):
        keyword = self.search_input.text()

        query = sa.select(m.Case)

        if not self.current_user.is_superuser:
            query = query.where(m.Case.investigator_id == self.current_user.id)

        if self.barcode:
            query = query.filter(
                m.Case.material_evidences.any(
                    m.MaterialEvidence.barcode == self.barcode.strip()
                )
            )

        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.casefold(m.Case.name).contains(keyword),
                    sa.func.casefold(m.Case.description).contains(keyword),
                )
            )

        if self.investigator_id:
            query = query.filter(m.Case.investigator_id == self.investigator_id)

        query = query.filter(
            sa.and_(
                m.Case.active.is_(True),
                m.Case.created >= self.from_date.toPyDateTime(),
                m.Case.created < self.to_date.toPyDateTime() + timedelta(days=1),
            )
        )

        query = query.order_by(m.Case.created.desc())
        results = session.scalars(query)
        return results.all()

    def refresh(self):
        raw_data = self.fetch_data()

        data = [list(s.CaseListItem.from_obj(obj)) for obj in raw_data]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )

        self.table_view.setModel(table_model)

        for i in range(len(data)):
            entity_id = data[i][0][1]
            button = QPushButton("✏️")
            button.clicked.connect(
                lambda _, case_id=entity_id: self.show_edit_form(case_id)
            )
            self.table_view.setIndexWidget(table_model.index(i, 0), button)

        return len(raw_data)

    def reset_params(self, ignore_barcode=False):
        self.search_input.clear()

        self.investigator_id = None

        if not ignore_barcode:
            self.barcode = ""

        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY

        self.investigator_filter.select.setCurrentIndex(-1)

        self.from_date_filter.datepicker.setDateTime(self.from_date)
        self.to_date_filter.datepicker.setDateTime(self.to_date)

    def reset(self):
        self.reset_params()
        self.refresh()

    def set_investigator(self, investigator_id: int):
        self.investigator_id = investigator_id
        self.refresh()

    def set_from_date(self, dt: QDateTime):
        self.from_date = dt
        self.refresh()

    def set_to_date(self, dt: QDateTime):
        self.to_date = dt
        self.refresh()

    def show_create_form(self):
        self.create_form = CaseCreateForm()
        self.create_form.on_save.connect(self.refresh)
        self.create_form.show()

    def show_edit_form(self, case_id: int):
        self.edit_form = CaseEditForm(case_id)
        self.edit_form.on_save.connect(self.refresh)
        self.edit_form.show()

    def show_create_material_evidence_form(self):
        self.create_form = MaterialEvidenceCreateForm()
        self.create_form.on_save.connect(self.refresh)
        self.create_form.show()

    def get_export_data(self):
        raw_data = self.fetch_data()
        dumped_data = [
            s.CaseExportItem.from_obj(obj).model_dump(mode="json") for obj in raw_data
        ]
        rows = [list(d.values()) for d in dumped_data]
        return rows

    def get_file_path(self, file_type: str):
        filename = f"дела-{datetime.now().strftime('%d-%m-%Y-%H-%M')}.{file_type}"
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

    def handle_scan(self, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                if not self.barcode:
                    QMessageBox.critical(self, "Поиск по QR", "Пустое значение")
                    self.qr_dialog.close()
                    return

                self.reset_params(ignore_barcode=True)
                count = self.refresh()

                self.barcode = ""
                self.qr_dialog.close()

                message = (
                    f"Найдено {count} запись(-и/-ей)"
                    if count
                    else "Нет доступа или ничего не найдено"
                )

                QMessageBox.information(self, "Поиск по QR", message)
                return
            elif event.text():
                self.barcode += event.text()

    def search_by_qr(self):
        self.qr_dialog.exec()
