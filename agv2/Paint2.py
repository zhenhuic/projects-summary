import sys, math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QRect
import time
#from carshow import Ui_mainwindow

# 读取所有点的数据 并用字典 id：[x,y]存储


def readpoints():
    points = {}
    with open('newpoint1.txt') as f:
        for line in f:
            point = line.split(',', -1)[0].strip()
            x = line.split(',', -1)[1].strip()
            y = line.split(',', -1)[2].strip()
            points[point] = [x, y]
    return points


class draw(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        #self.data = {1: 1, 2: 89, 3: 2, 4: 34, 5: 56, 6: 6, 7: 55, 8: 7, 9: 78}
        self.data = {'carStart1': 82, 'carStart2': 825, 'carStart3': 13675, 'carStart4': 666,
                     'carStart5': 89, 'carStart6': 566, 'carStart7': 372, 'carStart8': 333, 'carStart9': 582,
                     'carFault1': "故障",  'carFault2': "无故障", 'carFault3': "无故障", 'carFault4': "无故障",
                     'carFault5': "无故障", 'carFault6': "故障", 'carFault7': "无故障", 'carFault8': "故障", 'carFault9': "无故障",
                     'carState1': "空闲", 'carState2': "挂起", 'carState3': "运行", 'carState4': "运行",
                     'carState5': "空闲", 'carState6': "运行", 'carState7': "空闲", 'carState8': "运行", 'carState9': "运行",
                     'faultCode1': '500', 'faultCode6': '511', 'faultCode8': '514', 'carAction1': "取货",
                     'carAction2': "取货", 'carAction3': "取货", 'carAction4': "取货", 'carAction5': "送货", 'carAction6': "送货",
                     'carAction7': "送货", 'carAction8': "二期取货", 'carAction9': "二期取货",'carNumber1': '1',
                     'carNumber2': '2', 'carNumber3': '3', 'carNumber4': '4', 'carNumber5': '5',
                     'carNumber6': '6', 'carNumber7': '7', 'carNumber8': '8', 'carNumber9': '9'}

    def paintEvent(self, event):
        # 故障小车数量num1 运行小车数量num2 空闲小车数量num3  挂起、静态操作 逻辑离线小车数量num4
        num1, num2, num3, num4 = 0, 0, 0, 0
        # 小车不同状态的具体车号
        guzhang = ''
        yunxing  = ''
        kongxian  = ''
        qita = ''
        points = readpoints()
        size = self.size()
        painter = QPainter()
        painter.begin(self)
        # painter.setBrush(Qt.black)
        painter.drawRect(self.rect())

        faultCodes = {'500': '发现障碍', '501': '用户暂停', '502': '控制台避免碰撞', '503': '发生碰撞', '504': '地标丢失',
                      '505': '急停按钮按下', '506': '导航信号弱', '507': '电池故障', '508': '伺服轴超差', '509': '伺服驱动器故障',
                      '510': '伺服电源故障', '511': '从等待状态退出', '512': '临时停车', '513': '通讯中断', '514': 'MCU的CAN通讯中断',
                      '515': '设备故障', '516': '舱限位开关作用', '517': '失速保护', '518': 'MCU的ALL-OK信号中断', '519': 'PLS安全继电器故障',
                      '520': 'PLS急停', '521': '电池异常', '522': '电池电压低', '523': '电池电压过低', '524': '电池系统故障',
                      '525': '同步传感器故障', '526':  'MCU通讯故障', '527': 'IO扩展块故障', '528': '上线节点不匹配', '529': '货物验证错误',
                      '530': '死锁无法解除', '531': '机械臂故障', '532': '地标传感器故障', '533': '导航传感器故障', '534': '路由搜索不通'}

        # 画宽路
        pen = QPen(QColor(0, 255, 128))
        painter.setPen(pen)
        painter.setBrush(QColor(0, 255, 128))

        # 节点448 至 358
        x = (-80.584 + 130) / 130 * size.width()
        y = (163 - 133) / 90 * size.height()
        painter.drawRect(x, y, 75.251 / 130 * size.width(), 2 / 90 * size.height())

        #  节点987 至 931
        x = (-125.663 + 130) / 130 * size.width()
        y = (163 - 121.2) / 90 * size.height()
        painter.drawRect(x, y, 58.135 / 130 * size.width(), 2 / 90 * size.height())

        # 节点 160 至  82
        x = (-80.584 + 130) / 130 * size.width()
        y = (163 - 103) / 90 * size.height()
        painter.drawRect(x, y, 73.751 / 130 * size.width(), 2 / 90 * size.height())

        # 节点 1043 至  897
        x = (-98.401 + 130) / 130 * size.width()
        y = (163 - 82.8) / 90 * size.height()
        painter.drawRect(x, y, 26.911 / 130 * size.width(), 2 / 90 * size.height())

        # 节点 380 至  82
        x = (-7.2 + 130) / 130 * size.width()
        y = (163 - 151.5) / 90 * size.height()
        painter.drawRect(x, y, 2.18 / 130 * size.width(), 50.5 / 90 * size.height())

        # 节点 448 至  562
        x = (-83 + 130) / 130 * size.width()
        y = (163 - 133) / 90 * size.height()
        painter.drawRect(x, y, 2.8 / 130 * size.width(), 52.8 / 90 * size.height())


        pen = QPen(QColor(200, 200, 200), 1.5, Qt.SolidLine)
        painter.setPen(pen)
        # 画路线
        with open('linearg1.txt') as f:
            for line in f:
                point1 = line.split(',', -1)[1].strip()
                point2 = line.split(',', -1)[2].strip()
                x1 = (float(points[point1][0]) + 130) / 130 * size.width()
                y1 = (163 - float(points[point1][1])) / 90 * size.height()
                x2 = (float(points[point2][0]) + 130) / 130 * size.width()
                y2 = (163 - float(points[point2][1])) / 90 * size.height()
                painter.drawLine(x1, y1, x2, y2)



        # 画点
        # with open('newpoint1.txt') as f:
        #     for line in f:
        #         x = float(line.split(',', -1)[1].strip())
        #         y = float(line.split(',', -1)[2].strip())
        #         point = line.split(',', -1)[0].strip()
        #         x = (x + 130) / 130
        #         y = (155 - y) / 90
        #         x = x * 1920
        #         y = y * 1080
        #
        #         pen = QPen(QColor(128, 0, 0), 3)  # 3是画笔的粗细
        #         painter.setPen(pen)
        #         painter.drawPoint(x, y)
        #         # painter.drawArc(x, y, 3, 3, 0, 360*16)
        #         # pen = QPen(QColor(60,179,113), 1)
        #         pen = QPen(Qt.darkGreen)
        #         painter.setPen(pen)
        #         painter.setFont(QFont('Times New Roman', 7))
        #         painter.drawText(x + 3, y - 1, point)


        #pen = QPen(QColor(141, 141, 212))
        pen = QPen(QColor(60, 60, 60))
        painter.setPen(pen)
        painter.setFont(QFont('微软雅黑', 14))
        painter.drawText(0.0677 * size.width(), 0.4109 * size.height(), '装箱线1号库')
        painter.drawText(0.0187 * size.width(), 0.4409 * size.height(), '装箱线2号库')
        painter.drawText(0.4427 * size.width(), 0.5446 * size.height(), '旧萨瓦取货库位')
        painter.drawText(0.4149 * size.width(), 0.9609 * size.height(), '新萨瓦取货库位')
        painter.drawText(0.9004 * size.width(), 0.1093 * size.height(), '手工焊接缓存库位')
        painter.drawText(0.9071 * size.width(), 0.1732 * size.height(), '充电站')
        painter.drawText(0.5078 * size.width(), 0.7031 * size.height(), '机器人1缓存库位')
        painter.drawText(0.5500 * size.width(), 0.6401 * size.height(), '机器人取货库位')
        painter.drawText(0.6338 * size.width(), 0.7040 * size.height(), '机器人2缓存库位')
        painter.drawText(0.7218 * size.width(), 0.7089 * size.height(), '自动焊接取货库位')
        painter.drawText(0.2013 * size.width(), 0.3931 * size.height(), '货物库位缓存区')
        painter.drawText(0.4020 * size.width(), 0.5595 * size.height(), '充电站')
        painter.drawText(0.3723 * size.width(), 0.9762 * size.height(), '充电站')
        painter.drawText(0.4697 * size.width(), 0.7277 * size.height(), '停车站')
        painter.drawText(0.1630 * size.width(), 0.4438 * size.height(), '停车站')
        painter.drawText(0.2114 * size.width(), 0.4271 * size.height(), '停车站')
        painter.drawText(0.3494 * size.width(), 0.4271 * size.height(), '停车站')
        painter.drawText(0.2906 * size.width(), 0.3931 * size.height(), '停车站')



        for i in range(1, 10):



            # if str(self.data[i]) in points:
            #     print('dsds')
            #     x = (float(points[str(self.data[i])][0]) + 130) / 130 * 1920
            #     y = (155 - float(points[str(self.data[i])][1])) / 90 * 1080
            #     painter.drawEllipse(x - 10, y - 10, 20, 20)
            #     #pen = QPen(QColor(255, 240, 245))
            #     pen = QPen(QColor(0, 0, 0))
            #     painter.setPen(pen)
            #     painter.drawText(x - 4, y + 6, str(i))


            if str(self.data['carStart' + str(i)]) in points:
                pen = QPen(QColor(255, 162, 117))
                painter.setPen(pen)
                painter.setBrush(QColor(255, 162, 117))

                x = (float(points[str(self.data['carStart' + str(i)])][0]) + 130) / 130 * size.width()
                y = (163 - float(points[str(self.data['carStart' + str(i)])][1])) / 90 * size.height()

                # # 描述每辆非故障小车的当前动作
                # if str(self.data['carFault' + str(i)]) != "故障":
                #     pen = QPen(QColor(129, 129, 129), 2, Qt.SolidLine)
                #     painter.setPen(pen)
                #     painter.drawLine(x, y, x - 25, y - 20)
                #     # painter.setBrush(QColor(192, 192, 192))
                #     painter.setBrush(Qt.NoBrush)
                #     painter.drawEllipse(x - 123, y - 42, 100, 25)
                #     painter.setFont(QFont('黑体', 13))
                #     pen = QPen(QColor(0, 0, 0))
                #     painter.setPen(pen)
                #     painter.drawText(x - 110, y - 20, self.data['carAction' + str(i)])

                # pen = QPen(QColor(128, 255, 255))
                # painter.setPen(pen)
                # painter.setBrush(QColor(128, 255, 255))
                # painter.drawEllipse(30 + (i - 1) * size.width() * 0.095, 70, 150, 150)
                # 判断是否空闲 为绿
                if str(self.data['carState' + str(i)]) == "空闲":
                    kongxian = kongxian + str(self.data['carNumber' + str(i)]) + '号 '
                    num3 = num3 + 1
                    pen = QPen(QColor(0, 128, 0))
                    painter.setPen(pen)
                    painter.setBrush(QColor(0, 128, 0))
                elif str(self.data['carState' + str(i)]) == "运行":
                    yunxing = yunxing + str(self.data['carNumber' + str(i)]) + '号 '
                    num2 = num2 + 1
                    pen = QPen(QColor(0, 128, 255))
                    painter.setPen(pen)
                    painter.setBrush(QColor(0, 128, 255))
                elif str(self.data['carState' + str(i)]) == "挂起" or str(self.data['carState' + str(i)]) == "静态" or str(self.data['carState' + str(i)]) == "离线":
                    qita = qita + str(self.data['carNumber' + str(i)]) + '号 '
                    num4 = num4 + 1
                    pen = QPen(QColor(162, 162, 162))
                    painter.setPen(pen)
                    painter.setBrush(QColor(162, 162, 162))
                # 判断是否故障 为红
                if str(self.data['carFault' + str(i)]) == "故障":
                    guzhang = guzhang + str(self.data['carNumber' + str(i)]) + '号 '
                    pen = QPen(QColor(255, 60, 60), 1.5, Qt.SolidLine)
                    painter.setPen(pen)
                    painter.drawLine(x, y, x - 23, y - 17)
                    # painter.setBrush(QColor(192, 192, 192))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawEllipse(x - 155, y - 40, 130, 30)
                    if self.data['faultCode' + str(i)] in faultCodes:
                        code = self.data['faultCode' + str(i)]
                        painter.setFont(QFont('微软雅黑', 13, QFont.Bold))
                        pen = QPen(QColor(0, 0, 0))
                        painter.setPen(pen)
                        painter.drawText(x - 140, y - 15, faultCodes[code])

                    num1 = num1 + 1
                    pen = QPen(QColor(255, 60, 60))
                    painter.setPen(pen)
                    painter.setBrush(QColor(255, 60, 60))
                # painter.drawEllipse(x - 10, y - 10, 20, 20)


                painter.drawRect(x - 12.5, y - 10, 25, 20)



                #显示各小车的顶部状态栏
               # painter.drawEllipse(75 + (i - 1) * size.width() * 0.095, 115, 60, 60)

                #pen = QPen(QColor(0, 0, 0))
                #painter.setPen(pen)
                painter.setFont(QFont('微软雅黑', 80, QFont.Bold))



                painter.drawText(75 + (i - 1) * size.width() * 0.095, 150, str(self.data['carNumber' + str(i)]))

                # pen = QPen(QColor(0, 0, 0))
                # painter.setPen(pen)
                # painter.setFont(QFont('微软雅黑', 24, QFont.Bold))
                # painter.drawText(70 + (i - 1) * size.width() * 0.095, 210, str(self.data['carState' + str(i)]))

                pen = QPen(QColor(255, 255, 255))
                painter.setPen(pen)
                painter.setFont(QFont('微软雅黑', 14, QFont.Bold))
                painter.drawText(x - 4, y + 6, str(self.data['carNumber' + str(i)]))

            elif str(self.data['carStart' + str(i)]).isdigit():
                # pen = QPen(QColor(162, 162, 162))
                # painter.setPen(pen)
                # painter.setBrush(QColor(162, 162, 162))
                # painter.drawEllipse(30 + (i - 1) * size.width() * 0.095, 70, 150, 150)
                # pen = QPen(QColor(255, 255, 255))
                # painter.setPen(pen)
                # painter.setBrush(QColor(255, 255, 255))
                # painter.drawEllipse(75 + (i - 1) * size.width() * 0.095, 115, 60, 60)


                pen = QPen(QColor(105, 105, 105))
                painter.setPen(pen)
                painter.setFont(QFont('微软雅黑', 50, QFont.Bold))
                # painter.drawText(75 + (i - 1) * size.width() * 0.095, 150, str(self.data['carNumber' + str(i)]))

                painter.drawText(30 + (i - 1) * size.width() * 0.095, 150, '暂无')




                # pen = QPen(QColor(0, 0, 0))
                # painter.setPen(pen)
                # painter.setFont(QFont('微软雅黑', 24, QFont.Bold))
                # painter.drawText(70 + (i - 1) * size.width() * 0.095, 210, '暂无')





        # 显示 故障小车数量num1 运行小车数量num2 空闲小车数量num3  挂起、静态操作 逻辑离线小车数量num4
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        painter.setFont(QFont('微软雅黑', 16))
        painter.drawText(0.0507 * size.width(), 0.5966 * size.height(),  '故障小车---')
        painter.drawText(0.0507 * size.width(), 0.6366 * size.height(), '运行小车---')
        painter.drawText(0.0507 * size.width(), 0.6766 * size.height(), '空闲小车---')
        painter.drawText(0.0077 * size.width(), 0.7166 * size.height(), '挂起、静态、离线---')

        pen = QPen(QColor(255, 60, 60))
        painter.setPen(pen)
        painter.setFont(QFont('微软雅黑', 16, QFont.Bold))
        #painter.setFontPointSize(QFont.Bold)
        painter.drawText(0.1147 * size.width(), 0.5966 * size.height(), guzhang)
        pen = QPen(QColor(0, 128, 255))
        painter.setPen(pen)
        painter.drawText(0.1147 * size.width(), 0.6366 * size.height(), yunxing)
        pen = QPen(QColor(0, 128, 0))
        painter.setPen(pen)
        painter.drawText(0.1147 * size.width(), 0.6766 * size.height(), kongxian)
        pen = QPen(QColor(162, 162, 162))
        painter.setPen(pen)
        painter.drawText(0.1147 * size.width(), 0.7166 * size.height(), qita)

        pen = QPen(QColor(255, 60, 60))
        painter.setPen(pen)
        painter.setFont(QFont('微软雅黑', 16))
        painter.setBrush(QColor(255, 60, 60))
        # painter.drawEllipse(0.0477 * size.width(), 0.5726 * size.height(), 15, 15)
        painter.drawRect(0.0687 * size.width(), 0.7526 * size.height(), 20, 15)

        pen = QPen(QColor(0, 128, 255))
        painter.setPen(pen)
        painter.setBrush(QColor(0, 128, 255))
        painter.drawRect(0.0687 * size.width(), 0.7806 * size.height(), 20, 15)

        pen = QPen(QColor(0, 128, 0))
        painter.setPen(pen)
        painter.setBrush(QColor(0, 128, 0))
        painter.drawRect(0.0687 * size.width(), 0.8086 * size.height(), 20, 15)

        pen = QPen(QColor(162, 162, 162))
        painter.setPen(pen)
        painter.setBrush(QColor(162, 162, 162))
        painter.drawRect(0.0687 * size.width(), 0.8366 * size.height(), 20, 15)

        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawText(0.091 * size.width(), 0.767 * size.height(), '---- 故障')
        painter.drawText(0.091 * size.width(), 0.795 * size.height(), '---- 运行中')
        painter.drawText(0.091 * size.width(), 0.823 * size.height(), '---- 空闲')
        painter.drawText(0.091 * size.width(), 0.851 * size.height(), '---- 挂起、静态、离线')
        painter.end()

