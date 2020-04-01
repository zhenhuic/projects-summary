# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: aa.py
# time: 2019/12/23 15:54


# python 画柱状图折线图
# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.ticker as mtick
# from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
# a=[1228.3,3.38,63.8,0.07,0.16,6.74,1896.18]  #数据
# b=[0.12,-12.44,1.82,16.67,6.67,-6.52,4.04]
# l=[i for i in range(7)]
#
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#
# fmt='%.2f%%'
# yticks = mtick.FormatStrFormatter(fmt)  #设置百分比形式的坐标轴
# lx=[u'粮食',u'棉花',u'油料',u'麻类',u'糖料',u'烤烟',u'蔬菜']
#
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(l, b,'or-',label=u'增长率');
# ax1.yaxis.set_major_formatter(yticks)
# for i,(_x,_y) in enumerate(zip(l,b)):
#     plt.text(_x,_y,b[i],color='black',fontsize=10,)  #将数值显示在图形上
# ax1.legend(loc=1)
# ax1.set_ylim([-20, 30]);
#
# ax1.set_ylabel('增长率');
# plt.legend(prop={'family':'SimHei','size':8})  #设置中文
# ax2 = ax1.twinx() # this is the important function
# plt.bar(l,a,alpha=0.3,color='blue',label=u'产量')
# ax2.legend(loc=2)
# ax2.set_ylim([0, 2500])  #设置y轴取值范围
# plt.legend(prop={'family':'SimHei','size':8},loc="upper left")
# plt.xticks(l,lx)
# plt.show()
#
# count = [1, 2, 1, 1]
# print(max(count))

# l = [i for i in range(7)]
# print(l)
# import matplotlib.pyplot as plt
# # Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
#
#
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
# plt.show()


import matplotlib.pyplot as plt
import numpy as np


# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 34, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]
#
# x = np.arange(len(labels))  # the label locations
# width = 0.35  # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, men_means, width, label='Men')
# rects2 = ax.bar(x + width/2, women_means, width, label='Women')
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# autolabel(rects1)
# autolabel(rects2)
#
# fig.tight_layout()
#
# plt.show()


cat = [1, 2, 3, 4, 5, 6]
dog = [2, 3, 4, 5, 6, 7]
activity = ["today", "-1", "-2", "-3", "-4", "-5"]

fig, ax = plt.subplots()
ax.plot(activity, dog, label="dog")
ax.plot(activity, cat, label="cat")
ax.legend()

plt.show()