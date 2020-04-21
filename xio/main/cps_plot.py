# coding=utf-8
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class FigureLineChart:

    jgqg_l = round(random.uniform(12, 14), 1)
    skzw_l = round(random.uniform(23, 25), 1)
    yld_l = round(random.uniform(10, 12), 1)
    jgdb_l = round(random.uniform(9, 11), 1)
    ABjzj_l = round(random.uniform(8, 10), 1)
    hbzw_l = round(random.uniform(33, 35), 1)
    zdhj_l = round(random.uniform(11, 13), 1)
    dmqz_l = round(random.uniform(6, 8), 1)
    pf_l = round(random.uniform(5, 7), 1)
    zp_l = round(random.uniform(7, 9), 1)

    jgqg_m = round(random.uniform(14, 16), 1)
    skzw_m = round(random.uniform(25, 27), 1)
    yld_m = round(random.uniform(12, 14), 1)
    jgdb_m = round(random.uniform(11, 13), 1)
    ABjzj_m = round(random.uniform(10, 12), 1)
    hbzw_m = round(random.uniform(35, 37), 1)
    zdhj_m = round(random.uniform(13, 15), 1)
    dmqz_m = round(random.uniform(8, 10), 1)
    pf_m = round(random.uniform(7, 9), 1)
    zp_m = round(random.uniform(9, 11), 1)

    jgqg_r = round(random.uniform(16, 18), 1)
    skzw_r = round(random.uniform(27, 29), 1)
    yld_r = round(random.uniform(14, 16), 1)
    jgdb_r = round(random.uniform(13, 15), 1)
    ABjzj_r = round(random.uniform(12, 14), 1)
    hbzw_r = round(random.uniform(37, 39), 1)
    zdhj_r = round(random.uniform(15, 17), 1)
    dmqz_r = round(random.uniform(10, 12), 1)
    pf_r = round(random.uniform(9, 11), 1)
    zp_r = round(random.uniform(11, 13), 1)

    def __init__(self):
        self.figure = plt.figure(figsize=(8.5, 3.7), facecolor='dimgray')
        self.canvas = FigureCanvas(self.figure)

    def update(self):
        self.jgqg_l = round(random.uniform(12, 14), 1)
        self.skzw_l = round(random.uniform(23, 25), 1)
        self.yld_l = round(random.uniform(10, 12), 1)
        self.jgdb_l = round(random.uniform(9, 11), 1)
        self.ABjzj_l = round(random.uniform(8, 10), 1)
        self.hbzw_l = round(random.uniform(33, 35), 1)
        self.zdhj_l = round(random.uniform(11, 13), 1)
        self.dmqz_l = round(random.uniform(6, 8), 1)
        self.pf_l = round(random.uniform(5, 7), 1)
        self.zp_l = round(random.uniform(7, 9), 1)

        self.jgqg_m = round(random.uniform(14, 16), 1)
        self.skzw_m = round(random.uniform(25, 27), 1)
        self.yld_m = round(random.uniform(12, 14), 1)
        self.jgdb_m = round(random.uniform(11, 13), 1)
        self.ABjzj_m = round(random.uniform(10, 12), 1)
        self.hbzw_m = round(random.uniform(35, 37), 1)
        self.zdhj_m = round(random.uniform(13, 15), 1)
        self.dmqz_m = round(random.uniform(8, 10), 1)
        self.pf_m = round(random.uniform(7, 9), 1)
        self.zp_m = round(random.uniform(9, 11), 1)

        self.jgqg_r = round(random.uniform(16, 18), 1)
        self.skzw_r = round(random.uniform(27, 29), 1)
        self.yld_r = round(random.uniform(14, 16), 1)
        self.jgdb_r = round(random.uniform(13, 15), 1)
        self.ABjzj_r = round(random.uniform(12, 14), 1)
        self.hbzw_r = round(random.uniform(37, 39), 1)
        self.zdhj_r = round(random.uniform(15, 17), 1)
        self.dmqz_r = round(random.uniform(10, 12), 1)
        self.pf_r = round(random.uniform(9, 11), 1)
        self.zp_r = round(random.uniform(11, 13), 1)

    def plotlinechart(self):
        x = ['激光切割', '数控折弯', '压螺钉', '激光打标', 'AB胶粘接', '厚板折弯', '自动焊接', '打磨去渣', '喷粉', '装配']
        y1 = [self.jgqg_r, self.skzw_r, self.yld_r, self.jgdb_r, self.ABjzj_r, self.hbzw_r, self.zdhj_r, self.dmqz_r, self.pf_r, self.zp_r]
        y2 = [self.jgqg_m, self.skzw_m, self.yld_m, self.jgdb_m, self.ABjzj_m, self.hbzw_m, self.zdhj_m, self.dmqz_m, self.pf_m, self.zp_m]
        y3 = [self.jgqg_l, self.skzw_l, self.yld_l, self.jgdb_l, self.ABjzj_l, self.hbzw_l, self.zdhj_l, self.dmqz_l, self.pf_l, self.zp_l]
        plt.bar(x, y1, label="最高耗时", color='red')
        plt.bar(x, y2, label="平均耗时", color='orange')
        plt.bar(x, y3, label="最低耗时", color='lightgreen')
        plt.xticks(np.arange(len(x)), x, rotation=0, fontsize=10)
        plt.xticks(rotation=0)
        plt.legend(loc="upper left")
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.ylabel('耗时(s)')
        plt.xlabel('工序')
        plt.savefig('1.jpg', dpi=100)
        plt.clf()
        # plt.rcParams['savefig.dpi'] = 300
        # plt.rcParams['figure.dpi'] = 300
        # plt.rcParams['figure.figsize'] = (15.0, 8.0)
        # plt.show()


if __name__ == '__main__':
    flc = FigureLineChart()
    flc.plotlinechart()
