import sys
import threading
import cv2
from PyQt4 import QtCore, QtGui
import datetime
import time

from visualize import angle_detection_ui_2
from visualize.angle_plot import Figure_LineChart
from camera.camera import Camera
from utils.timer import Timer


class MainWindow(QtGui.QMainWindow):
    """
    主窗口类，程序入口
    """
    image = None
    angle_array = [89.15, 90.12, 90.2, 89.53, 89.62, 89.63, 90.32, 90.11, 90.42, 90.21]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = angle_detection_ui_2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Run.clicked.connect(self.run_detection_threading)  # 开启一个角度检测的线程
        self.play_pic_threading = Timer('updatePlay()')
        self.connect(self.play_pic_threading, QtCore.SIGNAL('updatePlay()'), self.play_pic)
        self.play_pic_threading.start()

        self.draw_threading = Timer('updatePlay()', 30)
        self.connect(self.draw_threading, QtCore.SIGNAL('updatePlay()'), self.draw)
        self.draw_threading.start()
        # self.cameraObject = Camera()
        # 初始image 为启动demo图片
        self.image = cv2.imread("visualize/demo.jpg")
        self.final_angle = 90.39079700749028
        self.detection_thread_flag = 0
        # self.run_detection_threading()

    def run_detection_draw(self):
        self.run_detection_threading()

    def run_detection_threading(self):
        """
        创建一个用于角度检测的线程
        :return:
        """
        if not self.detection_thread_flag:
            self.thread_detection = threading.Thread(target=self.run_detection)
            self.thread_detection.start()

            self.detection_thread_flag = 1

    def run_detection(self):
        """
        循环运行检测
        :return:
        """
        while True:
            # cameraObject中take_picture()方法只有在拍照后
            img, file_path, final_angle, product_id, product_length, product_wide, product_high = self.cameraObject.take_picture()
            self.image = img
            # img = cv2.imread("image_2018_5_30/139268_2018-05-30-13-47-57.jpg")

            print("角度:", final_angle)
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            recent_time = time.strftime("%H:%M:%S", time.localtime())
            print(date, recent_time)
            print()
            self.final_angle = final_angle
            # self.ui.warning_window.setText("当前工件角度为："+ str(final_angle))

            self.angle_array.append(final_angle)
            # self.play_pic(img) # images of detection
            self.image = img
            # self.draw(angle_array) # top 100 angle list
            # self.thread_figure = Timer('updatePlay()', sleep_time=2)
            # self.connect(self.thread_figure, QtCore.SIGNAL('updatePlay()'), self.draw(angle_array))
            # self.thread_figure.start()

    def draw(self):
        def draw_linechart(y):
            fp = Figure_LineChart()
            fp.plot(y)
            graphicscene_fp = QtGui.QGraphicsScene()
            graphicscene_fp.addWidget(fp.canvas)
            self.ui.graphicsView.setScene(graphicscene_fp)
            self.ui.graphicsView.show()

        draw_linechart(self.angle_array)

    def play_pic(self):
        # img=cv2.imread("image_2018_5_30/139268_2018-05-30-13-47-57.jpg")
        # angle_lsd = AngleDetectionLSD()
        # img, angle = angle_lsd.detect_lsd("image_2018_5_30/139268_2018-05-30-13-47-57.jpg")
        if self.image is not None:
            frame_change = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # change colorspace
            frame_resize = cv2.resize(frame_change, (400, 300), interpolation=cv2.INTER_AREA)
            image = QtGui.QImage(frame_resize.data, frame_resize.shape[1], frame_resize.shape[0],
                                 QtGui.QImage.Format_RGB888)
            self.ui.image_window.setPixmap(QtGui.QPixmap.fromImage(image))
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            font.setWeight(75)
            self.ui.warning_window.setFont(font)
            self.ui.warning_window.setText("当前工件角度为：" + str(self.final_angle))

        # linechart_img = cv2.imread('./test.png')
        # frame_change_2 = cv2.cvtColor(linechart_img, cv2.COLOR_BGR2RGB)  # change colorspace
        # frame_resize_2 = cv2.resize(frame_change_2, (400, 520), interpolation=cv2.INTER_AREA)
        # image_2 = QtGui.QImage(frame_resize_2.data, frame_resize_2.shape[1], frame_resize_2.shape[0],
        #                      QtGui.QImage.Format_RGB888)
        # self.ui.linechart_window.setPixmap(QtGui.QPixmap.fromImage(image_2))

    def draw_linechart(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import random

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
        plt.plot(x1, 89.0 * y_ones, 'c--')  # draw line of y=89.0
        plt.plot(x1, 91.0 * y_ones, 'c--')  # draw line of y=91.0
        plt.plot(x1, 90.0 * y_ones, 'm--')  # draw line of y=90.0
        plt.yticks([88.5, 89.0, 89.5, 90.0, 90.5, 91.0, 91.5])
        plt.title(u'折弯机角度检测')
        axes.spines['top'].set_visible(False)  # 去掉上边框
        axes.spines['bottom'].set_visible(False)  # 去掉下边框
        axes.spines['left'].set_visible(False)  # 去掉左边框
        axes.spines['right'].set_visible(False)  # 去掉右边框

        # plt.ylabel("Angle")

        axes2 = plt.subplot(212)
        plt.plot(x1, y2, 'bo-')
        plt.plot(x1, 0.0 * y_ones, 'c--')
        plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0])
        axes2.spines['top'].set_visible(False)  # 去掉上边框
        axes2.spines['bottom'].set_visible(False)  # 去掉下边框
        axes2.spines['left'].set_visible(False)  # 去掉左边框
        axes2.spines['right'].set_visible(False)  # 去掉右边框

        # plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 80.5],[r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$really\ good$'])
        # plt.plot(x1,y1,'ro-',x2,y2,'g+-',x3,y3,'b^-')
        # plt.title('The Lasers in Three Conditions')
        # plt.xlabel('row')
        # plt.ylabel('column')
        # plt.legend()
        fig = plt.gcf()
        plt.savefig('./test.png')
        # img = cv2.imread('./test.png')
        # cv2.imshow('img', img)
        # cv2.waitKey()
        # plt.show()
        # self.canvas_line.draw()
        # plt.close('all')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # path = "image_2018_5_30/139268_2018-05-30-13-47-57.jpg"
    # angle_lsd = AngleDetectionLSD()
    # img, angle = angle_lsd.detect_lsd(path)
    mainapp = MainWindow()
    app.setQuitOnLastWindowClosed(True)
    mainapp.show()
    sys.exit(app.exec_())
