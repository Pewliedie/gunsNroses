import locale
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.audit import init_audit
from src.config import ICON_PATH
from src.db import init_db
from src.views.auth import AuthenticationView


def main():
    init_db()
    init_audit()

    locale.setlocale(locale.LC_ALL, "")

    app = QApplication(sys.argv)
    app_icon = QIcon(ICON_PATH)
    app.setWindowIcon(app_icon)

    main_view = AuthenticationView()
    main_view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
