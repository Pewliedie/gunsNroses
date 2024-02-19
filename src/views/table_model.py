from datetime import datetime

from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers, hide_first_column=True):
        super(TableModel, self).__init__()
        self.hide_first_column = hide_first_column
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()

            if col == 0 and self.hide_first_column:
                return None

            value = self._data[row][col][1]

            if isinstance(value, datetime):
                return value.strftime("%d %b %Y %H:%M:%S")

            return value
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._headers[section]
        return super().headerData(section, orientation, role)
