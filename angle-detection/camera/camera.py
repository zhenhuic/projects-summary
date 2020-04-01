import ctypes
import datetime
import time
import random
import pandas as pd

from dete_algs.angle_detection_LSD import AngleDetectionLSD
from data_info.opc_product_info import ProductInfo
from data_info.database import SqlServer, MySql
from utils.utils import correct_angle


class Camera:
    """
    负责初始化相机、聚焦、拍照
    """

    def __init__(self):
        self.dll = ctypes.cdll.LoadLibrary("camera/Dll20180426.dll")
        self.zoomfocus = pd.read_csv("zoomfocus.csv")
        self.camera = ctypes.cdll.LoadLibrary("camera/dll2.dll")
        deviceCount = self.camera.getDeviceCount()
        if deviceCount == 0:
            print("找不到相机")
            exit()
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.connect(("127.0.0.1", 40000))
        # self.s.setblocking(0)
        # first param device id; second trigger mode
        # 初始相机具体参数看dll代码，第一个是设备id（相机编号从0开始），
        # 第二是触发模式（软触发为0，硬触发为1）

        self.camera.initDevice(0, 1)
        self.camera.setExposure(4000)  # 设置曝光率
        self.camera.setIris(400)  # 设置增益
        self.camera.delayTime(500)  # 延迟拍照单位毫秒
        self.camera.GPIn(1)  # 设置输入电平
        self.camera.GPOut(0)  # 设置输出电平
        self.pictureNum = 0
        self.triggerNum = 0
        self.zoom = None
        self.focus = None
        self.final_angle = 89.32
        self.opc = ProductInfo()  # 初始化OPC server连接，用于下面方法中获取工件信息

    def get_product_info(self):
        """
        获取工件的id, 长度，宽度， 高度(通过OPC)
        :return:
        """
        product_info = self.opc.get_product_info()
        return product_info

    def zoom_focus(self, length):
        distance = int((1500 - length / 2) // 10 * 10)
        zoom = int(self.zoomfocus.query("distance ==  " + str(distance)).values[0][4])
        focus = int(self.zoomfocus.query("distance ==  " + str(distance)).values[0][3])
        return (zoom, focus)

    def take_picture(self):
        """
        1. 获取工件长度
        2. 等待拍照
        3. 拍照检测
        4. 检测结果保存在数据库(数据库分为两个部分：mysql(我们自己的数据库)和sql server(楼上用来展示的数据))
        5. 一轮结束重新开始步骤 1-4
        :return:
            一个包括照片、图片路径、最终检测角度、工件信息的元组
            (images,filePath, final_angle, product_id, product_length, product_wide, product_high)
        """
        print("Waiting for the picture...")
        Tries = 5000
        while self.camera.getImageReceived() == 0:
            Tries = Tries - 1
            if Tries == 0:
                # print(camera.getImageReceived())
                Tries = 200

            time.sleep(0.01)

        length = 1612

        try:
            product_id, product_length, product_wide, product_high = self.get_product_info()

            if product_length is not None:
                if length != product_length and product_length != 0.0:
                    length = product_length
                    print("从工单获取长度 " + str(length))
                    zoom, focus = self.zoom_focus(length)
                else:
                    print("从本地获取长度 " + str(length))
                    zoom, focus = self.zoom_focus(length)
            else:
                length = 1612
                zoom, focus = self.zoom_focus(length)
                product_id = 404
                product_length = 404
                product_wide = 404
                product_high = 404

        except:

            length = 1612
            zoom, focus = self.zoom_focus(length)
            product_id = 404
            product_length = 404
            product_wide = 404
            product_high = 404
        if zoom is not None and focus is not None:
            self.camera.setZoom(zoom)
            self.camera.setFocus(focus)
            # print("zoom", zoom, "focus", focus)

        if self.camera.getImageReceived() == 1:
            nowtime = datetime.datetime.now().strftime("%H_%M_%S")
            picture_date = time.strftime("%Y_%m_%d")
            path = "images/records"
            # if os.path.exists(path) == False:
            #     os.chdir('images')
            #     os.mkdir(str(1))
            filePath = path + "/" + str(picture_date) + "_" + str(nowtime) + ".jpg"
            self.camera.saveImage(bytes(filePath, encoding="utf-8"))
            angle_lsd = AngleDetectionLSD()
            image, final_angle = angle_lsd.detect_lsd(filePath)
            # self.s.send(self.send_angle(angle=final_angle))
            time.sleep(3)
            self.camera.setImageReceived(0)
        else:
            time.sleep(1)

        final_angle = correct_angle(final_angle)  # correct!! TODO

        # 新的工件信息更新后，把工件信息存储到SQL Server 和 MySQL
        sqlserver = SqlServer()
        sqlserver.add_data_into_db(final_angle)

        mysql = MySql()
        mysql.add_data_into_db(product_length, filePath, final_angle)
        print("Taken, Detected, Saved.")
        return image, filePath, final_angle, product_id, product_length, product_wide, product_high

    def camera_close(self):
        self.camera.close()
