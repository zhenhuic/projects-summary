import sys

from PyQt5.QtWidgets import *
from Ui2 import Ui_MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #self.fullScreen.triggered.connect(self.showFullScreen)
        #self.exitFullScreen.triggered.connect(self.showNormal)


if __name__ == '__main__':
    sys.excepthook = except_hook  # print the traceback to stdout/stderr
    app = QApplication(sys.argv)
    window = MyWindow()

    window.setWindowTitle('AGV小车看板')
    #window.showFullScreen()
    window.show()
    sys.exit(app.exec_())