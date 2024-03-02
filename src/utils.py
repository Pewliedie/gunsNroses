import os
import sys
import time
from datetime import datetime
from typing import Callable

import cv2
import qrcode
import sqlalchemy as sa
import win32print
import win32ui
from PIL import ImageWin
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

import src.models as m
from src.config import (
    IMAGE_PRINT_HEIGHT,
    IMAGE_PRINT_WIDTH,
    ROOT_DIR,
    TARGET_PRINTER_NAME,
)
from src.db import session
from src.log import logger

__all__ = (
    "printer_processor",
    "video_recorder",
    "exception_handler",
    "get_current_user",
)


class PrinterProcessor:
    def __init__(self, printer_name: str):
        self.printer_name = printer_name

    def get_printers(self):
        return [
            printer[2]
            for printer in win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL, None, 1
            )
        ]

    def print_qr_code(
        self, text, on_end: None = None, on_error: Callable[[str], None] | None = None
    ):
        if self.printer_name not in self.get_printers():
            error_message = "Принтер не найден"
            if on_error:
                on_error(error_message)
            return

        image = qrcode.make(text)

        printer_handle = win32print.OpenPrinter(self.printer_name)
        win32print.GetPrinter(printer_handle)

        printer_dc = win32ui.CreateDC()
        printer_dc.CreatePrinterDC(self.printer_name)

        win32print.StartDocPrinter(printer_handle, 1, ("QR Code", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)

        printer_dc.StartDoc("QR Code")
        printer_dc.StartPage()

        dib = ImageWin.Dib(image)
        dib.draw(
            printer_dc.GetHandleOutput(), (0, 0, IMAGE_PRINT_WIDTH, IMAGE_PRINT_HEIGHT)
        )

        printer_dc.EndPage()
        printer_dc.EndDoc()

        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)

        if on_end:
            on_end()


printer_processor = PrinterProcessor(TARGET_PRINTER_NAME)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            QMessageBox.critical(
                None,
                "Ошибка",
                "Возникла ошибка в ходе работы приложения. "
                f"Обратитесь в тех.поддержку. "
                f"Подробнее: {e}",
            )
            sys.exit(-1)

    return wrapper


class VideoRecorder(QThread):

    finished = pyqtSignal()

    def __init__(self, save_path=ROOT_DIR + '/records', record_duration=10):
        super().__init__()
        self.running = False
        camera_index = self.get_camera_index()
        if camera_index is None:
            logger.error("No camera found for recording")
            return

        self.camera_index = camera_index
        self.save_path = save_path
        self.record_duration = record_duration

    def run(self):
        self.running = True
        try:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.save_path}/video_{current_time}.mp4"
            cap = cv2.VideoCapture(self.camera_index + cv2.CAP_DSHOW)

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            start_time = time.time()

            while self.running and (time.time() - start_time) < self.record_duration:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
        finally:
            self.finished.emit()

    def get_camera_index(self) -> int | None:
        # session.query(m.Camera).filter(m.Camera.type == m.CameraType.REC).first()
        return 0

    def stop(self):
        self.running = False


video_recorder = VideoRecorder()


def get_current_user() -> m.User | None:
    current_session = session.scalar(
        sa.select(m.Session).where(m.Session.active.is_(True))
    )
    return current_session.user if current_session else None
