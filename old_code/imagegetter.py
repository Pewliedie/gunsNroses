import sqlite3

from PIL import Image
from PyQt6 import QtGui, QtWidgets


# Функция для получения изображения штрих-кода из базы данных
def get_barcode_image(barcode_id):
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()
    cursor.execute("SELECT barcode FROM test WHERE barcode = ?", (barcode_id,))
    result = cursor.fetchone()
    db_connection.close()

    if result:
        barcode_data = result[0]
        image_path = f".\\barcode\\barcode{barcode_data}.png"
        try:
            image = Image.open(image_path)
            return image
        except IOError:
            print("Ошибка загрузки изображения штрих-кода.")

    return None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Просмотр штрих-кода")
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)

        # Создание кнопки для запроса изображения штрих-кода
        self.button = QtWidgets.QPushButton("Получить штрих-код", self)
        self.button.clicked.connect(self.show_barcode_image)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_barcode_image(self):
        barcode_id = '2023062215571546721125550'  # Здесь вы можете указать нужный идентификатор штрих-кода
        image = get_barcode_image(barcode_id)
        if image:
            image_data = image.tobytes()
            qimage = QtGui.QImage.fromData(image_data)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.label.setPixmap(pixmap)


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
