import sys
import time
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
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

    selected_flag = False
    flc = FigureLineChart()
    message_window = MyWindow()

    s7300warns = ["OP20安全门未锁", "OP20冲床报警", "OP20冲床程序切换失败报警", "OP20冲床误动作报警", "OP20废料口报警",
                  "OP20机器人故障", "OP20夹钳状态报警", "OP20一级报警", "OP20二级报警", "OP20真空检测超时报警", "OP30安全门未锁",
                  "OP30二级报警", "OP30材料尺寸超差报警", "OP30机器人故障", "OP30机器人码垛上限到", "OP30一级报警", "OP40安全门未锁",
                  "OP40材料尺寸超差报警", "OP40二级报警", "OP40机器人故障", "OP40机器人码垛上限到", "OP20冲床靠山气缸伸出未到位",
                  "OP20冲床靠山气缸缩回未到位", "OP20料塔端定位气缸1伸出未到位", "OP20料塔端定位气缸1缩回未到位", "OP20料塔端定位气缸2伸出未到位",
                  "OP20料塔端定位气缸2缩回未到位", "OP20线体定位气缸1伸出未到位", "OP20线体定位气缸1缩回未到位", "OP20线体定位气缸2伸出未到位",
                  "OP20线体定位气缸2缩回未到位", "OP20小车1码垛数量达到上限", "OP20小车2码垛数量达到上限", "OP30磁力吸盘伸出未到位", "OP30磁力吸盘缩回未到位",
                  "OP30高度调整气缸伸出未到位", "OP30高度调整气缸缩回未到位", "OP30厚度检测气缸伸出未到位", "OP30宽度检测气缸伸出未到位", "OP30宽度检测气缸缩回未到位",
                  "OP30长度检测气缸伸出未到位", "OP30长度检测气缸缩回未到位", "OP40定位台长度检测气缸伸出到位", "OP40定位台长度检测气缸缩回到位", "OP40高度调整气缸伸出未到位",
                  "OP40高度调整气缸缩回未到位", "OP40厚度检测气缸伸出未到位", "OP40宽度检测气缸伸出未到位", "OP40宽度检测气缸缩回未到位", "OP40长度检测气缸缩回未到位",
                  "OP40长度检测气缸伸出未到位"]

    dcbhj = ["负向极限", "焊机急停", "焊接启动", "急停", "启动或停止", "伺服急停", "伺服开", "伺服原点", "伺服准备好", "送丝", "泄压阀开", "油泵开", "正向极限"]

    xinsawanini = ["门板前左角度", "门板中部左角度", "门板后左角度", "门板前右角度", "门板中部右角度", "门板后右角度"]

    @pyqtSlot()
    def select(self):
        self.selected_flag = True
        if self.comboBox.currentText() == "厚板线":
            self.comboBox_2.clear()
            for i in range(len(self.s7300warns)):
                self.comboBox_2.addItem(self.s7300warns[i])
            self.comboBox_3.clear()
            self.comboBox_3.addItem("报警")
        elif self.comboBox.currentText() == "侧板焊接线":
            self.comboBox_2.clear()
            for i in range(len(self.dcbhj)):
                self.comboBox_2.addItem(self.dcbhj[i])
            self.comboBox_3.clear()
            self.comboBox_3.addItem("一般")
        elif self.comboBox.currentText() == "新萨瓦尼尼线":
            self.comboBox_2.clear()
            for i in range(len(self.xinsawanini)):
                self.comboBox_2.addItem(self.xinsawanini[i])
                self.comboBox_3.clear()
                self.comboBox_3.addItem("一般")

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
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
