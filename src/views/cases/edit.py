import sqlalchemy as sa
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
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


class CaseEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, case_id: int):
        super().__init__()

        self.error = False

        self.material_evidences = []
        self.selected_material_evidences = []
        self.current_user = get_current_user()

        self.setWindowTitle("Редактировать дело")
        self.setMinimumSize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)

        self.init_ui(case_id)

    def init_ui(self, case_id: int):
        # Get the case data
        self.case = self.get_data(case_id)

        if not self.case:
            self.error = True
            QMessageBox.critical(self, "Ошибка", "Дело не найдено")
            self.close()
            return

        # Create the UI elements
        name_label = QLabel("Наименование")
        self.name_input = QLineEdit(self.case.name)

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit(self.case.description)

        user_select_label = QLabel("Следователь")
        self.user_select = QComboBox()

        material_evidences_list_label = QLabel("Вещ.доки")
        self.material_evidences_list_view = QListWidget()
        self.material_evidences_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self.refresh_material_evidences()

        self.users = self.list_users()
        self.user_select.addItems([str(user) for user in self.users])

        for user in self.users:
            if user.id == self.case.investigator_id:
                self.user_select.setCurrentIndex(self.users.index(user))

        add_material_evidence_button = QPushButton("Добавить вещ.док")
        save_button = QPushButton("Сохранить")
        delete_button = QPushButton("Удалить")

        layout = QVBoxLayout()

        # Add the UI elements to the layout
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
        layout.addWidget(delete_button)

        self.setLayout(layout)

        # Connect signals to slots
        self.material_evidences_list_view.selectionModel().selectionChanged.connect(
            self.update_selection
        )
        add_material_evidence_button.clicked.connect(
            self.show_create_material_evidence_form
        )
        save_button.clicked.connect(self.save)
        delete_button.clicked.connect(self.delete)

    def show(self):
        if self.error:
            return
        return super().show()

    def get_data(self, entity_id: int) -> m.Case | None:
        # Retrieve the case from the database
        query = sa.select(m.Case).where(m.Case.id == entity_id)
        case: m.Case | None = session.scalar(query)

        if (
            case.investigator_id != self.current_user.id
            and not self.current_user.is_superuser
        ):
            return None

        return case

    def show_create_material_evidence_form(self):
        # Show the create material evidence form
        self.create_form = MaterialEvidenceCreateForm()
        self.create_form.on_save.connect(self.refresh_material_evidences)
        self.create_form.show()

    def select_material_evidences(self):
        # Select the material evidences that are associated with the case
        for material_evidence in self.material_evidences:
            if material_evidence.id in [me.id for me in self.case.material_evidences]:
                index = self.material_evidences.index(material_evidence)
                item = self.material_evidences_list_view.item(index)
                item.setSelected(True)
        self.update_selection()

    def refresh_material_evidences(self):
        # Refresh the list of material evidences
        query = sa.select(m.MaterialEvidence).filter(
            m.MaterialEvidence.created_by_id == self.current_user.id,
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
        self.select_material_evidences()

    def list_users(self):
        # Retrieve the list of active users
        query = sa.select(m.User).where(m.User.active.is_(True))
        results = session.scalars(query).all()
        return [UserSelectItem.from_obj(obj) for obj in results]

    def update_selection(self):
        # Update the selected material evidences
        selected_indexes = [
            index.row() for index in self.material_evidences_list_view.selectedIndexes()
        ]
        self.selected_material_evidences = [
            material_evidence.id
            for (index, material_evidence) in enumerate(self.material_evidences)
            if index in selected_indexes
        ]

    def validate(self):
        # Validate the form inputs
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

        # Update the case with the form inputs
        self.case.name = self.name_input.text()
        self.case.description = self.description_textarea.toPlainText()
        if self.current_user.is_superuser:
            self.case.investigator_id = self.users[self.user_select.currentIndex()].id
        self.case.material_evidences = material_evidences

        if session.is_modified(self.case):
            session.commit()
            self.on_save.emit()

        self.close()

    def delete(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение удаления")
        messagebox.setText("Вы уверены, что хотите удалить дело?")

        messagebox.addButton("Да", QMessageBox.ButtonRole.YesRole)
        messagebox.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        response = messagebox.exec()

        if response == QMessageBox.ButtonRole.NoRole:
            return

        for material_evidence in self.case.material_evidences:
            material_evidence.case_id = None

        self.case.active = False
        session.commit()
        self.on_save.emit()
        self.close()
