# -*- coding: utf-8 -*-
# @Time    : 2020/4/25 11:50 AM
# @Author  : sichengli
# @FileName: Main.py
# @Software: PyCharm



from Database.utils import *
from QTDesigner.delete import Ui_Dialog_delete
from QTDesigner.main import *
from QTDesigner.add import *
import matplotlib
import warnings
from matplotlib.figure import Figure
import sys
import numpy as np
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
warnings.filterwarnings("ignore")
matplotlib.use("Qt5Agg")  # 声明使用QT5
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

class MyFigure(FigureCanvas):
    def __init__(self, width=4, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        self.ax1 = self.fig.add_subplot(111)


class Main(Ui_MainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.settingSearchQAcitonFunction()
        self.settingSettingQActionFunction()
        self.utils = Utils()


    def settingSearchQAcitonFunction(self):

        self.jointNameSearch("transducer_")
        self.jointNameSearch("OP20_")
        self.jointNameSearch("OP30_")
        self.jointNameSearch("OP40_")
        self.jointNameSearch("systemError_")
        self.Transducer.triggered.connect(lambda: self.actionSearchMultiple(self.Transducer))
        self.OP20.triggered.connect(lambda: self.actionSearchMultiple(self.OP20))
        self.OP30.triggered.connect(lambda: self.actionSearchMultiple(self.OP30))
        self.OP40.triggered.connect(lambda: self.actionSearchMultiple(self.OP40))
        self.systemError.triggered.connect(lambda: self.actionSearchMultiple(self.systemError))

    def jointNameSearch(self, prefix):

        i = 1
        while True:
            name = prefix + str(i)
            if getattr(self, name, -1) == -1:
                break
            else:
                self.bandingSearch(name)
                i += 1

    def bandingSearch(self, name):
        getattr(self, name).triggered.connect(lambda: self.actionSearchSingle(getattr(self, name)))

    def settingSettingQActionFunction(self):
        getattr(self, "setting_1").triggered.connect(lambda: self.actionAdd())
        getattr(self, "setting_2").triggered.connect(lambda: self.actionDelete())
        getattr(self, "setting_3").triggered.connect(lambda: self.actionExit())



    def actionAdd(self):
        dialog = Ui_Dialog_add()
        if dialog.addFlag:
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.mainWindow, '通知', '成功，是否重启更新系统', msg_box.Cancel |msg_box.Ok, msg_box.Cancel)
            if reply == QMessageBox.Ok:
                self.mainWindow.close()
                self.mainWindow.destroy()
                a = Main()

    def actionDelete(self):
        dialog = Ui_Dialog_delete()
        if dialog.deleteFlag:
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.mainWindow, '通知', '成功，是否重启更新系统', msg_box.Cancel |msg_box.Ok, msg_box.Cancel)
            if reply == QMessageBox.Ok:
                self.mainWindow.close()
                self.mainWindow.destroy()
                a = Main()

    def actionExit(self):
        self.mainWindow.close()

    def actionSearchSingle(self, component):

        name = component.text()
        singleTimeSpend = self.utils.selectSingleTimeSpendBYName(name)
        self.drawSingleTimeSpend(singleTimeSpend, name)

        singleFrequencyAndTime = self.utils.selectSingleFrequencyAndTimeCostByName(name)
        self.drawSingleFrequencyAndTime(singleFrequencyAndTime, name)

    def drawSingleTimeSpend(self, singleTimeSpend, buttonName):
        """
        画今日效率的饼图
        """
        labels = '损失', '正常(正常时长/工作时长)'
        sizes = [singleTimeSpend, (24 * 64 - singleTimeSpend)]
        # explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig = MyFigure(width=5, height=7, dpi=100)
        fig.ax1.set_title(buttonName + "——今日工效详情")
        fig.ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        fig.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_1_today.setScene(graphicscene)
        self.graphicsView_1_today.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawSingleFrequencyAndTime(self, singleFrequencyAndTime, name):
        """
        画折线和柱形图
        """
        count = []
        time = []
        for each in singleFrequencyAndTime:
            count.append(each[1])
            time.append(each[2])
        fig = MyFigure(width=5, height=7, dpi=100)
        fig.ax2 = fig.ax1.twinx()
        l = [i for i in range(7)]
        for i, (_x, _y) in enumerate(zip(l, count)):
            fig.ax1.text(_x + 0.1, _y + 0.1, count[i], color='red', fontsize=10)  # 将数值显示在图形上
        # plt.rcParams['font.sans-serif'] = ['StimHei']  # 用来正常显示中文标签
        lx = [u'0', u'1', u'2', u'3', u'4', u'5', u'6']
        today = datetime.datetime.now()
        today_0 = (today + datetime.timedelta(days=0)).strftime("%m-%d")
        today_1 = (today + datetime.timedelta(days=-1)).strftime("%m-%d")
        today_2 = (today + datetime.timedelta(days=-2)).strftime("%m-%d")
        today_3 = (today + datetime.timedelta(days=-3)).strftime("%m-%d")
        today_4 = (today + datetime.timedelta(days=-4)).strftime("%m-%d")
        today_5 = (today + datetime.timedelta(days=-5)).strftime("%m-%d")
        today_6 = (today + datetime.timedelta(days=-6)).strftime("%m-%d")

        xDate = [str(today_6), str(today_5), str(today_4), str(today_3), str(today_2), str(today_1), str(today_0)]

        fig.ax1.set_title(name + '——近七天数据')
        fig.ax1.plot(xDate, count, 'or-', label=u'次数(/次)')
        fig.ax1.legend(loc=2)
        fig.ax1.set_ylim([0, max(count) * 2])

        # for i, (_x, _y) in enumerate(zip(l, time)):
        #     fig.ax2.text(_x - 0.3, _y, time[i], color='blue', fontsize=10)
        fig.ax2.bar(xDate, time, alpha=0.3, color='blue', label=u'故障时常(/分钟)')
        fig.ax2.legend(loc=1)
        fig.ax2.set_ylim([0, max(time) * 2])  # 设置y轴取值范围

        # plt.xticks(l, lx)

        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_1_week.setScene(graphicscene)
        self.graphicsView_1_week.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def actionSearchMultiple(self, component):
        if component.title() == "系统故障":
            name = "系统故障"
        else:
            name = component.title()
        self.drawMultipleFrequencyOfToday(name)
        self.drawMultipleFrequencyOfWeek(name)

    def drawMultipleFrequencyOfToday(self, name):
        """
        画今日的报警次数:柱状图
        resultList:[[名称，次数], [名称，次数],...]
        """
        resultList = self.utils.selectMultipleFrequencyOfToday(name)
        if len(resultList) == 0:
            pass
        labels = []
        frequency = []
        for each in resultList:
            labels.append(each[0])
            frequency.append(each[1])
        x = np.arange(len(labels))  # the label locations
        fig = MyFigure(width=11, height=3.5, dpi=100)
        rects1 = fig.ax1.bar(x,frequency, label='频次')
        fig.ax1.set_ylabel('次数(/次)')
        fig.ax1.set_title(str(name) + "报警——今日频次")
        fig.ax1.set_xticks(x)
        fig.ax1.set_xticklabels(labels)
        if len(frequency) != 0:
            fig.ax1.legend()

        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_2_frequency.setScene(graphicscene)
        self.graphicsView_2_frequency.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawMultipleFrequencyOfWeek(self, name):
        """
        画近一周的报警频次
        """
        frequencyOfWeekDict = self.utils.selectMultipleFrequencyOfWeek(name)

        if len(frequencyOfWeekDict) == 0:
            pass
        fig = MyFigure(width=11, height=3.5, dpi=100)
        today = datetime.datetime.now()
        today_0 = (today + datetime.timedelta(days=0)).strftime("%m-%d")
        today_1 = (today + datetime.timedelta(days=-1)).strftime("%m-%d")
        today_2 = (today + datetime.timedelta(days=-2)).strftime("%m-%d")
        today_3 = (today + datetime.timedelta(days=-3)).strftime("%m-%d")
        today_4 = (today + datetime.timedelta(days=-4)).strftime("%m-%d")
        today_5 = (today + datetime.timedelta(days=-5)).strftime("%m-%d")
        today_6 = (today + datetime.timedelta(days=-6)).strftime("%m-%d")

        xDate = [str(today_6), str(today_5), str(today_4), str(today_3), str(today_2), str(today_1), str(today_0)]
        for each in frequencyOfWeekDict:
            fig.ax1.plot(xDate, frequencyOfWeekDict[each], label=each)
        if len(frequencyOfWeekDict) != 0:
            fig.ax1.legend()
        fig.ax1.set_title(str(name) + "报警——近7天波形")
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_2_week.setScene(graphicscene)
        self.graphicsView_2_week.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签




if __name__ == '__main__':
    app = QApplication(sys.argv)

    a = Main()

    sys.exit(app.exec())