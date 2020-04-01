import cv2
import numpy as np


cap=cv2.VideoCapture('../videos/fixM5000_2.mp4')
background_mask_roi = None
es=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,4))
while (True):
    ret,frame = cap.read()
    frame = cv2.resize(frame,(1280,720))
    lower = np.array([100, 43, 46])
    upper = np.array([124, 255, 255])
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])

    if background_mask_roi is not None:
        frame_roi = frame[200:400,900:1100]
        background_hsv = cv2.cvtColor(frame_roi,cv2.COLOR_BGR2HSV)
        background_hsv = cv2.GaussianBlur(background_hsv,(21,21),0)
        background_roi = cv2.inRange(background_hsv,lower,upper)
        #background_mask_roi = background_mask[300:700,1350:1700]

        background_mask_roi = background_mask_roi[200:400, 900:1100]
        hsv=cv2.cvtColor(background_mask_roi,cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv,(21,21),0)
        mask_roi = cv2.inRange(hsv, lower, upper)
        #mask_roi = mask[300:700,1350:1700]

        diff = cv2.absdiff(background_roi, mask_roi)
        diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff, es, iterations=2)
        diff_sum = np.sum(diff)
        print(diff_sum)
        #res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('frame', frame)
        cv2.imshow('frame_roi',frame_roi)
        cv2.imshow('mask', mask_roi)
        cv2.imshow('diff', diff)
        cv2.waitKey(10)
    background_mask_roi = frame


cv2.destroyAllWindows()
cap.release()
