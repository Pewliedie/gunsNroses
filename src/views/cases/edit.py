import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
)

import src.models as m
from src.config import NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT
from src.db import session


# TODO: Просмотр и редактрование в одном окне
class CaseEditForm(QWidget):
    def __init__(self, entity_id: int, window_title: str):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setMinimumSize(NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT)
        self.case = self.get_data(entity_id)

        name_label = QLabel("Наименование")
        self.name_input = QLineEdit()
        self.name_input.setText(self.case.name)

        description_label = QLabel("Описание")
        self.description_textarea = QTextEdit()
        self.description_textarea.setLayout(self.case.description)

        user_select_label = QLabel("Следователь")
        self.user_select = QComboBox()

        # self.users = self.list_users()
        # self.user_select.addItems([str(user) for user in self.users])

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_textarea)

        layout.addWidget(user_select_label)
        layout.addWidget(self.user_select)

        layout.addWidget(save_button)

        self.setLayout(layout)

        # save_button.clicked.connect(self.save)

    def get_data(self, entity_id: int):
        query = sa.select(m.Case).where(m.Case.id == entity_id)
        result: m.Case | None = session.scalar(query)
        return result

    def validate(self):
        pass

    def save(self):
        self.validate()
        self.case.name = self.name_input.text()
        self.case.description = self.description_textarea
        if session.is_modified(self.case):
            session.commit()
