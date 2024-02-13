import locale
import sys

from PyQt6.QtWidgets import QApplication
from src.widgets.auth import AuthenticationForm

def main():
    
    locale.setlocale(locale.LC_ALL, "")
    app = QApplication(sys.argv)
    window = AuthenticationForm()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
