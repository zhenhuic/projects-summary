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
    def __init__(self, start_x=950, mid_x=1337, end_x=1910, start_y=700, end_y=1215):
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

    def lsd(self, img, img_roi_canny, start_x, start_y):
        lsd = cv2.createLineSegmentDetector(0)
        lsd_lines = lsd.detect(img_roi_canny)
        # lsd_lines2d = lsd.detect(img_roi_canny)[0]
        # draw_img = lsd.drawSegments(img, lsd_lines2d)
        cv2.waitKey(0)
        long_line = None
        max_length = -1
        for line in lsd_lines[0]:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            if max_length < ((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)):
                max_length = (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)
                long_line = line
                # cv2.line(img, (x0 + start_x, y0 + start_y), (x1 + start_x, y1 + start_y), (0, 255, 0), 1, cv2.LINE_AA)
                # cv2.imshow("LSD", img)
                # cv2.waitKey(200)
        x0 = int(round(long_line[0][0]))
        y0 = int(round(long_line[0][1]))
        x1 = int(round(long_line[0][2]))
        y1 = int(round(long_line[0][3]))
        # print("x0__y0__x1__y1_______")
        # print(x0, y0, x1, y1)
        radian = math.atan(abs(x0 - x1) * 1.0 / abs(y0 - y1))
        angle = radian * 180 / math.pi
        # print(angle)
        cv2.line(img, (x0 + start_x, y0 + start_y), (x1 + start_x, y1 + start_y),
                 (255, 0, 0), 15, cv2.LINE_AA)
        return img, angle

    def detect_lsd(self, path):
        # 调用函数设置roi区域并且进行canny边缘检测，return边缘检测后的roi区域
        img = cv2.imread(path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_roi_canny_left = self.set_roi_canny(img_gray, self.start_x, self.mid_x,
                                                self.start_y, self.end_y)
        img_roi_canny_right = self.set_roi_canny(img_gray, self.mid_x + 1, self.end_x,
                                                 self.start_y, self.end_y)
        img_left, angle_left = self.lsd(img, img_roi_canny_left, self.start_x, self.start_y)
        img_right, angle_right = self.lsd(img, img_roi_canny_right, self.mid_x + 1, self.start_y)
        res_angle = angle_left + angle_right
        return img, res_angle


# lines = cv2.HoughLines(img_roi_canny, 3, np.pi / 18000, 100)
# roi_copy = img_roi_canny.copy()
# img_copy = img.copy()
# lines2d = lines[:, 0, :]  # 提取为为二维
# lines2d = lines2d[np.lexsort(lines2d[:, ::-1].T)]  # 将数组按照第一列rho的值进行递增排序
# ad = Ad3()
# for rho, theta in lines2d[:]:
#     ad.draw_line(roi_copy, img_copy, rho, theta)


# blurred = cv2.GaussianBlur(img_canny, (3, 3), 0)
# cv2.imshow("GaussianBlur", img_canny)
# plt.imshow(img)
# plt.show()

# cv2.imwrite("images/test_1_gas_1.bmp", blurred)
# cv2.imwrite("images/test_11_canny_70_150.bmp", img_canny)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

if __name__ == "__main__":
    path = "image1/test15.jpg"
    angle_lsd = AngleDetectionLSD()
    img, angle = angle_lsd.detect_lsd(path)
    print(angle)
    plt.imshow(img)
    plt.show()







