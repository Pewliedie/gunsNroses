import sqlalchemy as sa
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
from src.utils import get_current_user


class UserEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, user_id: int):
        super().__init__()

        self.current_user = get_current_user()
        self.error = False

        self.setWindowTitle("Редактировать пользователя")
        self.setMinimumWidth(DIALOG_MIN_WIDTH)

        self.init_ui(user_id)

    def init_ui(self, user_id: int):
        self.user = self.get_data(user_id)

        if not self.user:
            self.error = True
            QMessageBox.critical(self, "Ошибка", "Пользователь не найден")
            self.close()
            return

        self.encoded_image_data = self.user.face.data if self.user.face else ""

        first_name_label = QLabel("Имя")
        self.first_name_input = QLineEdit(self.user.first_name)

        last_name_label = QLabel("Фамилия")
        self.last_name_input = QLineEdit(self.user.last_name)

        phone_number_label = QLabel("Номер телефона")
        self.phone_number_input = QLineEdit(self.user.phone_number)
        self.phone_number_input.setInputMask("+7-000-000-00-00")

        password_label = QLabel("Пароль пользователя")
        self.password_input = QLineEdit()

        rank_label = QLabel("Звание")
        self.rank_combobox = QComboBox()
        self.rank_combobox.addItems(RANK_LIST)

        for i in range(self.rank_combobox.count()):
            if self.rank_combobox.itemText(i) == self.user.rank:
                self.rank_combobox.setCurrentIndex(i)
                break

        open_image_button = QPushButton("Добавить изображение (Face ID)")
        save_button = QPushButton("Сохранить")
        deactivate_button = QPushButton("Деактивировать")

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

        if self.current_user.id != self.user.id:
            layout.addWidget(deactivate_button)

        self.setLayout(layout)

        open_image_button.clicked.connect(self.open_image)
        save_button.clicked.connect(self.save)
        deactivate_button.clicked.connect(self.deactivate)

    def show(self):
        if self.error:
            return
        return super().show()

    def get_data(self, entity_id: int) -> m.User | None:
        query = sa.select(m.User).where(m.User.id == entity_id)
        result: m.User | None = session.scalar(query)
        return result

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

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False

        return True

    def save(self):
        valid = self.validate()

        if not valid:
            return

        self.user.first_name = self.first_name_input.text()
        self.user.last_name = self.last_name_input.text()
        self.user.phone_number = self.phone_number_input.text()
        self.user.rank = self.rank_combobox.currentText()

        if self.password_input.text():
            self.user.set_password(self.password_input.text())

        if self.encoded_image_data:
            self.user.face.data = self.encoded_image_data
        else:
            face = m.FaceID(user_id=self.user.id, data=self.encoded_image_data)
            session.add(face)
            session.flush()
            self.user.face_id = face.id

        session.commit()
        self.on_save.emit()
        self.close()

    def deactivate(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение деактивации")
        messagebox.setText("Вы уверены, что хотите деактивировать пользователя?")

        messagebox.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        messagebox.setDefaultButton(QMessageBox.StandardButton.Yes)

        messagebox.button(QMessageBox.StandardButton.Yes).setText("Да")
        messagebox.button(QMessageBox.StandardButton.No).setText("Нет")

        response = messagebox.exec()

        if response == QMessageBox.StandardButton.No:
            return

        self.user.active = False
        session.commit()
        self.on_save.emit()
        self.close()
