import threading
import datetime
import time
import socketserver
import cv2
from data import data_access


def data_deal(func):  # 要接受参数就要改成三层装饰器
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        return func(*args, **kwargs)

    return wrapper


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    action = None  # 用来通知显示现在是由于什么原因导致静止

    @data_deal
    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        # print(data)
        if data == 'action1':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data == 'action2':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data == 'action3':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data == 'action4':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data == 'action5':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data == 'action6':
            dz = data  # 动作
            da = data_access.DataAccess()
            da.insert_action(dz)
            action = data
        elif data[0:4] == 'stop':
            dz = data[4:]
            da = data_access.DataAccess()
            da.insert_action(dz, FLAG='end')
            # 更新动作表
            result = da.select_("select * from dz ORDER BY SJC DESC limit 2")
            time_diff = int((result[0][0] - result[1][0]).seconds)
            lossTime = data_access.EquipmentTimeData()
            result_loss = lossTime.select_("select * from loss ORDER BY SJ DESC limit 1")
            current_time = datetime.datetime.now().strftime('%Y-%m-%d')
            time_diff = time_diff + result_loss[0][int(dz[-1])]  # 此处投机
            lossTime.update_('update loss set ' + dz + '=' + str(time_diff) + ' where SJ="%s"' % current_time)

            action = None


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class XioStore(object):
    HOST = 'localhost'
    PORT = 8081

    def __init__(self):
        self.frame_left = None
        self.frame_right = None
        da = data_access.EquipmentTimeData()  # 对损失项统计表进行操作
        result_loss = da.select_("select * from loss ORDER BY SJ DESC limit 1")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(result_loss[0][0]) != current_time:
            da.update('insert into loss(SJ,action1,action2,action3,action4,action5,action6,action7,action8)values'
                      '("%s",%d,%d,%d,%d,%d,%d,%d,%d)' % (current_time, 0, 0, 0, 0, 0, 0, 0, 0))
        else:
            pass

        da_oee = data_access.OEEData()  # 对oee实时利用率进行统计
        result_oee = da_oee.select_('select * from oee_date ORDER BY SJC DESC limit 1')
        if str(result_oee[0][0]) != current_time:
            da_oee.update_('insert into oee_date(SJC,O8,O9,O10,O11,O12,O13,O14,O15,O16,O17,O18)values'
                           '("' + current_time + '",0,0,0,0,0,0,0,0,0,0,0)')
        else:
            pass

        self.server = ThreadedTCPServer((self.HOST, self.PORT), ThreadedTCPRequestHandler)  # 该线程用来一直监听客户端的请求
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

        self.data_thread = threading.Thread(target=self.read_data)
        self.data_thread.start()

    def video_receive_local(self, cam1='./videos/left_cam.mp4', cam2='./videos/right_cam.mp4', time_flag=True):
        '''该方法用来接收本地视频
        :param cam1: 左摄像头数据源
        :param cam2: 右摄像头数据源
        :param time_flag: 是否休眠，本地视频为True
        :return: None
        '''
        self.left_cam = cv2.VideoCapture(cam1)
        self.right_cam = cv2.VideoCapture(cam2)
        ret_1, frame_1 = self.left_cam.read()
        ret_2, frame_2 = self.right_cam.read()
        while True:
            self.frame_left = frame_1
            self.frame_right = frame_2
            if ret_1 is False:
                self.left_cam = cv2.VideoCapture(cam1)
            if ret_2 is False:
                self.right_cam = cv2.VideoCapture(cam2)
            ret_1, frame_1 = self.left_cam.read()
            ret_1, frame_2 = self.right_cam.read()
            if time_flag is True:
                time.sleep(0.04)

    def video_receive_rstp(self, cam1='rstp:', cam2='rstp:'):
        '''该方法用来接收网络视频
        :param cam1: 左摄像头数据源
        :param cam2: 右摄像头数据源
        :return: None
        '''
        self.video_receive_local(cam1=cam1, cam2=cam2, time_flag=False)

    def read_data(self):
        #隔天情况
        da = data_access.EquipmentTimeData()  # 对损失项统计表进行操作
        result_loss = da.select_("select * from loss ORDER BY SJ DESC limit 1")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(result_loss[0][0]) != current_time:
            da.update('insert into loss(SJ,action1,action2,action3,action4,action5,action6,action7-action8)values'
                      '("%s",%d,%d,%d,%d,%d,%d,%d,%d)' % (current_time, 0, 0, 0, 0, 0, 0, 0, 0))
        else:
            pass

        da_oee = data_access.OEEData()  # 对oee实时利用率进行统计
        result_oee = da_oee.select_('select * from oee_date ORDER BY SJC DESC limit 1')
        if str(result_oee[0][0]) != current_time:
            da_oee.update_('insert into oee_date(SJC,O8,O9,O10,O11,O12,O13,O14,O15,O16,O17,O18)values'
                           '("' + current_time + '",,00,0,0,0,0,0,0,0,0,0)')
        else:
            pass

        # 对效率表进行更新
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        lossTime = data_access.EquipmentTimeData()
        result_loss = lossTime.select_("select * from loss ORDER BY SJ DESC limit 1")
        zongshijian = time.strftime('%H:%M:%S', time.localtime(time.time()))
        fiveS = result_loss[0][1]
        eat = result_loss[0][2]
        yuzhuangpei = result_loss[0][3]
        huanqiping = result_loss[0][4]
        huanhansi = result_loss[0][5]
        tiaoshi = result_loss[0][6]
        others = result_loss[0][7]
        fuheshijian = (int(zongshijian.split(':')[0]) - 8) * 3600 + int(zongshijian.split(':')[1]) * 60 + int(
            zongshijian.split(':')[2]) - fiveS - eat
        shijijiagong_1 = fuheshijian - yuzhuangpei - huanqiping - huanhansi - tiaoshi - others
        eff = int(shijijiagong_1 / fuheshijian * 100)  # 计算效率

        hour = time.localtime()[3]  # 实时更新
        da_oee = data_access.OEEData()
        da_oee.update_("update oee_date set O" + str(hour) + "=" + str(eff) + ' where SJC="' + current_time + '"')

        #对日报进行更新,设置为5点多进行对日报的更新
        da_dr=data_access.DayreportData()
        result_dr=da_dr.select_('select * from dayreport ORDER BY RIQI DESC limit 1')
        if str(da_dr[0][0])!=current_time and hour>16 :
            da_dr.update_()#由于数据不足，此处sql暂未写入

        time.sleep(600)


if __name__ == '__main__':
    xio_store = XioStore()
    xio_store
