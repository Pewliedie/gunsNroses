from PyQt6.QtWidgets import QMainWindow, QLabel
from src.db import init_db

init_db()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt6 App")
        self.label = QLabel("Hello, PyQt6!", self)
        self.setCentralWidget(self.label)
