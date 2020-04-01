import cv2 as cv
import numpy as np


def threshold_judgement(image, threshold):  # 阈值判断,若np.sum大于阈值则判断通过
    diff_sum = np.sum(image)
    print(diff_sum)
    if diff_sum > threshold:
        return 1
    else:
        return 0


# def time_stop(time):

