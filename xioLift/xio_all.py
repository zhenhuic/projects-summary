from PyQt4 import QtGui, QtCore
import uifiles.xio_all_ui as ui
import sys
import cv2
from numpy import *
import threading
import datetime
from utils.utils import Timer, MyQueue
from utils.vision import featrue_detection, diff, background_diff
import socketserver
import time
from figure.figure_plot import *
from data import data_access

from PyQt4.QtGui import *
from PyQt4.QtCore import QDir


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
        self.return_value.append("")


class XioAll(QtGui.QWidget):
    '''这个类为主程序类
    '''

    def __init__(self):
        super(XioAll, self).__init__()
        self.ui = ui.Ui_Form()
        self.ui.setupUi(self)

        self.frame_left = None
        self.frame_right = None
        self.is_work = True
        self.one_static_time = 0  # 一次故障静止的时间
        self.all_time = 0  # 一天的工作时间
        self.q = MyQueue()  # 存放帧队列,改为存放状态比较好

        # 按钮功能
        self.connect(self.ui.fileSelectButton, QtCore.SIGNAL('clicked()'), self.fileSelect)
        self.connect(self.ui.mailSenderButton, QtCore.SIGNAL('clicked()'), self.mailSend)
        self.connect(self.ui.confirmDateButton, QtCore.SIGNAL('clicked()'), self.displayMonthData)

        self.thread_figure = Timer('updatePlay()', sleep_time=120)  # 该线程用来每隔2分钟刷新绘图区
        self.connect(self.thread_figure, QtCore.SIGNAL('updatePlay()'), self.draw)
        self.thread_figure.start()

        self.thread_video_receive = threading.Thread(target=self.video_receive_local)  # 该线程用来读取视频流
        self.thread_video_receive.start()

        self.thread_time = Timer('updatePlay()')  # 该线程用来每隔0.04秒在label上绘图
        self.connect(self.thread_time, QtCore.SIGNAL('updatePlay()'), self.video_play)
        self.thread_time.start()

        self.thread_recogn171 = Timer('updatePlay()', sleep_time=0.2)  # 该线程用来每隔一秒分析图像
        self.connect(self.thread_recogn171, QtCore.SIGNAL('updatePlay()'), self.video_reco173)
        self.thread_recogn171.start()

        self.thread_data = Timer('updatePlay()', sleep_time=1800)  # 该线程用来每隔半小时向数据库读取数据
        self.connect(self.thread_data, QtCore.SIGNAL('updatePlay()'), self.data_read)
        self.thread_data.start()

        # 厚板171夜间
        # self.nppeb_image = cv2.imread('./images/173d.jpg')
        # self.M5000_work_ = self.nppeb_image[350:450, 550:700]
        # self.nppeb_mach_time = [0] * 50
        # self.nppeb_tuo_time = [0] * 50
        # self.nppeb_work_time = [0] * 100
        # self.nppeb_mach_stop_time = None
        # self.nppeb_mach_start_time = None
        # self.nppeb_tiao_start_time = None
        # self.nppeb_tiao_stop_time = None
        # self.nppeb_background_roi = None
        # self.nppeb_tuo_start_time = None
        # self.nppeb_tuo_stop_time = None
        # self.nppeb_tuo_background_roi = None
        # self.nppeb_frame_roi = None
        # self.pic_n171mach = False
        # self.picstime = 0

        self.CamPath = ""

        # 定时投入文字
        self.putTextStart_time = None

        # 数据库操作
        self.da = data_access.DataAccess()

        # 若日期发生改变，自行插入全零数据
        result_loss = self.da.select_("select * from loss ORDER BY SJ DESC limit 1")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(result_loss[0][0]) != current_time:
            self.da.operate_('insert into loss(SJ,action1,action2,action3,action4,action5,action6)values'
                             '("%s",%d,%d,%d,%d,%d,%d)' % (
                                 current_time, random.randint(0, 50), random.randint(0, 50),
                                 random.randint(300, 400),
                                 random.randint(300, 400), 0, 0))
        else:
            pass

        result_oee = self.da.select_('select * from oee_date ORDER BY SJC DESC limit 1')
        if str(result_oee[0][0]) != current_time:
            self.da.operate_('insert into oee_date(SJC,O8,O9,O10,O11,O12,O13,O14,O15,O16,O17,O18)values'
                             '("' + current_time + '",0,0,0,0,0,0,0,0,0,0,0)')
        else:
            pass

        # self.M5000_work_background = cv2.imread('images/173d.jpg')
        # self.M5000_work_background = cv2.resize(self.M5000_work_background,(1280,720))
        self.M5000_work_background = None
        self.op20_work_background = cv2.imread('E:/projects-summary/xioLift/maindo/images/173d.jpg')
        self.op20_work_background = cv2.resize(self.op20_work_background, (1280, 720))
        self.M5000_fix_backgrond = cv2.imread('E:/projects-summary/xioLift/maindo/images/173f.png')
        self.M5000_fix_backgrond = cv2.resize(self.M5000_fix_backgrond, (1280, 720))
        self.op20_night_background = cv2.imread('E:/projects-summary/xioLift/maindo/images/173n.png')
        self.op20_night_background = cv2.resize(self.op20_night_background, (1280, 720))
        self.M5000_work_start_judge = False
        self.M5000_work_time = [0] * 25
        self.M5000_jud_start_judge = False
        self.M5000_jud_time = [0] * 20
        self.houban_huan_backgrond = None
        self.houban_huan_judge = False
        self.houban_huan_time = [0] * 20
        self.M5000_fix_judge = False
        self.M5000_fix_time = [0] * 10
        self.houban_material_backgrond = None
        self.houban_material_judge = False
        self.houban_material_all_judge = False
        self.houban_material_time = [0] * 20
        self.houban_material_all_time = [0] * 30

    def fileSelect(self):
        absolute_path = QFileDialog.getOpenFileName(self, '视频选择',
                                                    '.', "MP4 files (*.mp4)")

        if self.CamPath != absolute_path:
            self.reFlushDetection()
            self.CamPath = absolute_path
        else:
            self.displayMessage("...未进行选择，视频源路径不变...")

    def reFlushDetection(self):

        self.M5000_work_background = None
        self.op20_work_background = cv2.imread('E:/projects-summary/xioLift/maindo/images/173d.jpg')
        self.op20_work_background = cv2.resize(self.op20_work_background, (1280, 720))
        self.M5000_fix_backgrond = cv2.imread('E:/projects-summary/xioLift/maindo/images/173f.png')
        self.M5000_fix_backgrond = cv2.resize(self.M5000_fix_backgrond, (1280, 720))
        self.op20_night_background = cv2.imread('E:/projects-summary/xioLift/maindo/images/173n.png')
        self.op20_night_background = cv2.resize(self.op20_night_background, (1280, 720))
        self.M5000_work_start_judge = False
        self.M5000_work_time = [0] * 25
        self.M5000_jud_start_judge = False
        self.M5000_jud_time = [0] * 20
        self.houban_huan_backgrond = None
        self.houban_huan_judge = False
        self.houban_huan_time = [0] * 20
        self.M5000_fix_judge = False
        self.M5000_fix_time = [0] * 10
        self.houban_material_backgrond = None
        self.houban_material_judge = False
        self.houban_material_all_judge = False
        self.houban_material_time = [0] * 20
        self.houban_material_all_time = [0] * 30

        self.displayMessage("......初始化参数成功......")

    def mailSend(self):
        list_mail = []
        dilogUi = warningBox(u"邮件发送", u"请输入邮箱：", list_mail)
        if dilogUi.exec_():
            return
        if len(list_mail[0]) != 0:
            print("准备发送！")
            import smtplib
            from email.mime.text import MIMEText

            list_oee = self.da.select_oee()
            list_loss = self.da.select_loss()
            dict_oee = {}
            hour = min(time.localtime()[3], 19)
            for i in range(8, hour + 1):
                dict_oee[str(i) + "点："] = list_oee[i - 8]
            sender = '619520071@qq.com'
            list_mail.append("442634234@qq.com")

            message = "厚板生产线生产数据\n" \
                      "" \
                      "今日OEE效能数据如下所示：\n" \
                      "{}" \
                      "\n" \
                      "*注：效率为0时未进行检测。\n" \
                      "\n" \
                      "今日设备运行情况分布如下所示：" \
                      "\n" \
                      "拖料：{} \n" \
                      "材料切换：{} \n" \
                      "机器工作：{} \n" \
                      "机器静止：{} \n".format(dict_oee, list_loss[0], list_loss[1], list_loss[2], list_loss[3])

            msg_wait = MIMEText(message, 'plain', 'utf-8')
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect("smtp.qq.com", 25)
                mail_license = "pddryrrqzlbkbcif"
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

    def video_receive_local(self, cam1='E:/projects-summary/xioLift/maindo/videos/173_10.mp4', cam2='./videos/n171.mp4', time_flag=True):
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
            frame = cv2.resize(frame, (1280, 720))
            frame_change = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 投入文字以及圆点
            if self.M5000_jud_start_judge is True:
                cv2.rectangle(frame_change, (540 + int(self.x1UP * 0.625), 140 + int(self.y1UP * 0.625)),
                              (540 + int(self.x2UP * 0.625), 140 + int(self.y2UP * 0.625)), (255, 0, 0), 4)
                if time.time() - self.putTextStart_time > 1 and time.time() - self.putTextStart_time < 4:
                    frame_change = putChineseText.cv2ImgAddText(frame_change, "工人在上方清理焊嘴中", 140, 60)

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

        draw_fp()
        draw_loss()
        draw_oee()

    def video_rec173(self):
        pass

    def video_reco173(self):
        frame = self.frame_left
        frame = cv2.resize(frame, (1280, 720))

        self.op20_night = featrue_detection(frame, self.op20_night_background, 60, 40, 300, 400, 200, 350)

        if self.M5000_work_background is not None:
            self.M5000_work_background_1 = background_diff(self.M5000_work_background, 0, 100, 600, 910)
            self.M5000_work_background_2 = background_diff(self.M5000_work_background, 100, 230, 600, 910)
            self.M5000_work_1 = diff(frame, self.M5000_work_background_1, 100000, 0, 100, 600, 910)
            self.M5000_work_2 = diff(frame, self.M5000_work_background_2, 100000, 100, 230, 600, 910)
            self.op20_work = featrue_detection(frame, self.op20_work_background, 60, 20, 260, 360, 500, 650)

            if (self.M5000_work_1 is True and self.M5000_work_2 is True and self.op20_night is True) or (
                    self.op20_work is True and self.op20_night is True):
                self.M5000_work_time.pop(0)
                self.M5000_work_time.append(1)

            if self.M5000_work_1 is True and self.M5000_work_2 is True and self.op20_work is False:
                self.M5000_work_time.pop(0)
                self.M5000_work_time.append(1)

            # 机器停工
            elif self.M5000_work_1 is False and self.op20_work is False:
                print('机器停工')
                self.M5000_work_time.pop(0)
                self.M5000_work_time.append(0)

                # 调整
                if self.op20_night is True:
                    if self.M5000_work_2 is True:
                        self.M5000_jud_time.pop(0)
                        self.M5000_jud_time.append(1)
                        # print('M5000_work_2',M5000_work_2)
                        # print('M5000_work_1', M5000_work_1)
                        # print('op20_work', op20_work)


                    elif self.M5000_work_2 is False:
                        self.M5000_jud_time.pop(0)
                        self.M5000_jud_time.append(0)

                    self.M5000_jud_time_sum = sum(self.M5000_jud_time)
                    # print(M5000_jud_time_sum)
                    if self.M5000_jud_start_judge is False and self.M5000_jud_time_sum > 4:
                        M5000_jud_start = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        # print('M5000_jud_start',self.M5000_jud_start)
                        self.displayMessage('开始调整机器')
                        self.da.insert_action_("MaterialChange", 0)
                        self.M5000_jud_start_judge = True
                        self.putTextStart_time = time.time()

                    if self.M5000_jud_start_judge is True and self.M5000_jud_time_sum <= 2:
                        M5000_jud_stop = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        # print('M5000_jud_stop', M5000_jud_stop)
                        self.displayMessage('完成调整机器')
                        self.da.insert_action_("MaterialChange", 1)
                        self.da.update_loss_("action1", 1)
                        self.M5000_jud_start_judge = False

                # 修理M5000
                self.M5000_fix = featrue_detection(frame, self.M5000_fix_backgrond, 60, 10, 0, 65, 350, 520)
                if self.M5000_fix is True:
                    self.M5000_fix_time.pop(0)
                    self.M5000_fix_time.append(0)

                else:
                    self.M5000_fix_time.pop(0)
                    self.M5000_fix_time.append(1)

                M5000_fix_time_sum = sum(self.M5000_fix_time)
                if self.M5000_fix_judge is False and M5000_fix_time_sum > 4:
                    M5000_fix_start = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    # print('M5000_fix_start', self.M5000_fix_start)
                    self.displayMessage('开始修理机器')  # 修理机器
                    self.M5000_fix_judge = True
                    self.da.insert_action_("MachineAdjust", 0)
                    self.putTextStart_time = time.time()

                if self.M5000_fix_judge is True and M5000_fix_time_sum <= 2:
                    M5000_fix_stop = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    # print('M5000_fix_stop', M5000_fix_stop)
                    self.displayMessage('完成修理机器')
                    self.da.insert_action_("MachineAdjust", 1)
                    self.da.update_loss_("action2", 1)
                    self.M5000_fix_judge = False

                # 调整材料
                if self.houban_material_backgrond is not None:
                    self.houban_material_backgrond_lower = background_diff(self.houban_material_backgrond, 550, 720,
                                                                           430,
                                                                           750)
                    self.houban_material_backgrond_all = background_diff(self.houban_material_backgrond, 190, 350, 1015,
                                                                         1100)

                    self.houban_material = diff(frame, self.houban_material_backgrond_lower, 1000000, 550, 720, 430,
                                                750)
                    self.houban_material_all = diff(frame, self.houban_material_backgrond_all, 100000, 190, 350, 1015,
                                                    1100)
                    # print('shang',houban_material_upper)
                    # print('xia',houban_material)
                    if self.houban_material is True:
                        self.houban_material_time.pop(0)
                        self.houban_material_time.append(1)

                    else:
                        self.houban_material_time.pop(0)
                        self.houban_material_time.append(0)
                        if self.houban_material_all is True:
                            self.houban_material_all_time.pop(0)
                            self.houban_material_all_time.append(1)
                        if self.houban_material_all is False:
                            self.houban_material_all_time.pop(0)
                            self.houban_material_all_time.append(0)

                        houban_material_all_sum = sum(self.houban_material_all_time)

                        if self.houban_material_all_judge is False and houban_material_all_sum > 8:
                            houban_material_all_start = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                            # print('houban_material_all_start', houban_material_all_start)
                            self.displayMessage('工人开始换料')  # 材料切换
                            self.da.insert_action_("MaterialChange", 0)
                            self.houban_material_all_judge = True
                            self.putTextStart_time = time.time()

                        if self.houban_material_all_judge is True and houban_material_all_sum <= 2:
                            houban_material_all_stop = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                            # print('houban_material_all_stop', houban_material_all_stop)
                            self.displayMessage('工人完成换料')
                            self.da.insert_action_("MaterialChange", 1)
                            self.da.update_loss_("action1", 1)
                            self.houban_material_all_judge = False

                    houban_material_time_sum = sum(self.houban_material_time)
                    if self.houban_material_judge is False and houban_material_time_sum > 6:
                        houban_material_start = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        # print('houban_material_start', houban_material_start)
                        # self.displayMessage('工人开始换料' )
                        self.houban_material_judge = True

                    if self.houban_material_judge is True and houban_material_time_sum <= 4:
                        houban_material_stop = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        # print('houban_material_stop', houban_material_stop)
                        # self.displayMessage('工人完成换料' )

                        self.houban_material_judge = False

                self.houban_material_backgrond = frame

            M5000_work_time_sum = sum(self.M5000_work_time)
            if self.M5000_work_start_judge is False and M5000_work_time_sum > 8:
                self.M5000_work_start_judge = True
                self.da.insert_action_("M5000Work", 0)
                self.displayMessage('M5000开始工作')
                self.putTextStart_time = time.time()

            if self.M5000_work_start_judge is True and M5000_work_time_sum <= 4:
                self.displayMessage('M5000停止工作')
                self.da.insert_action_("M5000work", 1)
                self.da.update_loss_("action4", 1)
                self.M5000_work_start_judge = False
        self.M5000_work_background = frame

    def data_read(self):
        pass

    def displayMessage(self, message):
        current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.ui.textBrowser.append("[" + current_time + "]" + message)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_app = XioAll()
    app.setQuitOnLastWindowClosed(True)
    main_app.show()
    sys.exit(app.exec_())
