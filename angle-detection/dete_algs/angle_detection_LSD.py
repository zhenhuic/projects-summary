# coding=utf-8
# @Time    : 000013/3/13 14:20
# @Author  : KayleZhuang
# @Site    : 
# @File    : angle_detection_LSD.py
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
#               ."" '<  `.___\_<|>_/___.'  >' "".
#              | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#              \  \ `-.   \_ __\ /__ _/   .-` /  /
#         ======`-.____`-.___\_____/___.-`____.-'======
#                            `=---='
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      Buddha Bless, No Bug !

import cv2
import matplotlib.pyplot as plt
import math


class AngleDetectionLSD:
    """
    利用LSD直线检测算法简介工件角度
    """

    def __init__(self, start_x=800, mid_x=1337, end_x=1910, start_y=700, end_y=1715):   #1215
        # img_gray = img
        self.start_x = start_x
        self.end_x = end_x

        self.mid_x = mid_x

        self.start_y = start_y
        self.end_y = end_y

    def set_roi_canny(self, img_gray, start_x, end_x, start_y, end_y, canny_low=50, canny_high=150):
        img_roi = img_gray[start_y: end_y, start_x: end_x]
        # 自己设置阈值为80
        # ret1, img_thd = cv2.threshold(img_roi, 80, 255, cv2.THRESH_BINARY)
        # 自适应阈值
        ret2, img_thd = cv2.threshold(img_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # img_roi_canny = cv2.Canny(img_roi, canny_low, canny_high, apertureSize=3)
        img_roi_canny = cv2.Canny(img_thd, 50, 150, apertureSize=3)
        return img_roi_canny

    def angle_correct(self, angle):
        # correct_angle = (angle - 89.5) * 0.1 + 89.5
        correct_angle = angle
        return correct_angle

    def extend_line(self, img, x0, y0, x1, y1):
        """
        延长检测出的直线，以便展示在界面上
        :param img:
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :return:
            延长后的线段，两点的坐标保存在一个元组中
            (point_res[0][0], point_res[0][1], point_res[1][0], point_res[1][1])
        """
        img_height = img.shape[0]
        img_width = img.shape[1]
        point_res = [[-1, -1],[-1, -1]]
        index = 0

        y_left = int((y0 - y1) * (0 - x1) * 1.0 / (x0 - x1) + y1)
        y_right = int((y0 - y1) * (img_width - x1) * 1.0 / (x0 - x1) + y1)
        x_top = int((x0 - x1) * (0 - y1) * 1.0 / (y0 - y1) + x1)
        x_down = int((x0 - x1) * (img_height - y1) * 1.0 / (y0 - y1) + x1)

        if 0 <= y_left <= img_height and index < 2:
            point_res[index] = [0, y_left]
            index += 1

        if 0 <= y_right <= img_height  and index < 2:
            point_res[index] = [img_width, y_right]
            index += 1

        if 0 <= x_top <= img_width and index < 2:
            point_res[index] = [x_top, 0]
            index += 1

        if 0 <= x_down <= img_width and index < 2:
            point_res[index] = [x_down, img_height]
            index += 1

        return point_res[0][0], point_res[0][1], point_res[1][0], point_res[1][1]

    def method_lsd(self, img, img_roi_canny, start_x, start_y):
        lsd = cv2.createLineSegmentDetector(0)
        lsd_lines = lsd.detect(img_roi_canny)
        # lsd_lines2d = lsd.detect(img_roi_canny)[0]
        # draw_img = lsd.drawSegments(img, lsd_lines2d)
        # cv2.waitKey(0)
        long_line = None
        max_length = -1
        slope = 0
        angle = 0
        for line in lsd_lines[0]:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            if y0 != y1 and x1 != x0:
                radian = math.atan(abs(x0 - x1) * 1.0 / abs(y0 - y1))
                angle = radian * 180 / math.pi
                slope = (y1 - y0) * 1.0 / (x1 - x0)
            if max_length < ((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)):
                    # 这个角度范围约束条件启用有时候会导致检测不到符合条件的边
                    # and (42 < angle < 48)\
                    # and ((start_x < 1300 and slope > 0) or (start_x > 1300 and slope < 0)):
                    
                    if (start_x < self.mid_x and slope < 0) or (start_x > self.mid_x and slope > 0) or angle < 30 or angle > 55:
                        continue
                    
                    max_length = (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)
                    long_line = line
                # cv2.line(img, (x0 + start_x, y0 + start_y), (x1 + start_x, y1 + start_y), (0, 255, 0), 1, cv2.LINE_AA)
                # cv2.imshow("LSD", img)
                # cv2.waitKey(200)
            
        x0 = int(round(long_line[0][0]))
        y0 = int(round(long_line[0][1]))
        x1 = int(round(long_line[0][2]))
        y1 = int(round(long_line[0][3]))
        #print(x0, y0, x1, y1)

        radian = math.atan(abs(x0 - x1) * 1.0 / abs(y0 - y1))
        angle = radian * 180 / math.pi
        x0, y0, x1, y1 = self.extend_line(img_roi_canny, x0, y0, x1, y1)
        # print("x0__y0__x1__y1_______")
        # print(x0, y0, x1, y1)
        # print(angle)
        # print("--------------")
        cv2.line(img, (x0 + start_x, y0 + start_y), (x1 + start_x, y1 + start_y),
                 (0, 255, 0), 10, cv2.LINE_AA)
        return img, angle

    def detect_lsd(self, path):
        """
        调用函数设置roi区域并且进行canny边缘检测
        :param path:
        :return: 边缘检测后的roi区域
        """
        img = cv2.imread(path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_roi_canny_left = self.set_roi_canny(img_gray, self.start_x, self.mid_x,
                                                self.start_y, self.end_y)
        img_roi_canny_right = self.set_roi_canny(img_gray, self.mid_x + 1, self.end_x,
                                                 self.start_y, self.end_y)
        img_left, angle_left = self.method_lsd(img, img_roi_canny_left, self.start_x, self.start_y)
        img_right, angle_right = self.method_lsd(img, img_roi_canny_right, self.mid_x + 1, self.start_y)
        res_angle = angle_left + angle_right
        # print("res_angle:",res_angle)
        correct_angle = self.angle_correct(res_angle)
        return img, correct_angle


if __name__ == "__main__":
    path = "images/1/2019_02_26_18_04_27.jpg"
    # path = "blur_images/img_1/1_blur.jpg"
    angle_lsd = AngleDetectionLSD()
    img, angle = angle_lsd.detect_lsd(path)
    print(angle)
    plt.imshow(img)
    # 存储启动时图
    # plt.savefig("./demo.jpg")
    plt.show()







