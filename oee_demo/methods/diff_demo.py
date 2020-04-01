import cv2
import sys
import numpy as np


cap = cv2.VideoCapture('../videos/mach.avi')
fourcc = cv2.VideoWriter_fourcc(*"MPEG")
out1 = cv2.VideoWriter('./output2.mp4', fourcc,10,(640,480))
out2 = cv2.VideoWriter('./output1.mp4', fourcc,10,(640,480))
background_roi = None
last_frame = None
while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(1280,720))
    if last_frame is not None:
        last_frame_gray = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
        last_frame_gray = cv2.GaussianBlur(last_frame_gray, (21, 21), 0)
        last_frame_roi = last_frame_gray[0:100,600:910]
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray,(21,21),0)
        frame_roi = frame_gray[0:100,600:910]

        if background_roi is None:
            background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            background = cv2.resize(background, (1280, 720))
            background = cv2.GaussianBlur(background,(21,21),0)
            background_roi = background[0:100,600:910]

        diff = cv2.absdiff(last_frame_roi,frame_roi)
        diff = cv2.threshold(diff,25,255,cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff,es,iterations=2)
        diff_sum = np.sum(diff)
        print(diff_sum)
        a = out1.write(diff)
        b = out2.write(frame_roi)
        cv2.imshow('diff', diff)
        cv2.imshow('frame', frame)
        cv2.imshow('roi', frame_roi)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    last_frame = frame

    # cv2.imshow('diff',diff)
    # cv2.imshow('frame',frame)
    # cv2.imshow('roi',frame_roi)
    # cv2.waitKey(25)

cv2.destroyAllWindows()
cap.release()