import sqlalchemy as sa
from PyQt6.QtWidgets import QHeaderView, QTableView, QVBoxLayout, QWidget

import src.models as m
import src.schemas as s
from src.db import session
from src.views.table_model import TableModel


class SessionListView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table_view = QTableView()
        self.headers = [
            "ID",
            "Пользователь",
            "Дата входа",
            "Дата выхода",
            "Время сессии",
        ]
        self.refresh()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table_view)

    def fetch_data(self):
        query = sa.select(m.Session).order_by(m.Session.login.desc())
        results = session.scalars(query)
        return results.all()

    def refresh(self):
        raw_data = self.fetch_data()
        data = [list(s.SessionListItem.from_obj(obj)) for obj in raw_data]

        table_model = TableModel(
            data=data,
            headers=self.headers,
            hide_first_column=False,
        )
        self.table_view.setModel(table_model)

        return len(data)
