from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import src.models as m
from src.config import DIALOG_MIN_HEIGHT, DIALOG_MIN_WIDTH
from src.db import session
from src.utils import get_current_user, printer_processor


class MaterialEvidenceCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_user = get_current_user()

        self.setWindowTitle("Добавить вещ.док")
        self.setMinimumSize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)

        self.init_ui()

    def init_ui(self):
        name_label = QLabel("Наименование")
        self.name_input = QLineEdit()

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit()

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(save_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)

    def validate(self):
        error_messages = []

        if not self.name_input.text():
            error_messages.append("Наименование не может быть пустым")

        if not self.description_textarea.toPlainText():
            error_messages.append("Описание не может быть пустым")

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

        material_evidence = m.MaterialEvidence(
            name=self.name_input.text(),
            description=self.description_textarea.toPlainText(),
            created_by_id=self.current_user.id,
        )

        session.add(material_evidence)
        session.commit()

        self.on_save.emit()
        self.close()

        printer_processor.print_qr_code(
            material_evidence.barcode, self.on_print_end, self.on_print_error
        )
