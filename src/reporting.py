from openpyxl import Workbook

def export_xlsx(headers: list[str], rows: list[str], file_name: str):
    wb = Workbook()
    ws = wb.active

    ws.append(headers)

    for row in rows:
        ws.append(row)

    wb.save(file_name)
