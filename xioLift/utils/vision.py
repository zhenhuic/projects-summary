import cv2
import numpy as np


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


def find_spark_left(img_gam, spark_roi):
    '''
    在固定区域检测火花
    :param img:
    :param spark_roi: 这个参数为一个不规则mask，二值图
    :return:
    '''
    hsv = cv2.cvtColor(img_gam, cv2.COLOR_BGR2HSV)

    # 火花颜色
    lower = np.array([0, 0, 250])
    upper = np.array([360, 10, 255])
    mask = cv2.inRange(hsv, lower, upper)
    # res_1 = cv2.bitwise_and(hsv,hsv,mask=mask) # hsv颜色选取火花颜色
    res = cv2.bitwise_and(mask, mask, mask=spark_roi)  # 在该区域检索
    num_res = res / 255
    s = np.sum(num_res)
    # print(s)
    if s > 1000:  # 实验得出左边焊接点700是个阈值
        return True
    return False


def find_spark_right(img_gam, spark_roi):
    return find_spark_left(img_gam, spark_roi)


def classify(source_image, compare_image, threshold_1, threshold_2):
    '''
    比较两幅图的相似度
    :param source_image: 基图, 灰度图
    :param compare_image: 随时待比较的图，灰度图
    :param threshold_1: 阈值1, 划定相似点质量
    :param threshold_2: 阈值2， 达到质量的相似点个数
    :return:
    '''
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(source_image, None)
    kp2, des2 = orb.detectAndCompute(compare_image, None)

    if des2 is None:  # 待比较的图比较单一，没有特征，显然与基图不相似
        return False

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # 暴力匹配
    matches = bf.match(des1, des2)
    matches = list(filter(lambda x: x.distance < threshold_1, matches))  # 过滤不合格的相似点
    # print(len(matches))
    if len(matches) > threshold_2:
        return True
    else:
        return False


class Vision():
    def __init__(self):
        self.machine_back = cv2.imread('./images/machine_back.jpg', 0)  # 机器一般静止图，后向
        self.machine_forward = cv2.imread('./images/machine_forward.jpg', 0)
        self.mb_loc = (80, 250, 470, 590)  # 机器一般静止位置，后向，这里可以改成切片模式
        self.mf_loc = (180, 420, 600, 810)

        self.people_back = cv2.imread('./images/people_back.jpg', 0)
        self.people_forward = cv2.imread('./images/people_forward.jpg', 0)
        self.pb_loc = (130, 260, 610, 690)
        self.pf_loc = (250, 420, 800, 900)

        self.mask_left = cv2.imread('./images/mask_1.jpg', 0)
        self.mask_right = cv2.imread('./images/mask_2.jpg', 0)

    def find_spark(self, img):
        img_gam = gamma_trans(img, 0.75)  # 光照归一化
        return find_spark_left(img_gam, self.mask_left) or find_spark_right(img_gam, self.mask_right)

    def judge_people(self, framegray):
        '''
        判断工人是否处于调试位置
        :param framegray: 原始帧的灰度图
        :return:
        '''

        def judge_people_back_similar(roi):  # 工人处于后向
            return classify(self.people_back, roi, 80, 15)

        def judge_people_forward_similar(roi):
            return classify(self.people_forward, roi, 70, 25)

        pb_roi = framegray[self.pb_loc[0]:self.pb_loc[1], self.pb_loc[2]:self.pb_loc[3]]
        pf_roi = framegray[self.pf_loc[0]:self.pf_loc[1], self.pf_loc[2]:self.pf_loc[3]]
        # cv2.imshow('1', pf_roi)
        pb_flag = judge_people_back_similar(pb_roi)
        pf_flag = judge_people_forward_similar(pf_roi)
        if pb_flag is True:
            # print('工人处于后向')
            pass
        if pf_flag is True:
            # print('工人处于前向')
            pass
        return pb_flag or pf_flag

    def judge_machine_static(self, framegray):
        '''
        判断机器是否在一般静止位置
        :param framegray: 原始帧的灰度图
        :return:
        '''

        def judge_machine_back_similar(roi):  # 机器处于后向
            return classify(self.machine_back, roi, 50, 80)

        def judge_machine_forward_similar(roi):  # 机器处于前向
            return classify(self.machine_back, roi, 65, 50)

        mb_roi = framegray[self.mb_loc[0]:self.mb_loc[1], self.mb_loc[2]:self.mb_loc[3]]
        mf_roi = framegray[self.mf_loc[0]:self.mf_loc[1], self.mf_loc[2]:self.mf_loc[3]]
        # cv2.imshow('1', mf_roi)
        mb_flag = judge_machine_back_similar(mb_roi)
        mf_flag = judge_machine_forward_similar(mf_roi)
        if mb_flag is True:
            # print('机器处于后向')
            pass
        if mf_flag is True:
            # print('机器处于前向')
            pass
        return mb_flag or mf_flag

    def tiaoshi(self, framegray):
        machine_tiaoshi_static = self.judge_machine_static(framegray)  # 机器调试位置静止
        people_tiaoshi_static = self.judge_people(framegray)

        if machine_tiaoshi_static and people_tiaoshi_static:
            return True
        else:
            return False


