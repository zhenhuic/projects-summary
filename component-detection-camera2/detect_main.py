import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage
import time
from component_lvtong import lvtong_detect
from component_xiangzi import xiangzi_detect
from stage1 import youyanji_detect
from stage2 import paomoban_detect
from stage3 import daxiangzi_detect
from component_youbei import youbei_detect
from config import *
from visualize import *
from util import *
from sql.database import *
from send_email import *

# 将opencv格式的图片格式转换为可以输出到界面的格式
def array_to_QImage(img, size):
    rgbImage = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    h, w, ch = rgbImage.shape
    bytes_per_line = ch * w
    qimage = QImage(rgbImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
    qimage = qimage.scaled(size[0], size[1])
    return qimage


def main(qthread):  # 加入参数qthread，用于pyqt的引用
    # threshold_youyanji = 20000000
    # threshold_paomoban = 8000000
    # threshold_paomoban_down = 2000000
    # threshold_daxiangzi = 45000000
    # threshold_lvotng = 1000000
    # threshold_xiangzi = 1700000  # 有时手可以达到108万（插泡沫板的时候）原来我设置的是120万
    # threshold_xiangzi_1 = 6000000  # 用于规避将最后的打包误检为“将箱子放入”
    # threshold_youyanji_down = 4000000
    put_number = 1
    flag_stage1 = 0
    flag_stage1_1 = 0  # 油烟机下落
    flag_stage2 = 0
    flag_stage2_1 = 0  # 泡沫板下落
    flag_stage3 = 0
    flag_lvtong = 0  # 绿筒放入
    flag_xiangzi = 0  # 箱子放入
    count_stage2_1 = 0
    count_xiangzi = 0
    gui_count = 0
    gui_bucket = 0
    gui_box = 0

    mask_lvtong = cv.imread('mask/mask_lvtong.jpg')
    mask_xiangzi = cv.imread('mask/mask_xiangzi.jpg')
    mask_stage1 = cv.imread('mask/mask_flage1.jpg')
    mask_stage2 = cv.imread('mask/mask_flage2.jpg')
    mask_stage3 = cv.imread('mask/mask_flag3.jpg')

    url = 'rtsp://admin:hdu417417@172.17.2.192:554/Streaming/Channels/201'
    capture = cv.VideoCapture(video_path)

    since = time.time()
    accum_time, curr_fps = 0, 0
    show_fps = 'FPS: ??'

    dbManager = DbManager()
    dbManager.connectDatabase()

    while True:
        ret, frame = capture.read()
        image = cv.resize(frame, (1280, 720))

        # cv.imshow("image", image)

        # 这里是在图片上加上文字的部分（放入零件的时候给一个信号这样子）
        if flag_stage2_1 == 0:
            frame_720 = image



        since, accum_time, curr_fps, show_fps = calc_fps(since, accum_time, curr_fps, show_fps)

        visualize = Visualize()

        if flag_xiangzi == 1:
            if gui_box == 0:
                # 在界面上显示，小包组件拿到
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '小包组件拿到')
                dbManager.record_process(0, 1)
                gui_box = 1
            image = visualize.draw_Chinese_words(image, '小包组件 拿到', (1000, 20), color=(0, 255, 0))
        if flag_lvtong == 1:
            if gui_bucket == 0:
                # 在界面上显示，小包组件拿到
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '风管拿到')
                dbManager.record_process(1, 0)
                gui_bucket = 1
            image = visualize.draw_Chinese_words(image, '风管 拿到', (1000, 58), color=(255, 255, 0))

        # visualize.draw(frame_720, flag_lvtong, flag_xiangzi, show_fps)
        qimage = array_to_QImage(frame_720, (855, 466))
        qthread.video_change_pixmap.emit(qimage)

        frame_720 = image
        paomoban_detect_result = paomoban_detect(frame_720, mask_stage2)  # 泡沫板检测的结果

        if flag_stage2 != 1:
            if youyanji_detect(frame_720, mask_stage1) > threshold_youyanji and flag_stage1 == 0 and flag_stage1_1 == 0:
                flag_stage1 = 1
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '操作行为识别：' + '开始装箱')
                dbManager.zhuagnxiang_sql_and_insert(put_number, 1, 0)


            if flag_stage1 == 1 and youyanji_detect(frame_720, mask_stage1) < threshold_youyanji_down:
                flag_stage1_1 = 1
        # 判断油烟机是否down进箱子里

        if flag_stage1_1 == 1:
            # 判断泡沫板的阈值是否满足，满足则进入stage2
            if paomoban_detect_result > threshold_paomoban:
                flag_stage2 = 1
        # 进入第二阶段_1,判断泡沫板是否down下去
        if flag_stage2 == 1 and flag_stage2_1 == 0 and paomoban_detect_result < threshold_paomoban_down:
            flag_stage2_1 = 1
            count_stage2_1 = 1  # 启动泡沫板二段检测计数器
        # count_stage2_1由于计算泡沫板下落之后过了多少帧
        if count_stage2_1 >= 1:
            # print(count_stage2_1)
            count_stage2_1 += 1

        # 进入第二阶段时开始判断零件的投放情况
        if flag_stage2_1 == 1:
            # 在这里加上两个零件的框框

            xiangzi_detect_result = xiangzi_detect(frame_720, mask_xiangzi)
            lvtong_detect_result = lvtong_detect(frame_720, mask_lvtong)

            if 3000000 > xiangzi_detect_result > 700000:
                mask_track_box = xiangzi_detect_tracking(frame_720, mask_xiangzi)
                frame_720 = box_tracking(mask_track_box, frame_720)

            if lvtong_detect_result > 300000:

                mask_track_bucket = lvtong_detect_tracking(frame_720, mask_lvtong)
                frame_720 = bucket_tracking(mask_track_bucket, frame_720)




            # count_stage += 1  # 时间停止器 count_stage 是时间暂停的帧数
            # 判断大箱子是否盖上，满足条件则发出打包完成的信号，进入第三阶段
            if daxiangzi_detect(frame_720, mask_stage3) > threshold_daxiangzi:
                flag_stage3 = 1
            # if count_stage > 10:
            # 判断零件的检测情况(桶)
            if lvtong_detect_result > threshold_lvotng:
                flag_lvtong = 1
            # 判断零件的检测情况(箱子)

            if xiangzi_detect_result > threshold_xiangzi and flag_xiangzi == 0 and count_xiangzi == 0:
                count_xiangzi = 1
            # 假如在连续的10帧都未检测到有大面积的黄色，那么就视为箱子放入
            if 10 > count_xiangzi >= 1:
                # print(count_xiangzi, xiangzi_detect(frame_720, mask_xiangzi))
                if xiangzi_detect_result < threshold_xiangzi_1:
                    count_xiangzi += 1
                else:
                    count_xiangzi = -1
            if count_xiangzi == 10:
                flag_xiangzi = 1
            if count_xiangzi == -1:
                count_xiangzi = 0

        # 在泡沫板下落之后的的一小段时间里检测满足阈值，则判断这个下落不是真正的下落
        # (这里的一小段时间指的就是满足阈值之后的“count_stage2_1”九帧内)
        if paomoban_detect_result > threshold_paomoban and flag_stage2_1 == 1 and count_stage2_1 < 40:
            flag_stage2_1 = 0
            count_stage2_1 = 1  # 重置泡沫板二段检测计数器
            if count_xiangzi > 0:  # 若在这时检测误检了箱子，count_xiangzi重置为0
                count_xiangzi = 0
            if flag_xiangzi == 1:  # 若在这时检测误检了箱子，将信号flag_xiangzi还原为0
                flag_xiangzi = 0

        if flag_stage3 == 1:
            timestr_image = time.strftime('%Y-%m-%d %H-%M-%S ', time.localtime())  # 冒号不可以出现在文件夹命名里面
            dbManager.zhuagnxiang_sql_and_insert(put_number, 0, 1)
            if flag_lvtong == 1 and flag_xiangzi == 1:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '第' + str(put_number) + '次装箱 零件投放成功')  # 第200次装箱 零件投放成功
                qthread.text_append.emit(timestr + '操作行为识别：' + '结束装箱' + "\n")
                print("投放成功")
            if flag_lvtong == 0 and flag_xiangzi == 1:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '第' + str(put_number) + '次装箱 零件投放失败，漏放绿桶')
                image = cv.putText(image, text='Kick your head!!!', org=(30, 25), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                                  fontScale=1.2, color=(0, 0, 255), thickness=2)

                # qimage = array_to_QImage(image, (358, 243))
                # qthread.record_change_pixmap.emit(qimage)
                #
                # visualize.draw(image, -1, -1, show_fps)
                cv.imwrite('./image/records' + '/' + timestr_image + '.jpg', image)  # 保存异常图片
            if flag_lvtong == 1 and flag_xiangzi == 0:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
                qthread.text_append.emit(timestr + '第' + str(put_number) + '次装箱 零件投放失败，漏放箱子')
                # qimage = array_to_QImage(image, (358, 243))
                # qthread.record_change_pixmap.emit(qimage)
                # visualize.draw(image, -1, -1, show_fps)  # 在图片上加上投放失败的信息
                # cv.imwrite('./image/records' + '/' + timestr_image + '.jpg', image)  # 保存异常图片
            # 这里两行注释掉了数据库
            dbManager.choose_sql_and_insert(flag_lvtong, flag_xiangzi, 0, (flag_lvtong and flag_xiangzi))

            flag_stage1 = 0
            flag_stage1_1 = 0
            flag_stage2 = 0
            flag_stage2_1 = 0
            flag_stage3 = 0
            flag_lvtong = 0
            flag_xiangzi = 0
            count_stage2_1 = 0
            count_xiangzi = 0
            put_number += 1
            gui_bucket = 0
            gui_box = 0
            # count_stage = 0

        #print(flag_stage1, flag_stage1_1, flag_stage2_1, flag_stage3, flag_lvtong, flag_xiangzi)
        #image = cv.resize(frame, (1280, 720))
        #cv.imshow("image", image)

        #cv.waitKey(0)
        # 不加这个不知道为什么cv.imshow会白屏

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main(None)
    cv.waitKey(1)
    cv.destroyAllWindows()

