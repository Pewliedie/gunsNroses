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


class CaseEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, case_id: int):
        super().__init__()
        self.selected_material_evidences = []

        self.setWindowTitle("Редактировать дело")
        self.setMinimumSize(NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT)

        self.init_ui(case_id)

    def init_ui(self, case_id: int):
        self.case = self.get_data(case_id)

        if not self.case:
            QMessageBox.critical(self, "Ошибка", "Дело не найдено")
            self.close()
            return

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
        self.material_evidences = self.list_material_evidence()
        self.material_evidences_list_view.addItems(
            [str(material_evidence) for material_evidence in self.material_evidences]
        )

        for material_evidence in self.material_evidences:
            if material_evidence.id in [me.id for me in self.case.material_evidences]:
                self.material_evidences_list_view.item(
                    self.material_evidences.index(material_evidence)
                ).setSelected(True)

        self.users = self.list_users()
        self.user_select.addItems([str(user) for user in self.users])

        for user in self.users:
            if user.id == self.case.investigator_id:
                self.user_select.setCurrentIndex(self.users.index(user))

        save_button = QPushButton("Сохранить")
        delete_button = QPushButton("Удалить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(material_evidences_list_label)
        layout.addWidget(self.material_evidences_list_view)

        layout.addWidget(user_select_label)
        layout.addWidget(self.user_select)

        layout.addWidget(save_button)
        layout.addWidget(delete_button)

        self.setLayout(layout)

        self.material_evidences_list_view.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        save_button.clicked.connect(self.save)
        delete_button.clicked.connect(self.delete)

    def get_data(self, entity_id: int) -> m.Case | None:
        query = sa.select(m.Case).where(m.Case.id == entity_id)
        result: m.Case | None = session.scalar(query)
        return result

    def list_material_evidence(self):
        query = sa.select(m.MaterialEvidence).where(
            sa.func.casefold(m.MaterialEvidence.status).notlike("Уничтожено"),
        )
        results = session.scalars(query)
        return [MaterialEvidenceSelectItem.from_obj(obj) for obj in results.all()]

    def list_users(self):
        query = sa.select(m.User).where(m.User.active.is_(True))
        results = session.scalars(query).all()
        return [UserSelectItem.from_obj(obj) for obj in results]

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

        if not self.user_select.currentText():
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

        self.case.name = self.name_input.text()
        self.case.description = self.description_textarea.toPlainText()
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
