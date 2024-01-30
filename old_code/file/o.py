from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDir, QFile, QFileInfo, Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DragAndDropWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel(
            "Drag and drop a file here", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setAcceptDrops(True)  # Enable accepting dragged objects

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        target_dir = "C:/Users/makar/Desktop/Meiram/бизнес/проект_26-07-2023/file/"
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
                    new_file_name = "new_file_name.jpeg"
                    # Perform moving the file to the current directory with the new name
                    QtCore.QFile(file_path).rename(
                        QtCore.QDir(target_dir).filePath(new_file_name)
                    )


class Ui_scanpage(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        # Create the DragAndDropWidget instance
        self.drag_and_drop_widget = DragAndDropWidget()
        # Set the layout of the QDialog to the layout of the DragAndDropWidget
        layout = QtWidgets.QVBoxLayout(Dialog)
        layout.addWidget(self.drag_and_drop_widget)

        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 70, 571, 371))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 70, 750, 500))
        self.textBrowser.setObjectName("textBrowser")
        self.layoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 40, 265, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 630, 320, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(400, 600, 40, 28))
        self.label.setObjectName("label")
        self.label4 = QtWidgets.QLabel(parent=Dialog)
        self.label4.setGeometry(QtCore.QRect(440, 600, 150, 28))
        self.label4.setObjectName("label")
        self.label3 = QtWidgets.QLabel(parent=Dialog)
        self.label3.setGeometry(QtCore.QRect(1050, 88, 300, 100))
        self.label3.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(400, 660, 150, 28))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(400, 630, 240, 28))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_4 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 660, 140, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(650, 630, 140, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.line = QtWidgets.QFrame(parent=Dialog)
        self.line.setGeometry(QtCore.QRect(800, 160, 700, 3))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(parent=Dialog)
        self.line_2.setGeometry(QtCore.QRect(800, 160, 3, 410))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(parent=Dialog)
        self.line_3.setGeometry(QtCore.QRect(1500, 160, 3, 410))
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(parent=Dialog)
        self.line_4.setGeometry(QtCore.QRect(800, 570, 700, 3))
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.drag_and_drop_widget = DragAndDropWidget()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "PushButton"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.pushButton_3.setText(_translate("Dialog", "PushButton"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.label3.setText(_translate("Dialog", "TextLabel"))
        self.label4.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_4.setText(_translate("Dialog", "PushButton"))
        self.pushButton_5.setText(_translate("Dialog", "PushButton"))
        self.label_2.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_scanpage()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())


import datetime
import os
import random
import sqlite3
import subprocess
import sys

import pyautogui
import qrcode
from pageAuth import Ui_Dialog
from pageenter1 import ui_enterpage2
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDir, QFile, QFileInfo, Qt
from PyQt6.QtGui import QImageReader, QImageWriter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qrcodepage import Ui_QRCodeWindow
from scanpage import Ui_scanpage
from winuser import duser

import old_code.barcode as barcode


class DragAndDropWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel(
            "Drag and drop a file here", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setAcceptDrops(True)  # Enable accepting dragged objects

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        target_dir = "C:/Users/makar/Desktop/Meiram/бизнес/проект_26-07-2023/file/"
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
                    new_file_name = "new_file_name.jpeg"
                    # Perform moving the file to the current directory with the new name
                    QtCore.QFile(file_path).rename(
                        QtCore.QDir(target_dir).filePath(new_file_name)
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
        self.dataEntryUI2.label3.setText("Переместите файл формата *.jpeg, *.jpg сюда:")
        self.dataEntryUI2.comboBox.setPlaceholderText("Не выбран")
        self.dataEntryUI2.comboBox.addItems(["Уничтожено", "Вручено", "На хранении"])
        self.dataEntryUI2.label_2.setText("")
        dataEntryWindow.exec()

    def openFolder(self):
        folder_path = r"C:\Users\Public\проект\rec\c5282770c2bcae4a3d6c6c93eac2b7ef"  # Замените на путь к папке, которую нужно открыть
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
        if result is not None:
            # Извлечь значения из результата
            status = result[1]
            print(status)
        filename = status
        file_paths = [
            os.path.join(
                "C:/Users/makar/Desktop/Meiram/бизнес/проект/file/", f"{filename}.jpg"
            ),
            os.path.join(
                "C:/Users/makar/Desktop/Meiram/бизнес/проект/file/", f"{filename}.png"
            ),
        ]

        for file_path in file_paths:
            if os.path.exists(file_path):
                os.startfile(file_path)
                break
        else:
            print("Файл не найден.")
            self.dataEntryUI2.label_2.setText("Файл не найден")

    def save_status(self):
        cursor = self.db_connection.cursor()
        status_text = self.dataEntryUI2.comboBox.currentText()
        barcode = self.dataEntryUI2.lineEdit.text()
        cursor.execute(
            "UPDATE test SET status=? WHERE barcode=?", (status_text, barcode)
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
