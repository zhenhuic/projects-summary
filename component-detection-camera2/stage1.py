import cv2 as cv
import numpy as np


def nextrace_object_demo(frame):
    '''
    在图片上只留下指定的一种颜色(油烟机的颜色)
    :param frame: 视频中的一帧
    :return: 处理后的只留下一种颜色的图片
    '''
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # 转换色彩空间为hsv
    lower_hsv = np.array([55, 0, 80])  # 设置过滤的颜色的低值
    upper_hsv = np.array([110, 40, 140])  # 设置过滤的颜色的高值
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)  # 调节图像颜色信息（H）、饱和度（S）、亮度（V）区间，选择白色区域
    mask = cv.bitwise_and(frame, frame, mask=mask)

    return mask


def youyanji_detect(frame, mask_):
    mask_ = cv.cvtColor(mask_, cv.COLOR_BGR2GRAY)
    img = cv.bitwise_and(frame, frame, mask=mask_)
    #cv.imshow("image", img)
    img = nextrace_object_demo(img)  # 调用上面的函数来提取绿色部分

    # cv.imshow("youyanji", img)
    num_youyanji = np.sum(img)
    #if num_youyanji > 20000000:
        #print(num_youyanji)
    return num_youyanji


if __name__ == '__main__':
    mask = cv.imread('mask/mask_flage1.jpg')
    image = cv.imread('mask/test3.jpg')
    # youyanji_detect(image, mask)

    capture = cv.VideoCapture("D:/laoban/2019-09-19.mp4")
    while True:
        ret, frame = capture.read()
        youyanji_detect(frame, mask)
        cv.waitKey(0)


    cv.destroyAllWindows()
