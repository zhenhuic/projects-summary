import sys
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.log_new import Ui_MainWindow
import random
import pymysql
from main.opc_plot import FigureLineChart
from PyQt5.QtGui import QPixmap
from main.message import MyWindow


class MainApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_2.clicked.connect(self.plot)
        self.pushButton.clicked.connect(self.export)
        self.pushButton_4.clicked.connect(self.open_conf)

    selected_flag = False
    flc = FigureLineChart()
    message_window = MyWindow()

    @pyqtSlot()
    def open_conf(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if filename[0]:
            try:
                f = open(filename[0], 'r')
                with f:
                    scx = f.readline().strip('\n')
                    count = 0
                    for i in range(self.comboBox.count()):
                        if self.comboBox.itemData(i) == scx:
                            count += 1
                    if count == 0:
                        self.comboBox.addItem(scx)
                    path = ("E:\\projects-summary\\xio\\tempfiles\\")
                    full_path = path + scx + '.txt'
                    file = open(full_path, 'w')
                    for line in f.readlines():
                        file.write(line)
                    file.close()
                f.close()
            except:
                pass

    @pyqtSlot()
    def select(self):
        self.selected_flag = True
        scx = self.comboBox.currentText()
        self.comboBox_2.clear()
        try:
            f = open("E:\\projects-summary\\xio\\tempfiles\\" + scx + ".txt", 'r')
            for line in f.readlines():
                self.comboBox_2.addItem(line.strip('\n'))
        except:
            pass

    @pyqtSlot()
    def export(self):
        if self.selected_flag is True:
            desktop_path = "C:\\Users\\dsx\\Desktop\\"
            all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLP'
            index = len(all_char) - 1
            tag = ''
            for i in range(6):
                num = random.randint(0, index)
                tag += all_char[num]
            full_path = desktop_path + tag + '.txt'
            file = open(full_path, 'w')
            scx = self.comboBox.currentText()
            bq = self.comboBox_2.currentText()
            start_date = self.dateEdit.dateTime()
            start_time = self.timeEdit.dateTime()
            end_date = self.dateEdit_2.dateTime()
            end_time = self.timeEdit_2.dateTime()
            start = str(start_date).split('(')[1][:-6].replace(', ', "-0").replace(",", "") + str(start_time).split('(')[1][11:].split(')')[0].replace(',', ':')+'0'
            end = str(end_date).split('(')[1][:-6].replace(', ', "-0").replace(",", "") + str(end_time).split('(')[1][11:].split(')')[0].replace(',', ':')+'0'
            log_type = self.comboBox_3.currentText()
            file.write('生产线：' + scx + '\n')
            file.write('PLC节点：' + bq + '\n')
            file.write('开始时间：' + start + '\n')
            file.write('结束时间：' + end + '\n')
            file.write('日志类型：' + log_type + '\n' + '\n')

            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='123456',
                                         db='opc',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            if self.comboBox.currentText() == "厚板线":
                sql = "select * from" + "`" + "s7300warning" + "`" + "WHERE BQ = %s AND SJ >= %s AND SJ <= %s"
                cursor.execute(sql, (bq, start, end))
                values = cursor.fetchall()
                messages = []
                for i in range(len(values)):
                    messages.append(values[i]["SCX"] + " " + values[i]["SB"] + " " + values[i]["BQ"] + " " + values[i]["BJ"] + " " + values[i]["SJ"] + " " + values[i]["BZ"])
                for i in range(len(messages)):
                    file.write(messages[i] + "\n")

            if self.comboBox.currentText() == "侧板焊接线":
                sql = "select * from" + "`" + "dcbhj" + "`" + "WHERE BQ = %s AND SJ >= %s AND SJ <= %s"
                cursor.execute(sql, (bq, start, end))
                values = cursor.fetchall()
                messages = []
                for i in range(len(values)):
                    messages.append(values[i]["SCX"] + " " + values[i]["SB"] + " " + values[i]["BQ"] + " " + values[i]["ZT"] + " " + values[i]["SJ"])
                for i in range(len(messages)):
                    file.write(messages[i] + "\n")

            if self.comboBox.currentText() == "新萨瓦尼尼线":
                sql = "select * from" + "`" + "xinsawanini" + "`" + "WHERE BQ = %s AND SJ >= %s AND SJ <= %s"
                cursor.execute(sql, (bq, start, end))
                values = cursor.fetchall()
                messages = []
                for i in range(len(values)):
                    messages.append(values[i]["SCX"] + " " + values[i]["SB"] + " " + values[i]["BQ"] + " " + values[i]["ZT"] + " " + values[i]["SJ"])
                for i in range(len(messages)):
                    file.write(messages[i] + "\n")

            self.message_window.msg()
            connection.close()
            file.close()
        else:
            return

    @pyqtSlot()
    def plot(self):
        time.sleep(1)
        if self.selected_flag is True:
            if self.comboBox.currentText() == "厚板线":
                self.flc.plotlinechart("houban", self.comboBox_5.currentText(), self.comboBox_2.currentText(), self.comboBox_4.currentText())
                if self.comboBox_5.currentText() == "日平均(7日)":
                    pix = QPixmap("1.png")
                    self.label_34.setPixmap(pix)
                elif self.comboBox_5.currentText() == "周平均(28日)":
                    pix = QPixmap("2.png")
                    self.label_34.setPixmap(pix)
            if self.comboBox.currentText() == "侧板焊接线":
                self.flc.plotlinechart("hanjie", self.comboBox_5.currentText(), self.comboBox_2.currentText(), self.comboBox_4.currentText())
                if self.comboBox_5.currentText() == "日平均(7日)":
                    pix = QPixmap("1.png")
                    self.label_34.setPixmap(pix)
                elif self.comboBox_5.currentText() == "周平均(28日)":
                    pix = QPixmap("2.png")
                    self.label_34.setPixmap(pix)
            if self.comboBox.currentText() == "新萨瓦尼尼线":
                self.flc.plotlinechart("xinsawanini", self.comboBox_5.currentText(), self.comboBox_2.currentText(), self.comboBox_4.currentText())
                if self.comboBox_5.currentText() == "日平均(7日)":
                    pix = QPixmap("1.png")
                    self.label_34.setPixmap(pix)
                elif self.comboBox_5.currentText() == "周平均(28日)":
                    pix = QPixmap("2.png")
                    self.label_34.setPixmap(pix)
        else:
            return


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook  # print the traceback to stdout/stderr
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
