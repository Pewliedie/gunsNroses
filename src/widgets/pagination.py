from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)


class PaginationWidget(QWidget):
    def __init__(self, total_pages):
        super().__init__()
        self.total_pages = total_pages
        self.current_page = 1

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

        self.update_label()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_label()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_label()

    def update_label(self):
        self.label.setText(f"Current Page: {self.current_page}/{self.total_pages}")


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    widget = PaginationWidget(total_pages=5)
    window.setCentralWidget(widget)
    window.show()
    app.exec()
