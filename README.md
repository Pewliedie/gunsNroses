pip install python-escpos


PyQt6: Библиотека для создания графического интерфейса.

Установка с помощью pip: pip install PyQt6
qrcode: Библиотека для создания QR-кодов.

Установка с помощью pip: pip install qrcode
pillow: Библиотека для работы с изображениями (требуется для qrcode).

Установка с помощью pip: pip install pillow

from PyQt6 import QtCore, QtGui, QtWidgets
from pageAuth import Ui_Dialog
from pageenter1 import ui_enterpage2
import sqlite3
import sys
import barceode
from scanpage import Ui_scanpage
import datetime
import qrcode
import datetime
import random
import pyautogui
import subprocess
from PyQt6.QtGui import QPixmap


from escpos.printer import Usb

# Создание экземпляра принтера
printer = Usb(0x0483, 0x5740, 0, profile="XP-365B")

# Данные для штрих-кода
barcode_data = "123456789"

# Печать штрих-кода
printer.barcode(barcode_data, "EAN13", 64, 2, "", "")

# Сохранение и отправка печати
printer.cut()
printer.close()

