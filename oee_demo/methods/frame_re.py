import cv2
import numpy as np

frame = cv2.imread('../pictures/ppebDayOriginal.png')

frame_re = cv2.resize(frame,(1280,720))

cv2.imshow('img1',frame)
print(np.shape(frame_re))
cv2.imshow('img',frame_re)
cv2.waitKey(0)

