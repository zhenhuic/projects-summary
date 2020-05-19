import datetime
import sys
import time
from main.send_email import Email
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.cps_new import Ui_MainWindow
from main.message import MyWindow
from ui.set_email_address import Ui_Dialog


class MainApp(QMainWindow, Ui_MainWindow):
    email_address = "1787626381@qq.com"

    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)

        self.show_h(False)
        self.show_z(False)
        self.show_b(False)

        self.pushButton.clicked.connect(self.open_conf)
        self.pushButton_2.clicked.connect(self.open_log)
        self.action_8.triggered.connect(self.set_email_address)

    def set_email_address(self):
        dialog = Ui_Dialog()
        self.email_address = dialog.lineEdit.text()
        print(self.email_address)

    def show_h(self, flag):
        if flag is False:
            self.label_hp1.setVisible(False)
            self.label_hp2.setVisible(False)
            self.label_hp3.setVisible(False)
            self.label_hp4.setVisible(False)
            self.label_hp5.setVisible(False)
            self.label_hp6.setVisible(False)
            self.label_hp7.setVisible(False)
            self.label_hp8.setVisible(False)
            self.label_hp9.setVisible(False)
            self.label_hp10.setVisible(False)

            self.label_ht1.setVisible(False)
            self.label_ht2.setVisible(False)
            self.label_ht3.setVisible(False)
            self.label_ht4.setVisible(False)
            self.label_ht5.setVisible(False)
            self.label_ht6.setVisible(False)
            self.label_ht7.setVisible(False)
            self.label_ht8.setVisible(False)
            self.label_ht9.setVisible(False)
            self.label_ht10.setVisible(False)

            self.label_ha1.setVisible(False)
            self.label_ha2.setVisible(False)
            self.label_ha3.setVisible(False)
            self.label_ha4.setVisible(False)
            self.label_ha5.setVisible(False)
            self.label_ha6.setVisible(False)
            self.label_ha7.setVisible(False)
            self.label_ha8.setVisible(False)
            self.label_ha9.setVisible(False)
            self.label_ha10.setVisible(False)

        elif flag is True:
            self.label_hp1.setVisible(True)
            self.label_hp2.setVisible(True)
            self.label_hp3.setVisible(True)
            self.label_hp4.setVisible(True)
            self.label_hp5.setVisible(True)
            self.label_hp6.setVisible(True)
            self.label_hp7.setVisible(True)
            self.label_hp8.setVisible(True)
            self.label_hp9.setVisible(True)
            self.label_hp10.setVisible(True)

            self.label_ht1.setVisible(True)
            self.label_ht2.setVisible(True)
            self.label_ht3.setVisible(True)
            self.label_ht4.setVisible(True)
            self.label_ht5.setVisible(True)
            self.label_ht6.setVisible(True)
            self.label_ht7.setVisible(True)
            self.label_ht8.setVisible(True)
            self.label_ht9.setVisible(True)
            self.label_ht10.setVisible(True)

            self.label_ha1.setVisible(True)
            self.label_ha2.setVisible(True)
            self.label_ha3.setVisible(True)
            self.label_ha4.setVisible(True)
            self.label_ha5.setVisible(True)
            self.label_ha6.setVisible(True)
            self.label_ha7.setVisible(True)
            self.label_ha8.setVisible(True)
            self.label_ha9.setVisible(True)
            self.label_ha10.setVisible(True)

    def show_z(self, flag):
        if flag is False:
            self.label_zp1.setVisible(False)
            self.label_zp2.setVisible(False)
            self.label_zp3.setVisible(False)
            self.label_zp4.setVisible(False)
            self.label_zp5.setVisible(False)
            self.label_zp6.setVisible(False)

            self.label_zt1.setVisible(False)
            self.label_zt2.setVisible(False)
            self.label_zt3.setVisible(False)
            self.label_zt4.setVisible(False)
            self.label_zt5.setVisible(False)
            self.label_zt6.setVisible(False)

            self.label_za1.setVisible(False)
            self.label_za2.setVisible(False)
            self.label_za3.setVisible(False)
            self.label_za4.setVisible(False)
            self.label_za5.setVisible(False)

        elif flag is True:
            self.label_zp1.setVisible(True)
            self.label_zp2.setVisible(True)
            self.label_zp3.setVisible(True)
            self.label_zp4.setVisible(True)
            self.label_zp5.setVisible(True)
            self.label_zp6.setVisible(True)

            self.label_zt1.setVisible(True)
            self.label_zt2.setVisible(True)
            self.label_zt3.setVisible(True)
            self.label_zt4.setVisible(True)
            self.label_zt5.setVisible(True)
            self.label_zt6.setVisible(True)

            self.label_za1.setVisible(True)
            self.label_za2.setVisible(True)
            self.label_za3.setVisible(True)
            self.label_za4.setVisible(True)
            self.label_za5.setVisible(True)

    def show_b(self, flag):
        if flag is False:
            self.label_bp1.setVisible(False)
            self.label_bp2.setVisible(False)
            self.label_bp3.setVisible(False)
            self.label_bp4.setVisible(False)
            self.label_bp5.setVisible(False)

            self.label_bt1.setVisible(False)
            self.label_bt2.setVisible(False)
            self.label_bt3.setVisible(False)
            self.label_bt4.setVisible(False)
            self.label_bt5.setVisible(False)

            self.label_ba1.setVisible(False)
            self.label_ba2.setVisible(False)
            self.label_ba3.setVisible(False)
            self.label_ba4.setVisible(False)

        elif flag is True:
            self.label_bp1.setVisible(True)
            self.label_bp2.setVisible(True)
            self.label_bp3.setVisible(True)
            self.label_bp4.setVisible(True)
            self.label_bp5.setVisible(True)

            self.label_bt1.setVisible(True)
            self.label_bt2.setVisible(True)
            self.label_bt3.setVisible(True)
            self.label_bt4.setVisible(True)
            self.label_bt5.setVisible(True)

            self.label_ba1.setVisible(True)
            self.label_ba2.setVisible(True)
            self.label_ba3.setVisible(True)
            self.label_ba4.setVisible(True)

    @pyqtSlot()
    def open_conf(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if filename[0]:
            try:
                f = open(filename[0], 'r')
                with f:
                    scx = f.readline()
                    time.sleep(1)
                    if scx == "厚板线\n":
                        self.label.setText("生产流程模型(厚板线)")
                        self.label_20.setText("流程挖掘与优化信息(厚板线)")
                        self.textEdit.clear()
                        self.show_h(True)
                        self.show_z(False)
                        self.show_b(False)
                    elif scx == "专机线\n":
                        self.label.setText("生产流程模型(专机线)")
                        self.label_20.setText("流程挖掘与优化信息(专机线)")
                        self.textEdit.clear()
                        self.show_h(False)
                        self.show_z(True)
                        self.show_b(False)
                    elif scx == "薄板线\n":
                        self.label.setText("生产流程模型(薄板线)")
                        self.label_20.setText("流程挖掘与优化信息(薄板线)")
                        self.textEdit.clear()
                        self.show_h(False)
                        self.show_z(False)
                        self.show_b(True)
                MyWindow().msg()
                f.close()
            except:
                pass

    @pyqtSlot()
    def open_log(self):
        email = Email()
        filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if filename[0]:
            try:
                f = open(filename[0], 'r')
                with f:
                    data = []
                    for line in f.readlines()[6:]:
                        data.append(line.strip('\n'))
                    if self.label.text() == "生产流程模型(厚板线)":
                        time.sleep(1)
                        hp1_start_time = []
                        hp1_end_time = []
                        hp1_time = []
                        hp2_start_time = []
                        hp2_end_time = []
                        hp2_time = []
                        hp3_start_time = []
                        hp3_end_time = []
                        hp3_time = []
                        hp4_start_time = []
                        hp4_end_time = []
                        hp4_time = []
                        hp5_start_time = []
                        hp5_end_time = []
                        hp5_time = []
                        hp6_start_time = []
                        hp6_end_time = []
                        hp6_time = []
                        hp7_start_time = []
                        hp7_end_time = []
                        hp7_time = []
                        hp8_start_time = []
                        hp8_end_time = []
                        hp8_time = []
                        hp9_start_time = []
                        hp9_end_time = []
                        hp9_time = []
                        hp10_start_time = []
                        hp10_end_time = []
                        hp10_time = []
                        hp1_fail = []
                        hp2_fail = []
                        hp3_fail = []
                        hp4_fail = []
                        hp5_fail = []
                        hp6_fail = []
                        hp7_fail = []
                        hp8_fail = []
                        hp9_fail = []
                        hp10_fail = []
                        hp1_fail_count = 0
                        hp2_fail_count = 0
                        hp3_fail_count = 0
                        hp4_fail_count = 0
                        hp5_fail_count = 0
                        hp6_fail_count = 0
                        hp7_fail_count = 0
                        hp8_fail_count = 0
                        hp9_fail_count = 0
                        hp10_fail_count = 0
                        for i in range(len(data)):
                            if self.label_hp1.text() in data[i] and "0-1" in data[i]:
                                hp1_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp1.text() in data[i] and "1-0" in data[i]:
                                hp1_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp1_fail.append(data[i].split(" ")[6])
                            if self.label_hp2.text() in data[i] and "0-1" in data[i]:
                                hp2_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp2.text() in data[i] and "1-0" in data[i]:
                                hp2_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp2_fail.append(data[i].split(" ")[6])
                            if self.label_hp3.text() in data[i] and "0-1" in data[i]:
                                hp3_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp3.text() in data[i] and "1-0" in data[i]:
                                hp3_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp3_fail.append(data[i].split(" ")[6])
                            if self.label_hp4.text() in data[i] and "0-1" in data[i]:
                                hp4_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp4.text() in data[i] and "1-0" in data[i]:
                                hp4_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp4_fail.append(data[i].split(" ")[6])
                            if self.label_hp5.text() in data[i] and "0-1" in data[i]:
                                hp5_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp5.text() in data[i] and "1-0" in data[i]:
                                hp5_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp5_fail.append(data[i].split(" ")[6])
                            if self.label_hp6.text() in data[i] and "0-1" in data[i]:
                                hp6_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp6.text() in data[i] and "1-0" in data[i]:
                                hp6_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp6_fail.append(data[i].split(" ")[6])
                            if self.label_hp7.text() in data[i] and "0-1" in data[i]:
                                hp7_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp7.text() in data[i] and "1-0" in data[i]:
                                hp7_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp7_fail.append(data[i].split(" ")[6])
                            if self.label_hp8.text() in data[i] and "0-1" in data[i]:
                                hp8_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp8.text() in data[i] and "1-0" in data[i]:
                                hp8_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp8_fail.append(data[i].split(" ")[6])
                            if self.label_hp9.text() in data[i] and "0-1" in data[i]:
                                hp9_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp9.text() in data[i] and "1-0" in data[i]:
                                hp9_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp9_fail.append(data[i].split(" ")[6])
                            if self.label_hp10.text() in data[i] and "0-1" in data[i]:
                                hp10_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_hp10.text() in data[i] and "1-0" in data[i]:
                                hp10_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                hp10_fail.append(data[i].split(" ")[6])
                        for j in range(len(hp1_start_time)):
                            hp1_time.append((hp1_end_time[j] - hp1_start_time[j]).seconds)
                            hp2_time.append((hp2_end_time[j] - hp2_start_time[j]).seconds)
                            hp3_time.append((hp3_end_time[j] - hp3_start_time[j]).seconds)
                            hp4_time.append((hp4_end_time[j] - hp4_start_time[j]).seconds)
                            hp5_time.append((hp5_end_time[j] - hp5_start_time[j]).seconds)
                            hp6_time.append((hp6_end_time[j] - hp6_start_time[j]).seconds)
                            hp7_time.append((hp7_end_time[j] - hp7_start_time[j]).seconds)
                            hp8_time.append((hp8_end_time[j] - hp8_start_time[j]).seconds)
                            hp9_time.append((hp9_end_time[j] - hp9_start_time[j]).seconds)
                            hp10_time.append((hp10_end_time[j] - hp10_start_time[j]).seconds)
                        self.label_ht1.setText("平均耗时:" + str(round(sum(hp1_time) / len(hp1_time), 1)) + "s")
                        self.label_ht2.setText("平均耗时:" + str(round(sum(hp2_time) / len(hp2_time), 1)) + "s")
                        self.label_ht3.setText("平均耗时:" + str(round(sum(hp3_time) / len(hp3_time), 1)) + "s")
                        self.label_ht4.setText("平均耗时:" + str(round(sum(hp4_time) / len(hp4_time), 1)) + "s")
                        self.label_ht5.setText("平均耗时:" + str(round(sum(hp5_time) / len(hp5_time), 1)) + "s")
                        self.label_ht6.setText("平均耗时:" + str(round(sum(hp6_time) / len(hp6_time), 1)) + "s")
                        self.label_ht7.setText("平均耗时:" + str(round(sum(hp7_time) / len(hp7_time), 1)) + "s")
                        self.label_ht8.setText("平均耗时:" + str(round(sum(hp8_time) / len(hp8_time), 1)) + "s")
                        self.label_ht9.setText("平均耗时:" + str(round(sum(hp9_time) / len(hp9_time), 1)) + "s")
                        self.label_ht10.setText("平均耗时:" + str(round(sum(hp10_time) / len(hp10_time), 1)) + "s")
                        MyWindow().msg()
                        f.close()
                        for i in range(len(hp1_fail)):
                            if hp1_fail[i] == "1":
                                hp1_fail_count += 1
                        for i in range(len(hp2_fail)):
                            if hp2_fail[i] == "1":
                                hp2_fail_count += 1
                        for i in range(len(hp3_fail)):
                            if hp3_fail[i] == "1":
                                hp3_fail_count += 1
                        for i in range(len(hp4_fail)):
                            if hp4_fail[i] == "1":
                                hp4_fail_count += 1
                        for i in range(len(hp5_fail)):
                            if hp5_fail[i] == "1":
                                hp5_fail_count += 1
                        for i in range(len(hp6_fail)):
                            if hp6_fail[i] == "1":
                                hp6_fail_count += 1
                        for i in range(len(hp7_fail)):
                            if hp7_fail[i] == "1":
                                hp7_fail_count += 1
                        for i in range(len(hp8_fail)):
                            if hp8_fail[i] == "1":
                                hp8_fail_count += 1
                        for i in range(len(hp9_fail)):
                            if hp9_fail[i] == "1":
                                hp9_fail_count += 1
                        for i in range(len(hp10_fail)):
                            if hp10_fail[i] == "1":
                                hp10_fail_count += 1
                        self.textEdit.clear()
                        self.textEdit.append("厚板线工序平均耗时与故障率信息\n")
                        self.textEdit.append(self.label_hp1.text() + self.label_ht1.text() + " 故障率：" + str(
                            hp1_fail_count / len(hp1_fail)) + "\n")
                        self.textEdit.append(self.label_hp2.text() + self.label_ht2.text() + " 故障率：" + str(
                            hp2_fail_count / len(hp2_fail)) + "\n")
                        self.textEdit.append(self.label_hp3.text() + self.label_ht3.text() + " 故障率：" + str(
                            hp3_fail_count / len(hp3_fail)) + "\n")
                        self.textEdit.append(self.label_hp4.text() + self.label_ht4.text() + " 故障率：" + str(
                            hp4_fail_count / len(hp4_fail)) + "\n")
                        self.textEdit.append(self.label_hp5.text() + self.label_ht5.text() + " 故障率：" + str(
                            hp5_fail_count / len(hp5_fail)) + "\n")
                        self.textEdit.append(self.label_hp6.text() + self.label_ht6.text() + " 故障率：" + str(
                            hp6_fail_count / len(hp6_fail)) + "\n")
                        self.textEdit.append(self.label_hp7.text() + self.label_ht7.text() + " 故障率：" + str(
                            hp7_fail_count / len(hp7_fail)) + "\n")
                        self.textEdit.append(self.label_hp8.text() + self.label_ht8.text() + " 故障率：" + str(
                            hp8_fail_count / len(hp8_fail)) + "\n")
                        self.textEdit.append(self.label_hp9.text() + self.label_ht9.text() + " 故障率：" + str(
                            hp9_fail_count / len(hp9_fail)) + "\n")
                        self.textEdit.append(self.label_hp10.text() + self.label_ht10.text() + " 故障率：" + str(
                            hp10_fail_count / len(hp10_fail)) + "\n")
                        total = float(self.label_ht1.text()[5:][:-1]) + float(self.label_ht2.text()[5:][:-1]) + float(
                            self.label_ht3.text()[5:][:-1]) + float(self.label_ht4.text()[5:][:-1]) + float(
                            self.label_ht5.text()[5:][:-1]) + float(self.label_ht6.text()[5:][:-1]) + float(
                            self.label_ht7.text()[5:][:-1]) + float(self.label_ht8.text()[5:][:-1]) + float(
                            self.label_ht9.text()[5:][:-1]) + float(self.label_ht10.text()[5:][:-1])
                        self.textEdit.append("厚板线工序平均耗时汇总：" + str(round(total, 1)) + "s\n")
                        self.textEdit.append("提示信息：厚板折弯工序加工耗时过长\n")
                        self.textEdit.append("优化建议：建议检查码垛堆叠以及机器人故障情况\n")
                        email.send_email(self.email_address, self.textEdit.toPlainText(), "提示信息")
                        self.textEdit.append("已发送邮件\n")
                    if self.label.text() == "生产流程模型(专机线)":
                        time.sleep(1)
                        zp1_start_time = []
                        zp1_end_time = []
                        zp1_time = []
                        zp2_start_time = []
                        zp2_end_time = []
                        zp2_time = []
                        zp3_start_time = []
                        zp3_end_time = []
                        zp3_time = []
                        zp4_start_time = []
                        zp4_end_time = []
                        zp4_time = []
                        zp5_start_time = []
                        zp5_end_time = []
                        zp5_time = []
                        zp6_start_time = []
                        zp6_end_time = []
                        zp6_time = []
                        zp1_fail = []
                        zp2_fail = []
                        zp3_fail = []
                        zp4_fail = []
                        zp5_fail = []
                        zp6_fail = []
                        zp1_fail_count = 0
                        zp2_fail_count = 0
                        zp3_fail_count = 0
                        zp4_fail_count = 0
                        zp5_fail_count = 0
                        zp6_fail_count = 0
                        for i in range(len(data)):
                            if self.label_zp1.text() in data[i] and "0-1" in data[i]:
                                zp1_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp1.text() in data[i] and "1-0" in data[i]:
                                zp1_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp1_fail.append(data[i].split(" ")[6])
                            if self.label_zp2.text() in data[i] and "0-1" in data[i]:
                                zp2_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp2.text() in data[i] and "1-0" in data[i]:
                                zp2_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp2_fail.append(data[i].split(" ")[6])
                            if self.label_zp3.text() in data[i] and "0-1" in data[i]:
                                zp3_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp3.text() in data[i] and "1-0" in data[i]:
                                zp3_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp3_fail.append(data[i].split(" ")[6])
                            if self.label_zp4.text() in data[i] and "0-1" in data[i]:
                                zp4_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp4.text() in data[i] and "1-0" in data[i]:
                                zp4_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp4_fail.append(data[i].split(" ")[6])
                            if self.label_zp5.text() in data[i] and "0-1" in data[i]:
                                zp5_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp5.text() in data[i] and "1-0" in data[i]:
                                zp5_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp5_fail.append(data[i].split(" ")[6])
                            if self.label_zp6.text() in data[i] and "0-1" in data[i]:
                                zp6_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_zp6.text() in data[i] and "1-0" in data[i]:
                                zp6_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                zp6_fail.append(data[i].split(" ")[6])
                        for j in range(len(zp1_start_time)):
                            zp1_time.append((zp1_end_time[j] - zp1_start_time[j]).seconds)
                            zp2_time.append((zp2_end_time[j] - zp2_start_time[j]).seconds)
                            zp3_time.append((zp3_end_time[j] - zp3_start_time[j]).seconds)
                            zp4_time.append((zp4_end_time[j] - zp4_start_time[j]).seconds)
                            zp5_time.append((zp5_end_time[j] - zp5_start_time[j]).seconds)
                            zp6_time.append((zp6_end_time[j] - zp6_start_time[j]).seconds)
                        self.label_zt1.setText("平均耗时:" + str(round(sum(zp1_time) / len(zp1_time), 1)) + "s")
                        self.label_zt2.setText("平均耗时:" + str(round(sum(zp2_time) / len(zp2_time), 1)) + "s")
                        self.label_zt3.setText("平均耗时:" + str(round(sum(zp3_time) / len(zp3_time), 1)) + "s")
                        self.label_zt4.setText("平均耗时:" + str(round(sum(zp4_time) / len(zp4_time), 1)) + "s")
                        self.label_zt5.setText("平均耗时:" + str(round(sum(zp5_time) / len(zp5_time), 1)) + "s")
                        self.label_zt6.setText("平均耗时:" + str(round(sum(zp6_time) / len(zp6_time), 1)) + "s")
                        MyWindow().msg()
                        f.close()
                        for i in range(len(zp1_fail)):
                            if zp1_fail[i] == "1":
                                zp1_fail_count += 1
                        for i in range(len(zp2_fail)):
                            if zp2_fail[i] == "1":
                                zp2_fail_count += 1
                        for i in range(len(zp3_fail)):
                            if zp3_fail[i] == "1":
                                zp3_fail_count += 1
                        for i in range(len(zp4_fail)):
                            if zp4_fail[i] == "1":
                                zp4_fail_count += 1
                        for i in range(len(zp5_fail)):
                            if zp5_fail[i] == "1":
                                zp5_fail_count += 1
                        for i in range(len(zp6_fail)):
                            if zp6_fail[i] == "1":
                                zp6_fail_count += 1
                        self.textEdit.clear()
                        self.textEdit.append("专机线工序平均耗时与故障率信息\n")
                        self.textEdit.append(self.label_hp1.text() + self.label_ht1.text() + " 故障率：" + str(
                            zp1_fail_count / len(zp1_fail)) + "\n")
                        self.textEdit.append(self.label_hp2.text() + self.label_ht2.text() + " 故障率：" + str(
                            zp2_fail_count / len(zp2_fail)) + "\n")
                        self.textEdit.append(self.label_hp3.text() + self.label_ht3.text() + " 故障率：" + str(
                            zp3_fail_count / len(zp3_fail)) + "\n")
                        self.textEdit.append(self.label_hp4.text() + self.label_ht4.text() + " 故障率：" + str(
                            zp4_fail_count / len(zp4_fail)) + "\n")
                        self.textEdit.append(self.label_hp5.text() + self.label_ht5.text() + " 故障率：" + str(
                            zp5_fail_count / len(zp5_fail)) + "\n")
                        self.textEdit.append(self.label_hp6.text() + self.label_ht6.text() + " 故障率：" + str(
                            zp6_fail_count / len(zp6_fail)) + "\n")
                        total = float(self.label_zt1.text()[5:][:-1]) + float(self.label_zt2.text()[5:][:-1]) + float(
                            self.label_zt3.text()[5:][:-1]) + float(self.label_zt4.text()[5:][:-1]) + float(
                            self.label_zt5.text()[5:][:-1]) + float(self.label_zt6.text()[5:][:-1])
                        self.textEdit.append("专机线工序平均耗时汇总：" + str(round(total, 1)) + "s\n")
                        self.textEdit.append("提示信息：自动折弯工序加工耗时过长\n")
                        self.textEdit.append("优化建议：建议检查折弯设备故障情况\n")
                        email.send_email(self.email_address, self.textEdit.toPlainText(), "提示信息")
                        self.textEdit.append("已发送邮件\n")
                    if self.label.text() == "生产流程模型(薄板线)":
                        time.sleep(1)
                        bp1_start_time = []
                        bp1_end_time = []
                        bp1_time = []
                        bp2_start_time = []
                        bp2_end_time = []
                        bp2_time = []
                        bp3_start_time = []
                        bp3_end_time = []
                        bp3_time = []
                        bp4_start_time = []
                        bp4_end_time = []
                        bp4_time = []
                        bp5_start_time = []
                        bp5_end_time = []
                        bp5_time = []
                        bp1_fail = []
                        bp2_fail = []
                        bp3_fail = []
                        bp4_fail = []
                        bp5_fail = []
                        bp1_fail_count = 0
                        bp2_fail_count = 0
                        bp3_fail_count = 0
                        bp4_fail_count = 0
                        bp5_fail_count = 0
                        for i in range(len(data)):
                            if self.label_bp1.text() in data[i] and "0-1" in data[i]:
                                bp1_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_bp1.text() in data[i] and "1-0" in data[i]:
                                bp1_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                bp1_fail.append(data[i].split(" ")[6])
                            if self.label_bp2.text() in data[i] and "0-1" in data[i]:
                                bp2_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_bp2.text() in data[i] and "1-0" in data[i]:
                                bp2_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                bp2_fail.append(data[i].split(" ")[6])
                            if self.label_bp3.text() in data[i] and "0-1" in data[i]:
                                bp3_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_bp3.text() in data[i] and "1-0" in data[i]:
                                bp3_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                bp3_fail.append(data[i].split(" ")[6])
                            if self.label_bp4.text() in data[i] and "0-1" in data[i]:
                                bp4_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_bp4.text() in data[i] and "1-0" in data[i]:
                                bp4_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                bp4_fail.append(data[i].split(" ")[6])
                            if self.label_bp5.text() in data[i] and "0-1" in data[i]:
                                bp5_start_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                            if self.label_bp5.text() in data[i] and "1-0" in data[i]:
                                bp5_end_time.append(datetime.datetime.strptime(data[i].split(" ")[5], "%H:%M:%S"))
                                bp5_fail.append(data[i].split(" ")[6])
                        for j in range(len(bp1_start_time)):
                            bp1_time.append((bp1_end_time[j] - bp1_start_time[j]).seconds)
                            bp2_time.append((bp2_end_time[j] - bp2_start_time[j]).seconds)
                            bp3_time.append((bp3_end_time[j] - bp3_start_time[j]).seconds)
                            bp4_time.append((bp4_end_time[j] - bp4_start_time[j]).seconds)
                            bp5_time.append((bp5_end_time[j] - bp5_start_time[j]).seconds)
                        self.label_bt1.setText("平均耗时:" + str(round(sum(bp1_time) / len(bp1_time), 1)) + "s")
                        self.label_bt2.setText("平均耗时:" + str(round(sum(bp2_time) / len(bp2_time), 1)) + "s")
                        self.label_bt3.setText("平均耗时:" + str(round(sum(bp3_time) / len(bp3_time), 1)) + "s")
                        self.label_bt4.setText("平均耗时:" + str(round(sum(bp4_time) / len(bp4_time), 1)) + "s")
                        self.label_bt5.setText("平均耗时:" + str(round(sum(bp5_time) / len(bp5_time), 1)) + "s")
                        MyWindow().msg()
                        f.close()
                        for i in range(len(bp1_fail)):
                            if bp1_fail[i] == "1":
                                bp1_fail_count += 1
                        for i in range(len(bp2_fail)):
                            if bp2_fail[i] == "1":
                                bp2_fail_count += 1
                        for i in range(len(bp3_fail)):
                            if bp3_fail[i] == "1":
                                bp3_fail_count += 1
                        for i in range(len(bp4_fail)):
                            if bp4_fail[i] == "1":
                                bp4_fail_count += 1
                        for i in range(len(bp5_fail)):
                            if bp5_fail[i] == "1":
                                bp5_fail_count += 1
                        self.textEdit.clear()
                        self.textEdit.append("专机线工序平均耗时与故障率信息\n")
                        self.textEdit.append(self.label_bp1.text() + self.label_bt1.text() + " 故障率：" + str(
                            bp1_fail_count / len(bp1_fail)) + "\n")
                        self.textEdit.append(self.label_hp2.text() + self.label_bt2.text() + " 故障率：" + str(
                            bp2_fail_count / len(bp2_fail)) + "\n")
                        self.textEdit.append(self.label_hp3.text() + self.label_bt3.text() + " 故障率：" + str(
                            bp3_fail_count / len(bp3_fail)) + "\n")
                        self.textEdit.append(self.label_hp4.text() + self.label_bt4.text() + " 故障率：" + str(
                            bp4_fail_count / len(bp4_fail)) + "\n")
                        self.textEdit.append(self.label_hp5.text() + self.label_bt5.text() + " 故障率：" + str(
                            bp5_fail_count / len(bp5_fail)) + "\n")
                        total = float(self.label_bt1.text()[5:][:-1]) + float(self.label_bt2.text()[5:][:-1]) + float(
                            self.label_bt3.text()[5:][:-1]) + float(self.label_bt4.text()[5:][:-1]) + float(
                            self.label_bt5.text()[5:][:-1])
                        self.textEdit.append("专机线工序平均耗时汇总：" + str(round(total, 1)) + "s\n")
                        self.textEdit.append("提示信息：自动折弯工序加工耗时过长\n")
                        self.textEdit.append("优化建议：建议检查折弯设备故障情况\n")
                        email.send_email(self.email_address, self.textEdit.toPlainText(), "提示信息")
                        self.textEdit.append("已发送邮件\n")
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
