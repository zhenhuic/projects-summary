# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: Main.py
# time: 2019/12/19 15:54

import matplotlib
from QtDesign.main import *
import numpy as np
from DataBase.utils import *
import warnings
warnings.filterwarnings("ignore")
matplotlib.use("Qt5Agg")  # 声明使用QT5


class MyFigure(FigureCanvas):
    def __init__(self, width=4, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        self.ax1 = self.fig.add_subplot(111)


class Main(Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.utils = Utils()
        self.drawMultipleFrequencyOfToday()
        self.drawMultipleFrequencyOfWeek()

    def buttonOnClick(self, button):
        """
        查询数据并画图
        singleFrequencyAndTime = [[i, count, cost],[i, count, cost],...]
        singleTimeSpend = timeCost
        """
        buttonName = button.text()
        singleFrequencyAndTime = self.utils.selectSingleFrequencyAndTimeCostByName(buttonName)
        singleTimeSpend = self.utils.selectSingleTimeSpendBYName(buttonName)
        self.drawSingleFrequencyAndTime(singleFrequencyAndTime, buttonName)
        self.drawSingleTimeSpend(singleTimeSpend, buttonName)

    def drawSingleFrequencyAndTime(self, singleFrequencyAndTime, buttonName):
        """
        画折线和柱形图
        """
        count = []
        time = []
        for each in singleFrequencyAndTime:
            count.append(each[1])
            time.append(each[2])
        fig = MyFigure(width=5.18, height=5, dpi=100)
        fig.ax2 = fig.ax1.twinx()
        l = [i for i in range(7)]
        for i, (_x, _y) in enumerate(zip(l, count)):
            fig.ax1.text(_x + 0.1, _y + 0.1, count[i], color='black', fontsize=10)  # 将数值显示在图形上
        plt.rcParams['font.sans-serif'] = ['StimHei']  # 用来正常显示中文标签
        lx = [u'0', u'1', u'2', u'3', u'4', u'5', u'6']
        fig.ax1.set_title(buttonName + '近七天数据')
        fig.ax1.plot(l, count, 'or-', label=u'次数(/次)')
        fig.ax1.legend(loc=1)
        fig.ax1.set_ylim([0, max(count) * 2])
        fig.ax2.bar(l, time, alpha=0.3, color='blue', label=u'报警时常(/分钟)')
        fig.ax2.legend(loc=2)
        fig.ax2.set_ylim([0, max(time) * 2])  # 设置y轴取值范围
        plt.xticks(l, lx)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_1.setScene(graphicscene)
        self.graphicsView_1.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawSingleTimeSpend(self, singleTimeSpend, buttonName):
        """
        画今日效率的饼图
        """
        labels = '损失', '正常'
        sizes = [singleTimeSpend, (24 * 64 - singleTimeSpend)]
        # explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig = MyFigure(width=5.18, height=5, dpi=100)
        fig.ax1.set_title(buttonName + "今日效率")
        fig.ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        fig.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_2.setScene(graphicscene)
        self.graphicsView_2.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawMultipleFrequencyOfToday(self):
        """
        画今日的报警次数:折线图
        resultList:[[名称，次数], [名称，次数],...]
        """
        resultList = self.utils.selectMultipleFrequencyOfToday()
        if len(resultList) == 0:
            pass
        labels = []
        frequency = []
        for each in resultList:
            labels.append(each[0])
            frequency.append(each[1])
        x = np.arange(len(labels))  # the label locations
        fig = MyFigure(width=10, height=3.4, dpi=100)
        rects1 = fig.ax1.bar(x,frequency, label='频次')
        fig.ax1.set_ylabel('次数(/次)')
        fig.ax1.set_title('今日报警频次')
        fig.ax1.set_xticks(x)
        fig.ax1.set_xticklabels(labels)
        if len(frequency) != 0:
            fig.ax1.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                fig.ax1.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        autolabel(rects1)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_3.setScene(graphicscene)
        self.graphicsView_3.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawMultipleFrequencyOfWeek(self):
        """
        画近一周的报警频次
        """
        frequencyOfWeekDict = self.utils.selectMultipleFrequencyOfWeek()
        if len(frequencyOfWeekDict) == 0:
            pass
        fig = MyFigure(width=10, height=3.4, dpi=100)
        xDate = ["today", "-1", "-2", "-3", "-4", "-5"]
        for each in frequencyOfWeekDict:
            fig.ax1.plot(xDate, frequencyOfWeekDict[each], label=each)
        if len(frequencyOfWeekDict) != 0:
            fig.ax1.legend()
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(fig)
        self.graphicsView_5.setScene(graphicscene)
        self.graphicsView_5.show()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Main()
    sys.exit(app.exec())
