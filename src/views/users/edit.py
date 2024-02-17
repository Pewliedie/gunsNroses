import sqlalchemy as sa
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QMessageBox,
    QFileDialog,
)

import src.models as m
from src.config import DIALOG_MIN_WIDTH, RANK_LIST
from src.db import session

from src.biometrics.recognition import Recognizer


class UserEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, user_id: int):
        super().__init__()

        self.setWindowTitle("Редактировать пользователя")
        self.setMinimumWidth(DIALOG_MIN_WIDTH)

        self.init_ui(user_id)

    def init_ui(self, user_id: int):
        self.user = self.get_data(user_id)

        if not self.user:
            QMessageBox.critical(self, "Ошибка", "Пользователь не найден")
            self.close()
            return

        self.encoding_image_data = "empty_data"
        first_name_label = QLabel("Имя")
        self.first_name_input = QLineEdit(self.user.first_name)

        last_name_label = QLabel("Фамилия")
        self.last_name_input = QLineEdit(self.user.last_name)

        phone_number_label = QLabel("Номер телефона")
        self.phone_number_input = QLineEdit(self.user.phone_number)
        self.phone_number_input.setInputMask("+7-000-000-00-00")

        password_label = QLabel("Пароль пользователя")
        self.password_input = QLineEdit(self.user.password)

        rank_label = QLabel("Звание")
        self.rank_combobox = QComboBox()
        self.rank_combobox.addItems(RANK_LIST)

        for i in range(self.rank_combobox.count()):
            if self.rank_combobox.itemText(i) == self.user.rank:
                self.rank_combobox.setCurrentIndex(i)
                break

        open_image_button = QPushButton("Добавить изображение (Face ID)")
        save_button = QPushButton("Сохранить")
        delete_button = QPushButton("Удалить")

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
        delete_button.clicked.connect(self.delete)

    def get_data(self, entity_id: int) -> m.User | None:
        query = sa.select(m.User).where(m.User.id == entity_id)
        result: m.User | None = session.scalar(query)
        return result

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
            password=self.password_input.text(),
            rank=self.rank_combobox.currentText(),
        )

        face_id = m.FaceID(user=user, data=self.encoding_image_data)

        session.add(user)
        session.add(face_id)
        session.commit()

        self.on_save.emit()
        self.close()

    def open_image(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("*.jpg")
        dialogSuccess = dialog.exec()

        recognizer = Recognizer()
        if dialogSuccess:
            image_path = dialog.selectedFiles()[0]
            self.encoding_image_data = recognizer.encode_image(image_path)

    def delete(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение удаления")
        messagebox.setText("Вы уверены, что хотите удалить пользователя?")

        messagebox.addButton("Да", QMessageBox.ButtonRole.YesRole)
        messagebox.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        response = messagebox.exec()

        if response == QMessageBox.ButtonRole.NoRole:
            return

        self.user.active = False
        session.commit()
        self.on_save.emit()
        self.close()
