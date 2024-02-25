import sqlalchemy as sa
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from pygrabber.dshow_graph import FilterGraph

import src.models as m
import src.schemas as s
from src.db import session
from src.views.table_model import TableModel
from .edit import WebCamCreateForm
from src.config import DIALOG_MIN_WIDTH


class WebCamListView(QWidget):

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

        find_button.clicked.connect(self.reset_webcams)

    def fetch_data(self):
        query = sa.select(m.WebCam).order_by(m.WebCam.name)
        results = session.scalars(query)
        return results.all()
    
    def reset_webcams(self):

        graph = FilterGraph()
        webcams = graph.get_input_devices()

        for index, webcam in enumerate(webcams):
            if not session.query(m.WebCam).filter(m.WebCam.device_id == index).first():
                session.add(m.WebCam(device_id=index, name=webcam, type=m.WebCamType.DEFAULT))
                session.commit()
        
        self.refresh()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.WebCamListItem.from_obj(obj)) for obj in raw_data]
        table_model = TableModel(
            data=data,
            headers=self.headers,
        )
        self.table_view.setModel(table_model)

        for i in range(len(data)):
            entity_id = data[i][0][1]
            button = QPushButton("✏️")
            button.clicked.connect(
                lambda _, webcam_id=entity_id: self.show_edit_form(webcam_id)
            )
            self.table_view.setIndexWidget(table_model.index(i, 0), button)

        return len(data)

    def show_create_form(self):
        self.create_form = WebCamCreateForm()
        self.create_form.on_save.connect(self.refresh)
        self.create_form.show()

    def show_edit_form(self, webcam_id: int):
        self.edit_form = WebCamCreateForm(webcam_id)
        self.edit_form.on_save.connect(self.refresh)
        self.edit_form.show()

