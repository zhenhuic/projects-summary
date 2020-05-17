import pymysql

connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456',
                                         db='opc',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
sql = "select * from" + "`" + "s7300warn" + "`"
cursor.execute(sql)
values = cursor.fetchall()
print(values)
