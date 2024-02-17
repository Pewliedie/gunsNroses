import locale
import sys

from PyQt6.QtWidgets import QApplication
from src.views import AuthenticationView
from PyQt6.QtGui import QIcon
from src.config import ROOT_DIR



def main():
    locale.setlocale(locale.LC_ALL, "")
    app = QApplication(sys.argv)
    app_icon = QIcon(ROOT_DIR + "/assets/icon.png")
    app.setWindowIcon(app_icon)
    window = AuthenticationView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
