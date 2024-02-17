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
from src.db import session
from src.schemas import MaterialEvidenceListItem, CaseSelectItem
from src.views.table_model import TableModel
from src.widgets import FilterWidget, DatePickerWidget
from .create import MaterialEvidenceCreateForm
from .edit import MaterialEvidenceEditForm


# TODO: пагинация
class MaterialEvidenceListView(QWidget):

    def __init__(self):
        super().__init__()

        self.case_id = None

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

        self.case_filter = FilterWidget("Дело", m.Case, CaseSelectItem, self.set_case)
        self.from_date_filter = DatePickerWidget(
            "Создан (От)", self.from_date, self.set_from_date
        )
        self.to_date_filter = DatePickerWidget(
            "Создан (До)", self.to_date, self.set_to_date
        )

        filters_layout.addWidget(self.case_filter)
        filters_layout.addWidget(self.from_date_filter)
        filters_layout.addWidget(self.to_date_filter)

        self.table_view = QTableView()

        self.headers = [
            "",
            "Наименование",
            "Дело",
            "Статус",
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
        keyword = self.search_input.text().lower()
        query = sa.select(m.MaterialEvidence)

        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.casefold(m.MaterialEvidence.name).contains(keyword),
                    sa.func.casefold(m.MaterialEvidence.description).contains(keyword),
                )
            )

        if self.case_id:
            query = query.filter(m.MaterialEvidence.case_id == self.case_id)

        query = query.filter(
            sa.and_(
                m.MaterialEvidence.active.is_(True),
                m.MaterialEvidence.created >= self.from_date.toPyDateTime(),
                m.MaterialEvidence.created
                < self.to_date.toPyDateTime() + timedelta(days=1),
            )
        )
        query = query.order_by(m.MaterialEvidence.name)
        results = session.scalars(query)
        data = [list(MaterialEvidenceListItem.from_obj(obj)) for obj in results.all()]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

        for i in range(len(data)):
            me_id = data[i][0][1]
            button = QPushButton("✏️")
            button.clicked.connect(lambda: self.show_edit_form(me_id))
            self.table_view.setIndexWidget(table_model.index(i, 0), button)

    def reset(self):
        self.search_input.clear()

        self.case_id = None

        self.from_date = TODAY.addMonths(-1)
        self.to_date = TODAY

        self.case_filter.select.setCurrentIndex(-1)

        self.from_date_filter.datepicker.setDateTime(self.from_date)
        self.to_date_filter.datepicker.setDateTime(self.to_date)

        self.fetch_data()

    def set_case(self, case_id: int):
        self.case_id = case_id
        self.fetch_data()

    def set_from_date(self, dt: QDateTime):
        self.from_date = dt
        self.fetch_data()

    def set_to_date(self, dt: QDateTime):
        self.to_date = dt
        self.fetch_data()

    def show_create_form(self):
        self.create_form = MaterialEvidenceCreateForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()

    def show_edit_form(self, me_id: int):
        self.edit_form = MaterialEvidenceEditForm(me_id)
        self.edit_form.on_save.connect(self.fetch_data)
        self.edit_form.show()
