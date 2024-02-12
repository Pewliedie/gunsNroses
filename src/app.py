from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
)
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

        # toolbar = QToolBar()
        # self.addToolBar(toolbar)

        barcode_layout = QHBoxLayout()
        barcode = QWidget()
        barcode.setLayout(barcode_layout)

        self.barcode_label = QLabel("Сканированный штрихкод: Н/Д")
        clear_button = QPushButton("Очистить")
        barcode_layout.addWidget(self.barcode_label)
        barcode_layout.addWidget(clear_button)

        tab = QTabWidget()

        tab.addTab(CaseListView(), "Дела")
        tab.addTab(MaterialEvidenceListView(), "Вещ.доки")
        tab.addTab(UserListView(), "Пользователи")

        main_layout.addWidget(barcode)
        main_layout.addWidget(tab)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        clear_button.clicked.connect(self.clear_barcode)

    def clear_barcode(self):
        self.barcode_label.setText("Сканированный штрихкод: Н/Д")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.barcode_label.setText(
                "Сканированный штрихкод: " + self.scanned_barcode
            )
            self.scanned_barcode = ""
        elif event.text():
            self.scanned_barcode += event.text()
