from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
    QCompleter,
)
from PyQt6.QtCore import QTimer, Qt

import sqlalchemy as sa

import src.config as config

from src.models import User, Session
from src.app import MainWindow
from src.biometrics.recognition import biometric_auth
from src.db import session
from src.schemas import UserSelectItem
from .users.create import UserCreateForm


class AuthenticationView(QWidget):

    def __init__(self):
        super().__init__()

        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.session_expired)
        self.session_timer.start(300000)  # 10 minutes session expiration time

        self.setWindowTitle("Авторизация")
        self.setMinimumSize(
            config.LOGIN_WINDOW_MIN_WIDTH, config.LOGIN_WINDOW_MIN_HEIGHT
        )
        self.setMaximumSize(
            config.LOGIN_WINDOW_MIN_WIDTH, config.LOGIN_WINDOW_MIN_HEIGHT
        )

        self.username_label = QLabel("Имя пользователя:")
        self.user_select = QComboBox()
        self.user_select.setEditable(True)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.face_id_button = QPushButton("Face ID")
        self.sign_up_button = QPushButton("Создать пользователя")

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

    def fetch_users(self):
        self.users = self.list_users()
        self.user_select.addItems([str(user) for user in self.users])

        completer = QCompleter([str(user) for user in self.users])
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.user_select.setCompleter(completer)

        self.sign_up_button.setEnabled(False)

        if not self.users:
            QMessageBox.warning(
                self, "Ошибка", "Нет доступных пользователей. Создайте пользователя."
            )
            self.sign_up_button.setEnabled(True)

    def authenticated_by_password(self):

        user_password = self.users[self.user_select.currentIndex()].password
        password = self.password_input.text()

        if user_password == password:
            self.open_main_window()
        else:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Неверный пароль. Попробуйте снова."
            )

    def authenticated_by_face_id(self):
        try:
            user_id = self.users[self.user_select.currentIndex()].id
            user = session.query(User).filter(User.id == user_id).first()
            authenticated = biometric_auth(user.face.data, str(user.face.id))
        except:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID"
            )
            authenticated = False

        if authenticated:
            active_session = Session(user=user)
            session.add(active_session)
            session.commit()
            self.open_main_window()

        else:
            QMessageBox.warning(
                self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID"
            )

    def session_expired(self):
        QMessageBox.warning(
            self,
            "Завершение сессии",
            "Время сессии истекло. Пожалуйста, авторизуйтесь снова",
        )
        self.close()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.session_timer.stop()
        self.hide()
        self.main_window.show()

    def open_create_user_window(self):
        self.create_user_window = UserCreateForm()
        self.create_user_window.on_save.connect(self.fetch_users)
        self.create_user_window.show()
