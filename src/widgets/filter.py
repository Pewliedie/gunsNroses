import sqlalchemy as sa
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QCompleter, QLabel, QVBoxLayout, QWidget
from sqlalchemy import event

from src.db import session


class FilterWidget(QWidget):
    def __init__(self, label: str, model, schema, on_change):
        super().__init__()

        self.selected_id = None
        self.model = model
        self.schema = schema
        self.on_change = on_change

        self.entities = []
        self.items = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(label)

        self.select = QComboBox()
        self.select.setEditable(True)

        self.refresh_items()

        completer = QCompleter(self.items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.select.setCompleter(completer)
        self.select.setCurrentIndex(-1)

        layout.addWidget(label)
        layout.addWidget(self.select)

        self.select.currentIndexChanged.connect(self.handle_change)

        self.listen_model()

    def fetch(self):
        query = sa.select(self.model).where(self.model.active.is_(True))
        results = session.scalars(query)
        return [self.schema.from_obj(obj) for obj in results.all()]

    def refresh_items(self):
        self.entities = self.fetch()
        self.items = [str(o) for o in self.entities]
        self.select.clear()
        self.select.addItems(self.items)

    def handle_change(self, index):
        if index == -1:
            return None
        self.on_change(self.entities[index].id)

    def listen_model(self):
        event.listen(self.model, "after_insert", self.refresh_items)
        event.listen(self.model, "after_update", self.refresh_items)
        event.listen(self.model, "after_delete", self.refresh_items)
