# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: reporter.py
# time: 2020/5/15 15:35

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

from Database.utils import Utils
from inOut.fetchAction import Email
from inOut.menu import Menu


class Ui_Dialog_reporter(object):

    def __init__(self, parent=None):
        self.fetchFlag = False
        self.dia = QDialog()
        self.setupUi(self.dia)
        self.addFlag = False
        self.dia.setWindowModality(Qt.ApplicationModal)

        self.generateButton.clicked.connect(lambda: self.generateRepoter())
        self.emailButton.clicked.connect(lambda: self.transmitReporter())
        self.closeButton.clicked.connect(lambda: self.closeDia())
        self.dia.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(740, 587)
        self.textEdit_1 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_1.setGeometry(QtCore.QRect(20, 100, 701, 391))
        self.textEdit_1.setObjectName("textEdit_1")

        self.comboBox_1 = QtWidgets.QComboBox(Dialog)
        self.comboBox_1.setGeometry(QtCore.QRect(20, 60, 121, 31))
        font = QtGui.QFont()
        # font.setFamily("Agency FB")
        font.setPointSize(14)
        self.comboBox_1.setFont(font)
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.emailButton = QtWidgets.QPushButton(Dialog)
        self.emailButton.setGeometry(QtCore.QRect(20, 550, 81, 31))
        self.emailButton.setObjectName("emailButton")
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(110, 500, 161, 31))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(20, 20, 201, 31))
        font = QtGui.QFont()
        # font.setFamily("Agency FB")
        font.setPointSize(24)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 500, 81, 31))
        font = QtGui.QFont()
        # font.setFamily("Agency FB")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.generateButton = QtWidgets.QPushButton(Dialog)
        self.generateButton.setGeometry(QtCore.QRect(160, 60, 81, 31))
        self.generateButton.setObjectName("generateButton")
        self.closeButton = QtWidgets.QPushButton(Dialog)
        self.closeButton.setGeometry(QtCore.QRect(640, 550, 81, 31))
        self.closeButton.setObjectName("closeButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox_1.setItemText(0, _translate("Dialog", "变频器"))
        self.comboBox_1.setItemText(1, _translate("Dialog", "OP20"))
        self.comboBox_1.setItemText(2, _translate("Dialog", "OP30"))
        self.comboBox_1.setItemText(3, _translate("Dialog", "OP40"))
        self.comboBox_1.setItemText(4, _translate("Dialog", "系统故障"))
        self.emailButton.setText(_translate("Dialog", "发送邮箱"))
        self.label_1.setText(_translate("Dialog", "分析报告"))
        self.label_2.setText(_translate("Dialog", "邮箱地址："))
        self.generateButton.setText(_translate("Dialog", "生成"))
        self.closeButton.setText(_translate("Dialog", "关闭"))

    def generateRepoter(self):
        self.textEdit_1.clear()
        name = self.comboBox_1.currentText()
        menu = Menu()
        nameList = menu.readerTitle("menuFile/" + str(name) + ".txt")
        util = Utils()
        header = str(self.comboBox_1.currentText()) + "\n\n今日故障报告如下：\n"
        self.textEdit_1.append(header)
        title = "点位名                                      " + "故障次数(/次)        " + "故障时长(/分钟)        \n"
        self.textEdit_1.append(title)
        for x in nameList:
            i = 25 - len(x)
            singleFrequencyAndTimeToday = util.selectSingleFrequencyAndTimeCostByName(x)[6]
            data = str(x) + " " * i * 2 + str(singleFrequencyAndTimeToday[1]) + " " * 15 + str(singleFrequencyAndTimeToday[2]) + "\n"
            self.textEdit_1.append(data)
        self.textEdit_1.append("-"*80 + "\n")

    def transmitReporter(self):
        if len(self.textEdit_1.toPlainText()) == 0:
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.dia, '提醒', '请先生成报告！',
                                     msg_box.Cancel | msg_box.Ok, msg_box.Cancel)
        else:
            msg = ""
            name = self.comboBox_1.currentText()
            menu = Menu()
            nameList = menu.readerTitle("menuFile/" + str(name) + ".txt")
            util = Utils()
            header = str(self.comboBox_1.currentText()) + "\n\n今日故障报告如下：\n"
            msg += header
            title = "点位名                                      " + "故障次数(/次)        " + "故障时长(/分钟)        \n"
            msg += title
            result = []
            for x in nameList:
                i = 25 - len(x)
                singleFrequencyAndTimeToday = util.selectSingleFrequencyAndTimeCostByName(x)[6]
                data = str(x) + " " * i * 2 + str(singleFrequencyAndTimeToday[1]) + " " * 15 + str(
                    singleFrequencyAndTimeToday[2]) + "\n"
                suggest = ""
                if singleFrequencyAndTimeToday[2] > 120:
                    suggest += "故障时间过长，请维修！\n"
                elif singleFrequencyAndTimeToday[1] > 5 and singleFrequencyAndTimeToday[2] < 120:
                    suggest += "存在隐藏故障，请检查！\n"
                else:
                    suggest += "（无）该点位表现良好！"
                result.append(str(x) + '------' + suggest)
                msg += data
            msg += "-" * 80 + "\n"
            msg += "建议：\n"
            for x in result:
                msg += x + '\n'
            msg += "-" * 80 + "\n"
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.dia, '通知', '检查邮箱：' + str(self.lineEdit_1.text()) + '?',
                                     msg_box.Cancel | msg_box.Ok, msg_box.Cancel)
            if reply == QMessageBox.Ok:
                fetch = Email()
                fetch.send_email(str(self.lineEdit_1.text()), msg)
                self.fetchFlag = True
                self.dia.close()

    def closeDia(self):
        self.dia.close()