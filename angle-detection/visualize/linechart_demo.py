# coding=utf-8
# @Time    : 000008/6/8 10:42
# @Author  : KayleZhuang
# @Site    : 
# @File    : linechart_demo.py
# @Software: PyCharm Community Edition
#
#                            _ooOoo_
#                           o8888888o
#                           88" . "88
#                           (| -_- |)
#                           O\  =  /O
#                        ____/`---'\____
#                      .'  \\|     |//  `.
#                     /  \\|||  :  |||//  \
#                    /  _||||| -:- |||||-  \
#                    |   | \\\  -  /// |   |
#                    | \_|  ''\---/''  |   |
#                    \  .-\__  `-`  ___/-. /
#                  ___`. .'  /--.--\  `. . __
#               ."" '<  `.___\_<|>_/___.'  >'"".
#              | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#              \  \ `-.   \_ __\ /__ _/   .-` /  /
#         ======`-.____`-.___\_____/___.-`____.-'======
#                            `=---='
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      Buddha Bless, No Bug !

import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# x1=[20,33,51,79,101,121,132,145,162,182,203,219,232,243,256,270,287,310,325]

y = []
for i in range(200):
    y.append(random.uniform(89, 91))
y1 = np.array(y)  # the detection angle

y_ones = np.ones(len(y1))
# print(y_ones)
# y1 = np.array([89.15, 90.12, 91.2, 88.53, 89.62, 89.63, 90.32, 90.11, 90.42, 90.21])
# print(y1)
y2 = abs(y1 - 90)  # detection angle abs 90
# print(y2)

x1 = np.arange(0, len(y1), 1)

# x2=[31,52,73,92,101,112,126,140,153,175,186,196,215,230,240,270,288,300]
# y2=[48,48,48,48,49,89,162,237,302,378,443,472,522,597,628,661,690,702]
# x3=[30,50,70,90,105,114,128,137,147,159,170,180,190,200,210,230,243,259,284,297,311]
# y3=[48,48,48,48,66,173,351,472,586,712,804,899,994,1094,1198,1360,1458,1578,1734,1797,1892]


# l1 = plt.plot(x1, y1, 'r--', label='type1')
# l2=plt.plot(x2,y2,'g--',label='type2')
# l3=plt.plot(x3,y3,'b--',label='type3')


img = plt.figure(1)
plt.figure(figsize=(8, 10))
axes = plt.subplot(211)
# plt.subplot(211,axisbg=(0.1843,0.3098,0.3098))
plt.plot(x1, y1, 'bo-')
plt.plot(x1, 89.0 * y_ones, 'c--') # draw line of y=89.0
plt.plot(x1, 91.0 * y_ones, 'c--') # draw line of y=91.0
plt.plot(x1, 90.0 * y_ones, 'm--') # draw line of y=90.0
plt.yticks([88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5])
plt.title(u'折弯机角度检测')
axes.spines['top'].set_visible(False)  # 去掉上边框
axes.spines['bottom'].set_visible(False)  # 去掉下边框
axes.spines['left'].set_visible(False)  # 去掉左边框
axes.spines['right'].set_visible(False)  # 去掉右边框

# plt.ylabel("Angle")

axes = plt.subplot(212)
plt.plot(x1, y2, 'bo-')
plt.plot(x1, 0.0 * y_ones, 'c--')
plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0])
axes.spines['top'].set_visible(False)  # 去掉上边框
axes.spines['bottom'].set_visible(False)  # 去掉下边框
axes.spines['left'].set_visible(False)  # 去掉左边框
axes.spines['right'].set_visible(False)  # 去掉右边框


# plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 80.5],[r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$really\ good$'])
# plt.plot(x1,y1,'ro-',x2,y2,'g+-',x3,y3,'b^-')
# plt.title('The Lasers in Three Conditions')
# plt.xlabel('row')
# plt.ylabel('column')
# plt.legend()
fig = plt.gcf()
plt.savefig('./test.png')
img = cv2.imread('./test.png')
cv2.imshow('img', img)
cv2.waitKey()
# plt.show()
# self.canvas_line.draw()
# plt.close('all')

