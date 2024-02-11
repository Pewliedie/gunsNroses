import sqlalchemy as sa
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QComboBox

from src.db import session


class FilterWidget(QWidget):
    def __init__(self, label: str, model, schema):
        super().__init__()
        self.options = self.fetch_options(model, schema)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(label)
        self.select = QComboBox()
        self.select.addItems([str(option) for option in self.options])
        self.select.setCurrentIndex(-1)

        layout.addWidget(label)
        layout.addWidget(self.select)

    def fetch_options(self, model, schema):
        query = sa.select(model)
        results = session.scalars(query)
        return [schema.from_obj(obj) for obj in results]
