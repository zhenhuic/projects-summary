import cv2

#img=cv2.imread('../pictures/fixM5000base.png')
img=cv2.imread('../pictures/173nightOriginal.png')

img1 = cv2.resize(img,(1280,720))

img_roi=img1[200: 300, 500: 750]


cv2.imshow('roi',img_roi)
cv2.waitKey(0)