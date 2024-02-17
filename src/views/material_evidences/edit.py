import sqlalchemy as sa
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import src.models as m
from src.config import DIALOG_MIN_HEIGHT, DIALOG_MIN_WIDTH, STATUS_LIST
from src.db import session


class MaterialEvidenceEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, me_id: int):
        super().__init__()

        self.setWindowTitle("Редактировать вещ.док")
        self.setMinimumSize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)

        self.init_ui(me_id)

    def init_ui(self, me_id: int):
        self.material_evidence = self.get_data(me_id)

        if not self.material_evidence:
            QMessageBox.critical(self, "Ошибка", "Вещ.док не найден")
            self.close()
            return

        name_label = QLabel("Наименование")
        self.name_input = QLineEdit(self.material_evidence.name)

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit(self.material_evidence.description)

        status_select_label = QLabel("Статус")
        self.status_select = QComboBox()
        self.status_select.addItems(STATUS_LIST)

        for i in range(self.status_select.count()):
            if self.status_select.itemText(i) == self.material_evidence.status:
                self.status_select.setCurrentIndex(i)
                break

        save_button = QPushButton("Сохранить")
        delete_button = QPushButton("Удалить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(status_select_label)
        layout.addWidget(self.status_select)

        layout.addWidget(save_button)
        layout.addWidget(delete_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)
        delete_button.clicked.connect(self.delete)

    def get_data(self, entity_id: int) -> m.MaterialEvidence | None:
        query = sa.select(m.MaterialEvidence).where(m.MaterialEvidence.id == entity_id)
        result: m.MaterialEvidence | None = session.scalar(query)
        return result

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

    def save(self):
        valid = self.validate()

        if not valid:
            return

        self.material_evidence.name = self.name_input.text()
        self.material_evidence.description = self.description_textarea.toPlainText()
        self.material_evidence.status = self.status_select.currentText()

        if session.is_modified(self.material_evidence):
            session.commit()
            self.on_save.emit()

        self.close()

    def delete(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение удаления")
        messagebox.setText("Вы уверены, что хотите удалить вещ.док?")

        messagebox.addButton("Да", QMessageBox.ButtonRole.YesRole)
        messagebox.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        response = messagebox.exec()

        if response == QMessageBox.ButtonRole.NoRole:
            return

        self.material_evidence.active = False
        session.commit()
        self.on_save.emit()
        self.close()
