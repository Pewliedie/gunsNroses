import sys
from typing import Callable

import qrcode
import win32print
import win32ui
from PIL import ImageWin
from PyQt6.QtWidgets import QMessageBox

from src.config import IMAGE_PRINT_HEIGHT, IMAGE_PRINT_WIDTH, TARGET_PRINTER_NAME
from src.log import logger

__all__ = ("printer_processor", "exception_handler")


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
