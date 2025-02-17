import os

from PyQt6.QtCore import QDateTime, QDir, QTimeZone

DEBUG = False
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(ROOT_DIR, "database.db")
ICON_PATH = os.path.join(ROOT_DIR, "assets/icon.png")
FONT_PATH = os.path.join(ROOT_DIR, "assets/fonts/Montserrat-Regular.ttf")
DESKTOP_PATH = QDir.homePath() + '/Desktop'

APP_NAME = "E-Aigaq"

MAIN_WINDOW_MIN_WIDTH = 1200
MAIN_WINDOW_MIN_HEIGHT = 800

DIALOG_MIN_WIDTH = 640
DIALOG_MIN_HEIGHT = 480

TODAY = QDateTime.currentDateTime()
TODAY.setTimeZone(QTimeZone.systemTimeZone())

TARGET_PRINTER_NAME = "Xprinter XP-365B"
IMAGE_PRINT_WIDTH = 200
IMAGE_PRINT_HEIGHT = 200


RANK_LIST = [
    # "Рядовой",
    "Младший сержант",
    "Сержант",
    "Старший сержант",
    "Старшина",
    "Младший лейтенант",
    "Лейтенант",
    "Старший лейтенант",
    "Капитан",
    "Майор",
    "Подполковник",
    "Полковник",
    # "Генерал-майор",
    # "Генерал-лейтенант",
    # "Генерал-полковник",
]
