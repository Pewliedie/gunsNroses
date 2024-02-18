import sqlalchemy as sa
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTabWidget, QVBoxLayout, QWidget

import src.config as config
from src.audit import init_audit
from src.db import init_db, session
from src.models import Session
from src.views import CaseListView, MaterialEvidenceListView, UserListView

init_db()
init_audit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            self.init_ui()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Возникла ошибка в ходе работы приложения"
                f"Обратитесь в тех.поддержку"
                f"Подробнее: {e}",
            )
            self.close()

    def init_ui(self):
        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MAIN_WINDOW_MIN_WIDTH, config.MAIN_WINDOW_MIN_HEIGHT)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.tab = QTabWidget()

        self.tab.addTab(CaseListView(), "Дела")
        self.tab.addTab(MaterialEvidenceListView(), "Вещ.доки")
        self.tab.addTab(UserListView(), "Пользователи")

        self.tab.currentChanged.connect(self.reset_list_view)
    
        main_layout.addWidget(self.tab)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def reset_list_view(self, index):
        list_view = self.tab.widget(index)
        if isinstance(list_view, CaseListView):
            list_view.reset()
        elif isinstance(list_view, MaterialEvidenceListView):
            list_view.reset()
        elif isinstance(list_view, UserListView):
            list_view.reset()

    def closeEvent(self, event):

        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение выхода")
        messagebox.setText("Вы уверены, что хотите выйти?")

        messagebox.addButton("Да", QMessageBox.ButtonRole.YesRole)
        messagebox.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        response = messagebox.exec()

        if response == QMessageBox.ButtonRole.NoRole:
            return

        query = sa.select(Session).where(Session.active.is_(True))
        active_session = session.scalars(query).first()
        active_session.active = False

        if session.is_modified(active_session):
            session.commit()

        return super().closeEvent(event)
