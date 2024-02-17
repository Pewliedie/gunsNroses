from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTabWidget, QVBoxLayout, QWidget

import src.config as config
from src.audit import init_audit
from src.db import init_db
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

        tab = QTabWidget()

        tab.addTab(CaseListView(), "Дела")
        tab.addTab(MaterialEvidenceListView(), "Вещ.доки")
        tab.addTab(UserListView(), "Пользователи")

        main_layout.addWidget(tab)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        print("Close event")
        return super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            # обработка введенных данных
            self.scanned_barcode = ""
        elif event.text():
            self.scanned_barcode += event.text()
