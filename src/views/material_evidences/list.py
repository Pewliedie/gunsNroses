import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QComboBox
)

import src.models as m
from src.db import session
from src.schemas import MaterialEvidenceListItem
from src.views.table_model import TableModel
from .create import MaterialEvidenceForm


# TODO: Фильтрация, поиск, пагинация
class MaterialEvidenceListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        controls = QWidget()
        controls.setLayout(controls_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите ключевое слово для поиска...")
        self.combo_box = QComboBox()

        add_button = QPushButton("Добавить")
        search_button = QPushButton("Поиск")

        controls_layout.addWidget(self.combo_box)
        controls_layout.addWidget(self.search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(add_button)

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
        layout.addWidget(self.table_view)

        add_button.clicked.connect(self.show_create_form)
        self.search_input.textChanged.connect(self.filter_data)

    def fetch_data(self):
        query = sa.select(m.MaterialEvidence).order_by(m.MaterialEvidence.name)
        results = session.scalars(query)
        self.table_model = TableModel(
            data=[list(MaterialEvidenceListItem.from_obj(obj)) for obj in results],
            headers=self.headers,
        )
        self.table_view.setModel(self.table_model)
        self.combo_box.addItems(self.headers)

    def show_create_form(self):
        self.create_form = MaterialEvidenceForm()
        self.create_form.on_save.connect(self.fetch_data)
        self.create_form.show()

    def filter_data(self, text):
        if text:
            filter_column = self.combo_box.currentIndex()

            for i in range(self.table_model.rowCount(filter_column)):
                item = self.table_model.item(i, filter_column)
                if self.filter_row(item, text):
                    self.table_view.showRow(i)
                else:
                    self.table_view.hideRow(i)
        else:
            for i in range(self.table_model.rowCount(0)):
                self.table_view.showRow(i)

    def filter_row(self, item, text):
        return text in str(item)
