from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer
from src.models import FaceID, User
from src.app import MainWindow
from src.biometrics.recognition import biometric_auth
import sqlalchemy as sa
from src.db import session


class AuthenticationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.face_id_button = QPushButton("Face ID")
        self.login_button.clicked.connect(self.login)
        self.face_id_button.clicked.connect(self.face_id)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.face_id_button)
        self.setLayout(layout)
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.session_expired)
        self.session_timer.start(600000)  #10 minutes session expiration time

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.session_timer.stop()  # Stop the session timer
            self.hide()  # Hide the authentication form
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверное имя пользователя или пароль. Попробуйте снова.")
            
    def face_id(self):
        try:
            user = session.query(User).filter(User.first_name == self.username_input.text()).first()
            face_id = session.query(FaceID).filter(FaceID.user == user).first()
            result = biometric_auth(face_id.data, str(face_id.id))
        except:
            QMessageBox.warning(self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID")
        
        try:
            if result == True:
                self.session_timer.stop()
                self.hide()
                self.open_main_window()
            else :
                QMessageBox.warning(self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID")
        except:
            QMessageBox.warning(self, "Ошибка авторизации", "Ошибка при аутентификации по FACE ID")

    def session_expired(self):
        QMessageBox.warning(self, "Завершение сессии", "Время сессии истекло. Пожалуйста, авторизуйтесь снова")
        self.close()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()