from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .table_model import TableModel

mock_data = [
    [4, 9, 2],
    [1, 0, 0],
    [3, 5, 0],
    [3, 3, 2],
    [7, 8, 9],
]


class UserListView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        controls_layout = QHBoxLayout()
        controls = QWidget()
        controls.setLayout(controls_layout)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Введите ключевое слово для поиска...")

        add_button = QPushButton("Добавить")
        search_button = QPushButton("Поиск")

        controls_layout.addWidget(search_input)
        controls_layout.addWidget(search_button)
        controls_layout.addWidget(add_button)

        table = QTableView()
        table_model = TableModel(mock_data)
        table.setModel(table_model)

        layout.addWidget(controls)
        layout.addWidget(table)
