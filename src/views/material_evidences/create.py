import uuid
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QMessageBox,
)

import src.models as m
from src.db import session
from src.config import NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT, STATUS_LIST

from src.utils import printer_processor


class MaterialEvidenceCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить вещ.док")
        self.setMinimumSize(NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT)
        self.init_ui()

    def init_ui(self):
        name_label = QLabel("Наименование")
        self.name_input = QLineEdit()

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit()

        status_select_label = QLabel("Статус")
        self.status_select = QComboBox()
        self.status_select.addItems(STATUS_LIST)

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(status_select_label)
        layout.addWidget(self.status_select)

        layout.addWidget(save_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)

    def validate(self):
        error_messages = []

        if not self.name_input.text():
            error_messages.append("Наименование не может быть пустым")

        if not self.description_textarea.toPlainText():
            error_messages.append("Постановление не может быть пустым")

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False

        return True

    def on_print_error(self, message):
        QMessageBox.critical(self, "Печать QR-кода", message)

    def on_print_end(self):
        QMessageBox.information(self, "Печать QR-кода", "Печать завершена")

    def save(self):
        valid = self.validate()

        if not valid:
            return

        uuid_value = str(uuid.uuid4())
        material_evidence = m.MaterialEvidence(
            name=self.name_input.text(),
            description=self.description_textarea.toPlainText(),
            status=self.status_select.currentText(),
            barcode=uuid_value,
        )
        session.add(material_evidence)
        session.commit()

        self.on_save.emit()
        self.close()

        printer_processor.print_qr_code(
            material_evidence.barcode, self.on_print_end, self.on_print_error
        )
