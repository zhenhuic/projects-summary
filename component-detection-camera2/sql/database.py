#!/usr/bin/env python
# coding:UTF-8
import io

import cv2
import pymysql
import logging
import sys
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
from matplotlib.ticker import MaxNLocator
from pylab import mpl
import subprocess
import numpy as np
import datetime

# 加入日志
# 获取logger实例
logger = logging.getLogger("dbSql")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("dbSql.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


def fig2img(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    return img


# 绘制表格
def draw_bar_chart(data: [int]):

    # 第三：绘制图形

    # 中文显示设置
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    width = 0.3
    # index = np.arange(len(sname))

    rr = plt.bar("风管放入个数", data[0], width, color='r', label="风管放入个数")
    rr = plt.bar("小包组件放入个数", data[1], width, color='r', label="小包组件放入个数")
    rr = plt.bar("投放成功次数", data[2], width, color='b', label="投放成功次数")
    rr = plt.bar("投放失败次数", data[3], width, color='c', label="投放失败次数")

    # r1 = plt.bar(sname, chinese, width, color='r', label='chinese')
    # r2 = plt.bar(index + width, math, width, color='b', label='math')
    # r3 = plt.bar(index + width + width, english, width, color='c', label='english')

    # 显示图像
    # plt.legend()
    # plt.show()

    # 关闭
    # self.cur.close()
    # self.db.close()
    return fig2img(rr)


def draw_bar_graph(names: [str], values: [int]) -> np.ndarray:
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    fig, ax = plt.subplots()
    ax.bar(names, values, color=['lightgreen', 'orange', 'turquoise', 'lightcoral', 'deepskyblue'])
    # 设置颜色
    # ax.set_facecolor("darkgray")
    plt.xticks(fontsize=8.6)
    # ax.set_title("")
    # ax.set_xlabel('')
    ax.set_ylabel('投放记录次数')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    img = fig2img(fig)
    return img


class DbManager:
    # 构造函数
    def __init__(self, host='localhost', port=3306, user='root',
                 passwd='123456', db='object_detection', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None
        self.x = [0, 1, 2, 3, 4]

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)
        except Exception:
            logger.error("connect Database failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    def count_records_between_datetime(self, table: str, start: str, end: str) -> [int]:
        if not self.connectDatabase():
            raise RuntimeError("数据库连接失败！")

        com1_sql = "SELECT count(*) FROM {} WHERE date >= '{}' AND date <= '{}' AND fengguan=1".format(table, start,
                                                                                                       end)
        com2_sql = "SELECT count(*) FROM {} WHERE date >= '{}' AND date <= '{}' AND xiaobao=1".format(table, start, end)
        suc_sql = "SELECT count(*) FROM {} WHERE date >= '{}' AND date <= '{}' AND success=1".format(table, start, end)
        fail_sql = "SELECT count(*) FROM {} WHERE date >= '{}' AND date <= '{}' AND success=0".format(table, start, end)
        print(com1_sql)
        self.cur.execute(com1_sql)
        com1_cnt = int(self.cur.fetchone()[0])

        self.cur.execute(com2_sql)
        com2_cnt = int(self.cur.fetchone()[0])

        self.cur.execute(suc_sql)
        suc_cnt = int(self.cur.fetchone()[0])

        self.cur.execute(fail_sql)
        fail_cnt = int(self.cur.fetchone()[0])
        return com1_cnt, com2_cnt, suc_cnt, fail_cnt, suc_cnt + fail_cnt

    # 根据零件的投放情况来选择要插入数据库的信息，其中com1表示桶，com2表示箱子
    def choose_sql_and_insert(self, com1: int, com2: int, com3: int, success: int):
        try:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO pack(date, fengguan, xiaobao, component3, success) values ('{}',{},{},{},{})".\
                format(dt, str(com1), str(com2), str(com3), str(success))
            # print(sql)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()


    def zhuagnxiang_sql_and_insert(self, ZX_id: int, ST_ZX: int, ED_ZX: int):
        try:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO zhuangxiang(date, zhuagnxiang_id, kaishizhuagnxiang, jieshuzhuagnxiang) values ('{}',{},{},{})".\
                format(dt, str(ZX_id), str(ST_ZX), str(ED_ZX))
            # print(sql)
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()


if __name__ == '__main__':
    dbManager = DbManager()
    dbManager.connectDatabase()
    dbManager.choose_sql_and_insert(0, 0, 0, 0)
