import cv2
import cv2 as cv
import numpy as np


# 将opencv格式的图片格式转换为可以输出到界面的格式
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage


def array_to_QImage(img, size):
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = img_array.shape
    bytes_per_line = ch * w
    qimage = QImage(img_array.data, w, h, bytes_per_line, QImage.Format_RGB888)
    if isinstance(size, QSize):
        qimage = qimage.scaled(size)
    else:
        qimage = qimage.scaled(size[0], size[1])
    return qimage


def threshold_judgement(image, threshold):  # 阈值判断,若np.sum大于阈值则判断通过
    diff_sum = np.sum(image)
    print(diff_sum)
    if diff_sum > threshold:
        return 1
    else:
        return 0


def xiangzi_detect_tracking(frame, mask_lvtong):
    #print(type(frame))
    mask_lvtong = cv.cvtColor(mask_lvtong, cv.COLOR_BGR2GRAY)
    img = cv.bitwise_and(frame, frame, mask=mask_lvtong)
    #cv.imshow("image", img)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # 转换色彩空间为hsv

    lower_hsv = np.array([15, 163, 30])  # 设置过滤的颜色的低值
    upper_hsv = np.array([55, 255, 175])  # 设置过滤的颜色的高值

    mask = cv.inRange(hsv, lower_hsv, upper_hsv)  # 调节图像颜色信息（H）、饱和度（S）、亮度（V）区间，选择白色区域

    mask_track = cv.bitwise_and(img, img, mask=mask)

    #cv.imshow("mask_track", mask_track)

    return mask_track

def box_tracking(image, frame):
    '''
    在二值图中将box找出来，并且在frame中显示出来
    :param image: 二值图
    :param frame: 当前的帧
    :return: 显示box之后的frame
    '''
    cotton = image[:, :, 0]  # 这是二值图像，仅取第一个通道
    # print(cotton.shape)
    # cv2.imshow('cotton', cotton)
    moments = cv.moments(cotton)
    #print(moments)
    cx, cy = moments['m10'] / moments['m00'], moments['m01'] / moments['m00']  # 质心
    # print(cx, cy)
    # 画外接矩形
    # x, y, w, h = cv.boundingRect(cotton)
    # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv.imshow('cotton1', frame)
    cv.rectangle(frame, (int(cx)-55, int(cy)-75), (int(cx)+55, int(cy)+75), (0, 255, 0), 3)
    cv.circle(frame, (int(cx), int(cy)), 8, (0, 0, 255), -1)
    return frame




def lvtong_detect_tracking(frame, mask_lvtong):
    #print(type(frame))
    mask_lvtong = cv.cvtColor(mask_lvtong, cv.COLOR_BGR2GRAY)
    img = cv.bitwise_and(frame, frame, mask=mask_lvtong)
    #cv.imshow("image", img)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # 转换色彩空间为hsv

    lower_hsv = np.array([78, 120, 46])  # 设置过滤的颜色的低值
    upper_hsv = np.array([99, 250, 255])  # 设置过滤的颜色的高值

    mask = cv.inRange(hsv, lower_hsv, upper_hsv)  # 调节图像颜色信息（H）、饱和度（S）、亮度（V）区间，选择白色区域

    mask_track = cv.bitwise_and(img, img, mask=mask)

    #cv.imshow("mask_track", mask_track)

    return mask_track


def bucket_tracking(image, frame):
    '''
    在二值图中将box找出来，并且在frame中显示出来
    :param image: 二值图
    :param frame: 当前的帧
    :return: 显示box之后的frame
    '''
    cotton = image[:, :, 0]  # 这是二值图像，仅取第一个通道
    # print(cotton.shape)
    # cv2.imshow('cotton', cotton)
    moments = cv.moments(cotton)
    # print(moments)
    cx, cy = moments['m10'] / moments['m00'], moments['m01'] / moments['m00']  # 质心
    # print(cx, cy)
    # 画外接矩形
    # x, y, w, h = cv.boundingRect(cotton)
    # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv.imshow('cotton1', frame)
    cv.rectangle(frame, (int(cx)-55, int(cy)-75), (int(cx)+55, int(cy)+75), (255, 0, 0), 3)
    cv.circle(frame, (int(cx), int(cy)), 8, (0, 0, 255), -1)
    return frame

# def time_stop(time):

if __name__ == '__main__':
    mask_xiangzi = cv.imread('mask/mask_xiangzi.jpg')
    #xiangzi_detect(image, mask)
    video_path = "./2019-10-31.mp4"
    capture = cv.VideoCapture(video_path)
    while True:
        ret, frame = capture.read()
        frame_720 = cv.resize(frame, (1280, 720))
        mask_track = xiangzi_detect_tracking(frame_720, mask_xiangzi)
        box_tracking(mask_track, frame_720)


        cv.waitKey(0)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

