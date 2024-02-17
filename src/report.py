from openpyxl import Workbook
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from src.config import FONT_PATH


def export_to_xlsx(headers: list[str], rows: list[str], file_path: str):
    wb = Workbook()
    ws = wb.active

    ws.append(headers)

    for row in rows:
        ws.append(row)

    wb.save(file_path)


def export_to_pdf(headers: list[str], rows: list[str], file_path: str):
    doc = SimpleDocTemplate(file_path, pagesize=landscape(A4))

    pdfmetrics.registerFont(TTFont('Montserrat', FONT_PATH))

    elements = []

    style = TableStyle(
        [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                (0.7, 0.7, 0.7),
            ),
            ("TEXTCOLOR", (0, 0), (-1, 0), (1, 1, 1)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
            ('FONTNAME', (0, 0), (-1, -1), 'Montserrat'),
        ]
    )

    table = Table([headers] + rows)
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)
