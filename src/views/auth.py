import sys

import sqlalchemy as sa
import cv2
import time
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QCompleter,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.app import MainWindow
from src.biometrics.recognition import biometric_auth
from src.db import session
from src.models import Session, User
from src.schemas import UserSelectItem
from src.utils import exception_handler

from .users.create import UserCreateForm


class VideoRecorder(QThread):
    finished = pyqtSignal()

    def __init__(self, camera_index=0, save_path=".", record_duration=10):
        super().__init__()
        self.camera_index = camera_index
        self.save_path = save_path
        self.record_duration = record_duration

    def run(self):
        # Получаем текущее время для имени файла
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.save_path}/video_{current_time}.mp4"

        cap = cv2.VideoCapture(self.camera_index)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        start_time = time.time()

        while (time.time() - start_time) < self.record_duration:  # Запись в течение заданного времени
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break

        cap.release()
        out.release()
        self.finished.emit()

class AuthenticationView(QWidget):
    @exception_handler
    def __init__(self):
        super().__init__()

        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.session_expired)
        self.session_timer.start(5 * 60 * 1000)
        

        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 200)

        self.username_label = QLabel("Имя пользователя:")
        self.user_select = QComboBox()
        self.user_select.setEditable(True)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.face_id_button = QPushButton("Face ID")
        self.sign_up_button = QPushButton("Создать пользователя")

        self.sign_up_button.hide()

        self.fetch_users()

        layout = QVBoxLayout()

        layout.addWidget(self.username_label)
        layout.addWidget(self.user_select)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.face_id_button)
        layout.addWidget(self.sign_up_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.authenticated_by_password)
        self.face_id_button.clicked.connect(self.authenticated_by_face_id)
        self.sign_up_button.clicked.connect(self.open_create_user_window)

    def list_users(self):
        query = sa.select(User).where(User.active.is_(True))
        results = session.scalars(query).all()
        return [UserSelectItem.from_obj(obj) for obj in results]

    def start_video_recording(self):
        self.video_recorder = VideoRecorder(camera_index=0, save_path=".", record_duration=10)
        self.video_recorder.finished.connect(self.recording_finished)
        self.video_recorder.start()
    
    def recording_finished(self):
        print('Recording finished')

    def fetch_users(self):
        self.users = self.list_users()

        self.user_select.addItems([str(user) for user in self.users])

        completer = QCompleter([str(user) for user in self.users])
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.user_select.setCompleter(completer)

        if not self.users:
            QMessageBox.warning(
                self, "Ошибка", "Нет доступных пользователей. Создайте пользователя."
            )
            self.sign_up_button.show()

    def manage_session(self, user: User):
        sessions = session.query(Session).filter(Session.active.is_(True)).all()

        for s in sessions:
            s.active = False

        new_session = Session(user=user)

        session.add(new_session)
        session.commit()

    def authenticated_by_password(self):
        user_id = self.users[self.user_select.currentIndex()].id
        user = session.scalar(sa.select(User).where(User.id == user_id))

        if not user:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Пользователь не найден. Попробуйте снова."
            )
            return

        password = self.password_input.text()

        if user.check_password(password):
            self.manage_session(user)
            self.open_main_window()
        else:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Неверный пароль. Попробуйте снова."
            )

    def authenticated_by_face_id(self):
        authenticated = False

        try:
            user_id = self.users[self.user_select.currentIndex()].id
            user = session.query(User).filter(User.id == user_id).first()
            authenticated = biometric_auth(user.face.data, str(user.face.id))
        except:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID"
            )

        if authenticated:
            self.manage_session(user)
            self.open_main_window()
        else:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID"
            )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.authenticated_by_password()

        return super().keyPressEvent(event)

    def session_expired(self):
        QMessageBox.warning(
            self,
            "Завершение сессии",
            "Время сессии истекло. Пожалуйста, авторизуйтесь снова",
        )
        sys.exit(0)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.session_timer.stop()
        self.hide()
        self.main_window.show()

    def open_create_user_window(self):
        self.create_user_window = UserCreateForm(is_superuser=True)
        self.create_user_window.on_save.connect(self.fetch_users)
        self.create_user_window.show()
