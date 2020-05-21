# import pymysql
#
# connection = pymysql.connect(host='10.19.3.49',
#                              user='root',
#                              password='123456',
#                              db='opc',
#                              charset='utf8',
#                              cursorclass=pymysql.cursors.DictCursor)

a = "PyQt5.QtCore.QDateTime(2020, 5, 1, 8, 4)"
# a = a.split('(')[1][:-7].replace(', ', '-')
# a_list = a.split('-')
# if int(a_list[1]) < 10:
#     a_list[1] = '0' + a_list[1]
# if int(a_list[2]) < 10:
#     a_list[2] = '0' + a_list[2]
# a = a_list[0] + '-' + a_list[1] + '-' + a_list[2]
# print(a)

b = a.split('(')[1][12:-1].replace(', ', ':')
b_list = b.split(":")
if int(b_list[0]) < 10:
    b_list[0] = '0' + b_list[0]
if int(b_list[1]) < 10:
    b_list[1] = '0' + b_list[1]
b = b_list[0] + ":" + b_list[1]
print(b)
