from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import src.models as m
from src.biometrics.recognition import recognizer
from src.config import DIALOG_MIN_WIDTH, RANK_LIST
from src.db import session


class UserCreateForm(QWidget):
    on_save = pyqtSignal()
    
    def __init__(self, is_superuser=False):
        super().__init__()
        
        self.is_superuser = is_superuser

        self.encoded_image_data = ""
        self.setWindowTitle('Добавить пользователя')
        self.setMinimumWidth(DIALOG_MIN_WIDTH)

        self.init_ui()

    def init_ui(self):
        first_name_label = QLabel("Имя")
        self.first_name_input = QLineEdit()

        last_name_label = QLabel("Фамилия")
        self.last_name_input = QLineEdit()

        phone_number_label = QLabel("Номер телефона")
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setInputMask("+7-000-000-00-00")

        password_label = QLabel("Пароль пользователя")
        self.password_input = QLineEdit()

        rank_label = QLabel("Звание")
        self.rank_combobox = QComboBox()
        self.rank_combobox.addItems(RANK_LIST)

        open_image_button = QPushButton("Добавить изображение (Face ID)")
        save_button = QPushButton("Сохранить")

        layout = QVBoxLayout()

        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_input)

        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_input)

        layout.addWidget(phone_number_label)
        layout.addWidget(self.phone_number_input)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        layout.addWidget(rank_label)
        layout.addWidget(self.rank_combobox)

        layout.addWidget(open_image_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

        open_image_button.clicked.connect(self.open_image)
        save_button.clicked.connect(self.save)

    def open_image(self):
        dialog = QFileDialog()

        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("*.jpg")

        dialogSuccess = dialog.exec()

        if dialogSuccess:
            image_path = dialog.selectedFiles()[0]
            self.encoded_image_data = recognizer.encode_image(image_path)

    def validate(self):
        error_messages = []

        if not self.first_name_input.text():
            error_messages.append("Имя обязательное поле")

        if not self.last_name_input.text():
            error_messages.append("Фамилия обязательное поле")

        if not self.phone_number_input.text():
            error_messages.append("Номер телефона обязательное поле")

        if not self.password_input.text():
            error_messages.append("Пароль обязательное поле")

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
            rank=self.rank_combobox.currentText(),
            is_superuser=self.is_superuser,
        )

        user.set_password(self.password_input.text())

        session.add(user)
        session.flush()

        if self.encoded_image_data:
            face_id = m.FaceID(user_id=user.id, data=self.encoded_image_data)
            session.add(face_id)

        session.commit()

        self.on_save.emit()
        self.close()
