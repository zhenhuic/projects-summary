import cv2
import numpy as np


def main():
    count = 0
    i = 0
    j = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cap = cv2.VideoCapture('blacktuo.mp4')

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    ret, frame3 = cap.read()

    frameInfo = frame1.shape()
    height = frameInfo[0]
    width = frameInfo[1]
    frame1 = cv2.resize(frame1, (int(width / 2), int(height / 2)))

    frameInfo = frame2.shape()
    height = frameInfo[0]
    width = frameInfo[1]
    frame2 = cv2.resize(frame2, (int(width / 2), int(height / 2)))

    frameInfo = frame3.shape()
    height = frameInfo[0]
    width = frameInfo[1]
    frame3 = cv2.resize(frame3, (int(width / 2), int(height / 2)))

    while ret:
        i += 1

        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

        # grey = cv2.equalizeHist(gray)
        # grey1 = cv2.equalizeHist(gray1)

        d = cv2.absdiff(gray1, gray)
        d2 = cv2.absdiff(gray2, gray1)

        blur1 = cv2.GaussianBlur(d, (5, 5), 0)
        blur2 = cv2.GaussianBlur(d2, (5, 5), 0)


        # blur = cv2.GaussianBlur(d, (5, 5), 0)  # 高斯模糊 减少图像噪声和降低细节层次
        #
        # medi = cv2.medianBlur(blur, 3, 0)
        #
        # blur1 = cv2.GaussianBlur(d2, (5, 5), 0)  # 高斯模糊 减少图像噪声和降低细节层次
        #
        # medi1 = cv2.medianBlur(blur1, 3, 0)
        #
        # #deno = cv2.fastNlMeansDenoising(blur, 3, 7, 21)
        #
        ret, th = cv2.threshold(blur1, 10, 255, cv2.THRESH_BINARY)
        ret, th1 = cv2.threshold(blur2, 10, 255, cv2.THRESH_BINARY)
        #
        # dilated = cv2.dilate(th, kernel, iterations=2)  # 膨胀
        #
        # eroded = cv2.erode(dilated, kernel, iterations=2)  # 腐蚀

        gra = cv2.bitwise_and(th, th1)
        segmetation = cv2.medianBlur(gra, 5)
        opening = cv2.morphologyEx(segmetation, cv2.MORPH_CLOSE, kernel)

        img, cnts, h = cv2.findContours(opening.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #cv2.drawContours(frame1, cnts,-1,(0,0,255),3)
        # for c in cnts:
        #     if cv2.contourArea(c) < 2000 or cv2.contourArea(c) > 30000:
        #         continue
        #     (x, y, w, h) = cv2.boundingRect(c)
        #     cv2.rectangle(frame1, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 2)
        #     fram = frame1[y - 1:y + h + 1, x - 1:x + w + 1]
        #     cv2.imwrite('img/hha' + str(i) + '.png', fram)

        lines = cv2.HoughLinesP(opening, 50, np.pi / 180, 10, minLineLength=100, maxLineGap=1)
        if lines is None:
            if i + j - count <= 300 and count != 0:
                count += 1
                j += 1
        else:
            count += 1
            j = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame1, (x1, y1), (x2, y2), (255, 0, 0), 2)
        #cv2.imwrite('img/' + str(i) + '.png', frame1)
        cv2.imshow('frame', frame1)
        #cv2.imshow('eroded', eroded)
        # cv2.imshow('blur', blur)
        # cv2.imshow('gray', gray)
        cv2.imshow('opening', opening)

        if cv2.waitKey(25) == 27:  # exit on ESC
            break

        frame1 = frame2
        frame2 = frame3
        ret, frame3 = cap.read()
        if not ret:
            break
        frameInfo = frame3.shape
        height = frameInfo[0]
        width = frameInfo[1]
        frame3 = cv2.resize(frame3, (int(width / 2), int(height / 2)))
    print(count)
    print(i)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()