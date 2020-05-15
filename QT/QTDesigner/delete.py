# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: delete.py.py
# time: 2020/5/13 11:04

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from inOut.menu import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from inOut.menu import Menu


class Ui_Dialog_delete(object):

    def __init__(self):
        self.dia = QDialog()
        self.setupUi(self.dia)
        self.dia.setWindowModality(Qt.ApplicationModal)
        self.deleteFlag = False
        self.okButton.clicked.connect(lambda: self.deleteConfirm())
        self.cancelButton.clicked.connect(lambda: self.deleteCancel())
        self.dia.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.comboBox_1 = QtWidgets.QComboBox(Dialog)
        self.comboBox_1.setGeometry(QtCore.QRect(120, 30, 81, 22))
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 70, 200, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_1.currentIndexChanged.connect(self.selectionchange)

        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(30, 70, 80, 21))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 80, 21))
        self.label_2.setObjectName("label_2")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 110, 61, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(110, 110, 61, 23))
        self.okButton.setObjectName("okButton")

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
        self.label_1.setText(_translate("Dialog", "具体点位："))
        self.label_2.setText(_translate("Dialog", "具体区域："))
        self.cancelButton.setText(_translate("Dialog", "cancle"))
        self.okButton.setText(_translate("Dialog", "ok"))

    def deleteConfirm(self):
        msg_box = QtWidgets.QMessageBox
        reply = msg_box.question(self.dia, '通知', '是否删除节点：' + str(self.comboBox_2.currentText()) + '?', msg_box.Cancel |msg_box.Ok, msg_box.Cancel)
        if reply == QMessageBox.Ok:
            menu = Menu()
            path = "menuFile/" + self.comboBox_1.currentText() + ".txt"
            name = self.comboBox_2.currentText()
            menu.delete(path, name)
            self.deleteFlag = True
            self.dia.close()

    def deleteCancel(self):
        self.dia.close()

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