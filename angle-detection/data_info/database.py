import datetime
import time
import pymssql
import pymysql


def get_recent_time():
    """
    获取当前日期时间并格式化
    :return: date, start_time, end_time
    """

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    recent_time = time.strftime("%H:%M:%S", time.localtime())

    ret_time = str(date) + ' ' + str(recent_time)
    return ret_time


def get_recent_date():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return date


class SqlServer:
    """
    负责连接SQL Server数据库，格式化数据，并把检测完的信息插入数据库

    """

    def __init__(self):
        self.server = "10.19.3.23"
        self.user = "sa"
        self.password = "q26248165."
        self.db = "LVS_EAP"
        self.conn = self._connect_sqlserver()  # 在创建对象时就创建连接

    def _connect_sqlserver(self):
        conn = pymssql.connect(self.server, self.user, self.password, self.db)
        print("SQL Server已连接")
        return conn

    def add_data_into_db(self, Angle, IndustrialPC='OP30'):

        # if self.conn is None:
            # 如果连接断开，则重新连接
            # self.conn = self._connect_sqlserver()

        # 格式化角度数据和当前时间，准备存入数据库
        Angle = round(Angle,2)
        #Angle = str(int(Angle)) + "°" + str(int((Angle % 1.0) * 60)) + "′" + str(int((Angle % 1.0) * 3600 % 60)) + '″'
     
        strTime = get_recent_time() + '.000'

        # print('IndustrialPC:', IndustrialPC)
        # print('Angle:', Angle)
        # print('strTime:', strTime)

        try:
            sql = "INSERT INTO LVS_XIO_OP30Write (IndustrialPC, Angle, strTime) VALUES('{}', '{}', '{}')".format(
                IndustrialPC, Angle, strTime)
            # print(sql)
            cursor = self.conn.cursor()
            # 执行SQL语句，插入数据到 LVS_XIO_OP30Write_copy 表，栏位名称为 IndustrialPC,Angle,strTime
            cursor.execute(sql)
            # 向数据库提交执行的语句
            self.conn.commit()
            

        except Exception as e:
            if self.conn is not None:
                self.conn.rollback()  # 发生错误时回滚
                cursor.close()
                self.conn.close()
            print("信息存入SQLServer失败！")
            
        finally:
            print("信息已存入SQLServer")
            # 关闭游标
            cursor.close()
            self.conn.close()


class MySql:
    """
    负责连接MySQL数据库，格式化数据，并把检测完的信息插入数据库
    """

    def __init__(self):
        self.server = '10.19.3.35'
        self.port = 3306
        self.user = "root"
        self.password = "123456"
        self.db = "shijue"
        self.conn = self._connect_mysql()  # 在创建对象时就创建连接

    def _connect_mysql(self):
        # 如果连接断开，则重新连接
        conn = pymysql.Connect(host=self.server, port=self.port, user=self.user, password=self.password, database=self.db)
        print("MySQL已连接")
        return conn

    def add_data_into_db(self, length, image_address, angle, camera_number=None, qualified=1):

        # if self.conn is None:
            # self.conn = self._connect_mysql()

        # 格式化角度数据和当前时间，准备存入数据库
        angle = round(angle, 2)  # 保留两位小数
        date = get_recent_date()
        timestamp = get_recent_time()

        try:
            sql = "INSERT INTO gjb (GJCD, CL_DATE, CL_TIME, TPLJ, CLJD, SFHG) VALUES({}, '{}', '{}', '{}', {}, {})".format(
                length, date, timestamp, image_address, angle, qualified)
            # print(sql)
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()  # 事务提交
            

        except Exception as e:
            if self.conn is not None:
                self.conn.rollback()  # 发生错误时回滚
                cursor.close()
                self.conn.close()
            print("信息存入MySQL失败！")
            
        finally:
            cursor.close()
            self.conn.close()
            print('信息已存入MySQL')

            
