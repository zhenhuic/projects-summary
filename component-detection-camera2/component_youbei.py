import cv2 as cv
import numpy as np


def nextrace_object_demo(frame):
    '''
    在图片上只留下指定的一种颜色(绿色)
    :param frame: 视频中的一帧
    :return: 处理后的只留下一种颜色的图片
    '''
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # 转换色彩空间为hsv
    lower_hsv = np.array([50, 40, 20])  # 设置过滤的颜色的低值
    upper_hsv = np.array([78, 70, 55])  # 设置过滤的颜色的高值

    # lower_hsv = np.array([50, 40, 20])  # 设置过滤的颜色的低值
    # upper_hsv = np.array([78, 70, 70])  # 设置过滤的颜色的高值
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)  # 调节图像颜色信息（H）、饱和度（S）、亮度（V）区间，选择白色区域
    mask = cv.bitwise_and(frame, frame, mask=mask)

    return mask


def youbei_detect(frame, mask_lvtong):
    mask_lvtong = cv.cvtColor(mask_lvtong, cv.COLOR_BGR2GRAY)
    img = cv.bitwise_and(frame, frame, mask=mask_lvtong)
    #cv.imshow("image", img)
    img = nextrace_object_demo(img)  # 调用上面的函数来提取绿色部分

    #cv.imshow("img", img)
    num_lvtong = np.sum(img)
    #print(num_lvtong)
    return num_lvtong


if __name__ == '__main__':
    mask = cv.imread('mask/mask_youbei.jpg')
    image = cv.imread('mask/test5.jpg')
    # youbei_detect(image, mask)



    capture = cv.VideoCapture("D:/laoban/2019-09-19.mp4")
    while True:
        ret, frame = capture.read()
        youbei_detect(frame, mask)
        cv.waitKey(0)
