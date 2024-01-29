from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QDir, QFile, QFileInfo
from PyQt6 import QtCore, QtWidgets


class DragAndDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setAcceptDrops(True)  # Enable accepting dragged objects

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        target_dir = "C:/Users/makar/Desktop/Meiram/бизнес/проект/file/"
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if QDir(file_path).exists():  # If the path points to a folder
                    # Perform moving the folder to the current directory
                    # You can specify another target folder if needed
                    QDir().rename(
                        file_path, QDir(target_dir).filePath(QDir(file_path).dirName())
                    )
                else:  # If the path points to a file
                    # Perform moving the file to the current directory
                    QFile(file_path).rename(
                        QDir(target_dir).filePath(QFileInfo(file_path).fileName())
                    )


class Ui_scanpage(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)

        # Create a DragAndDropWidget instance and set it as central widget
        self.drag_and_drop_widget = DragAndDropWidget()
        Dialog.setCentralWidget(self.drag_and_drop_widget)

        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 70, 571, 371))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 70, 750, 500))
        self.textBrowser.setObjectName("textBrowser")
        self.layoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 40, 265, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 600, 320, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(400, 600, 150, 28))
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(parent=Dialog)
        self.label2.setGeometry(QtCore.QRect(1100, 250, 150, 28))
        self.label2.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 630, 250, 28))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_4 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 660, 150, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(650, 630, 150, 28))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "PushButton"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.pushButton_3.setText(_translate("Dialog", "PushButton"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.label2.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_4.setText(_translate("Dialog", "PushButton"))
        self.pushButton_5.setText(_translate("Dialog", "PushButton"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()  # Use QMainWindow for central widget support
    ui = Ui_scanpage()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
