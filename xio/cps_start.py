import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.cps import Ui_MainWindow
from ui.cps_model import Ui_MainWindow2
from ui.cps_analyse import Ui_MainWindow3


class CPS(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


class Model(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow2()
        self.main_ui.setupUi(self)


class Analyse(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow3()
        self.main_ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cps = CPS()
    model = Model()
    analyse = Analyse()
    btn = cps.main_ui.pushButton
    btn.clicked.connect(model.show)
    btn2 = cps.main_ui.pushButton_2
    btn2.clicked.connect(analyse.show)
    cps.show()
    sys.exit(app.exec_())
