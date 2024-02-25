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
    QHBoxLayout
)

import src.models as m
import sqlalchemy as sa
from src.config import DIALOG_MIN_WIDTH
from src.db import session
from .viewer import WebcamViewer


class WebCamCreateForm(QWidget):
    on_save = pyqtSignal()

    def __init__(self, webcam_id = None):
        super().__init__()
        self.setWindowTitle('Настройки веб-камеры')
        self.setMinimumWidth(DIALOG_MIN_WIDTH)
        self.error = False
        self.init_ui(webcam_id)

    def init_ui(self, webcam_id = None):
        
        self.webcam = self.get_data(webcam_id)

        if self.webcam:
            self.setWindowTitle(f"Настройки веб-камеры - {self.webcam.name}")
        else:
            self.error = True
            QMessageBox.critical(self, "Ошибка", "Веб-камера не найдена")
            self.close()
            return
        
        name_label = QLabel("Наименование")
        self.name_label_input = QLineEdit(self.webcam.name)
        
        webcam_type = QLabel("Тип камеры")
        self.webcam_type_select = QComboBox()
        self.webcam_type_select.addItems([t.value for t in m.WebCamType])

        for i in range(self.webcam_type_select.count()):
            if m.WebCamType(self.webcam_type_select.itemText(i)) == self.webcam.type:
                self.webcam_type_select.setCurrentIndex(i)
                break
        
        save_button = QPushButton("Сохранить")
        open_webcam_button = QPushButton("Просмотреть изображение с веб-камеры")

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.name_label_input)
        layout.addWidget(webcam_type)
        layout.addWidget(self.webcam_type_select)
        layout.addWidget(save_button)
        layout.addWidget(open_webcam_button)
                
        self.setLayout(layout)

        open_webcam_button.clicked.connect(self.open_webcam)
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
    
    def get_data(self, webcam_id) -> m.WebCam | None:
        query = sa.select(m.WebCam).where(m.WebCam.id == webcam_id)
        result: m.WebCam | None = session.scalar(query)
        return result

    def open_webcam(self):
        self.webcam_viewer = WebcamViewer(self.webcam.device_id)
        self.webcam_viewer.show()
        
    def save(self):
        valid = self.validate()

        if not valid:
            return

        self.webcam.name = self.name_label_input.text()
        self.webcam.type = m.WebCamType(self.webcam_type_select.currentText())
        
        session.commit()
        self.on_save.emit()
        self.close()

    def closeEvent(self, event):
        if hasattr(self, "webcam_viewer"):
            self.webcam_viewer.close()

        super().closeEvent(event)