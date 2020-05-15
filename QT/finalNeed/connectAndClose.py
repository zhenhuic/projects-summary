# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 2:04 PM
# @Author  : sichengli
# @FileName: connectAndClose.py
# @Software: PyCharm
import pymysql

# 10.19.3.35
class ConnectAndClose:

    def database_connect(self):
        """连接数据库"""
        con = pymysql.Connect('localhost', 'root', '123456', 'newopc')
        return con, con.cursor()

    def database_close(self, con, cursor):
        con.commit()
        cursor.close()
        con.close()


if '__main__' == __name__:
    con, cursor = ConnectAndClose().database_connect()
    print(con)

