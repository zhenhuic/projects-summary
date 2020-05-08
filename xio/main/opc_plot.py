# coding=utf-8
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class FigureLineChart:
    def __init__(self):
        self.figure = plt.figure(figsize=(8.5, 3.7), facecolor='dimgray')
        self.canvas = FigureCanvas(self.figure)

    def plotlinechart(self, days, bq, warn):
        if days == "日平均(7日)":
            x = [1, 2, 3, 4, 5, 6, 7]
            y = []
            for i in range(len(x)):
                y.append(random.randint(0, 5))
            plt.bar(x, y, label=days, color='black')
            plt.title(bq + " 近7天 " + warn)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.xlabel("日期")
            plt.ylabel("次数")
            plt.savefig('1.png')
            plt.clf()
        elif days == "周平均(30日)":
            x = [1, 2, 3, 4]
            y = []
            for i in range(len(x)):
                y.append(random.randint(0, 20))
            plt.bar(x, y, label=days, color='black')
            plt.title(bq + " 近4周 " + warn)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.xlabel("日期")
            plt.ylabel("次数")
            plt.savefig('2.png')
            plt.clf()
