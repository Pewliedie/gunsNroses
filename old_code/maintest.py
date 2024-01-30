import sqlite3
import sys

from pageAuth import Ui_Dialog
from pageenter1 import ui_enterpage2
from PyQt6 import QtCore, QtWidgets

import old_code.barcode as barcode


class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("Ввести данные")
        self.ui.pushButton_2.setText("Сканировать")
        self.ui.pushButton.clicked.connect(self.openDataEntryWindow)

    def openDataEntryWindow(self):
        self.close()  # Закрыть текущее окно
        dataEntryWindow = QtWidgets.QDialog()
        self.dataEntryUI = ui_enterpage2()
        self.dataEntryUI.setupUi(dataEntryWindow)
        self.dataEntryUI.label.setText(
            "Постановление\nо признании и приобщении к делу вещественных доказательств"
        )
        self.dataEntryUI.label_2.setText("Г. Караганда")
        self.dataEntryUI.label_3.setText("УСТАНОВИЛ:")
        self.dataEntryUI.label_4.setText("ПОСТАНОВИЛ:")
        self.dataEntryUI.label_5.setText("Дата:")
        self.dataEntryUI.plainTextEdit.setPlaceholderText("Введите данные")
        self.dataEntryUI.lineEdit.setPlaceholderText("в формате гг-мм-дд")
        self.dataEntryUI.lineEdit_2.setPlaceholderText("Вещь док 1")
        self.dataEntryUI.lineEdit_3.setPlaceholderText("Вещь док 2")
        self.dataEntryUI.lineEdit_4.setPlaceholderText("Вещь док 3")
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
        date = self.dataEntryUI.lineEdit.text()
        all_textline = f"{text_linentext1}, {text_linentext2}, {text_linentext3}"
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO test (postanovlenye, veshdock, date, barcode) VALUES (?, ?, ?, ?)",
            (text_plaintext, all_textline, date, barcode.data_string),
        )
        self.db_connection.commit()

    def openAuthWindow(self):
        self.show()  # Открыть первое окно
        self.sender().parent().close()  # Закрыть текущее окно

    def openSvgFromDatabase(self, svg_data):
        svg_widget = QtWidgets.QSvgWidget()
        svg_widget.load(QtCore.QByteArray.fromBase64(svg_data))
        svg_widget.show()

    def openSvgFromDatabaseById(self, barcode_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT barcode FROM test WHERE id=?", (barcode_id,))
        result = cursor.fetchone()
        if result is not None:
            svg_data = result[0]
            self.openSvgFromDatabase(svg_data)


app = QtWidgets.QApplication([])
application = Login()
application.show()
sys.exit(app.exec())
