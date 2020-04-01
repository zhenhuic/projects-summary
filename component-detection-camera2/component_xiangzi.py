import cv2 as cv
import numpy as np


def nextrace_object_demo(frame):
    '''
    在图片上只留下指定的一种颜色(黄色)
    :param frame: 视频中的一帧
    :return: 处理后的只留下一种颜色的图片
    '''
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # 转换色彩空间为hsv

    lower_hsv = np.array([15, 163, 30])  # 设置过滤的颜色的低值
    upper_hsv = np.array([55, 255, 175])  # 设置过滤的颜色的高值

    #lower_hsv = np.array([15, 200, 30])  # 设置过滤的颜色的低值
    #upper_hsv = np.array([55, 255, 175])  # 设置过滤的颜色的高值
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)  # 调节图像颜色信息（H）、饱和度（S）、亮度（V）区间，选择白色区域
    mask = cv.bitwise_and(frame, frame, mask=mask)

    return mask


def xiangzi_detect(frame, mask_lvtong):
    #print(type(frame))
    mask_lvtong = cv.cvtColor(mask_lvtong, cv.COLOR_BGR2GRAY)
    img = cv.bitwise_and(frame, frame, mask=mask_lvtong)
    #cv.imshow("image", img)
    img = nextrace_object_demo(img)  # 调用上面的函数来提取绿色部分

    #cv.imshow("xiangzi", img)
    num_xiangzi = np.sum(img)
    #if num_xiangzi > 1000000:
        #print(num_xiangzi)
    return num_xiangzi


if __name__ == '__main__':
    mask = cv.imread('mask/mask_xiangzi.jpg')
    image = cv.imread('mask/test2.jpg')
    #xiangzi_detect(image, mask)

    capture = cv.VideoCapture("D:/laoban/2019-10-313.mp4")
    while True:
        ret, frame = capture.read()
        xiangzi_detect(frame, mask)
        cv.waitKey(0)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break