def featrue_detection(frame, compare_image, threshold_1, threshold_2, a, b, i, j):
    frame = frame[a:b, i:j]
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    compare_image = compare_image[a:b, i:j]
    compare_image_gray = cv2.cvtColor(compare_image, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(frame_gray, None)
    kp2, des2 = orb.detectAndCompute(compare_image_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = list(filter(lambda x: x.distance < threshold_1, matches))  # 过滤不合格的相似点

    if len(matches) > threshold_2:
        return False
    else:
        return True


def lines_diff(frame, frame2, frame3, a, b, i, j):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    frame = cv2.resize(frame, (1280, 720))
    frame2 = cv2.resize(frame2, (1280, 720))
    frame3 = cv2.resize(frame3, (1280, 720))

    frame = frame[a:b, i:j]
    frame2 = frame2[a:b, i:j]
    frame3 = frame3[a:b, i:j]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

    d = cv2.absdiff(gray1, gray)
    d2 = cv2.absdiff(gray2, gray1)

    blur1 = cv2.GaussianBlur(d, (5, 5), 0)
    blur2 = cv2.GaussianBlur(d2, (5, 5), 0)

    _, th = cv2.threshold(blur1, 10, 255, cv2.THRESH_BINARY)
    _, th1 = cv2.threshold(blur2, 10, 255, cv2.THRESH_BINARY)

    # bitwise_and是对二进制数据进行“与”操作，即对图像（灰度图像或彩色图像均可）每个像素值进行二进制“与”操作，1 & 1 = 1，1 & 0 = 0，0 & 1 = 0，0 & 0 = 0
    gra = cv2.bitwise_and(th, th1)
    # 基本思想是用像素点邻域灰度值的中值来代替该像素点的灰度值，让周围的像素值接近真实的值从而消除孤立的噪声点
    segmetation = cv2.medianBlur(gra, 5)
    # 闭运算：先膨胀，再腐蚀，可清除小黑点
    opening = cv2.morphologyEx(segmetation, cv2.MORPH_CLOSE, kernel)

    lines = cv2.HoughLinesP(opening, 50, np.pi / 180, 10, minLineLength=100, maxLineGap=5)
    if lines is None:
        return lines, False

    else:
        return lines, True


def background_diff(frame, a, b, i, j):
    '''
    生产背景图
    :param frame: 循环第一帧
    :return: 背景图的感兴趣区域
    '''
    background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    background = cv2.GaussianBlur(background, (21, 21), 0)
    background_roi = background[a:b, i:j]
    return background_roi


def diff(frame, background_roi, threshold_1, a, b, i, j):
    '''
    帧间差分
    :param background_roi: 循环第一帧
    :param threshold_1: 阈值
    :return: True：识别到该动作；FALSE：未识别到动作
    '''
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    gray_frame_roi = gray_frame[a:b, i:j]

    diff = cv2.absdiff(background_roi, gray_frame_roi)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)
    diff_sum = np.sum(diff)

    if diff_sum > threshold_1:
        return True

    else:
        return False


if __name__ == '__main__':
    # v = Vision()
    # cap = cv2.VideoCapture('/Users/kaimingcheng/PycharmProjects/xiaowork/maindo/videos/left_cam.mp4')
    # while (1):
    #     # Take each frame
    #     _, img = cap.read()
    #
    #     print(v.find_spark(img))

    v = Vision()
    cap = cv2.VideoCapture('./videos/testback.mp4')
    while (1):
        _, img = cap.read()
        cv2.imshow('', img)
        cv2.waitKey(25)
        framegray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if v.tiaoshi(framegray):
            print('tiaoshi')
