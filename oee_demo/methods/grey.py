import cv2

img = cv2.imread('../pictures/blacktuo1.png',cv2.COLOR_BGR2GRAY)

cv2.imshow('img',img)
cv2.waitKey(0)