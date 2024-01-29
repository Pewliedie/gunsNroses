from pageAuth import Ui_Dialog
from pageenter1 import ui_enterpage2
import sqlite3
import sys
from scanpage import Ui_scanpage
import datetime
import qrcode
import datetime
import random
import pyautogui
import subprocess
from PyQt6.QtGui import QPixmap
from winuser import duser
import os
from PyQt6.QtWidgets import (
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore, QtWidgets
import os
import sys


class DragAndDropWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel(
            "Переместите файл формата *.jpeg, *.jpg сюда",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setAcceptDrops(True)  # Enable accepting dragged objects
        self.setFixedWidth(800)  # Set your desired width
        self.setFixedHeight(500)  # Set your desired height

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        target_dir = "C:/Users/Public/проект_27-07-2023/file/"
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if QtCore.QDir(file_path).exists():  # If the path points to a folder
                    # Perform moving the folder to the current directory
                    # You can specify another target folder if needed
                    QtCore.QDir().rename(
                        file_path,
                        QtCore.QDir(target_dir).filePath(
                            QtCore.QDir(file_path).dirName()
                        ),
                    )
                else:  # If the path points to a file
                    # Get the new file name (you can use any logic to generate a new name)
                    try:
                        new_file_name = f"{barcode1}.jpeg"
                        # Perform moving the file to the current directory with the new name
                        QtCore.QFile(file_path).rename(
                            QtCore.QDir(target_dir).filePath(new_file_name)
                        )
                    except NameError:
                        error_message = (
                            "Данные не заполнены. Не удается сохранить файл."
                        )
                        QMessageBox.critical(
                            self, "Ошибка", error_message, QMessageBox.StandardButton.Ok
                        )


class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("Ввести данные")
        self.ui.pushButton_2.setText("Сканировать")
        self.ui.pushButton.clicked.connect(self.openDataEntryWindow)
        self.ui.pushButton_2.clicked.connect(self.openDataScanpageWindow)
        self.ui.label_3.setText("Департамент полиции Карагандинской области МВД РК")
        pixmap = QPixmap("Logo_MVD_KZ250.png")
        self.ui.label.setPixmap(pixmap)

    def openDataScanpageWindow(self):
        self.close()  # Закрыть текущее окно
        dataEntryWindow = QtWidgets.QDialog()
        self.dataEntryUI2 = Ui_scanpage()
        self.dataEntryUI2.setupUi(dataEntryWindow)
        self.dataEntryUI2.pushButton.setText("Найти")
        self.dataEntryUI2.pushButton_2.setText("Назад")
        self.dataEntryUI2.pushButton_2.clicked.connect(self.openAuthWindow)
        self.dataEntryUI2.lineEdit.setPlaceholderText("Ввести id")
        self.dataEntryUI2.textBrowser.setText("Результат")
        self.dataEntryUI2.pushButton.clicked.connect(
            self.SearchId
        )  # Связать нажатие кнопки с методом поиска
        self.db_connection = sqlite3.connect("database.db")
        self.dataEntryUI2.pushButton_3.setText("Открыть папку c видео файлами")
        self.dataEntryUI2.pushButton_3.clicked.connect(self.openFolder)
        self.dataEntryUI2.label.setText("Статус:")
        self.dataEntryUI2.label4.setText("Не выбран")
        self.dataEntryUI2.pushButton_4.setText("Открыть скан")
        self.dataEntryUI2.pushButton_5.setText("Сохранить")
        self.dataEntryUI2.pushButton_4.clicked.connect(self.openImage)
        self.dataEntryUI2.pushButton_5.clicked.connect(self.save_status)
        self.dataEntryUI2.label3.setText("")
        self.dataEntryUI2.comboBox.setPlaceholderText("Не выбран")
        self.dataEntryUI2.comboBox.addItems(["Уничтожено", "Вручено", "На хранении"])
        self.dataEntryUI2.label_2.setText("")
        # Создайте экземпляр класса DragAndDropWidget и добавьте его в макет окна
        self.drag_and_drop_widget = DragAndDropWidget()
        main_layout = QtWidgets.QVBoxLayout(dataEntryWindow)
        x = 780
        y = 100
        self.drag_and_drop_widget.move(x, y)
        h_layout = QtWidgets.QHBoxLayout()  # Горизонтальный макет для выравнивания
        h_layout.addWidget(self.drag_and_drop_widget)
        main_layout.addLayout(h_layout)
        layout = QtWidgets.QVBoxLayout(dataEntryWindow)
        layout.addWidget(self.drag_and_drop_widget)
        dataEntryWindow.exec()

    def openFolder(self):
        folder_path = r"C:\Users\Public\проект_27-07-2023\rec\c5282770c2bcae4a3d6c6c93eac2b7ef"  # Замените на путь к папке, которую нужно открыть
        subprocess.Popen(f'explorer "{folder_path}"')

    def SearchId(self):
        cursor = self.db_connection.cursor()
        text_linentext1 = self.dataEntryUI2.lineEdit.text()
        cursor.execute("SELECT * FROM test WHERE barcode=?", (text_linentext1,))
        result = cursor.fetchone()

        if result is not None:
            # Извлечь значения из результата
            postanovlenye = result[0]  # Индекс 1 соответствует столбцу 'postanovlenye'
            veshdock = result[2]  # Индекс 2 соответствует столбцу 'veshdock'
            sledovatel = result[4]
            date = result[3]
            barcode = result[1]
            userpc = result[5]
            status = result[6]
            # Установить значения в textBrowser
            self.dataEntryUI2.textBrowser.setText(
                f"""                                                                      Постановление\n                                    о признании и приобщении к делу вещественных доказательств\n\nг.Караганда                                                                                                                                                  Дата заполнения: {date}\n\n{sledovatel}\n\n                                                                      УСТАНОВИЛ:\n{postanovlenye}\n\n                                                                      ПОСТАНОВИЛ:\nПризнать и приобщить к материалам досудебного расследования в качестве вещественного доказательства:\n{veshdock}\n\nИдентификатор:\n{barcode}\n\nКем создано: {userpc}"""
            )
            self.dataEntryUI2.label4.setText(status)
        else:
            self.dataEntryUI2.textBrowser.setText("Результат не найден")

    def openImage(self):
        cursor = self.db_connection.cursor()
        text_linentext1 = self.dataEntryUI2.lineEdit.text()
        cursor.execute("SELECT * FROM test WHERE barcode=?", (text_linentext1,))
        result = cursor.fetchone()
        try:
            if result is not None:
                # Извлечь значения из результата
                status = result[1]
                print(status)
                filename = status
                file_paths = [
                    os.path.join(
                        "C:/Users/Public/проект_27-07-2023/file/", f"{filename}.jpg"
                    ),
                    os.path.join(
                        "C:/Users/Public/проект_27-07-2023/file/", f"{filename}.jpeg"
                    ),
                ]
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.startfile(file_path)
                    break
            else:
                print("Файл не найден.")
                self.dataEntryUI2.label_2.setText("Файл не найден")
        except UnboundLocalError:
            error_message = "Данные не заполнены. Не удается найти файл."
            QMessageBox.critical(
                self, "Ошибка", error_message, QMessageBox.StandardButton.Ok
            )

    def save_status(self):
        cursor = self.db_connection.cursor()
        status_text = self.dataEntryUI2.comboBox.currentText()
        global barcode1
        barcode1 = self.dataEntryUI2.lineEdit.text()
        cursor.execute(
            "UPDATE test SET status=? WHERE barcode=?", (status_text, barcode1)
        )
        self.dataEntryUI2.label4.setText(status_text)
        self.db_connection.commit()

    def openDataEntryWindow(self):
        self.close()  # Закрыть текущее окно
        dataEntryWindow = QtWidgets.QDialog()
        self.dataEntryUI = ui_enterpage2()
        self.dataEntryUI.setupUi(dataEntryWindow)
        self.dataEntryUI.label.setText(
            """                              Постановление\nо признании и приобщении к делу вещественных доказательств"""
        )
        self.dataEntryUI.label_2.setText("""   г.Караганда""")
        self.dataEntryUI.label_3.setText(
            """                                                                    УСТАНОВИЛ:"""
        )
        self.dataEntryUI.label_4.setText(
            """                                                                    ПОСТАНОВИЛ:\nПризнать и приобщить к материалам досудебного расследования в качестве вещественного доказательства:"""
        )
        self.dataEntryUI.label_5.setText("Дата:")
        self.dataEntryUI.plainTextEdit.setPlaceholderText("Введите данные")
        self.dataEntryUI.lineEdit.setPlaceholderText("в формате гггг-мм-дд")
        self.dataEntryUI.lineEdit_2.setPlaceholderText("Вещь док 1")
        self.dataEntryUI.lineEdit_3.setPlaceholderText("Вещь док 2")
        self.dataEntryUI.lineEdit_4.setPlaceholderText("Вещь док 3")
        self.dataEntryUI.plainTextEdit_2.setPlainText(
            "Следователь Кировского ОП УП г.Караганда                      №324 Центрального ОП по адресу: ул.Терешковой 36, рассмотрев материалы уголовного дела №"
        )
        self.dataEntryUI.pushButton.setText("сохранить")
        self.dataEntryUI.pushButton_2.setText("назад")
        self.dataEntryUI.pushButton_2.clicked.connect(
            self.openAuthWindow
        )  # Связать нажатие кнопки с открытием первого окна
        self.dataEntryUI.pushButton.clicked.connect(
            self.saveDataToDatabase
        )  # Связать нажатие кнопки с сохранением данных
        self.db_connection = sqlite3.connect(
            "database.db"
        )  # Подключиться к базе данных SQLite
        dataEntryWindow.exec()

    def saveDataToDatabase(self):
        text_plaintext = (
            self.dataEntryUI.plainTextEdit.toPlainText()
        )  # Получить введенные данные
        text_linentext1 = self.dataEntryUI.lineEdit_2.text()
        text_linentext2 = self.dataEntryUI.lineEdit_3.text()
        text_linentext3 = self.dataEntryUI.lineEdit_4.text()
        sledov = self.dataEntryUI.plainTextEdit_2.toPlainText()
        date = self.dataEntryUI.lineEdit.text()
        all_textline = f"{text_linentext1}, {text_linentext2}, {text_linentext3}"
        cursor = self.db_connection.cursor()
        barcode = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        current_datetime = datetime.datetime.now()
        # Получение текущей даты и времени
        current_datetime = datetime.datetime.now()
        # Генерация случайного числа из секунд
        random_number = random.randint(0, 59)
        # Получение текущих координат мыши
        mouse_position = pyautogui.position()
        # Создание строки, объединяющей дату, случайное число и координаты мыши
        data_string = (
            f"{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}+{random_number}"
        )
        data_string = ''.join(c for c in data_string if c.isdigit())
        data_string = f"{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        data_string = ''.join(c for c in data_string if c.isdigit())
        barcode.add_data(data_string)
        barcode.make(fit=True)
        barcode_image = barcode.make_image(fill_color="black", back_color="white")
        barcode_image.save(
            f"./barcode/L{data_string}.png"
        )  # Сохранение штрих-кода в файл
        cursor.execute(
            "INSERT INTO test (postanovlenye, veshdock, date, barcode, sledovatel, user) VALUES (?, ?, ?, ?, ?, ?)",
            (text_plaintext, all_textline, date, data_string, sledov, duser),
        )
        self.db_connection.commit()
        self.show()  # Открыть первое окно
        self.sender().parent().close()  # З
        self.openQRCodeWindow(data_string)  # Открыть окно с QR-кодом

    def openQRCodeWindow(self, data_string):
        os.startfile(f".\\barcode\\L{data_string}.png", "print")

    def openAuthWindow(self):
        self.show()  # Открыть первое окно
        self.sender().parent().close()  # З


app = QtWidgets.QApplication([])
application = Login()
application.show()
sys.exit(app.exec())
