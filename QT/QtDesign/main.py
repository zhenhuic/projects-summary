# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from DataBase.utils import *
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties


class MyFigure(FigureCanvas):
    def __init__(self, width=4, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()


class Ui_MainWindow(object):

    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainWindow)
        self.mainWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1089, 871)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.ALL = QtWidgets.QTabWidget(self.centralwidget)
        self.ALL.setGeometry(QtCore.QRect(10, 10, 1071, 851))
        self.ALL.setObjectName("ALL")

        self.singleBQ = QtWidgets.QWidget()
        self.singleBQ.setObjectName("singleBQ")
        self.gridLayoutWidget = QtWidgets.QWidget(self.singleBQ)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1051, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_18 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout.addWidget(self.pushButton_18, 1, 3, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 0, 4, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout.addWidget(self.pushButton_16, 3, 3, 1, 1)
        self.pushButton_21 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_21.setObjectName("pushButton_21")
        self.gridLayout.addWidget(self.pushButton_21, 1, 6, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 0, 0, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout.addWidget(self.pushButton_15, 3, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.pushButton_26 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_26.setObjectName("pushButton_26")
        self.gridLayout.addWidget(self.pushButton_26, 3, 4, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 3, 0, 1, 1)
        self.pushButton_25 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_25.setObjectName("pushButton_25")
        self.gridLayout.addWidget(self.pushButton_25, 2, 6, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 2, 2, 1, 1)
        self.pushButton_24 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_24.setObjectName("pushButton_24")
        self.gridLayout.addWidget(self.pushButton_24, 2, 5, 1, 1)
        self.pushButton_28 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_28.setObjectName("pushButton_28")
        self.gridLayout.addWidget(self.pushButton_28, 3, 6, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 2, 0, 1, 1)
        self.pushButton_23 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_23.setObjectName("pushButton_23")
        self.gridLayout.addWidget(self.pushButton_23, 2, 4, 1, 1)
        self.pushButton_27 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_27.setObjectName("pushButton_27")
        self.gridLayout.addWidget(self.pushButton_27, 3, 5, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 3, 1, 1)
        self.pushButton_22 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_22.setObjectName("pushButton_22")
        self.gridLayout.addWidget(self.pushButton_22, 2, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout.addWidget(self.pushButton_20, 1, 5, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout.addWidget(self.pushButton_17, 1, 2, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 2, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 5, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 1, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 3, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 0, 6, 1, 1)
        self.pushButton_19 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_19.setObjectName("pushButton_19")
        self.gridLayout.addWidget(self.pushButton_19, 1, 4, 1, 1)
        self.graphicsView_1 = QtWidgets.QGraphicsView(self.singleBQ)
        self.graphicsView_1.setGeometry(QtCore.QRect(10, 250, 521, 551))
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.singleBQ)
        self.graphicsView_2.setGeometry(QtCore.QRect(540, 250, 521, 551))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.ALL.addTab(self.singleBQ, "")
        self.SomeBQ = QtWidgets.QWidget()
        self.SomeBQ.setObjectName("SomeBQ")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.SomeBQ)
        self.graphicsView_3.setGeometry(QtCore.QRect(10, 40, 1045, 351))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.label_1 = QtWidgets.QLabel(self.SomeBQ)
        self.label_1.setGeometry(QtCore.QRect(10, 5, 131, 31))
        self.label_1.setObjectName("label_1")
        # self.label_2 = QtWidgets.QLabel(self.SomeBQ)
        # self.label_2.setGeometry(QtCore.QRect(550, 0, 131, 31))
        # self.label_2.setObjectName("label_2")
        # self.graphicsView_4 = QtWidgets.QGraphicsView(self.SomeBQ)
        # self.graphicsView_4.setGeometry(QtCore.QRect(550, 40, 501, 351))
        # self.graphicsView_4.setObjectName("graphicsView_4")
        self.singleBQ.setStyleSheet("background-color: rgb(39, 39, 39);\n"


                               "color: rgb(255, 255, 255);\n"
                               "")

        self.SomeBQ.setStyleSheet("background-color: rgb(39, 39, 39);\n"


                                    "color: rgb(255, 255, 255);\n"
                                    "")
        self.label_3 = QtWidgets.QLabel(self.SomeBQ)
        self.label_3.setGeometry(QtCore.QRect(10, 400, 131, 31))
        self.label_3.setObjectName("label_3")
        self.graphicsView_5 = QtWidgets.QGraphicsView(self.SomeBQ)
        self.graphicsView_5.setGeometry(QtCore.QRect(10, 430, 1045, 381))
        self.graphicsView_5.setObjectName("graphicsView_5")
        # self.label_4 = QtWidgets.QLabel(self.SomeBQ)
        # self.label_4.setGeometry(QtCore.QRect(550, 395, 131, 31))
        # self.label_4.setObjectName("label_4")
        # self.graphicsView_6 = QtWidgets.QGraphicsView(self.SomeBQ)
        # self.graphicsView_6.setGeometry(QtCore.QRect(550, 430, 501, 381))
        # self.graphicsView_6.setObjectName("graphicsView_6")
        self.ALL.addTab(self.SomeBQ, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.ALL.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.settingButtonClick()

    def settingStyleSheet(self):
        """
        设置各个控件的背景颜色
        """
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ALL.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.pushButton_1.setText(_translate("MainWindow", "1号变频器故障反馈"))
        self.pushButton_2.setText(_translate("MainWindow", "2号变频器故障反馈"))
        self.pushButton_3.setText(_translate("MainWindow", "3号变频器故障反馈"))
        self.pushButton_4.setText(_translate("MainWindow", "4号变频器故障反馈"))
        self.pushButton_5.setText(_translate("MainWindow", "OP20侧气压低"))
        self.pushButton_6.setText(_translate("MainWindow", "OP20冲床报警"))
        self.pushButton_7.setText(_translate("MainWindow", "OP20冲床靠山气缸伸出未到位"))
        self.pushButton_8.setText(_translate("MainWindow", "OP20冲床靠山气缸缩回未到位"))
        self.pushButton_9.setText(_translate("MainWindow", "OP20夹钳状态报警"))
        self.pushButton_10.setText(_translate("MainWindow", "OP20安全门未锁"))
        self.pushButton_11.setText(_translate("MainWindow", "OP20小车1码垛数量达到上限"))
        self.pushButton_12.setText(_translate("MainWindow", "OP20小车2码垛数量达到上限"))
        self.pushButton_13.setText(_translate("MainWindow", "OP20料塔端定位气缸1伸出未到位"))
        self.pushButton_14.setText(_translate("MainWindow", "OP20料塔端定位气缸2伸出未到位"))
        self.pushButton_15.setText(_translate("MainWindow", "OP20机器人急停"))
        self.pushButton_16.setText(_translate("MainWindow", "OP20机器人故障"))
        self.pushButton_17.setText(_translate("MainWindow", "OP30机器人急停"))
        self.pushButton_18.setText(_translate("MainWindow", "OP30机器人故障"))
        self.pushButton_20.setText(_translate("MainWindow", "OP30码垛产品不一致"))
        self.pushButton_19.setText(_translate("MainWindow", "OP40安全门未锁"))
        self.pushButton_21.setText(_translate("MainWindow", "OP40宽度检测气缸缩回未到位"))
        self.pushButton_22.setText(_translate("MainWindow", "OP40急停"))
        self.pushButton_23.setText(_translate("MainWindow", "OP40机器人故障"))
        self.pushButton_24.setText(_translate("MainWindow", "OP40机器人码垛上限到"))
        self.pushButton_25.setText(_translate("MainWindow", "OP40码垛产品不一致"))
        self.pushButton_26.setText(_translate("MainWindow", "码垛产品不一致"))
        self.pushButton_27.setText(_translate("MainWindow", "系统急停"))
        self.pushButton_28.setText(_translate("MainWindow", "null"))
        self.ALL.setTabText(self.ALL.indexOf(self.singleBQ), _translate("MainWindow", "单例分析"))
        self.label_1.setText(_translate("MainWindow", "频次综合分析"))
        # self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "近一周报警波形"))
        # self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.ALL.setTabText(self.ALL.indexOf(self.SomeBQ), _translate("MainWindow", "多例分析"))

    def draw_line_BendingMachine(self):
        # x = [1, 2, 3]
        # y = [1, 2, 2]
        fig = MyFigure(width=4.7, height=3.7, dpi=100)
        # F.axes.plot(x, y)
        # F.axes.scatter(x, y)
        # F.axes.set_xlabel('时刻')
        # F.axes.set_ylabel('效率')
        # F.axes.set_title('折弯机效率图')
        # F.axes.set_xticks(x, minor=True)
        font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
        a = [1228.3, 3.38, 63.8, 0.07, 0.16, 6.74, 1896.18]  # 数据
        b = [0.12, -12.44, 1.82, 16.67, 6.67, -6.52, 4.04]
        l = [i for i in range(7)]

        plt.rcParams['font.sans-serif'] = ['StimHei']  # 用来正常显示中文标签

        fmt = '%.2f%%'
        yticks = mtick.FormatStrFormatter(fmt)  # 设置百分比形式的坐标轴
        lx = [u'粮食', u'棉花', u'油料', u'麻类', u'糖料', u'烤烟', u'蔬菜']

        # fig = plt.figure()
        # ax1 = fig.add_subplot(111)
        fig.ax1.set_title('近七天数据')
        fig.ax1.plot(l, b, 'or-', label=u'增长率')
        fig.ax1.yaxis.set_major_formatter(yticks)
        fig.ax1.legend(loc=1)
        fig.ax1.set_ylim([-20, 30])

        fig.ax1.set_ylabel('增长率')
        # plt.legend(prop={'family': 'SimHei', 'size': 8})  # 设置中文
        # ax2 = fig.ax1.twinx()  # this is the important function
        fig.ax2.bar(l, a, alpha=0.3, color='blue', label=u'产量')
        fig.ax2.legend(loc=2)
        fig.ax2.set_ylim([0, 2500])  # 设置y轴取值范围
        # plt.legend(prop={'family': 'SimHei', 'size': 8}, loc="upper left")
        plt.xticks(l, lx)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_6.setScene(graphicscene)
        self.graphicsView_6.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def settingButtonClick(self):
        """
        给相应的按钮添加点击事件
        根据传递按钮的参数分别查询数据库
        """
        self.pushButton_1.clicked.connect(lambda: self.buttonOnClick(self.pushButton_1))
        self.pushButton_2.clicked.connect(lambda: self.buttonOnClick(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.buttonOnClick(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.buttonOnClick(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.buttonOnClick(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.buttonOnClick(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.buttonOnClick(self.pushButton_7))
        self.pushButton_8.clicked.connect(lambda: self.buttonOnClick(self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.buttonOnClick(self.pushButton_9))
        self.pushButton_10.clicked.connect(lambda: self.buttonOnClick(self.pushButton_10))
        self.pushButton_11.clicked.connect(lambda: self.buttonOnClick(self.pushButton_11))
        self.pushButton_12.clicked.connect(lambda: self.buttonOnClick(self.pushButton_12))
        self.pushButton_13.clicked.connect(lambda: self.buttonOnClick(self.pushButton_13))
        self.pushButton_14.clicked.connect(lambda: self.buttonOnClick(self.pushButton_14))
        self.pushButton_15.clicked.connect(lambda: self.buttonOnClick(self.pushButton_15))
        self.pushButton_16.clicked.connect(lambda: self.buttonOnClick(self.pushButton_16))
        self.pushButton_17.clicked.connect(lambda: self.buttonOnClick(self.pushButton_17))
        self.pushButton_18.clicked.connect(lambda: self.buttonOnClick(self.pushButton_18))
        self.pushButton_19.clicked.connect(lambda: self.buttonOnClick(self.pushButton_19))
        self.pushButton_20.clicked.connect(lambda: self.buttonOnClick(self.pushButton_20))
        self.pushButton_21.clicked.connect(lambda: self.buttonOnClick(self.pushButton_21))
        self.pushButton_22.clicked.connect(lambda: self.buttonOnClick(self.pushButton_22))
        self.pushButton_23.clicked.connect(lambda: self.buttonOnClick(self.pushButton_23))
        self.pushButton_24.clicked.connect(lambda: self.buttonOnClick(self.pushButton_24))
        self.pushButton_25.clicked.connect(lambda: self.buttonOnClick(self.pushButton_25))
        self.pushButton_26.clicked.connect(lambda: self.buttonOnClick(self.pushButton_26))
        self.pushButton_27.clicked.connect(lambda: self.buttonOnClick(self.pushButton_27))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    a = Ui_MainWindow()

    sys.exit(app.exec())
