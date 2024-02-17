from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
from PyQt6.QtCore import QTimer

import sqlalchemy as sa
import src.config as config

from src.models import User
from src.app import MainWindow
from src.biometrics.recognition import biometric_auth
from src.db import session
from src.schemas import UserSelectItem

class AuthenticationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setMinimumSize(config.LOGIN_WINDOW_MIN_WIDTH, config.LOGIN_WINDOW_MIN_HEIGHT)
        self.setMaximumSize(config.LOGIN_WINDOW_MIN_WIDTH, config.LOGIN_WINDOW_MIN_HEIGHT)
        
        self.username_label = QLabel("Имя пользователя:")
        self.user_select = QComboBox()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.users = self.list_users()
        self.user_select.addItems([str(user) for user in self.users])

        self.login_button = QPushButton("Войти")
        self.face_id_button = QPushButton("Face ID")
        self.login_button.clicked.connect(self.login)
        self.face_id_button.clicked.connect(self.face_id)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.user_select)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.face_id_button)
        self.setLayout(layout)
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.session_expired)
        self.session_timer.start(300000)  #10 minutes session expiration time

    def list_users(self):
        query = sa.select(User).where(User.active.is_(True))
        results = session.scalars(query).all()
        return [UserSelectItem.from_obj(obj) for obj in results]

    def login(self):
        user_password = self.users[self.user_select.currentIndex()].password
        password = self.password_input.text()
        if user_password == password:
            self.session_timer.stop()  
            self.hide() 
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверный пароль. Попробуйте снова.")
            
    def face_id(self):
        try:
            user_id = self.users[self.user_select.currentIndex()].id
            user = session.query(User).filter(User.id == user_id).first()
            result = biometric_auth(user.face_id.data, str(user.face_id.id))
        except:
            QMessageBox.warning(self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID")
            result = False
        
        if result == True:
            self.session_timer.stop()
            self.hide()
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID")

    def session_expired(self):
        QMessageBox.warning(self, "Завершение сессии", "Время сессии истекло. Пожалуйста, авторизуйтесь снова")
        self.close()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()