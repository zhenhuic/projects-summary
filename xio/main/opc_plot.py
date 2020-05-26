# coding=utf-8
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pymysql


class FigureLineChart:
    def __init__(self):
        self.figure = plt.figure(figsize=(8.5, 3.7), facecolor='dimgray')
        self.canvas = FigureCanvas(self.figure)

    def plotlinechart(self, scx, days, bq, warn):
        if days == "日平均(7日)":
            x = [(datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                 datetime.datetime.now().strftime("%Y-%m-%d")]
            y = []
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d") - datetime.timedelta(days=6)).strftime(
                "%Y-%m-%d")
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456',
                                         db='opc',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            if scx == "houban":
                sql = "select * from" + "`" + "s7300warning" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s AND BJ = '报警'"
                cursor.execute(sql, (bq, start_time, (
                            datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d")))
                day1 = cursor.fetchall()
                y.clear()
                y.append(len(day1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=1)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=2)).strftime("%Y-%m-%d")))
                day2 = cursor.fetchall()
                y.append(len(day2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=2)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=3)).strftime("%Y-%m-%d")))
                day3 = cursor.fetchall()
                y.append(len(day3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=3)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=4)).strftime("%Y-%m-%d")))
                day4 = cursor.fetchall()
                y.append(len(day4))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=4)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=5)).strftime("%Y-%m-%d")))
                day5 = cursor.fetchall()
                y.append(len(day5))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=5)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=6)).strftime("%Y-%m-%d")))
                day6 = cursor.fetchall()
                y.append(len(day6))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=7)).strftime("%Y-%m-%d")))
                day7 = cursor.fetchall()
                y.append(len(day7))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近7天 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('1.png')
                plt.clf()
            if scx == "hanjie":
                sql = "select * from" + "`" + "dcbhj" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s AND ZT = '0-1'"
                cursor.execute(sql, (bq, start_time, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d")))
                day1 = cursor.fetchall()
                y.clear()
                y.append(len(day1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=1)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=2)).strftime("%Y-%m-%d")))
                day2 = cursor.fetchall()
                y.append(len(day2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=2)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=3)).strftime("%Y-%m-%d")))
                day3 = cursor.fetchall()
                y.append(len(day3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=3)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=4)).strftime("%Y-%m-%d")))
                day4 = cursor.fetchall()
                y.append(len(day4))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=4)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=5)).strftime("%Y-%m-%d")))
                day5 = cursor.fetchall()
                y.append(len(day5))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=5)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=6)).strftime("%Y-%m-%d")))
                day6 = cursor.fetchall()
                y.append(len(day6))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=7)).strftime("%Y-%m-%d")))
                day7 = cursor.fetchall()
                y.append(len(day7))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近7天 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('1.png')
                plt.clf()
            if scx == "xinsawanini":
                sql = "select * from" + "`" + "xinsawanini" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s"
                cursor.execute(sql, (bq, start_time, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d")))
                day1 = cursor.fetchall()
                y.clear()
                y.append(len(day1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=1)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=2)).strftime("%Y-%m-%d")))
                day2 = cursor.fetchall()
                y.append(len(day2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=2)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=3)).strftime("%Y-%m-%d")))
                day3 = cursor.fetchall()
                y.append(len(day3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=3)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=4)).strftime("%Y-%m-%d")))
                day4 = cursor.fetchall()
                y.append(len(day4))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=4)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=5)).strftime("%Y-%m-%d")))
                day5 = cursor.fetchall()
                y.append(len(day5))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=5)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=6)).strftime("%Y-%m-%d")))
                day6 = cursor.fetchall()
                y.append(len(day6))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=7)).strftime("%Y-%m-%d")))
                day7 = cursor.fetchall()
                y.append(len(day7))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近7天 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('1.png')
                plt.clf()
        elif days == "周平均(28日)":
            x = [(datetime.datetime.now() - datetime.timedelta(days=27)).strftime("%Y-%m-%d") + "-" + (
                    datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d") + "-" + (
                         datetime.datetime.now() - datetime.timedelta(days=13)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=13)).strftime("%Y-%m-%d") + "-" + (
                         datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
                 (datetime.datetime.now() - datetime.timedelta(days=6)).strftime(
                     "%Y-%m-%d") + "-" + datetime.datetime.now().strftime("%Y-%m-%d")]
            y = []
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d") - datetime.timedelta(days=27)).strftime(
                "%Y-%m-%d")
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456',
                                         db='opc',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            if scx == "houban":
                sql = "select * from" + "`" + "s7300warning" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s AND BJ = '报警'"
                cursor.execute(sql, (bq, start_time, (
                            datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=6)).strftime(
                    "%Y-%m-%d")))
                week1 = cursor.fetchall()
                y.clear()
                y.append(len(week1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=13)).strftime("%Y-%m-%d")))
                week2 = cursor.fetchall()
                y.append(len(week2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=13)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=20)).strftime("%Y-%m-%d")))
                week3 = cursor.fetchall()
                y.append(len(week3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=20)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=27)).strftime("%Y-%m-%d")))
                week4 = cursor.fetchall()
                y.append(len(week4))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近4周 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('2.png')
                plt.clf()
            if scx == "hanjie":
                sql = "select * from" + "`" + "dcbhj" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s AND ZT = '0-1'"
                cursor.execute(sql, (bq, start_time, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=6)).strftime(
                    "%Y-%m-%d")))
                week1 = cursor.fetchall()
                y.clear()
                y.append(len(week1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=13)).strftime("%Y-%m-%d")))
                week2 = cursor.fetchall()
                y.append(len(week2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=13)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=20)).strftime("%Y-%m-%d")))
                week3 = cursor.fetchall()
                y.append(len(week3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=20)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=27)).strftime("%Y-%m-%d")))
                week4 = cursor.fetchall()
                y.append(len(week4))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近4周 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('2.png')
                plt.clf()
            if scx == "xinsawanini":
                sql = "select * from" + "`" + "xinsawanini" + "`" + "WHERE BQ = %s AND SJ > %s AND SJ < %s"
                cursor.execute(sql, (bq, start_time, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(days=6)).strftime(
                    "%Y-%m-%d")))
                week1 = cursor.fetchall()
                y.clear()
                y.append(len(week1))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=6)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                                         days=13)).strftime("%Y-%m-%d")))
                week2 = cursor.fetchall()
                y.append(len(week2))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=13)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=20)).strftime("%Y-%m-%d")))
                week3 = cursor.fetchall()
                y.append(len(week3))
                cursor.execute(sql, (bq, (
                        datetime.datetime.strptime(start_time, "%Y-%m-%d") + datetime.timedelta(
                    days=20)).strftime("%Y-%m-%d"), (
                                             datetime.datetime.strptime(start_time,
                                                                        "%Y-%m-%d") + datetime.timedelta(
                                         days=27)).strftime("%Y-%m-%d")))
                week4 = cursor.fetchall()
                y.append(len(week4))
                plt.bar(x, y, label=days, color='orange')
                plt.title(bq + " 近4周 " + warn)
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.xlabel("日期")
                plt.ylabel("次数")
                plt.savefig('2.png')
                plt.clf()
