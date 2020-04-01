# coding=utf-8
from opcua import Client


class ProductInfo:
    """
    通过OPC server获取工件长度
    """

    def __init__(self, opc_tcp="opc.tcp://10.19.3.35:49320"):
        self.opc_tcp = opc_tcp
        self.client = Client(self.opc_tcp)
        self.client.connect()  # 在创建对象时就创建连接
        print("OPC已连接")

    def get_product_info(self, node="ns=2;s=houban.S7300.OP30折弯板材长度"):
        """
        获取工件的id、长度、宽度、高度
        :return: product_id, product_length, product_width, product_height
        """

        product_id, product_width, product_height = 11011, 150, 120  # 主要是长度，其他量随意值

        try:

            # 获取点位和点位值
            my_node = self.client.get_node(node)
            product_length = my_node.get_value()

            return product_id, product_length, product_width, product_height

        except Exception as e:
            print(e)
