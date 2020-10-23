from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
import time
import sys
import logging
#from opcua.ua.uaerrors import BadNodeIdUnknown
from Zone import isZone
#from opcua import Client
#from opcua import ua


class BackendThread(QThread):
    update_data = pyqtSignal(dict)
    client = None
    Client1 = None

    def reconnect(self, count):
        if count >= 3:
            try:
                try:
                    self.client.disconnect()
                except Exception as e:
                    pass
                self.client.connect()
                print("opc已重新连接")
                count = 0
                return count
            except Exception as e:
                print(e)
                print("opc无法重新连接")
                return count
        else:
            return count

    def getValue(self, i, name):
        node_id = "ns=2;s=AGVkanban.fx3u." + str(i) + name
        value = self.client.get_node(node_id).get_value()
        # print(value)
        return value

    def run(self):
        strftime = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
        logging.basicConfig(filename='logs/' + strftime + '.log', level=logging.WARNING,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
        data = {}
        # 计数器 判断是否重连 依据为是否多次获取当前动作指令数据异常
        count = 0
        # try:
        #     self.client = Client("opc.tcp://10.19.3.49:49320/AGVkanban.fx3u")
        #     self.client.connect()
        #     print("opc1已连接")
        #
        #     self.client1 = Client("opc.tcp://127.0.0.1:49320")
        #     self.client1.connect()
        #     print("opc2已连接")
        # except Exception as e:
        #     #print(e)
        #     print("opc连接失败，退出")
        #     # sys.exit(1)
        temp1 = [False, False, False, False, False, False]
        m = 0
        while True:
            # 作为6个报警灯是否是报警状态的标志 True 为亮
            temp = [False, False, False, False, False, False]
            for i in range(1, 10):
                # try:
                #     # print(count)
                #     count = self.reconnect(count)
                #     # print(count)
                #     number = self.getValue(i, "号车车号")
                #     print(number)
                # except Exception as e:
                #     count = count + 1
                #     msg = "读取" + str(i) + '号车车号异常'
                #     print(msg)
                #     number = 'exception'
                # try:
                #     number = self.getValue(i, "号车车号")
                # except Exception as e:
                #     msg = "读取第" + str(i) + "车车号异常"
                #     print(msg)
                #     number = 'exception'
                #
                # try:
                #
                #     action = self.getValue(i, "号车当前动作指令")
                # except Exception as e:
                #     msg = "读取" + str(i) + '号车当前动作指令异常'
                #     print(msg)
                #     action = 'exception'
                #
                # try:
                #     battery = self.getValue(i, '号车电池状态')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车电池状态异常"
                #     print(msg)
                #     battery = 'exception'
                #
                # try:
                #     state = self.getValue(i, '号车工作状态')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车工作状态异常"
                #     print(msg)
                #     state = 'exception'
                #
                # try:
                #     fault = self.getValue(i, '号车故障')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车故障异常"
                #     print(msg)
                #     fault = 'exception'
                #
                # try:
                #     goods = self.getValue(i, '号车货物状态')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车货物状态异常"
                #     print(msg)
                #     goods = 'exception'
                #
                # try:
                #     progress = self.getValue(i, '号车进度量')
                # except Exception or BadNodeIdUnknown:
                #     msg = "读取" + str(i) + "号车进度量异常"
                #     print(msg)
                #     progress = 'exception'
                #
                # try:
                #     dest = self.getValue(i, '号车目的地')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车目的地异常"
                #     print(msg)
                #     dest = 'exception'
                #
                # try:
                #     start = self.getValue(i, '号车起点')
                #     #print(start, number)
                #     #print(i)
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车起点异常"
                #     print(msg)
                #     start = 'exception'
                #
                # try:
                #     end = self.getValue(i, '号车终点')
                # except Exception as e:
                #     msg = "读取" + str(i) + "号车终点异常"
                #     print(msg)
                #     end = 'exception'
                number = i
                if i in (1, 2, 4, 7,):
                    action = 28901
                elif i in (3, 5):
                    action = 28902
                elif i == 6:
                    action = 28906
                elif i == 8:
                    action = 65535
                else:
                    action = 65535

                battery = 1

                if i in (1, 2, 4, 7,):
                    state = 1
                elif i in (3, 5):
                    state = 1
                elif i == 6:
                    state = 1
                elif i == 8:
                    state = 0
                else:
                    state = 0

                if i != 9:
                    fault = 65535
                else:
                    fault = 525

                if i != 8:
                    goods = 1
                else:
                    goods = 0


                starts = [0, 82, 110, 155, 190, 279, 354, 502, 565, 649]
                start = starts[i] + m
                m = m + 1

                dests = [0, 85, 330, 420, 600, 777, 923, 944, 678, 1044]
                dest = dests[i]

                if str(number).isdigit():
                    data['carNumber' + str(i)] = number
                    # i = number
                #print(i)

                if str(action) == '28901':
                    data['carAction' + str(i)] = '取货'
                elif str(action) == '28902':
                    data['carAction' + str(i)] = '送货'
                elif str(action) == '28906':
                    data['carAction' + str(i)] = '二期取货'
                elif str(action) == '28907':
                    data['carAction' + str(i)] = '二期送货'
                elif str(action) == '65532':
                    data['carAction' + str(i)] = '充电'
                elif str(action) == '65535':
                    data['carAction' + str(i)] = '无动作'
                else:
                    data['carAction' + str(i)] = '获取失败'

                if str(battery) == '0':
                    data['carBattery' + str(i)] = '满电'
                elif str(battery) == '1':
                    data['carBattery' + str(i)] = '正常'
                elif str(battery) == '2':
                    data['carBattery' + str(i)] = '低电量'
                elif str(battery) == '3':
                    data['carBattery' + str(i)] = '极低'
                else:
                    data['carBattery' + str(i)] = '获取失败'

                if str(state) == '0':
                    data['carState' + str(i)] = '空闲'
                elif str(state) == '1':
                    data['carState' + str(i)] = '运行'
                elif str(state) == '2':
                    data['carState' + str(i)] = '挂起'
                elif str(state) == '4':
                    data['carState' + str(i)] = '静态'
                elif str(state) == '7':
                    data['carState' + str(i)] = '离线'
                else:
                    data['carState' + str(i)] = '获取失败'

                if str(fault).isdigit():
                    data['faultCode' + str(i)] = str(fault)
                    if str(fault) == '65535':
                        data['carFault' + str(i)] = '无故障'
                    elif int(str(fault)) in range(500, 535):
                        logging.warning('%s号小车故障，故障代码为  %s', str(number),  str(fault))
                        data['carFault' + str(i)] = '故障'


                    else:
                        # logging.warning('%s号小车故障,故障代码未记录，为  %s', str(number), str(fault))
                        data['carFault' + str(i)] = '异常'
                else:
                    data['faultCode' + str(i)] = '获取失败'
                    data['carFault' + str(i)] = '获取失败'

                if str(goods) == '0':
                    data['carGoods' + str(i)] = '无货'
                elif str(goods) == '1':
                    data['carGoods' + str(i)] = '有货'
                else:
                    data['carGoods' + str(i)] = '获取失败'



                if str(dest).isdigit():
                    data['carDest' + str(i)] = str(dest)
                    if str(dest) == '65535':
                        data['carDest' + str(i)] = '无'
                else:
                    data['carDest' + str(i)] = '获取失败'

                if str(start).isdigit():
                    data['carStart' + str(i)] = str(start)
                else:
                    data['carStart' + str(i)] = '获取失败'




                #client.get_node("ns=2;s=AGVkanban.fx3u." + "1号车车号").get_value()
                # data['carAction' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + "号车当前动作指令").get_value()
                # data['carBattery' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车电池状态').get_value()
                # data['carState' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车工作状态').get_value()
                # data['carFault' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车故障').get_value()
                # data['carGoods' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车货物状态').get_value()
                # data['carProgress' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车进度量').get_value()
                # data['carDest' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车目的地').get_value()
                # data['carStart' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车起点').get_value()
                # data['carEnd' + str(i)] = client.get_node("ns=2;s=AGVkanban.fx3u." + str(i) + '号车终点').get_value()
            self.update_data.emit(data)
            # print("发送成功")

            # # 红 1 黑1 2 黑2 3 蓝 4 黄 5 紫 6
            #
            # nodeId = {}
            # nodeId[1] = 'ns=2;s=shougonghanjieAGVbaojing.FX3U.shougonghanjieAGV'
            #
            # # 好像拼音写错了
            # nodeId[2] = 'ns=2;s=jiaobizhuanxiangAGVbaojing.FX3U.jiaobizhuangxiangAGV'
            # # 好像和 新萨瓦尼尼 1 2 颠倒了
            # nodeId[3] = 'ns=2;s=sawanini1houdaoAGVbaojing.FX3U.sawanini1houdaoAGV'
            # nodeId[4] = 'ns=2;s=houbanAGVbaojing.FX3U.houbanAGV'
            # # 好像拼音写错了
            # nodeId[5] = 'ns=2;s=houbanjiguanAGVbaojing.FX3U.houbanjiguangAGV'
            # # 好像和 新萨瓦尼尼 1 2 颠倒了
            # nodeId[6] = 'ns=2;s=sawanini2houdaoAGVbaojing.FX3U.sawanini2AGV'
            #
            # for i in range(0, 6):
            #     if temp[i] != temp1[i]:
            #         try:
            #             print(nodeId[i + 1])
            #             self.client1.get_node(nodeId[i + 1]).set_attribute(ua.AttributeIds.Value,
            #                                                                ua.DataValue(variant=ua.Variant(temp[i])))
            #         except Exception as e:
            #             print('报警灯opc异常')
            #             try:
            #                 self.client1.disconnect()
            #             except Exception as e:
            #                 pass
            #             self.client1.connect()
            #             print('报警灯opc已重新连接')
            #     # 将上次查询报警灯的状态赋给temp1 之后 若是各个报警灯的状态不变 ，则不进行opc赋值
            # temp1 = temp
            #
            # # if count >= 3:
            # #     try:
            # #         self.client.disconnect()
            # #         self.client.connect()
            # #         count = 0
            # #         print("opc已重新连接")
            # #     except Exception as e:
            # #         print(e)
            # #         print("opc无法重新连接")
            # # else:
            # #     count = 0



            time.sleep(5)

