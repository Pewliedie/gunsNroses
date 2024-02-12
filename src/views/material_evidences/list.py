import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QLabel,
)
from PyQt6.QtCore import Qt

import src.models as m
from src.db import session
from src.schemas import MaterialEvidenceListItem, CaseSelectItem
from src.views.table_model import TableModel
from src.widgets import FilterWidget
from .create import MaterialEvidenceForm


# TODO: Фильтрация, пагинация
class MaterialEvidenceListView(QWidget):

    def __init__(self):
        super().__init__()

        self.scanned_barcode = ""

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        filters_layout = QHBoxLayout()

        self.barcode_label = QLabel("Сканированный штрихкод: Н/Д")

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

        case_filter = FilterWidget("Дело", m.Case, CaseSelectItem)
        filters_layout.addWidget(case_filter)

        self.table_view = QTableView()

        self.headers = [
            "ID",
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
        layout.addWidget(self.barcode_label)
        layout.addWidget(self.table_view)

        search_button.clicked.connect(self.search)
        reset_button.clicked.connect(self.reset)
        add_button.clicked.connect(self.show_create_form)

    def fetch_data(self, keyword: str | None = None):
        query = sa.select(m.MaterialEvidence)
        if keyword:
            query = query.filter(
                sa.or_(
                    sa.func.lower(m.MaterialEvidence.name).contains(keyword),
                    sa.func.lower(m.MaterialEvidence.description).contains(keyword),
                )
            )
        query = query.order_by(m.MaterialEvidence.name)
        results = session.scalars(query)
        self.table_model = TableModel(
            data=[list(MaterialEvidenceListItem.from_obj(obj)) for obj in results],
            headers=self.headers,
        )
        self.table_view.setModel(self.table_model)

    def search(self):
        keyword = self.search_input.text().lower()
        if keyword:
            self.fetch_data(keyword)

    def reset(self):
        self.search_input.clear()
        self.fetch_data()

    def show_create_form(self):
        self.create_form = MaterialEvidenceForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()
