import sqlalchemy as sa
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
from src.utils import get_current_user


class MaterialEvidenceEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, me_id: int):
        super().__init__()

        self.error = False
        self.current_user = get_current_user()

        self.setWindowTitle("Редактировать вещ.док")
        self.setMinimumSize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)

        self.init_ui(me_id)

    def init_ui(self, me_id: int):
        self.material_evidence = self.get_data(me_id)

        if not self.material_evidence:
            self.error = True
            QMessageBox.critical(self, "Ошибка", "Вещ.док не найден")
            self.close()
            return

        case_label = QLabel(
            f"Дело: {self.material_evidence.case.name if self.material_evidence.case else 'Не прикреплено'}"
        )

        name_label = QLabel("Наименование")
        self.name_input = QLineEdit(self.material_evidence.name)

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit(self.material_evidence.description)

        status_label = QLabel(f"Статус: {self.material_evidence.status.value}")
        last_event = self.material_evidence.last_event
        last_event_info = (
            f'{last_event.action.value} - {last_event.user} - {last_event.created.strftime("%d %b %Y %H:%M:%S")}'
            if last_event
            else "Нет событий"
        )
        last_event_label = QLabel(f"Последнее событие: {last_event_info}")

        save_button = QPushButton("Сохранить")
        archive_button = QPushButton("Архивировать")

        take_button = QPushButton("Забрать")
        return_button = QPushButton("Вернуть")
        destroy_button = QPushButton("Уничтожить")

        layout = QVBoxLayout()

        layout.addWidget(case_label)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(status_label)
        layout.addWidget(last_event_label)

        layout.addWidget(save_button)
        layout.addWidget(archive_button)
        layout.addWidget(return_button)
        layout.addWidget(take_button)
        layout.addWidget(destroy_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)
        archive_button.clicked.connect(self.archive)
        return_button.clicked.connect(self.return_event)
        take_button.clicked.connect(self.take_event)
        destroy_button.clicked.connect(self.destroy_event)

    def show(self):
        if self.error:
            return
        return super().show()

    def get_data(self, entity_id: int) -> m.MaterialEvidence | None:
        query = sa.select(m.MaterialEvidence).where(m.MaterialEvidence.id == entity_id)
        result: m.MaterialEvidence | None = session.scalar(query)
        return result

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

    def save(self):
        valid = self.validate()

        if not valid:
            return

        self.material_evidence.name = self.name_input.text()
        self.material_evidence.description = self.description_textarea.toPlainText()

        if session.is_modified(self.material_evidence):
            session.commit()
            self.on_save.emit()

        self.close()

    def archive(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение архивации")
        messagebox.setText("Вы уверены, что хотите архивировать вещ.док?")

        messagebox.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        messagebox.setDefaultButton(QMessageBox.StandardButton.No)

        messagebox.button(QMessageBox.StandardButton.Yes).setText("Да")
        messagebox.button(QMessageBox.StandardButton.No).setText("Нет")

        response = messagebox.exec()

        if response == QMessageBox.StandardButton.No:
            return

        self.create_event(m.MaterialEvidenceStatus.ARCHIVED.name)

    def return_event(self):
        self.create_event(m.MaterialEvidenceStatus.IN_STORAGE.name)

    def take_event(self):
        self.create_event(m.MaterialEvidenceStatus.TAKEN.name)

    def destroy_event(self):
        self.create_event(m.MaterialEvidenceStatus.DESTROYED.name)

    def create_event(self, status: str):
        self.material_evidence.status = status

        event = m.MaterialEvidenceEvent(
            user_id=self.current_user.id,
            material_evidence_id=self.material_evidence.id,
            action=status,
        )

        session.add(event)
        session.commit()

        self.on_save.emit()
        self.close()
