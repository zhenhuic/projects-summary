# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: zhenhui.py
# time: 2020/5/12 10:04
from datetime import datetime

from finalNeed.utils import *
import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
import numpy as np

class MyFigure():

    def __init__(self):

        self.fig = plt.figure(figsize=(8, 8))
        self.ax1 = self.fig.add_subplot(111)


class Demo:
    def __init__(self):
        self.utils = Utils()

    def drawPie(self, name):
        """
        调用  画饼图-----第一张图
        :param name: 部件名字
        :return:
        """
        singleTimeSpend = self.utils.selectSingleTimeSpendBYName(name)
        self.drawSingleTimeSpend(singleTimeSpend, name)

    def drawBarAndLine(self, name):
        """
         调用  画柱状图 + 折线图-----第二张图
        :param name: 点位名字
        :return:
        """
        singleFrequencyAndTime = self.utils.selectSingleFrequencyAndTimeCostByName(name)
        self.drawSingleFrequencyAndTime(singleFrequencyAndTime, name)

    def drawMultipleToday(self, name):
        """
        调用   画第三张图
        :param name: 点位名字
        :return:
        """
        self.drawMultipleFrequencyOfToday(name)

    def drawMultipleWeek(self, name):
        """
        调用   画第四张图
        :param name: 点位名字
        :return:
        """
        self.drawMultipleFrequencyOfWeek(name)

    def drawSingleTimeSpend(self, singleTimeSpend, name):
        """
        画饼图---------第一张图
        :param singleTimeSpend: 故障时间损耗
        :param name: 点位名字
        :return:
        """
        labels = '损失', '正常(正常时长/工作时长)'
        sizes = [singleTimeSpend, (24 * 64 - singleTimeSpend)]
        # explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig = MyFigure()
        fig.ax1.set_title(name + "——今日工效详情")
        fig.ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
        fig.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.show()

    def drawSingleFrequencyAndTime(self, singleFrequencyAndTime, name):
        """
        画折线和柱形图-------第二张图
        :param singleFrequencyAndTime: 故障频次和时间
        :param name: 点位名字
        :return:
        """
        count = []
        time = []
        for each in singleFrequencyAndTime:
            count.append(each[1])
            time.append(each[2])
        fig = MyFigure()
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


        plt.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

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
        fig = MyFigure()
        rects1 = fig.ax1.bar(x, frequency, label='频次')
        fig.ax1.set_ylabel('次数(/次)')
        fig.ax1.set_title(str(name) + "报警——今日频次")
        fig.ax1.set_xticks(x)
        fig.ax1.set_xticklabels(labels)
        if len(frequency) != 0:
            fig.ax1.legend()

        plt.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def drawMultipleFrequencyOfWeek(self, name):
        """
        画近一周的报警频次
        """
        frequencyOfWeekDict = self.utils.selectMultipleFrequencyOfWeek(name)

        if len(frequencyOfWeekDict) == 0:
            pass
        fig = MyFigure()
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
        plt.show()
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


if __name__ == '__main__':
    demo = Demo()
    demo.drawPie("OP30厚度检测气缸伸出未到位")
    demo.drawBarAndLine("OP30厚度检测气缸伸出未到位")
    demo.drawMultipleToday("OP30")
    demo.drawMultipleWeek("OP30")