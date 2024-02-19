import sys

import sqlalchemy as sa
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTabWidget, QVBoxLayout, QWidget

import src.config as config
from src.audit import init_audit
from src.db import init_db, session
from src.log import logger
from src.models import Session
from src.utils import exception_handler
from src.views import (
    AuditListView,
    CaseListView,
    MaterialEvidenceListView,
    SessionListView,
    UserListView,
)

init_db()
init_audit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    @exception_handler
    def init_ui(self):
        current_session = self.get_current_session()

        if not current_session:
            QMessageBox.critical(self, "Ошибка", "Не удалось получить сессию")
            self.close()
            return

        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MAIN_WINDOW_MIN_WIDTH, config.MAIN_WINDOW_MIN_HEIGHT)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.tab = QTabWidget()

        self.tab.addTab(CaseListView(), "Дела")
        self.tab.addTab(MaterialEvidenceListView(), "Вещ.доки")

        if current_session.user.is_superuser:
            self.tab.addTab(UserListView(), "Пользователи")
            self.tab.addTab(SessionListView(), "Сессии")
            self.tab.addTab(AuditListView(), "Аудит")

        self.tab.currentChanged.connect(self.refresh_list_view)

        main_layout.addWidget(self.tab)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def get_current_session(self):
        query = sa.select(Session).where(Session.active.is_(True))
        return session.scalars(query).first()

    def refresh_list_view(self, index):
        list_view = self.tab.widget(index)

        if isinstance(
            list_view, (CaseListView, MaterialEvidenceListView, UserListView)
        ):
            list_view.refresh()

    def closeEvent(self, event):
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение выхода")
        messagebox.setText("Вы уверены, что хотите выйти?")

        messagebox.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        messagebox.setDefaultButton(QMessageBox.StandardButton.Yes)

        messagebox.button(QMessageBox.StandardButton.Yes).setText("Да")
        messagebox.button(QMessageBox.StandardButton.No).setText("Нет")

        response = messagebox.exec()

        if response == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
            return

        query = (
            sa.select(Session)
            .where(Session.active.is_(True))
            .order_by(Session.login.desc())
        )

        active_session = session.scalars(query).first()
        active_session.active = False

        session.commit()

        return super().closeEvent(event)
