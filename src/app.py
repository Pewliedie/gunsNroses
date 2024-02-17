from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QMessageBox,
)
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtCore import Qt
import src.config as config
from src.db import init_db
from src.views import CaseListView, MaterialEvidenceListView, UserListView

init_db()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanned_barcode = ""

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
        print("Close event")
        return super().closeEvent(event)

    def clear_barcode(self):
        self.barcode_label.setText("Сканированный штрихкод: Н/Д")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            # обработка введенных данных
            self.scanned_barcode = ""
        elif event.text():
            self.scanned_barcode += event.text()
