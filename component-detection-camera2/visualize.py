import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#from utils.utils import plot_one_box
#from configs.config import max_object_bbox_area_dict,\
    #min_object_bbox_area_dict


def calc_fps(start_time, accum_time, curr_fps, show_fps):
    curr_time = time.time()
    exec_time = curr_time - start_time
    accum_time += exec_time
    curr_fps += 1
    if accum_time > 1:
        accum_time = accum_time - 1
        show_fps = "FPS: " + str(curr_fps)
        curr_fps = 0
    return curr_time, accum_time, curr_fps, show_fps


class Visualize:

    @staticmethod
    def draw_fps(img_array, show_fps):
        img_array = cv2.putText(img_array, text=show_fps, org=(2, 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.2, color=(255, 200, 0), thickness=1)
        return img_array

    @staticmethod
    def draw_Chinese_words(img_array, contents, coord, color):
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_array)

        # PIL图片上打印汉字
        draw = ImageDraw.Draw(img)  # 图片上打印
        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")
        draw.text(coord, contents, color, font=font)

        # PIL 图片转 cv2 图片
        img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_array

    def draw(self, img, flage_component1, flage_component2, fps):
        #print(fps)
        #img = self.draw_fps(img, fps)
        img = cv2.putText(img, text=fps, org=(100, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale =1, color=(255, 200, 0), thickness=2)
        if flage_component1 == 1:
            img = cv2.putText(img, text='buket get', org=(1000, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=1.2, color=(255, 255, 0), thickness=2)
        if flage_component2 == 1:
            img = cv2.putText(img, text='box get', org=(1000, 58), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=1.2, color=(0, 255, 0), thickness=2)
        if flage_component1 == -1 and flage_component2 == -1:
            img = cv2.putText(img, text='packing  failed', org=(1000, 91), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=1.2, color=(0, 0, 255), thickness=2)
        return img
