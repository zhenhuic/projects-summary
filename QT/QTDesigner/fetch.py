# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Lab417\xio-intrusion-detection\configs\email.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

from Database.utils import Utils
from inOut.fetchAction import Email
from inOut.menu import Menu


class Ui_Dialog_fetch(object):

    def __init__(self, parent=None):
        self.fetchFlag = False
        self.dia = QDialog()
        self.setupUi(self.dia)
        self.addFlag = False
        self.dia.setWindowModality(Qt.ApplicationModal)
        self.okButton.clicked.connect(lambda:self.fetchConfirm())
        self.cancelButton.clicked.connect(lambda:self.cancel())
        self.dia.exec_()


    def setupUi(self, Dialog):
        Dialog.setObjectName("提取信息")
        Dialog.resize(335, 180)
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(30, 30, 71, 21))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 71, 20))
        self.label_2.setObjectName("label_2")
        self.comboBox_1 = QtWidgets.QComboBox(Dialog)
        self.comboBox_1.setGeometry(QtCore.QRect(110, 30, 91, 22))
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.currentIndexChanged.connect(self.selectionchange)


        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(80, 150, 75, 23))
        self.okButton.setObjectName("okButton")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(170, 150, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(65, 70, 71, 21))
        self.label_4.setObjectName("label_4")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(110, 70, 200, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 110, 113, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.comboBox_1.setItemText(0, _translate("Dialog", ""))
        self.comboBox_1.setItemText(1, _translate("Dialog", "变频器"))
        self.comboBox_1.setItemText(2, _translate("Dialog", "OP20"))
        self.comboBox_1.setItemText(3, _translate("Dialog", "OP30"))
        self.comboBox_1.setItemText(4, _translate("Dialog", "OP40"))
        self.comboBox_1.setItemText(5, _translate("Dialog", "系统故障"))


        self.label_1.setText(_translate("Dialog", "抽取流水线："))
        self.label_4.setText(_translate("Dialog", "点位："))
        self.label_2.setText(_translate("Dialog", "待发送邮箱："))
        self.okButton.setText(_translate("Dialog", "ok"))
        self.cancelButton.setText(_translate("Dialog", "cancel"))

    def selectionchange(self):
        self.comboBox_2.clear()
        _translate = QtCore.QCoreApplication.translate
        menu = Menu()
        list = menu.readerTitle("menuFile/"+self.comboBox_1.currentText()+".txt")
        i = 0
        for each in list:
            self.comboBox_2.addItem("")
            self.comboBox_2.setItemText(i, _translate("Dialog", str(each)))
            i += 1

    def fetchConfirm(self):
        msg_box = QtWidgets.QMessageBox
        reply = msg_box.question(self.dia, '通知', '检查邮箱：' + str(self.lineEdit.text()) + '?',
                                 msg_box.Cancel | msg_box.Ok, msg_box.Cancel)
        if reply == QMessageBox.Ok:
            fetch = Email()
            utils = Utils()
            header = "您好，"+str(self.comboBox_2.currentText())+"点位———今日报告如下：\n______________________________________\n______________________________________\n"
            title = "故障次数（/次）        故障时长（/分钟）                    \n"

            singleFrequencyAndTimeToday = utils.selectSingleFrequencyAndTimeCostByName(self.comboBox_2.currentText())[6]

            data = str(singleFrequencyAndTimeToday[1]) + "                            " + str(singleFrequencyAndTimeToday[2]) + "\n______________________________________\n"
            suggest = ""
            if singleFrequencyAndTimeToday[2] > 120:
                suggest += "故障时间过长，请维修！\n"
            elif singleFrequencyAndTimeToday[1] > 5 and singleFrequencyAndTimeToday[2] < 120:
                suggest += "存在隐藏故障，请检查！\n"
            else:
                suggest += "该点位表现良好！"
            msg = header + title + data + suggest
            fetch.send_email(str(self.lineEdit.text()), msg)
            self.fetchFlag = False
            self.dia.close()

    def cancel(self):
        self.dia.close()
