import sqlalchemy as sa
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import src.models as m
from src.config import DIALOG_MIN_WIDTH
from src.db import session

from .viewer import CameraViewer


class CameraEditForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, camera_id=None):
        super().__init__()
        self.setWindowTitle('Настройки камеры')
        self.setMinimumWidth(DIALOG_MIN_WIDTH)
        self.error = False
        self.init_ui(camera_id)

    def init_ui(self, camera_id=None):

        self.camera = self.get_data(camera_id)

        if self.camera:
            self.setWindowTitle(f"Настройки камеры - {self.camera.name}")
        else:
            self.error = True
            QMessageBox.critical(self, "Ошибка", "Камера не найдена")
            self.close()
            return

        name_label = QLabel("Наименование")
        self.name_label_input = QLineEdit(self.camera.name)

        camera_type = QLabel("Тип камеры")
        self.camera_type_select = QComboBox()
        self.camera_type_select.addItems([t.value for t in m.CameraType])

        for i in range(self.camera_type_select.count()):
            if m.CameraType(self.camera_type_select.itemText(i)) == self.camera.type:
                self.camera_type_select.setCurrentIndex(i)
                break

        save_button = QPushButton("Сохранить")
        open_camera_button = QPushButton("Просмотреть изображение с камеры")

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_input)
        layout.addWidget(camera_type)
        layout.addWidget(self.camera_type_select)
        layout.addWidget(save_button)
        layout.addWidget(open_camera_button)

        self.setLayout(layout)

        open_camera_button.clicked.connect(self.open_camera)
        save_button.clicked.connect(self.save)

    def validate(self):
        error_messages = []

        if not self.name_label_input.text():
            error_messages.append("Наименование обязательное поле")

        if error_messages:
            messagebox = QMessageBox()
            messagebox.critical(self, "Ошибка валидации", "\n".join(error_messages))
            return False
        return True

    def get_data(self, camera_id) -> m.Camera | None:
        query = sa.select(m.Camera).where(m.Camera.id == camera_id)
        result: m.Camera | None = session.scalar(query)
        return result

    def open_camera(self):
        self.camera_viewer = CameraViewer(self.camera.device_id)
        self.camera_viewer.show()

    def save(self):
        valid = self.validate()

        if not valid:
            return

        self.camera.name = self.name_label_input.text()
        self.camera.type = m.CameraType(self.camera_type_select.currentText())

        session.commit()
        self.on_save.emit()
        self.close()

    def closeEvent(self, event):
        # TODO: надо переписать этот костыл, АРТУР!
        if hasattr(self, "camera_viewer"):
            self.camera_viewer.close()
        super().closeEvent(event)
