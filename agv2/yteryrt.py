from opcua import Client
from opcua import ua

# client = Client("opc.tcp://10.19.3.49:49320/AGVkanban.fx3u")
# try:
#     client.connect()
#
# except OSError as e:
#     print(e)
#
# print(client.get_node("ns=2;s=AGVkanban.fx3u." + "7号车当前动作指令").get_value())

client1 = Client("opc.tcp://127.0.0.1:49320")
client1.connect()
client1.disconnect()

try:
    client1.disconnect()
except Exception as e:
    pass


client1.connect()

nodeId = {}
nodeId[1] = 'ns=2;s=shougonghanjieAGVbaojing.FX3U.shougonghanjieAGV'

# 好像拼音写错了
nodeId[2] = 'ns=2;s=jiaobizhuanxiangAGVbaojing.FX3U.jiaobizhuangxiangAGV'
# 好像和 新萨瓦尼尼 1 2 颠倒了
nodeId[3] = 'ns=2;s=sawanini1houdaoAGVbaojing.FX3U.sawanini1houdaoAGV'
nodeId[4] = 'ns=2;s=houbanAGVbaojing.FX3U.houbanAGV'
# 好像拼音写错了
nodeId[5] = 'ns=2;s=houbanjiguanAGVbaojing.FX3U.houbanjiguangAGV'
# 好像和 新萨瓦尼尼 1 2 颠倒了
nodeId[6] = 'ns=2;s=sawanini2houdaoAGVbaojing.FX3U.sawanini2AGV'


client1.get_node(nodeId[2]).set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(False)))
