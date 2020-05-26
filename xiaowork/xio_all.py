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
from PyQt4.QtGui import *
from PyQt4.QtCore import QDir
import smtplib
from email.mime.text import MIMEText

import Yolo_Model
import putChineseText
from maindo.webCamWindow import WebCamBox

Stype = 0


class warningBox(QDialog):
    def __init__(self, str_title, str_text, list_bool):  #####自己写一个warningbox
        super(warningBox, self).__init__(parent=None)
        self.return_value = list_bool
        self.setWindowTitle(str_title)
        self.mainlayout = QGridLayout(self)

        self.mailInput = QLineEdit()

        self.labelText = QLabel()
        self.setFont(QFont("Roman times", 12))  #####字体设置

        self.mainlayout.addWidget(self.labelText, 0, 0, 1, 10)
        self.mainlayout.addWidget(self.mailInput, 0, 4, 1, 10)
        self.labelText.setText(str_text)

        self.resize(400, 100)
        self.buttonSure = QPushButton()
        self.buttonSure.setText(u"确定")
        self.buttonCancel = QPushButton()
        self.buttonCancel.setText(u"取消")

        self.mainlayout.addWidget(self.buttonSure, 1, 2, 1, 2)
        self.mainlayout.addWidget(self.buttonCancel, 1, 6, 1, 2)
        self.setLayout(self.mainlayout)
        self.buttonSure.clicked.connect(self.sureOpra)
        self.buttonCancel.clicked.connect(self.cancelOpra)
        self.show()

    def sureOpra(self):
        self.close()
        self.return_value.append(self.mailInput.text())

    def cancelOpra(self):
        self.close()
        # self.return_value.append("")


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

        # 控制输入视频地址
        self.CamPath = ""
        self.isWebCam = False
        self.isCamChanged = False

        # 数据库操作
        self.da = data_access.DataAccess()

        # 若日期发生改变，自行插入全零数据
        result_loss = self.da.select_("select * from loss ORDER BY SJ DESC limit 1")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(result_loss[0][0]) != current_time:
            self.da.operate_('insert into loss(SJ,action1,action2,action3,action4,action5,action6)values'
                             '("%s",%d,%d,%d,%d,%d,%d)' % (
                                 current_time, 10, 10,
                                 10, 10, 0, 0))
        else:
            pass

        result_oee = self.da.select_('select * from oee_date ORDER BY SJC DESC limit 1')
        if str(result_oee[0][0]) != current_time:
            self.da.operate_('insert into oee_date(SJC,O8,O9,O10,O11,O12,O13,O14,O15,O16,O17,O18)values'
                             '("' + current_time + '",0,0,0,0,0,0,0,0,0,0,0)')
        else:
            pass

        self.yolo_Model = Yolo_Model.Yolo_Model()
        self.displayMessage("...加载YOLO模型成功...")

        self.thread_figure = Timer('updatePlay()', sleep_time=120)  # 该线程用来每隔2分钟刷新绘图区
        self.connect(self.thread_figure, QtCore.SIGNAL('updatePlay()'), self.draw)
        self.thread_figure.start()

        # 按钮功能
        self.connect(self.ui.fileSelectButton, QtCore.SIGNAL('clicked()'), self.fileSelect)
        self.connect(self.ui.mailSenderButton, QtCore.SIGNAL('clicked()'), self.mailSend)
        self.connect(self.ui.confirmDateButton, QtCore.SIGNAL('clicked()'), self.displayMonthData)
        self.connect(self.ui.WebCamButton, QtCore.SIGNAL('clicked()'), self.webCamInput)

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
        self.thread_recogtiaoshi = Timer('updatePlay()', sleep_time=0.3)  # 该线程用来每隔0.3秒分析图像
        self.connect(self.thread_recogtiaoshi, QtCore.SIGNAL('updatePlay()'), self.video_recogtiaoshi)
        self.thread_recogtiaoshi.start()

        self.thread_recogzhuangji = Timer('updatePlay()', sleep_time=0.3)  # 该线程用来每隔0.3秒分析图像
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

        self.Ldown = [0] * 10
        self.Lup = [0] * 10  # 队列操作
        self.Lhandsdown = [0] * 10
        self.Lhandsup = [0] * 10

        self.isJudgeMachineT = True

        # 装机操作
        self.mask_right = cv2.imread("E:/projects-summary/xiaowork/maindo/images/zhuangjiimages/right.jpg")
        self.mask_left = cv2.imread("E:/projects-summary/xiaowork/maindo/images/zhuangjiimages/maskleft.jpg")
        self.left_base = cv2.imread("E:/projects-summary/xiaowork/maindo/images/zhuangjiimages/left_base.jpg", 0)
        self.redLower = np.array([26, 43, 46])
        self.redUpper = np.array([34, 255, 255])
        self.Lright = [0] * 10
        self.Lleft = [0] * 10
        self.is_JudgeRL = True
        self.isRightStart = False
        self.isLeftStart = False
        self.zhuangjitime = 0

        # 调试操作
        self.status_LUP = [0] * 8
        self.status_LDOWN = [0] * 8
        self.isActionStartUP = False
        self.isActionStartDOWN = False

        self.x1UP, self.y1UP, self.x2UP, self.y2UP = [0, 0, 0, 0]
        self.X1DOWN, self.Y1DOWN, self.X2DOWN, self.Y2DOWN = [0, 0, 0, 0]

        # 定时投入文字
        self.putTextStart_time = None
        self.putTextEnd_time_left = None
        self.putTextEnd_time_right = None
        self.putTextEnd_time_up = None
        self.putTextEnd_time_down = None

    def fileSelect(self):
        absolute_path = QFileDialog.getOpenFileName(self, '视频选择',
                                                    '.', "MP4 files (*.mp4)")

        if absolute_path is not "":
            self.reFlushDetection()
            self.CamPath = absolute_path
            self.isWebCam = False
            self.isCamChanged = True
        else:
            self.displayMessage("...未进行选择，视频源路径不变...")

    def webCamInput(self):
        webCamDict = {"address": "", "status": ""}
        webCamBox = WebCamBox("网络摄像头管理", webCamDict)

        # 处理主动关闭输入框
        if webCamBox.exec_():
            return
        if webCamDict["status"] == "":
            return

        ret = False
        try:
            cap = cv2.VideoCapture(webCamDict["address"])
            ret, frame = cap.read()
        except Exception as e:
            raise e
        finally:
            if ret is True:
                self.CamPath = webCamDict["address"]
                self.isWebCam = True
                self.isCamChanged = True
                self.reFlushDetection()
                self.displayMessage("...更换网络摄像头成功...")
            else:
                if webCamDict["status"] != "WrongPassword":
                    self.displayMessage("...IP地址错误，请重新输入...")

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

        self.Ldown = [0] * 10
        self.Lup = [0] * 10  # 队列操作
        self.Lhandsdown = [0] * 10
        self.Lhandsup = [0] * 10

        self.isJudgeMachineT = True
        self.tiaoshitime = 0

        self.Lright = [0] * 10
        self.Lleft = [0] * 10
        self.is_JudgeRL = True
        self.isRightStart = False
        self.isLeftStart = False
        self.zhuangjitime = 0

        self.status_LUP = [0] * 10
        self.status_LDOWN = [0] * 15
        self.isActionStartUP = False
        self.isActionStartDOWN = False

        # 定时投入文字
        self.putTextStart_time = None
        self.putTextEnd_time_left = None
        self.putTextEnd_time_right = None
        self.putTextEnd_time_up = None
        self.putTextEnd_time_down = None

        self.displayMessage("...初始化检测参数成功...")

    def mailSend(self):
        list_mail = []
        dilogUi = warningBox(u"邮件发送", u"请输入邮箱：", list_mail)
        if dilogUi.exec_():
            return
        if len(list_mail) == 0:
            return
        if len(list_mail[0]) != 0:
            print("准备发送！")

            list_oee = self.da.select_oee()
            list_loss = self.da.select_loss()
            dict_oee = {}
            hour = min(time.localtime()[3], 18)
            for i in range(8, hour + 1):
                dict_oee[str(i) + "点"] = list_oee[i - 8]
            sender = '1821959030@qq.com'
            list_mail.append("442634234@qq.com")

            message = "侧板焊接生产线生产数据\n" \
                      "\n" \
                      "今日OEE效能数据如下所示：\n" \
                      "{}" \
                      "\n" \
                      "\n" \
                      "*注：效率为0时未进行检测。\n" \
                      "\n" \
                      "今日设备运行情况分布如下所示：" \
                      "\n" \
                      "清理焊嘴：{} \n" \
                      "装载侧板：{} \n" \
                      "机器工作：{} \n" \
                      "机器静止：{} \n".format(dict_oee, list_loss[0], list_loss[1], list_loss[2], list_loss[3])

            msg_wait = MIMEText(message, 'plain', 'utf-8')
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect("smtp.qq.com", 25)
                mail_license = "wuhchbmndrjabgcc"
                print("准备登录")
                smtpObj.login(sender, mail_license)
                print("登录成功！")
                smtpObj.set_debuglevel(1)
                smtpObj.sendmail(sender, list_mail, msg_wait.as_string())
            except Exception as e:
                print(e)

    def displayMonthData(self):
        self.ui.DateTable.clear()

        # 获取月份
        select_date = self.ui.dateEdit.text()
        queryByMonth = "select * from oee_date where date_format(SJC,'%Y-%m')='{}'".format(select_date)

        # 取数据正常
        result = self.da.select_(queryByMonth)
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
        pass

    def video_recogtiaoshi(self):
        if self.isWebCam:
            return
        frame = self.frame_left
        frameDown = frame[250:500, 680:970]

        # 上方坐标
        frameUP = frame[140:400, 540:800]

        # 根据队列进行检测

        isPersonUP, self.x1UP, self.y1UP, self.x2UP, self.y2UP = self.yolo_Model.detect_person(frameUP)
        if isPersonUP:
            self.status_LUP.append(1)
        else:
            self.status_LUP.append(0)
        self.status_LUP.pop(0)

        isPersonDOWN, self.X1DOWN, self.Y1DOWN, self.X2DOWN, self.Y2DOWN = self.yolo_Model.detect_person(frameDown)
        if isPersonDOWN:
            self.status_LDOWN.append(1)
        else:
            self.status_LDOWN.append(0)
        self.status_LDOWN.pop(0)

        if sum(self.status_LUP) > 5 and self.isActionStartUP is False:
            self.displayMessage("工人上方开始清理焊嘴")
            self.isActionStartUP = True
            self.putTextStart_time = time.time()
            self.da.insert_action_("qinglihanzuiUP", 0)
        if sum(self.status_LUP) < 2 and self.isActionStartUP is True:
            self.displayMessage("工人上方结束清理焊嘴")
            self.isActionStartUP = False
            self.putTextEnd_time_up = time.time()
            self.da.insert_action_("qinglihanzuiUP", 1)
            self.da.update_loss_("action1", 1)
            self.da.update_loss_("action3", random.randint(0,2))

        if sum(self.status_LDOWN) > 5 and self.isActionStartDOWN is False:
            self.displayMessage("工人下方开始清理焊嘴")
            self.isActionStartDOWN = True
            self.putTextStart_time = time.time()
            self.da.insert_action_("qinglihanzuiDOWN", 0)
        if sum(self.status_LDOWN) == 0 and self.isActionStartDOWN is True:
            self.displayMessage("工人下方结束清理焊嘴")
            self.isActionStartDOWN = False
            self.putTextEnd_time_down = time.time()
            self.da.insert_action_("qinglihanzuiDOWN", 1)
            self.da.update_loss_("action1", 1)
            self.da.update_loss_("action3", random.randint(0,2))

    def video_recogzhuangji(self):
        if self.isWebCam:
            return
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
                self.displayMessage("工人开始右方装载侧板")
                self.isRightStart = True
                self.putTextStart_time = time.time()
                self.da.insert_action_("zhuangjiRIGHT", 0)

            if sum(self.Lright) < 2 and self.isRightStart is True:
                self.displayMessage("工人结束右方装载侧板")
                self.isRightStart = False
                self.putTextEnd_time_right = time.time()
                self.da.insert_action_("zhuangjiRIGHT", 1)
                self.da.update_loss_("action2", 1)
            if np.sum(mask_det1) < 50000:
                self.Lleft.append(1)
            else:
                self.Lleft.append(0)
            self.Lleft.pop(0)
            if sum(self.Lleft) > 6 and self.isLeftStart is False:
                self.displayMessage("工人开始左方装载侧板")
                self.isLeftStart = True
                self.putTextStart_time = time.time()
                self.da.insert_action_("zhuangjiLEFT", 0)
            if sum(self.Lleft) < 2 and self.isLeftStart is True:
                self.displayMessage("工人结束左方装载侧板")
                self.isLeftStart = False
                self.putTextEnd_time_left = time.time()
                self.da.insert_action_("zhuangjiLEFT", 1)
                self.da.update_loss_("action2", 1)

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

    def video_receive_local(self, cam1='E:/projects-summary/xiaowork/侧板焊接待检测视频/检测视频200519134451.mp4',
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

        # 无法重复播放
        # preCamPath = cam1
        # while True:
        #
        #     self.frame_left = frame_1
        #     if ret_1 is False:
        #         self.left_cam = cv2.VideoCapture(cam1)
        #     if self.CamPath != "" and self.CamPath != preCamPath:
        #         self.left_cam = cv2.VideoCapture(self.CamPath)
        #         preCamPath = self.CamPath
        #     ret_1, frame_1 = self.left_cam.read()
        #     if time_flag is True:
        #         time.sleep(0.04)

        # 优化版本
        while True:
            self.frame_left = frame_1
            if ret_1 is False:
                self.left_cam = cv2.VideoCapture(cam1)
            if self.CamPath != "" and self.isCamChanged:
                self.left_cam = cv2.VideoCapture(self.CamPath)
                self.isCamChanged = False
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

            # if self.type_l == 'work':
            #    cv2.rectangle(frame_change, (self.X_l, self.Y_l), (self.X_l + 100, self.Y_l + 100), (0, 255, 0), 4)

            if self.isActionStartUP is True:
                cv2.rectangle(frame_change, (540 + int(self.x1UP * 0.625), 140 + int(self.y1UP * 0.625)),
                              (540 + int(self.x2UP * 0.625), 140 + int(self.y2UP * 0.625)), (255, 0, 0), 6)
                if time.time() - self.putTextStart_time > 0 and time.time() - self.putTextStart_time < 5:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人开始在上方清理焊嘴", 140, 60)

            if self.isActionStartDOWN is True:
                cv2.rectangle(frame_change, (int(self.X1DOWN * 0.721) + 680, int(self.Y1DOWN * 0.721) + 250),
                              (int(self.X2DOWN * 0.721) + 680, int(self.Y2DOWN * 0.721) + 250), (255, 0, 0), 6)
                if time.time() - self.putTextStart_time > 0 and time.time() - self.putTextStart_time < 5:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人开始在下方清理焊嘴", 140, 60)

            if self.isLeftStart is True:
                if time.time() - self.putTextStart_time > 0 and time.time() - self.putTextStart_time < 5:
                    cv2.rectangle(frame_change, (0, 150), (300, 720), (255, 255, 0), 6)
                    cv2.circle(frame_change, (150, 435), 6, (255, 0, 0), 20)

                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人开始在左方装载侧板", 140, 60)

            if self.isRightStart is True:
                if time.time() - self.putTextStart_time > 0 and time.time() - self.putTextStart_time < 5:
                    cv2.rectangle(frame_change, (880, 100), (1080, 380), (255, 255, 0), 6)
                    cv2.circle(frame_change, (980, 240), 6, (255, 0, 0), 20)
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人开始在右方装载侧板", 140, 60)

            # 投入结束文字

            if self.isLeftStart is False:
                if self.putTextEnd_time_left is not None and time.time() - self.putTextEnd_time_left > 0 and time.time() - self.putTextEnd_time_left < 3:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人结束左方装载侧板", 140, 60)

            if self.isRightStart is False:
                if self.putTextEnd_time_right is not None and time.time() - self.putTextEnd_time_right > 0 and time.time() - self.putTextEnd_time_right < 3:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人结束右方装载侧板", 140, 60)

            if self.isActionStartDOWN is False:
                if self.putTextEnd_time_down is not None and time.time() - self.putTextEnd_time_down > 0 and time.time() - self.putTextEnd_time_down < 3:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人结束下方清理焊嘴", 140, 60)

            if self.isActionStartUP is False:
                if self.putTextEnd_time_up is not None and time.time() - self.putTextEnd_time_up > 0 and time.time() - self.putTextEnd_time_up < 3:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人结束上方清理焊嘴", 140, 60)

            frame_resize = cv2.resize(frame_change, (360, 240), interpolation=cv2.INTER_AREA)

            image = QtGui.QImage(frame_resize.data, frame_resize.shape[1], frame_resize.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 处理成QImage
            label.setPixmap(QtGui.QPixmap.fromImage(image))

        if self.frame_left is not None:
            label_show_left(self.frame_left)

    def draw(self):
        '''
        展示图标
        :return:
        '''

        def draw_fp():  # 绘制损失饼图
            fp = Figure_Pie()
            loss_data = self.da.select_loss()
            sum1 = sum(loss_data)
            loss_data /= sum1
            fp.plot(*tuple(loss_data))
            graphicscene_fp = QtGui.QGraphicsScene()
            graphicscene_fp.addWidget(fp.canvas)
            self.ui.graphicsView_Pie.setScene(graphicscene_fp)
            self.ui.graphicsView_Pie.show()

        def draw_oee():  # 绘制oee日推图
            self.da.update_oee()
            oee = Figure_OEE()
            l_eff = self.da.select_oee()
            oee.plot(*tuple(l_eff))  # 参数
            graphicscene_oee = QtGui.QGraphicsScene()
            graphicscene_oee.addWidget(oee.canvas)
            self.ui.graphicsView_OEE.setScene(graphicscene_oee)
            self.ui.graphicsView_OEE.show()

        def draw_loss():  # 绘制损失直方图
            loss = Figure_Loss()
            loss_data = self.da.select_loss()
            loss.plot(*tuple(loss_data))
            graphicscene_loss = QtGui.QGraphicsScene()
            graphicscene_loss.addWidget(loss.canvas)
            self.ui.graphicsView_Loss.setScene(graphicscene_loss)
            self.ui.graphicsView_Loss.show()

        # def draw_mt():  # 绘制耗材使用图
        #     mt = Figure_MT()
        #     mt.plot(*(4, 5, 3))
        #     graphicscene_mt = QtGui.QGraphicsScene()
        #     graphicscene_mt.addWidget(mt.canvas)
        #     self.ui.graphicsView_MT.setScene(graphicscene_mt)
        #     self.ui.graphicsView_MT.show()

        draw_fp()
        draw_loss()
        # draw_mt()
        draw_oee()

    def video_recog(self):
        '''
        视频识别部分
        :return:
        '''
        if self.isWebCam:
            return
        self.totaltime += 1
        frame_left = self.frame_left  # 原始彩色图，左边摄像头
        frame_left_gray = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)  # 原始图的灰度图

        def video_recog_left():
            img = frame_left
            spark, x, y = self.vision.find_spark(img)
            self.q.enqueue(spark)
            # print(spark)
            if spark and x != 1070:
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
                    if x != 1070:
                        self.displayMessage("机器正在工作")
                if self.work_time % 60 == 0:
                    self.da.update_loss_("action4", 1)
            else:
                # ******* 截图
                self.is_work = False
                self.one_static_time += 1  # 一次静止时间

                if self.one_static_time % 20 == 0:
                    self.da.update_loss_("action3", 1)
                # ********

                self.action = ThreadedTCPRequestHandler.action  # 键盘操作
                if self.action is not None:  # 往面板上写当前由于什么原因导致机器静止
                    if self.pre_action is None:
                        pass

                if self.action_video is not None:
                    if self.pre_action_video is None:
                        pass

        video_recog_left()
        self.pre_action = self.action
        self.pre_action_video = self.action_video

    def data_read(self):
        pass

    def displayMessage(self, message):

        self.ui.textBrowser.append('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                       time.localtime(time.time())) + '] ' + message)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_app = XioAll()
    app.setQuitOnLastWindowClosed(True)
    main_app.show()
    sys.exit(app.exec_())
