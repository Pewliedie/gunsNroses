from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        print(data)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if len(self._data) > 0:
            return len(self._data[0].dict())
        else:
            return 0
