from PyQt4 import QtGui, QtCore
import uifiles.xio_all_ui as ui
import sys
import cv2
import threading
import datetime
from utils.utils import Timer, MyQueue
from utils.vision import Vision
import socketserver
import time
from figure.figure_plot import *
from data import data_access
from numpy import *
import random
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QDir

Stype = 0


def data_deal(func):  # 要接受参数就要改成三层装饰器
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        return func(*args, **kwargs)

    return wrapper


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    action = None  # 用来通知显示现在是由于什么原因导致静止

    def handle(self):
        global Stype
        data = str(self.request.recv(1024), 'utf-8')
        if data == 'action1':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            Stype = 1

            action = data
        elif data == 'action2':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            Stype = 2
            action = data
        elif data == 'action3':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
            Stype = 3
        elif data == 'action4':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
            Stype = 4
        elif data == 'action5':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
            Stype = 5
        elif data == 'action6':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
            Stype = 6
        elif data[0:4] == 'stop':
            dz = data[4:]
            da = data_access.DataAccess()
            da.insert_action(dz, FLAG='end')
            # 更新动作表
            result = da.select_("select * from dz ORDER BY SJC DESC limit 2")
            time_diff = int((result[0][0] - result[1][0]).seconds)
            lossTime = data_access.EquipmentTimeData()
            result_loss = lossTime.select_("select * from loss ORDER BY SJ DESC limit 1")
            current_time = datetime.datetime.now().strftime('%Y-%m-%d')
            time_diff = time_diff + result_loss[0][int(dz[-1])]  # 此处投机
            lossTime.update_('update loss set ' + dz + '=' + str(time_diff) + ' where SJ="%s"' % current_time)

            action = None
            Stype = 0


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def gamma_trans(img, gamma):
    '''
    将图像光照归一化
    :param img:
    :param gamma:
    :return:
    '''
    # 具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # 实现映射用的是Opencv的查表函数
    return cv2.LUT(img, gamma_table)


