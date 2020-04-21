import random
import time
import cv2

# while True:
#     a = round(random.uniform(9.5, 10), 1)
#     print(a)
#     a = round(random.uniform(9.5, 10), 1)
#     print(a)
#     time.sleep(1)

src=cv2.imread('1.jpg')
cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('input_image', src)
cv2.waitKey(0)
cv2.destroyAllWindows()