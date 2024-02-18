import sqlalchemy as sa
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QCompleter, QLabel, QVBoxLayout, QWidget

from src.db import session


class FilterWidget(QWidget):
    def __init__(self, label: str, model, schema, on_change):
        super().__init__()
        self.model = model
        self.schema = schema
        
        self.options = self.fetch_options()
        self.on_change = on_change

        option_items = [str(option) for option in self.options]

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(label)
        self.select = QComboBox()
        self.select.setEditable(True)
        self.select.addItems(option_items)

        completer = QCompleter(option_items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.select.setCompleter(completer)
        self.select.setCurrentIndex(-1)

        layout.addWidget(label)
        layout.addWidget(self.select)

        self.select.currentIndexChanged.connect(self.handle_change)

    def refresh(self):
        self.options = self.fetch_options()
        option_items = [str(option) for option in self.options]
        self.select.clear()
        self.select.addItems(option_items)
    
    def handle_change(self, index):
        if index == -1:
            return None
        self.on_change(self.options[index].id)

    def fetch_options(self):
        query = sa.select(self.model).where(self.model.active.is_(True))
        results = session.scalars(query)
        return [self.schema.from_obj(obj) for obj in results.all()]
