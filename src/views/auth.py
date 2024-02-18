from PyQt6.QtGui import QKeyEvent
import sqlalchemy as sa
from PyQt6.QtCore import Qt, QTimer
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

import sqlalchemy as sa

from src.models import User, Session
from src.app import MainWindow
from src.biometrics.recognition import biometric_auth
from src.db import session
from src.models import Session, User
from src.schemas import UserSelectItem

from .users.create import UserCreateForm


class AuthenticationView(QWidget):
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
        self.parent().close()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.session_timer.stop()
        self.hide()
        self.main_window.show()

    def open_create_user_window(self):
        self.create_user_window = UserCreateForm()
        self.create_user_window.on_save.connect(self.fetch_users)
        self.create_user_window.show()
