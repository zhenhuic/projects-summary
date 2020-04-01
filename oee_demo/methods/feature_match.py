import cv2
import numpy as np
from matplotlib import pyplot as plt

source_image = cv2.imread('../pictures/173dayOriginal.jpg')
source_image = cv2.cvtColor(source_image,cv2.COLOR_BGR2GRAY)
source_image = cv2.resize(source_image,(1280,720))
source_image_roi  = source_image[260:360,500:650]
# compare_image = cv2.imread('../pictures/ppebDayOriginal.png',cv2.IMREAD_GRAYSCALE)
# compare_image_roi = compare_image[350:450,550:660]
cap = cv2.VideoCapture('../videos/mach.avi')
while(True):
    ret,frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    compare_image_roi = frame[260:360,500:650]

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(source_image_roi, None)
    kp2, des2 = orb.detectAndCompute(compare_image_roi, None)

    # if des2 is None:  # 待比较的图比较单一，没有特征，显然与基图不相似
    #    return Fals

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    #print(matches)
    matches = list(filter(lambda x: x.distance < 60, matches))  # 过滤不合格的相似点
    print(len(matches))
    if len(matches) > 10:
         print(True)

    else:
         print(False)

    cv2.imshow('frame',frame)
    cv2.waitKey(25)

    # img3 = cv2.drawMatches(source_image_roi,kp1,compare_image_roi,kp2,matches[0:40],compare_image_roi,flags=2)
    # plt.imshow(img3),plt.show()

cv2.destroyAllWindows()
cap.release()
