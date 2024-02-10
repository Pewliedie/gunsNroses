from PyQt6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QVBoxLayout, QWidget

import src.config as config
from src.db import init_db
from src.views import CaseListView, MaterialEvidenceListView, UserListView

init_db()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MAIN_WINDOW_MIN_WIDTH, config.MAIN_WINDOW_MIN_HEIGHT)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # toolbar = QToolBar()
        # self.addToolBar(toolbar)

        tab = QTabWidget()
        tab.addTab(CaseListView(), "Дела")
        tab.addTab(MaterialEvidenceListView(), "Вещ.доки")
        tab.addTab(UserListView(), "Пользователи")

        main_layout.addWidget(tab)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
