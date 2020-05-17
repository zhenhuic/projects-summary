from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def msg(self):
        reply = QMessageBox.information(self, "提示", "操作成功", QMessageBox.Yes)
