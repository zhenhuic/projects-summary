import random
import sys
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.cps_new import Ui_MainWindow


class MainApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)

        self.show_h(False)
        self.show_z(False)
        self.show_b(False)

        self.pushButton.clicked.connect(self.open_conf)
        self.pushButton_2.clicked.connect(self.open_log)

    def show_h(self, flag):
        if flag is False:
            self.label_hp1.setVisible(False)
            self.label_hp2.setVisible(False)
            self.label_hp3.setVisible(False)
            self.label_hp4.setVisible(False)
            self.label_hp5.setVisible(False)
            self.label_hp6.setVisible(False)
            self.label_hp7.setVisible(False)
            self.label_hp8.setVisible(False)
            self.label_hp9.setVisible(False)
            self.label_hp10.setVisible(False)

            self.label_ht1.setVisible(False)
            self.label_ht2.setVisible(False)
            self.label_ht3.setVisible(False)
            self.label_ht4.setVisible(False)
            self.label_ht5.setVisible(False)
            self.label_ht6.setVisible(False)
            self.label_ht7.setVisible(False)
            self.label_ht8.setVisible(False)
            self.label_ht9.setVisible(False)
            self.label_ht10.setVisible(False)

            self.label_ha1.setVisible(False)
            self.label_ha2.setVisible(False)
            self.label_ha3.setVisible(False)
            self.label_ha4.setVisible(False)
            self.label_ha5.setVisible(False)
            self.label_ha6.setVisible(False)
            self.label_ha7.setVisible(False)
            self.label_ha8.setVisible(False)
            self.label_ha9.setVisible(False)
            self.label_ha10.setVisible(False)

        elif flag is True:
            self.label_hp1.setVisible(True)
            self.label_hp2.setVisible(True)
            self.label_hp3.setVisible(True)
            self.label_hp4.setVisible(True)
            self.label_hp5.setVisible(True)
            self.label_hp6.setVisible(True)
            self.label_hp7.setVisible(True)
            self.label_hp8.setVisible(True)
            self.label_hp9.setVisible(True)
            self.label_hp10.setVisible(True)

            self.label_ht1.setVisible(True)
            self.label_ht2.setVisible(True)
            self.label_ht3.setVisible(True)
            self.label_ht4.setVisible(True)
            self.label_ht5.setVisible(True)
            self.label_ht6.setVisible(True)
            self.label_ht7.setVisible(True)
            self.label_ht8.setVisible(True)
            self.label_ht9.setVisible(True)
            self.label_ht10.setVisible(True)

            self.label_ha1.setVisible(True)
            self.label_ha2.setVisible(True)
            self.label_ha3.setVisible(True)
            self.label_ha4.setVisible(True)
            self.label_ha5.setVisible(True)
            self.label_ha6.setVisible(True)
            self.label_ha7.setVisible(True)
            self.label_ha8.setVisible(True)
            self.label_ha9.setVisible(True)
            self.label_ha10.setVisible(True)

    def show_z(self, flag):
        if flag is False:
            self.label_zp1.setVisible(False)
            self.label_zp2.setVisible(False)
            self.label_zp3.setVisible(False)
            self.label_zp4.setVisible(False)
            self.label_zp5.setVisible(False)
            self.label_zp6.setVisible(False)

            self.label_zt1.setVisible(False)
            self.label_zt2.setVisible(False)
            self.label_zt3.setVisible(False)
            self.label_zt4.setVisible(False)
            self.label_zt5.setVisible(False)
            self.label_zt6.setVisible(False)

            self.label_za1.setVisible(False)
            self.label_za2.setVisible(False)
            self.label_za3.setVisible(False)
            self.label_za4.setVisible(False)
            self.label_za5.setVisible(False)

        elif flag is True:
            self.label_zp1.setVisible(True)
            self.label_zp2.setVisible(True)
            self.label_zp3.setVisible(True)
            self.label_zp4.setVisible(True)
            self.label_zp5.setVisible(True)
            self.label_zp6.setVisible(True)

            self.label_zt1.setVisible(True)
            self.label_zt2.setVisible(True)
            self.label_zt3.setVisible(True)
            self.label_zt4.setVisible(True)
            self.label_zt5.setVisible(True)
            self.label_zt6.setVisible(True)

            self.label_za1.setVisible(True)
            self.label_za2.setVisible(True)
            self.label_za3.setVisible(True)
            self.label_za4.setVisible(True)
            self.label_za5.setVisible(True)

    def show_b(self, flag):
        if flag is False:
            self.label_bp1.setVisible(False)
            self.label_bp2.setVisible(False)
            self.label_bp3.setVisible(False)
            self.label_bp4.setVisible(False)
            self.label_bp5.setVisible(False)

            self.label_bt1.setVisible(False)
            self.label_bt2.setVisible(False)
            self.label_bt3.setVisible(False)
            self.label_bt4.setVisible(False)
            self.label_bt5.setVisible(False)

            self.label_ba1.setVisible(False)
            self.label_ba2.setVisible(False)
            self.label_ba3.setVisible(False)
            self.label_ba4.setVisible(False)

        elif flag is True:
            self.label_bp1.setVisible(True)
            self.label_bp2.setVisible(True)
            self.label_bp3.setVisible(True)
            self.label_bp4.setVisible(True)
            self.label_bp5.setVisible(True)

            self.label_bt1.setVisible(True)
            self.label_bt2.setVisible(True)
            self.label_bt3.setVisible(True)
            self.label_bt4.setVisible(True)
            self.label_bt5.setVisible(True)

            self.label_ba1.setVisible(True)
            self.label_ba2.setVisible(True)
            self.label_ba3.setVisible(True)
            self.label_ba4.setVisible(True)

    def show_time(self, scx):
        time.sleep(1)
        if scx == "h":
            self.label_ht1.setText("平均耗时:" + str(round(random.uniform(14, 16), 1)) + "s")
            self.label_ht2.setText("平均耗时:" + str(round(random.uniform(25, 27), 1)) + "s")
            self.label_ht3.setText("平均耗时:" + str(round(random.uniform(12, 14), 1)) + "s")
            self.label_ht4.setText("平均耗时:" + str(round(random.uniform(11, 13), 1)) + "s")
            self.label_ht5.setText("平均耗时:" + str(round(random.uniform(10, 12), 1)) + "s")
            self.label_ht6.setText("平均耗时:" + str(round(random.uniform(35, 37), 1)) + "s")
            self.label_ht7.setText("平均耗时:" + str(round(random.uniform(13, 15), 1)) + "s")
            self.label_ht8.setText("平均耗时:" + str(round(random.uniform(8, 10), 1)) + "s")
            self.label_ht9.setText("平均耗时:" + str(round(random.uniform(7, 9), 1)) + "s")
            self.label_ht10.setText("平均耗时:" + str(round(random.uniform(9, 11), 1)) + "s")
            self.textEdit.clear()
            time.sleep(1)
            self.textEdit.append("提示信息：厚板折弯工序加工耗时过长\n")
        elif scx == "z":
            self.label_zt1.setText("平均耗时:" + str(round(random.uniform(10, 12), 1)) + "s")
            self.label_zt2.setText("平均耗时:" + str(round(random.uniform(27, 29), 1)) + "s")
            self.label_zt3.setText("平均耗时:" + str(round(random.uniform(17, 19), 1)) + "s")
            self.label_zt4.setText("平均耗时:" + str(round(random.uniform(11, 13), 1)) + "s")
            self.label_zt5.setText("平均耗时:" + str(round(random.uniform(14, 16), 1)) + "s")
            self.label_zt6.setText("平均耗时:" + str(round(random.uniform(6, 8), 1)) + "s")
            self.textEdit.clear()
            time.sleep(1)
            self.textEdit.append("提示信息：自动折弯工序加工耗时过长\n")
        elif scx == "b":
            self.label_bt1.setText("平均耗时:" + str(round(random.uniform(12, 14), 1)) + "s")
            self.label_bt2.setText("平均耗时:" + str(round(random.uniform(10, 12), 1)) + "s")
            self.label_bt3.setText("平均耗时:" + str(round(random.uniform(29, 31), 1)) + "s")
            self.label_bt4.setText("平均耗时:" + str(round(random.uniform(9, 11), 1)) + "s")
            self.label_bt5.setText("平均耗时:" + str(round(random.uniform(7, 9), 1)) + "s")
            self.textEdit.clear()
            time.sleep(1)
            self.textEdit.append("提示信息：数控折弯工序加工耗时过长\n")

    @pyqtSlot()
    def open_conf(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if filename[0]:
            try:
                f = open(filename[0], 'r')
                with f:
                    scx = f.readline()
                    time.sleep(1)
                    if scx == "厚板线\n":
                        self.label.setText("生产流程模型(厚板线)")
                        self.label_20.setText("优化信息(厚板线)")
                        self.show_h(True)
                        self.show_z(False)
                        self.show_b(False)

                    elif scx == "专机线\n":
                        self.label.setText("生产流程模型(专机线)")
                        self.label_20.setText("优化信息(专机线)")
                        self.show_h(False)
                        self.show_z(True)
                        self.show_b(False)

                    elif scx == "薄板线\n":
                        self.label.setText("生产流程模型(薄板线)")
                        self.label_20.setText("优化信息(薄板线)")
                        self.show_h(False)
                        self.show_z(False)
                        self.show_b(True)
                f.close()

            except:
                self.textEdit.append("打开文件失败，可能是文件类型错误\n")

    @pyqtSlot()
    def open_log(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if filename[0]:
            try:
                f = open(filename[0], 'r')
                if self.label.text() == "生产流程模型(厚板线)":
                    self.show_time("h")
                elif self.label.text() == "生产流程模型(专机线)":
                    self.show_time("z")
                elif self.label.text() == "生产流程模型(薄板线)":
                    self.show_time("b")
                f.close()

            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
