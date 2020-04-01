import cv2
import numpy as np
from utils import vision

def find_spark_left(img_gam, spark_roi): #已改写，wqw
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
    break_flag=False
    for i in range(100,470,10):
        for j in range(130,1100,15):
            if np.sum(num_res[i:i+50,j:j+50])>700:
                #print(i,j)
                break_flag=True
                break
        if break_flag==True:
            break

    s = np.sum(num_res)

    if s > 700:  # 实验得出左边焊接点700是个阈值
        return True,s,j,i
    else:
        return False,s,0,0


spark_roi_right=cv2.imread('../maindo/images/mask_4.jpg', 0)
spark_roi_left=cv2.imread('../maindo/images/mask_1.jpg',0)
if __name__ == '__main__':
    v =vision.Vision()
    cap = cv2.VideoCapture('E:\\xiaowork\\maindo\\videos\\hello1111.avi')
    while (1):
        _, img = cap.read()
        print(img.shape)
        img_gam = vision.gamma_trans(img, 0.8)
        hsv = cv2.cvtColor(img_gam, cv2.COLOR_BGR2HSV)

        # 火花颜色
        lower = np.array([0, 0, 250])
        upper = np.array([360, 10, 255])
        mask = cv2.inRange(hsv, lower, upper)
        # res_1 = cv2.bitwise_and(hsv,hsv,mask=mask) # hsv颜色选取火花颜色
        res = cv2.bitwise_and(mask, mask, mask=spark_roi_right)  # 在该区域检索
        cv2.imshow("二值化", res)
        ISWOrk,s,X_1,Y_1=find_spark_left(img_gam,spark_roi_right)
        if ISWOrk is True:
            print(s)
            cv2.rectangle(img, (X_1, Y_1), (X_1 + 100, Y_1 + 100), (0, 255, 0), 4)
        else:
            print("未工作时阈值是：",s)

        cv2.imshow('2',img)
        cv2.waitKey(20)
        cap = cv2.VideoCapture('E:\\xiaowork\\maindo\\videos\\hello1111.avi')