from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QMessageBox,
)
import sqlalchemy as sa
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import src.config as config
from src.db import init_db, session
from src.models import Session
from src.audit import init_audit
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
                "Возникла ошибка в ходе работы приложения. Подробнее: " + str(e),
            )

    def init_ui(self):
        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MAIN_WINDOW_MIN_WIDTH, config.MAIN_WINDOW_MIN_HEIGHT)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        toolbar = QToolBar()
        tab = QTabWidget()

        tab.addTab(CaseListView(), "Дела")
        tab.addTab(MaterialEvidenceListView(), "Вещ.доки")
        tab.addTab(UserListView(), "Пользователи")

        find_case_action = QAction("Найти дела по штрихкоду", self)
        find_material_evidence_action = QAction("Найти вещ.док по штрихкоду", self)

        toolbar.addAction(find_case_action)
        toolbar.addAction(find_material_evidence_action)

        main_layout.addWidget(tab)
        main_widget.setLayout(main_layout)
        self.addToolBar(toolbar)
        self.setCentralWidget(main_widget)

    def closeEvent(self, event):

        messagebox = QMessageBox()
        messagebox.setWindowTitle("Подтверждение удаления")
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

    def clear_barcode(self):
        self.barcode_label.setText("Сканированный штрихкод: Н/Д")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            # обработка введенных данных
            self.scanned_barcode = ""
        elif event.text():
            self.scanned_barcode += event.text()
