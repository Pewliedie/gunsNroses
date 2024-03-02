import sqlalchemy as sa
from pygrabber.dshow_graph import FilterGraph
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView, QPushButton, QTableView, QVBoxLayout, QWidget

import src.models as m
import src.schemas as s
from src.config import DIALOG_MIN_WIDTH
from src.db import session
from src.views.table_model import TableModel

from .edit import CameraEditForm


class CameraListView(QWidget):

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список веб-камер")
        self.setMinimumWidth(DIALOG_MIN_WIDTH)
        layout = QVBoxLayout()

        self.setLayout(layout)

        self.table_view = QTableView()
        self.headers = [
            "",
            "Номер устройства",
            "Наименование",
            "Тип",
        ]

        find_button = QPushButton("Инициализировать веб-камеры")

        self.refresh()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(find_button)
        layout.addWidget(self.table_view)

        find_button.clicked.connect(self.reset_cameras)

    def fetch_data(self):
        query = sa.select(m.Camera).order_by(m.Camera.name)
        results = session.scalars(query)
        return results.all()

    def reset_cameras(self):

        graph = FilterGraph()
        cameras = graph.get_input_devices()

        for index, camera in enumerate(cameras):
            if not session.query(m.Camera).filter(m.Camera.device_id == index).first():
                session.add(
                    m.Camera(device_id=index, name=camera, type=m.CameraType.DEFAULT)
                )
                session.commit()

        self.refresh()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.CameraListItem.from_obj(obj)) for obj in raw_data]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

        for i in range(len(data)):
            entity_id = data[i][0][1]
            button = QPushButton("✏️")
            button.clicked.connect(
                lambda _, camera_id=entity_id: self.show_edit_form(camera_id)
            )
            self.table_view.setIndexWidget(table_model.index(i, 0), button)

        return len(data)

    # TODO: код дублируется
    def show_create_form(self):
        self.create_form = CameraEditForm()
        self.create_form.on_save.connect(self.refresh)
        self.create_form.show()

    def show_edit_form(self, camera_id: int):
        self.edit_form = CameraEditForm(camera_id)
        self.edit_form.on_save.connect(self.refresh)
        self.edit_form.show()

    def closeEvent(self, event):
        self.finished.emit()
        super().closeEvent(event)
