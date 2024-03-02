import sqlalchemy as sa
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QCompleter,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import src.models as m
from src.config import DIALOG_MIN_HEIGHT, DIALOG_MIN_WIDTH
from src.db import session
from src.schemas import MaterialEvidenceSelectItem, UserSelectItem
from src.utils import get_current_user
from src.views.material_evidences.create import MaterialEvidenceCreateForm


class CaseCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.material_evidences = []
        self.selected_material_evidences = []
        self.current_user = get_current_user()

        self.setWindowTitle("Добавить дело")
        self.setMinimumSize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)
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
        self.refresh_material_evidences()

        self.users = self.list_users()
        user_items = [str(user) for user in self.users]
        self.user_select.addItems([str(user) for user in self.users])
        self.user_select.setEditable(True)

        completer = QCompleter(user_items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.user_select.setCompleter(completer)

        save_button = QPushButton("Сохранить")
        add_material_evidence_button = QPushButton("Добавить вещ.док")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(material_evidences_list_label)
        layout.addWidget(self.material_evidences_list_view)

        if self.current_user.is_superuser:
            layout.addWidget(user_select_label)
            layout.addWidget(self.user_select)

        layout.addWidget(add_material_evidence_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

        self.material_evidences_list_view.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

        add_material_evidence_button.clicked.connect(
            self.show_create_material_evidence_form
        )
        save_button.clicked.connect(self.save)

    def show_create_material_evidence_form(self):
        self.create_form = MaterialEvidenceCreateForm()
        self.create_form.on_save.connect(self.refresh_material_evidences)
        self.create_form.show()

    def refresh_material_evidences(self):
        query = sa.select(m.MaterialEvidence).filter(
            m.MaterialEvidence.created_by_id == self.current_user.id,
            m.MaterialEvidence.case_id.is_(None),
            m.MaterialEvidence.status != m.MaterialEvidenceStatus.DESTROYED,
        )
        results = session.scalars(query)
        self.material_evidences = [
            MaterialEvidenceSelectItem.from_obj(obj) for obj in results.all()
        ]
        self.material_evidences_list_view.clear()
        self.material_evidences_list_view.addItems(
            [str(material_evidence) for material_evidence in self.material_evidences]
        )

    def list_users(self):
        query = sa.select(m.User).where(m.User.active.is_(True))
        results = session.scalars(query)
        return [UserSelectItem.from_obj(obj) for obj in results.all()]

    def on_selection_changed(self):
        selected_indexes = [
            index.row() for index in self.material_evidences_list_view.selectedIndexes()
        ]
        self.selected_material_evidences = [
            material_evidence.id
            for (index, material_evidence) in enumerate(self.material_evidences)
            if index in selected_indexes
        ]

    def validate(self):
        error_messages = []

        if not self.name_input.text():
            error_messages.append("Наименование не может быть пустым")

        if not self.description_textarea.toPlainText():
            error_messages.append("Описание не может быть пустым")

        if not self.user_select.currentText() and self.current_user.is_superuser:
            error_messages.append("Не выбран следователь")

        if not self.selected_material_evidences:
            error_messages.append("Не выбраны вещественные доказательства")

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False

        return True

    def save(self):
        valid = self.validate()

        if not valid:
            return

        query = sa.select(m.MaterialEvidence).filter(
            m.MaterialEvidence.id.in_(self.selected_material_evidences)
        )

        material_evidences = session.scalars(query).all()
        investigator_id = (
            self.users[self.user_select.currentIndex()].id
            if self.current_user.is_superuser
            else self.current_user.id
        )
        case = m.Case(
            name=self.name_input.text(),
            description=self.description_textarea.toPlainText(),
            investigator_id=investigator_id,
        )
        case.material_evidences = material_evidences
        session.add(case)
        session.commit()

        self.on_save.emit()
        self.close()
