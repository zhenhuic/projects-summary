import random
import sys
import threading
import time
import cv2
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import *
from main.cps_plot import FigureLineChart
from ui.mining import Ui_MainWindow


class CPS(QMainWindow):

    flag = False
    flc = FigureLineChart()

    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.main_ui.action.triggered.connect(self.action_trigger)
        self.main_ui.action_2.triggered.connect(self.action_trigger2)
        self.main_ui.action_3.triggered.connect(self.action_trigger3)
        self.main_ui.action_4.triggered.connect(self.action_trigger4)
        self.main_ui.action_5.triggered.connect(self.action_trigger5)

    # 菜单栏-运行-开始
    def action_trigger(self):
        t = threading.Thread(target=self.run)
        t.start()

    # 菜单栏-运行-停止
    def action_trigger5(self):
        self.flag = False
        if self.main_ui.label.text() == "生产流程工序实时耗时分析(厚板线) - 运行中":
            self.main_ui.label.setText("生产流程工序实时耗时分析(厚板线) - 暂停")
            self.main_ui.label_33.setText("生产流程工序耗时统计(厚板线) - 暂停")
        elif self.main_ui.label.text() == "生产流程工序实时耗时分析(焊接线) - 运行中":
            self.main_ui.label.setText("生产流程工序实时耗时分析(焊接线) - 暂停")
            self.main_ui.label_33.setText("生产流程工序耗时统计(焊接线) - 暂停")
        elif self.main_ui.label.text() == "生产流程工序实时耗时分析(新萨瓦尼尼线) - 运行中":
            self.main_ui.label.setText("生产流程工序实时耗时分析(新萨瓦尼尼线) - 暂停")
            self.main_ui.label_33.setText("生产流程工序耗时统计(新萨瓦尼尼线) - 暂停")

    def run(self):
        self.flag = True
        while self.flag:
            if self.main_ui.label.text() == "生产流程工序实时耗时分析(厚板线)":
                self.main_ui.label.setText("生产流程工序实时耗时分析(厚板线) - 运行中")
                self.main_ui.label_33.setText("生产流程工序耗时统计(厚板线) - 运行中")
            elif self.main_ui.label.text() == "生产流程工序实时耗时分析(焊接线)":
                self.main_ui.label.setText("生产流程工序实时耗时分析(焊接线) - 运行中")
                self.main_ui.label_33.setText("生产流程工序耗时统计(焊接线) - 运行中")
            elif self.main_ui.label.text() == "生产流程工序实时耗时分析(新萨瓦尼尼线)":
                self.main_ui.label.setText("生产流程工序实时耗时分析(新萨瓦尼尼线) - 运行中")
                self.main_ui.label_33.setText("生产流程工序耗时统计(新萨瓦尼尼线) - 运行中")
            time.sleep(random.uniform(5, 10))
            self.main_ui.label_23.setText("实时耗时：" + str(self.flc.jgqg_m) + "s")
            self.main_ui.label_24.setText("实时耗时：" + str(self.flc.skzw_m) + "s")
            self.main_ui.label_25.setText("实时耗时：" + str(self.flc.hbzw_m) + "s")
            self.main_ui.label_26.setText("实时耗时：" + str(self.flc.yld_m) + "s")
            self.main_ui.label_27.setText("实时耗时：" + str(self.flc.zdhj_m) + "s")
            self.main_ui.label_28.setText("实时耗时：" + str(self.flc.dmqz_m) + "s")
            self.main_ui.label_29.setText("实时耗时：" + str(self.flc.jgdb_m) + "s")
            self.main_ui.label_30.setText("实时耗时：" + str(self.flc.ABjzj_m) + "s")
            self.main_ui.label_31.setText("实时耗时：" + str(self.flc.pf_m) + "s")
            self.main_ui.label_32.setText("实时耗时：" + str(self.flc.zp_m) + "s")
            self.plot()
            pix = QPixmap("1.jpg")
            self.main_ui.label_34.setPixmap(pix)
            self.flc.update()

    # 菜单栏-设置-监控线设置-厚板线
    def action_trigger2(self):
        self.main_ui.label.setText("生产流程工序实时耗时分析(厚板线)")
        self.main_ui.label_33.setText("生产流程工序耗时统计(厚板线)")

    # 菜单栏-设置-监控线设置-焊接线
    def action_trigger3(self):
        self.main_ui.label.setText("生产流程工序实时耗时分析(焊接线)")
        self.main_ui.label_33.setText("生产流程工序耗时统计(焊接线)")

    # 菜单栏-设置-监控线设置-新萨瓦尼尼线
    def action_trigger4(self):
        self.main_ui.label.setText("生产流程工序实时耗时分析(新萨瓦尼尼线)")
        self.main_ui.label_33.setText("生产流程工序耗时统计(新萨瓦尼尼线)")

    # 绘图
    def plot(self):
        self.flc.plotlinechart()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    cps = CPS()
    cps.show()
    sys.exit(app.exec_())
