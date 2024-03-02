import cv2
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QWidget


class CameraViewer(QWidget):
    def __init__(self, camera_index=0):
        super().__init__()
        self.setWindowTitle("Просмотр изображения с камеры")
        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.camera_label = QLabel(self)
        self.layout.addWidget(self.camera_label)
        self.setLayout(self.layout)
        self.init_camera(camera_index)

    def init_camera(self, camera_index):
        self.capture = cv2.VideoCapture(camera_index)
        if not self.capture.isOpened():
            message_box = QMessageBox(
                QMessageBox.Icon.Critical, "Ошибка", "Не удалось открыть камеру"
            )
            message_box.exec()
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(25)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(
                rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
            )

            p = QPixmap.fromImage(convert_to_Qt_format)
            scaled_p = p.scaled(
                self.camera_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.camera_label.setPixmap(scaled_p)

    def closeEvent(self, event):
        if self.capture.isOpened():
            self.capture.release()

        super().closeEvent(event)
