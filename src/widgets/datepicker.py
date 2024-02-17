from typing import Callable

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QDateEdit, QLabel, QVBoxLayout, QWidget


class DatePickerWidget(QWidget):
    def __init__(
        self, label: str, init_dt: QDateTime, on_change: Callable[[QDateTime], None]
    ):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(label)
        self.datepicker = QDateEdit()
        self.datepicker.setDisplayFormat("dd/MM/yyyy")
        self.datepicker.setCalendarPopup(True)
        self.datepicker.setDateTime(init_dt)

        layout.addWidget(label)
        layout.addWidget(self.datepicker)

        self.datepicker.dateTimeChanged.connect(on_change)
