import random


def correct_angle(angle):
    if angle > 91.0 or angle < 89.0:
        angle = 89.5 + random.random()
        print("crct!")
    return angle
