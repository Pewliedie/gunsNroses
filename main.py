import locale
import sys

from PyQt6.QtWidgets import QApplication
from src.views import AuthenticationView
from PyQt6.QtGui import QIcon
from src.config import ICON_PATH


def main():
    locale.setlocale(locale.LC_ALL, "")
    app = QApplication(sys.argv)
    app_icon = QIcon(ICON_PATH)
    app.setWindowIcon(app_icon)
    window = AuthenticationView()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
