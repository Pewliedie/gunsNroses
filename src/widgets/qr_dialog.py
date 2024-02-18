from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class QRDialog(QDialog):
    def __init__(self, on_scan, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.on_scan = on_scan

        self.setWindowTitle("Поиск по QR")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()

        label = QLabel("Сканируйте QR-код для поиска...")
        button = QPushButton("Отменить")

        button.setDefault(False)
        button.setAutoDefault(False)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

        button.clicked.connect(self.close)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        self.on_scan(event)
        return super().eventFilter(obj, event)
