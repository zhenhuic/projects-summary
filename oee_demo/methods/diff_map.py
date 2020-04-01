import cv2
import numpy as np

cap = cv2.VideoCapture('../videos/fixM5000.mp4')
background_roi = None
# img1 = cv2.imread('../pictures/ppeb_work-0002.png')
# background = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# background = cv2.GaussianBlur(background,(21,21),0)
# background_roi = background[400:500,380:450]
#ret,frame = cap.read()
while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(1280,720))

    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray,(21,21),0)
    frame_roi = frame_gray[300:720,400:1280]

    # pre_img = frame_roi

    # ret2,frame2 = cap.read()
    # frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)
    # frame2_roi = frame2_gray[400:500, 380:450]

    if background_roi is None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.resize(background, (1280, 720))
        background = cv2.GaussianBlur(background,(21,21),0)
        background_roi = background[300:720,400:1280]


    diff = cv2.absdiff(background_roi,frame_roi)
    diff = cv2.threshold(diff,25,255,cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff,es,iterations=2)
    diff_sum = np.sum(diff)
    print(diff_sum)

    cv2.imshow('diff',diff)
    cv2.imshow('frame',frame)
    cv2.imshow('roi',frame_roi)
    # cv2.imshow('roi2',frame2_roi)
    cv2.waitKey(25)

cv2.destroyAllWindows()
cap.release()