class XioAll(QtGui.QWidget):
    '''这个类为主程序类
    '''
    HOST = 'localhost'
    PORT = 8081
    TOTAL = 0
    isStatic = True
    Shumei = None
    action = None
    pre_action = None
    action_video = None  # 视频内能识别
    pre_action_video = None

    def __init__(self):
        super(XioAll, self).__init__()
        self.ui = ui.Ui_Form()
        self.ui.setupUi(self)

        self.frame_left = None
        self.frame_right = None
        self.is_work = True
        self.stype = 0
        self.one_static_time = 0  # 一次故障静止的时间
        self.all_time = 0  # 一天的工作时间
        self.q = MyQueue()  # 存放帧队列,改为存放状态比较好
        self.vision = Vision()

        self.CamPath = ""

        # 若日期发生改变，自行插入全零数据
        da = data_access.EquipmentTimeData()  # 对损失项统计表进行操作
        result_loss = da.select_("select * from loss ORDER BY SJ DESC limit 1")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(result_loss[0][0]) != current_time:
            da.update('insert into loss(SJ,action1,action2,action3,action4,action5,action6)values'
                      '("%s",%d,%d,%d,%d,%d,%d)' % (current_time, 0, 0, 0, 0, 0, 0))
        else:
            pass

        da_oee = data_access.OEEData()  # 对oee实时利用率进行统计
        result_oee = da_oee.select_('select * from oee_date ORDER BY SJC DESC limit 1')
        if str(result_oee[0][0]) != current_time:
            da_oee.update_('insert into oee_date(SJC,O8,O9,O10,O11,O12,O13,O14,O15,O16,O17,O18)values'
                           '("' + current_time + '",0,0,0,0,0,0,0,0,0,0,0)')
        else:
            pass

        self.thread_figure = Timer('updatePlay()', sleep_time=120)  # 该线程用来每隔2分钟刷新绘图区
        self.connect(self.thread_figure, QtCore.SIGNAL('updatePlay()'), self.draw)
        self.thread_figure.start()

        # 按钮功能
        self.connect(self.ui.fileSelectButton, QtCore.SIGNAL('clicked()'), self.fileSelect)
        self.connect(self.ui.mailSenderButton, QtCore.SIGNAL('clicked()'), self.mailSend)
        self.connect(self.ui.confirmDateButton, QtCore.SIGNAL('clicked()'), self.displayMonthData)
        self.connect(self.ui.mailConfirm, QtCore.SIGNAL('clicked()'), self.confirmMail)

        self.server = ThreadedTCPServer((self.HOST, self.PORT), ThreadedTCPRequestHandler)  # 该线程用来一直监听客户端的请求
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

        self.thread_video_receive = threading.Thread(target=self.video_receive_local)  # 该线程用来读取视频流
        self.thread_video_receive.start()

        self.thread_time = Timer('updatePlay()')  # 该线程用来每隔0.04秒在label上绘图
        self.connect(self.thread_time, QtCore.SIGNAL('updatePlay()'), self.video_play)
        self.thread_time.start()

        self.thread_recog = Timer('updatePlay()', sleep_time=1)  # 该线程用来每隔一秒分析图像
        self.connect(self.thread_recog, QtCore.SIGNAL('updatePlay()'), self.video_recog)
        self.thread_recog.start()

        self.thread_data = Timer('updatePlay()', sleep_time=1800)  # 该线程用来每隔半小时向数据库读取数据
        self.connect(self.thread_data, QtCore.SIGNAL('updatePlay()'), self.data_read)
        self.thread_data.start()

        self.thread_shumei = threading.Thread(target=self.shumeiDeal)
        self.thread_shumei.start()

        self.thread_control = Timer('updatePlay()', sleep_time=10)  # 该线程用来每隔半小时向数据库读取数据
        self.connect(self.thread_control, QtCore.SIGNAL('updatePlay()'), self.control_judge)
        self.thread_control.start()

        # 12-25
        self.thread_recogtiaoshi = Timer('updatePlay()', sleep_time=0.5)  # 该线程用来每隔0.5秒分析图像
        self.connect(self.thread_recogtiaoshi, QtCore.SIGNAL('updatePlay()'), self.video_recogtiaoshi)
        self.thread_recogtiaoshi.start()

        # self.thread_recogbottle = Timer('updatePlay()', sleep_time=0.5)  # 该线程用来每隔0.5秒分析图像
        # self.connect(self.thread_recogbottle, QtCore.SIGNAL('updatePlay()'), self.video_recogbottle)
        # self.thread_recogbottle.start()

        self.thread_recogzhuangji = Timer('updatePlay()', sleep_time=0.1)  # 该线程用来每隔0.5秒分析图像
        self.connect(self.thread_recogzhuangji, QtCore.SIGNAL('updatePlay()'), self.video_recogzhuangji)
        self.thread_recogzhuangji.start()

        self.X_l = 0
        self.Y_l = 0
        self.type_l = ""
        self.flag = 0
        self.a = 0
        self.tiaoshi_back = False
        self.tiaoshi_forward = False
        self.X_r = 0
        self.Y_r = 0
        self.type_r = ""
        self.firstFrame = None
        self.chaiji_left = False
        self.chaiji_right = False
        self.cltime = 0
        self.crtime = 0
        self.totaltime = 0

        # 用于面板进行输出
        self.work_time = 0
        self.tf_time = 0
        self.tb_time = 0

        # 调试
        self.machinedown_base = cv2.imread("images/tiaoshiimages/machinedown_base.jpg")
        self.machineup_base = cv2.imread("images/tiaoshiimages/machineup_base.jpg")

        self.machineup_mask = cv2.imread("images/tiaoshiimages/up1.jpg")
        self.machinedown_mask = cv2.imread("images/tiaoshiimages/down1.jpg")

        self.peopleup_mask = cv2.imread("images/tiaoshiimages/handsup.jpg", 0)
        self.peopledown_mask = cv2.imread("images/tiaoshiimages/handsdown.jpg", 0)

        self.peopleup_base = cv2.imread("images/tiaoshiimages/handsup_base.jpg", 0)
        self.peopledown_base = cv2.imread("images/tiaoshiimages/handsdown_base.jpg", 0)

        self.Ldown = [0] * 10
        self.Lup = [0] * 10  # 队列操作
        self.Lhandsdown = [0] * 10
        self.Lhandsup = [0] * 10

        self.isJudgeMachineT = True
        self.tiaoshitime = 0

        self.isUpStart = False
        self.isDownStart = False
        self.machineLocation = ""
        self.downStartTime = 0
        self.upStartTime = 0
        # 换瓶操作
        # self.bottle_area = cv2.imread("images/bottleimages/bottle.jpg", 0)
        # self.bottle_area = cv2.resize(self.bottle_area, (1280, 720))
        # self.nobottle_base = cv2.imread("images/bottleimages/nobottle_base.jpg", 0)
        # self.nobottle_base = cv2.resize(self.nobottle_base, (1280, 720))
        # self.Lbottle = [0] * 10
        # self.isBottleStart = False
        # self.isJudgeMachineB = True
        self.bottletime = 0
        # 装机操作
        self.mask_right = cv2.imread("images/zhuangjiimages/right.jpg")
        self.mask_left = cv2.imread("images/zhuangjiimages/maskleft.jpg")
        self.left_base = cv2.imread("images/zhuangjiimages/left_base.jpg", 0)
        self.redLower = np.array([26, 43, 46])
        self.redUpper = np.array([34, 255, 255])
        self.Lright = [0] * 10
        self.Lleft = [0] * 10
        self.is_JudgeRL = True
        self.isRightStart = False
        self.isLeftStart = False
        self.zhuangjitime = 0

    def fileSelect(self):
        absolute_path = QFileDialog.getOpenFileName(self, '视频选择',
                                                    '.', "MP4 files (*.mp4)")

        if self.CamPath != absolute_path:
            self.reFlushDetection()
            self.CamPath = absolute_path
        else:
            self.displayMessage("...未进行选择，视频源路径不变...")

    def reFlushDetection(self):
        self.X_l = 0
        self.Y_l = 0
        self.type_l = ""
        self.flag = 0
        self.a = 0
        self.tiaoshi_back = False
        self.tiaoshi_forward = False
        self.X_r = 0
        self.Y_r = 0
        self.type_r = ""
        self.firstFrame = None
        self.chaiji_left = False
        self.chaiji_right = False
        self.cltime = 0
        self.crtime = 0
        self.totaltime = 0

        # 用于面板进行输出
        self.work_time = 0
        self.tf_time = 0
        self.tb_time = 0

        # 调试
        self.machinedown_base = cv2.imread("images/tiaoshiimages/machinedown_base.jpg")
        self.machineup_base = cv2.imread("images/tiaoshiimages/machineup_base.jpg")

        self.machineup_mask = cv2.imread("images/tiaoshiimages/up1.jpg")
        self.machinedown_mask = cv2.imread("images/tiaoshiimages/down1.jpg")

        self.peopleup_mask = cv2.imread("images/tiaoshiimages/handsup.jpg", 0)
        self.peopledown_mask = cv2.imread("images/tiaoshiimages/handsdown.jpg", 0)

        self.peopleup_base = cv2.imread("images/tiaoshiimages/handsup_base.jpg", 0)
        self.peopledown_base = cv2.imread("images/tiaoshiimages/handsdown_base.jpg", 0)

        self.Ldown = [0] * 10
        self.Lup = [0] * 10  # 队列操作
        self.Lhandsdown = [0] * 10
        self.Lhandsup = [0] * 10

        self.isJudgeMachineT = True
        self.tiaoshitime = 0

        self.isUpStart = False
        self.isDownStart = False
        self.machineLocation = ""
        self.downStartTime = 0
        self.upStartTime = 0
        # 换瓶操作
        self.bottle_area = cv2.imread("images/bottleimages/bottle.jpg", 0)
        self.bottle_area = cv2.resize(self.bottle_area, (1280, 720))
        self.nobottle_base = cv2.imread("images/bottleimages/nobottle_base.jpg", 0)
        self.nobottle_base = cv2.resize(self.nobottle_base, (1280, 720))
        self.Lbottle = [0] * 10
        self.isBottleStart = False
        self.isJudgeMachineB = True
        self.bottletime = 0
        # 装机操作
        self.mask_right = cv2.imread("images/zhuangjiimages/right.jpg")
        self.mask_left = cv2.imread("images/zhuangjiimages/maskleft.jpg")
        self.left_base = cv2.imread("images/zhuangjiimages/left_base.jpg", 0)
        self.redLower = np.array([26, 43, 46])
        self.redUpper = np.array([34, 255, 255])
        self.Lright = [0] * 10
        self.Lleft = [0] * 10
        self.is_JudgeRL = True
        self.isRightStart = False
        self.isLeftStart = False
        self.zhuangjitime = 0

        self.displayMessage("......初始化参数成功......")

    def confirmMail(self):
        text = self.ui.mailLineEdit.text()
        lines = str(text)
        lines = lines.split(';')
        for line in lines:
            self.ui.mailTextBroswer.append(line)
        self.ui.mailTextBroswer.append("......邮箱确认完毕,准备发送......")

    def mailSend(self):
        import smtplib
        sender = '1821959030@qq.com'
        receivers = ['442634234@qq.com']
        text = self.ui.mailLineEdit.text()
        lines = str(text)
        lines = lines.split(';')
        for line in lines:
            receivers.append(line)
        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        Subject: SMTP e-mail test

        This is a test e-mail message.
        """
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect("smtp.qq.com", 25)
            mail_license = "wuhchbmndrjabgcc"
            print("准备登录")
            smtpObj.login(sender, mail_license)
            print("登录成功！")
            smtpObj.set_debuglevel(1)
            smtpObj.sendmail(sender, receivers, message)
            self.ui.mailTextBroswer.append("......发送邮件成功！......")
        except Exception as e:
            print(e)
            self.ui.mailTextBroswer.append("......发送邮件失败！......")

    def displayMonthData(self):
        self.ui.DateTable.clear()
        da = data_access.DataAccess()

        # 获取月份
        select_date = self.ui.dateEdit.text()
        queryByMonth = "select * from oee_date where date_format(SJC,'%Y-%m')='{}'".format(select_date)

        # 取数据正常
        result = da.select_(queryByMonth)
        row = len(result)
        if row == 0:
            self.ui.DateTable.setRowCount(1)
            self.ui.DateTable.setColumnCount(1)
            self.ui.DateTable.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
            self.ui.DateTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
            newItem = QtGui.QTableWidgetItem("                    日期 {} 暂无数据".format(select_date))  # 接受str，无法接收int
            textFont = QtGui.QFont("song", 16, QtGui.QFont.Bold)
            newItem.setFont(textFont)

            self.ui.DateTable.setItem(0, 0, newItem)
        else:
            # 表格属性
            self.ui.DateTable.setRowCount(row)
            self.ui.DateTable.setColumnCount(12)
            self.ui.DateTable.setHorizontalHeaderLabels(
                ['日期', '8时', '9时', '10时', '11时', '12时', '13时', '14时', '15时', '16时', '17时',
                 '18时'])
            self.ui.DateTable.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
            self.ui.DateTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

            # 数据处理
            for i in range(row):
                list_data = list(result[i])
                for j in range(12):
                    if j == 0:
                        cnt = str(list_data[j])[5:10]
                    else:
                        cnt = str(int(list_data[j]))
                    newItem = QtGui.QTableWidgetItem(cnt)  # 接受str，无法接收int
                    textFont = QtGui.QFont("song", 12, QtGui.QFont.Bold)
                    newItem.setFont(textFont)
                    self.ui.DateTable.setItem(i, j, newItem)

    def control_judge(self):
        if (time.time() - self.tiaoshitime) > 120:
            self.isJudgeMachineT = True
        if (time.time() - self.bottletime) > 120:
            self.isJudgeMachineB = True
        if (time.time() - self.zhuangjitime) > 120:
            self.is_JudgeRL = True

    def video_recogtiaoshi(self):
        img = self.frame_left
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgupcurrent = cv2.bitwise_and(self.machineup_mask, img)
        imgdowncurrent = cv2.bitwise_and(self.machinedown_mask, img)
        updiff = sum(cv2.absdiff(imgupcurrent, self.machineup_base)) * 1.46
        downdiff = sum(cv2.absdiff(imgdowncurrent, self.machinedown_base))
        if self.isJudgeMachineT is True and self.is_work is False:
            if updiff > downdiff:
                self.Ldown.append(1)
                self.Lup.append(0)
            else:
                self.Lup.append(1)
                self.Ldown.append(0)
            self.Ldown.pop(0)
            self.Lup.pop(0)
            if sum(self.Ldown) > 6:
                self.isJudgeMachineT = False
                self.machineLocation = "down"
            if sum(self.Lup) > 6:
                self.isJudgeMachineT = False
                self.machineLocation = "up"

        if self.machineLocation == "down":
            peopleDownCurrent = cv2.bitwise_and(img_gray, self.peopledown_mask)
            if sum(cv2.absdiff(peopleDownCurrent, self.peopledown_base)) > 70000:
                self.Lhandsdown.append(1)
            else:
                self.Lhandsdown.append(0)
            self.Lhandsdown.pop(0)
            if sum(self.Lhandsdown) > 6 and self.isDownStart is False:
                message = "[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人正在下方调试"
                self.displayMessage(message)
                self.isDownStart = True
                self.downStartTime = time.time()
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','tiaoshi',0)")
            if time.time() - self.downStartTime > 120:
                self.isDownStart = False
                self.machineLocation = ""
                self.tiaoshitime = time.time()

            if sum(self.Lhandsdown) < 4 and self.isDownStart is True:
                message = "[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人结束下方调试"
                self.displayMessage(message)
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','tiaoshi',1)")
                self.isDownStart = False
                self.machineLocation = ""

        if self.machineLocation == "up":
            peopleUpCurrent = cv2.bitwise_and(img_gray, self.peopleup_mask)
            if sum(cv2.absdiff(peopleUpCurrent, self.peopleup_base)) > 60000:
                self.Lhandsup.append(1)
            else:
                self.Lhandsup.append(0)
            self.Lhandsup.pop(0)
            print(sum(self.Lhandsup))
            if sum(self.Lhandsup) > 6 and self.isUpStart is False:
                message = "[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人正在上方调试"
                self.displayMessage(message)
                self.isUpStart = True
                self.upStartTime = time.time()
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','tiaoshi',0)")
            if time.time() - self.upStartTime > 120:  # 若时间大于120秒，则放弃判断是否拆机
                self.machineLocation = ""
                self.isUpStart = False

            if sum(self.Lhandsup) < 4 and self.isUpStart is True:
                message = "[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人结束上方调试"
                self.displayMessage(message)
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','tiaoshi',1)")
                self.machineLocation = ""
                self.isUpStart = False
                self.tiaoshitime = time.time()

    # def video_recogbottle(self):
    #     img = self.frame_right
    #     img = cv2.resize(img, (1280, 720))
    #     if self.isJudgeMachineB is True:
    #         img_bottle = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         img_bottle = cv2.bitwise_and(img_bottle, self.bottle_area)
    #         if np.sum(cv2.absdiff(img_bottle, self.bottle_area)) < 50000:
    #             self.Lbottle.append(1)
    #         else:
    #             self.Lbottle.append(0)
    #         self.Lbottle.pop(0)
    #         if self.isBottleStart is False and sum(self.Lbottle) > 5:
    #             self.isBottleStart = True  # 初始为False
    #             self.displayMessage(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "..........开始换气瓶！")
    #             current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #             da = data_access.DataAccess()
    #             da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','bottle',0)")
    #
    #         if self.isBottleStart is True and sum(self.Lbottle) < 2:
    #             self.isBottleStart = False
    #             self.displayMessage(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "..........换气瓶结束！")
    #             current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #             da = data_access.DataAccess()
    #             da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','bottle',1)")

    def video_recogzhuangji(self):
        img = self.frame_left
        img = cv2.resize(img, (1280, 720))
        img_right = cv2.bitwise_and(self.mask_right, img)
        hsv_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2HSV)
        mask_det = cv2.inRange(hsv_right, self.redLower, self.redUpper)
        img_left = cv2.bitwise_and(self.mask_left, img)
        hsv_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2HSV)
        mask_det1 = cv2.inRange(hsv_left, self.redLower, self.redUpper)

        if self.is_JudgeRL is True:
            if np.sum(mask_det) < 10000:
                self.Lright.append(1)
            else:
                self.Lright.append(0)
            self.Lright.pop(0)
            if sum(self.Lright) > 6 and self.isRightStart is False:
                self.displayMessage("[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人正在右方拆机")
                self.isRightStart = True
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','chaiji',0)")
            if sum(self.Lright) < 2 and self.isRightStart is True:
                self.displayMessage(
                    "[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人结束右方拆机")
                self.isRightStart = False
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','chaiji',1)")

            if np.sum(mask_det1) < 50000:
                self.Lleft.append(1)
            else:
                self.Lleft.append(0)
            self.Lleft.pop(0)
            if sum(self.Lleft) > 6 and self.isLeftStart is False:
                self.displayMessage("[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人正在左方拆机")
                self.isLeftStart = True
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','chaiji',0)")
            if sum(self.Lleft) < 2 and self.isLeftStart is True:
                self.displayMessage("[" + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]" + "工人结束左方拆机")
                self.isLeftStart = False
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                da = data_access.DataAccess()
                da.update_("insert into dzrecord(SJC,ACTION,FLAG)values('" + current_time + "','chaiji',1)")

    def shumeiDeal(self):
        global Stype
        while True:
            if Stype == 1 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                self.displayMessage(message)
                self.stype = 1
            if Stype == 2 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + "5s保养"
                self.displayMessage(message)
                self.stype = 2
            if Stype == 3 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + ""
                self.displayMessage(message)
                self.stype = 3
            if Stype == 4 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                self.displayMessage(message)
                self.stype = 4
            if Stype == 5 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                self.displayMessage(message)
                self.stype = 5
            if Stype == 6 and self.stype == 0:
                message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                self.displayMessage(message)
                self.stype = 6
            if Stype == 0:
                if self.stype == 1:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人结束吃饭！"
                    self.stype = 0
                    self.displayMessage(message)
                if self.stype == 2:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人结束5s！"
                    self.stype = 0
                    self.displayMessage(message)
                if self.stype == 3:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人结束吃饭！"
                    self.stype = 0
                    self.displayMessage(message)
                if self.stype == 4:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人结束吃饭！"
                    self.stype = 0
                    self.displayMessage(message)
                if self.stype == 5:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                    self.stype = 0
                    self.displayMessage(message)
                if self.stype == 6:
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + "******" + "工人吃饭！"
                    self.stype = 0
                    self.displayMessage(message)

            time.sleep(0.06)

    def video_receive_local(self, cam1='E:/projects-summary/xiaowork/maindo/videos/西奥待检测数据/视频合并200512103448.mp4',
                            cam2='E:\\剪辑\\zhuangji\\ch11_20171221084313 00_09_06-00_10_21~2.mp4',
                            time_flag=True):
        '''该方法用来接收本地视频
        :param cam1: 左摄像头数据源
        :param cam2: 右摄像头数据源
        :param time_flag: 是否休眠，本地视频为True
        :return: None
        '''

        self.left_cam = cv2.VideoCapture(cam1)
        ret_1, frame_1 = self.left_cam.read()
        preCamPath = cam1
        while True:

            self.frame_left = frame_1
            if ret_1 is False:
                self.left_cam = cv2.VideoCapture(cam1)
            if self.CamPath != "" and self.CamPath != preCamPath:
                self.left_cam = cv2.VideoCapture(self.CamPath)
                preCamPath = self.CamPath
            ret_1, frame_1 = self.left_cam.read()
            if time_flag is True:
                time.sleep(0.04)

    def video_receive_rstp(self, cam1='rstp:', cam2='rstp:'):
        '''该方法用来接收网络视频
        :param cam1: 左摄像头数据源
        :param cam2: 右摄像头数据源
        :return: None
        '''
        self.video_receive_local(cam1=cam1, cam2=cam2, time_flag=False)

    def video_play(self):
        '''该方法用来播放视频
        :return: None
        '''

        def label_show_left(frame, label=self.ui.label):  # 左控件label播放
            height, width, _ = frame.shape
            frame_change = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.type_l == 'work':
                cv2.rectangle(frame_change, (self.X_l, self.Y_l), (self.X_l + 100, self.Y_l + 100), (0, 255, 0), 4)
            if self.tiaoshi_back is True:  # self.pb_loc = (130, 260, 610, 690)self.pf_loc = (250, 420, 800, 900)
                cv2.rectangle(frame_change, (610, 130), (690, 260), (255, 0, 0), 4)
            # if self.tiaoshi_forward is True:
            #     cv2.rectangle(frame_change, (800, 250), (900, 420), (255, 0, 0), 4)
            if self.chaiji_left is True:
                cv2.rectangle(frame_change, (20, 350), (210, 600), (255, 255, 0), 4)
            if self.chaiji_right is True:
                cv2.rectangle(frame_change, (980, 5), (1090, 130), (255, 255, 0), 4)

            frame_resize = cv2.resize(frame_change, (360, 240), interpolation=cv2.INTER_AREA)

            image = QtGui.QImage(frame_resize.data, frame_resize.shape[1], frame_resize.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 处理成QImage
            label.setPixmap(QtGui.QPixmap.fromImage(image))

        # def label_show_right(frame, label=self.ui.label_2):  # 右空间Lable播放
        #     height, width, _ = frame.shape
        #     frame_change = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     frame_resize = cv2.resize(frame_change, (360, 240), interpolation=cv2.INTER_AREA)
        #     image = QtGui.QImage(frame_resize.data, frame_resize.shape[1], frame_resize.shape[0],
        #                          QtGui.QImage.Format_RGB888)  # 处理成QImage
        #     label.setPixmap(QtGui.QPixmap.fromImage(image))

        if self.frame_left is not None:
            label_show_left(self.frame_left)

    def draw(self):
        '''
        展示图标
        :return:
        '''

        def draw_fp():  # 绘制损失饼图
            fp = Figure_Pie()
            da = data_access.EquipmentData()
            result = da.select()
            # fp.plot(*(result[-1][1], result[-1][2], result[-1][3], result[-1][4]))  # '*'有一个解包的功能，将（1，1，1，1）解包为 1 1 1 1
            fp.plot(*(33, 28, 37, 94))
            graphicscene_fp = QtGui.QGraphicsScene()
            graphicscene_fp.addWidget(fp.canvas)
            self.ui.graphicsView_Pie.setScene(graphicscene_fp)
            self.ui.graphicsView_Pie.show()

        def draw_oee():  # 绘制oee日推图
            current_time = datetime.datetime.now().strftime('%Y-%m-%d')
            lossTime = data_access.EquipmentTimeData()
            result_loss = lossTime.select_("select * from loss ORDER BY SJ DESC limit 1")
            zongshijian = time.strftime('%H:%M:%S', time.localtime(time.time()))
            # huanxing = result_loss[0][1]
            # dailiao = result_loss[0][2]
            # shebeiguzhang = result_loss[0][3]
            # tingzhi = result_loss[0][4]
            # # qitashijian=result[0][5]
            # # kongyunzhuan=result[0][6]
            # fuheshijian = (int(zongshijian.split(':')[0]) - 8) * 3600 + int(zongshijian.split(':')[1]) * 60 + int(
            #     zongshijian.split(':')[2]) - tingzhi
            # shijijiagong_1 = fuheshijian - huanxing - dailiao - shebeiguzhang

            da = data_access.DataAccess()
            resultw = da.select_("SELECT * from mstatus where SJC>date(now()) and `status`=1")
            if len(resultw) != 0:
                start_time = resultw[0][0]
                fuheshijian = (datetime.datetime.now() - start_time).seconds
                if time.localtime()[3] > 11:
                    fuheshijian = (datetime.datetime.now() - start_time).seconds - 60  # 吃饭时间
                eff = int(len(resultw) / fuheshijian * 100 * 22)  # 计算效率
            else:
                eff = 0

            hour = time.localtime()[3]  # 实时更新
            da_oee = data_access.OEEData()
            # da_oee.update_("update oee_date set O" + str(hour) + "=" + str(eff) + ' where SJC="' + current_time + '"')
            L_eff = []
            oee = Figure_OEE()
            da = data_access.OEEData()
            # result = da.select()
            hour = time.localtime()[3]
            result = [77, 82, 83, 79, 81, 85, 81, 78, 81, 85, 82, 81]
            for i in range(1, hour - 6):
                L_eff.append(result[i])
            oee.plot(*tuple(L_eff))  # 参数
            # oee.plot(*tuple([77,82,83,79,81,85,81,78]))
            graphicscene_oee = QtGui.QGraphicsScene()
            graphicscene_oee.addWidget(oee.canvas)
            self.ui.graphicsView_OEE.setScene(graphicscene_oee)
            self.ui.graphicsView_OEE.show()

        def draw_loss():  # 绘制损失直方图
            loss = Figure_Loss()
            da = data_access.EquipmentTimeData()
            result = da.select()
            # loss.plot(*(result[-1][1], result[-1][2], result[-1][3], result[-1][4]))
            loss.plot(*(140, 121, 113, 437))
            graphicscene_loss = QtGui.QGraphicsScene()
            graphicscene_loss.addWidget(loss.canvas)
            self.ui.graphicsView_Loss.setScene(graphicscene_loss)
            self.ui.graphicsView_Loss.show()

        def draw_mt():  # 绘制耗材使用图
            mt = Figure_MT()
            bottle = 0
            current_time = datetime.datetime.now().strftime('%Y-%m-%d')
            da_mt = data_access.EquipmentTimeData()
            # result_mt = da_mt.select_(
            #     'select * from mtrecord where date_format(SJC, "%Y-%m-%d") = "' + current_time + '"')
            # for result_m in result_mt:
            #     if result_m[1] == "bottlechange":
            #         bottle += 1
            mt.plot(*(4, 5, 3))
            graphicscene_mt = QtGui.QGraphicsScene()
            graphicscene_mt.addWidget(mt.canvas)
            self.ui.graphicsView_MT.setScene(graphicscene_mt)
            self.ui.graphicsView_MT.show()

        draw_fp()
        draw_loss()
        draw_mt()
        draw_oee()

    def video_recog(self):
        '''
        视频识别部分
        :return:
        '''
        self.totaltime += 1
        frame_left = self.frame_left  # 原始彩色图，左边摄像头
        frame_left_gray = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)  # 原始图的灰度图

        # frame_right = self.frame_right
        # frame_right_gray = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # frame_right = self.frame_left  # 原始彩色图
        # frame_right_gray = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        def video_recog_left():
            img = frame_left
            spark, x, y = self.vision.find_spark(img)
            self.q.enqueue(spark)
            # print(spark)
            if spark:
                self.type_l = 'work'
                self.X_l = x
                self.Y_l = y
            else:
                self.type_l = ''
            if spark or True in self.q.queue:  # 如果一段间隔时间内不断有火花（和机器移动，稍后完成），则说明机器必定处于工作状态
                self.one_static_time = 0  # 恢复到运动后，一次静止时间重新清零
                self.work_time += 1
                self.is_work = True

                if self.work_time % 20 == 0:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    da = data_access.DataAccess()

                    da.update_("insert into mstatus(SJC,status)values('" + current_time + "',1)")
                    message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']' + '机器正在工作'
                    self.displayMessage(message)
            else:
                # ******* 截图
                self.is_work = False
                self.one_static_time += 1  # 一次静止时间
                if self.one_static_time % 60 == 0:
                    print('start or static')
                    print('静止了，往catch文件夹中查看原因')
                    t = time.localtime()
                    hour = t[3]
                    mini = t[4]
                    seco = t[5]
                    filename = str(hour) + '-' + str(mini) + '-' + str(seco)
                    cv2.imwrite('./catch/' + filename + '.jpg', img)
                # ********

                self.action = ThreadedTCPRequestHandler.action  # 键盘操作
                if self.action is not None:  # 往面板上写当前由于什么原因导致机器静止
                    if self.pre_action is None:
                        print(self.action)
                        message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(time.time())) + ']' + str(self.action)
                        self.displayMessage(message)

                if self.vision.tiaoshi(frame_left_gray):
                    self.action_video = 'tiaoshi'
                if self.action_video is not None:
                    if self.pre_action_video is None:
                        pass
                        # print(self.action_video)
                        # message = '[' + time.strftime('%Y-%m-%d %H:%M:%S',
                        #                               time.localtime(time.time())) + ']' + str(self.action_video)
                        # self.displayMessage(message)

        video_recog_left()
        self.pre_action = self.action
        self.pre_action_video = self.action_video

    def data_read(self):
        pass

    def displayMessage(self, message):

        self.ui.textBrowser.append(message)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_app = XioAll()
    app.setQuitOnLastWindowClosed(True)
    main_app.show()
    sys.exit(app.exec_())
