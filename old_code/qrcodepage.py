from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_QRCodeWindow(object):
    def setupUi(self, QRCodeWindow):
        QRCodeWindow.setObjectName("QRCodeWindow")
        QRCodeWindow.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(QRCodeWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(QRCodeWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(QRCodeWindow)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(QRCodeWindow)  # Добавленный виджет label_3
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(QRCodeWindow)
        QtCore.QMetaObject.connectSlotsByName(QRCodeWindow)

    def retranslateUi(self, QRCodeWindow):
        _translate = QtCore.QCoreApplication.translate
        QRCodeWindow.setWindowTitle(_translate("QRCodeWindow", "QR Code"))
        self.label.setText(_translate("QRCodeWindow", "QR Code"))
        self.label_2.setText(_translate("QRCodeWindow", "Additional Label"))
        self.label_3.setText(
            _translate("QRCodeWindow", "QR Code Image")
        )  # Текст для label_3
