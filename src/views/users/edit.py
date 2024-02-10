from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QMessageBox,
)

import src.models as m
from src.config import NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT, RANK_LIST
from src.db import session


# TODO: Просмотр и редактрование в одном окне
class UserCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить пользователя')
        self.setMinimumSize(NESTED_WINDOW_MIN_WIDTH, NESTED_DIALOG_MIN_HEIGHT)
        self.init_ui()

    def init_ui(self):
        first_name_label = QLabel("Имя")
        self.first_name_input = QLineEdit()

        last_name_label = QLabel("Фамилия")
        self.last_name_input = QLineEdit()

        phone_number_label = QLabel("Номер телефона")
        self.phone_number_input = QLineEdit()

        rank_label = QLabel("Звание")
        self.rank_combobox = QComboBox()
        self.rank_combobox.addItems(RANK_LIST)

        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)

        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_input)

        layout.addWidget(phone_number_label)
        layout.addWidget(self.phone_number_input)

        layout.addWidget(rank_label)
        layout.addWidget(self.rank_input)

        layout.addWidget(save_button)

        self.setLayout(layout)

        save_button.clicked.connect(self.save)

    def validate(self):
        error_messages = []

        if not self.first_name_input.text():
            error_messages.append("Имя обязательное поле")

        if not self.last_name_input.text():
            error_messages.append("Фамилия обязательное поле")

        if not self.phone_number_input.text():
            error_messages.append("Номер телефона обязательное поле")

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False

        return True

    def save(self):
        valid = self.validate()

        if not valid:
            return

        user = m.User(
            first_name=self.first_name_input.text(),
            last_name=self.last_name_input.text(),
            phone_number=self.phone_number_input.text(),
            rank=self.phone_number_input.text(),
        )
        session.add(user)
        session.commit()

        self.on_save.emit()
        self.close()
