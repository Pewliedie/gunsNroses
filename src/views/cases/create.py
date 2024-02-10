import sqlalchemy as sa
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
    QListWidget,
    QAbstractItemView,
)

import src.models as m
from src.config import NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT
from src.db import session
from src.schemas import UserSelectItem, MaterialEvidenceSelectItem


class CaseCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить дело')
        self.setMinimumSize(NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT)
        self.init_ui()

    def init_ui(self):
        name_label = QLabel("Наименование")
        self.name_input = QLineEdit()

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit()

        user_select_label = QLabel("Следователь")
        self.user_select = QComboBox()

        material_evidences_list_label = QLabel("Вещ.доки")
        self.material_evidences_list_view = QListWidget()
        self.material_evidences_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self.material_evidences = self.list_material_evidence()
        self.material_evidences_list_view.addItems(
            [str(material_evidence) for material_evidence in self.material_evidences]
        )

        self.users = self.list_users()
        self.user_select.addItems([str(user) for user in self.users])

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        # TODO: обработчик выбора в списке
        layout.addWidget(material_evidences_list_label)
        layout.addWidget(self.material_evidences_list_view)

        layout.addWidget(user_select_label)
        layout.addWidget(self.user_select)

        layout.addWidget(save_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)

    def list_material_evidence(self):
        query = sa.select(m.MaterialEvidence).where(
            sa.and_(
                m.MaterialEvidence.case_id.is_(None),
                m.MaterialEvidence.status.notilike('Уничтожено'),
            )
        )
        results = session.scalars(query).all()
        return [MaterialEvidenceSelectItem.from_obj(obj) for obj in results]

    def list_users(self):
        query = sa.select(m.User).where(m.User.active.is_(True))
        results = session.scalars(query).all()
        return [UserSelectItem.from_obj(obj) for obj in results]

    def validate(self):
        error_messages = []

        if not self.name_input.text():
            error_messages.append("Наименование не может быть пустым")

        if not self.description_textarea.toPlainText():
            error_messages.append("Описание не может быть пустым")

        if not self.user_select.currentText():
            error_messages.append("Не выбран следователь")

        # TODO: валидация списка вещ.доков

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False

        return True

    def save(self):
        # self.material_evidences_list_view.selectedIndexes()
        valid = self.validate()

        if not valid:
            return

        # TODO: добавлять вещ доки по обратной ссылке case.material_evidences
        case = m.Case(
            name=self.name_input.text(),
            description=self.description_textarea.toPlainText(),
            investigator_id=self.users[self.user_select.currentIndex()].id,
        )

        session.add(case)
        session.commit()

        self.on_save.emit()
        self.close()
