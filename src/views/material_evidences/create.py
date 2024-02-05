from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
)
import src.models as m
from src.db import session
import sqlalchemy as sa
from src.schemas import UserOut


class CaseFormWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        heading = QLabel("Добавить дело")

        name_label = QLabel("Название")
        self.name_input = QLineEdit()

        description_label = QLabel("Описание")
        self.description_edit = QTextEdit()

        user_select_label = QLabel("Следователь")
        self.user_select = QComboBox()

        self.users = self.list_users()
        if self.users:
            self.selected_user = self.users[0]
        self.user_select.addItems([str(user) for user in self.users])

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(heading)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(description_label)
        layout.addWidget(self.description_edit)

        layout.addWidget(user_select_label)
        layout.addWidget(self.user_select)

        layout.addWidget(save_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)

    def list_users(self):
        query = sa.select(m.User).where(m.User.active.is_(True))
        results = session.scalars(query).all()
        return [UserOut.from_obj(obj) for obj in results]

    def save(self):
        case = m.Case(
            name=self.name_input.text(),
            description=self.description_edit.toPlainText(),
            investigator_id=self.users[self.user_select.currentIndex()].id,
        )
        session.add(case)
        session.commit()
        self.hide()
