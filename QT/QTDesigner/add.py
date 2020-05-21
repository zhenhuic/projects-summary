# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from inOut.menu import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class Ui_Dialog_add(object):

    def __init__(self, parent=None):
        self.dia = QDialog()
        self.setupUi(self.dia)
        self.addFlag = False
        self.dia.setWindowModality(Qt.ApplicationModal)
        self.okButton.clicked.connect(lambda:self.addConfirm())
        self.cancelButton.clicked.connect(lambda:self.cancelConfirm())
        self.dia.exec_()

    # def __init__(self, parent=None):
        # self.dia = QDialog()
        # self.setupUi(self.dia)
        # self.dia.setWindowModality(Qt.ApplicationModal)
        # self.dia.exec_()
    def setupUi(self, QDialog):
        QDialog.setObjectName("Dialog")
        QDialog.resize(317, 200)
        self.comboBox = QtWidgets.QComboBox(QDialog)
        self.comboBox.setGeometry(QtCore.QRect(200, 40, 104, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(QDialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 170, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(QDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 170, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(QDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 170, 21))
        self.label_3.setObjectName("label_3")

        self.name = QtWidgets.QLineEdit(QDialog)
        self.name.setGeometry(QtCore.QRect(200, 80, 111, 21))
        self.name.setObjectName("lineEdit")

        self.ip = QtWidgets.QLineEdit(QDialog)
        self.ip.setGeometry(QtCore.QRect(200, 120, 111, 21))
        self.ip.setObjectName("lineEdit_2")
        self.cancelButton = QtWidgets.QPushButton(QDialog)
        self.cancelButton.setGeometry(QtCore.QRect(230, 160, 81, 32))
        self.cancelButton.setObjectName("cancleButton")
        self.okButton = QtWidgets.QPushButton(QDialog)
        self.okButton.setGeometry(QtCore.QRect(150, 160, 81, 32))
        self.okButton.setObjectName("okButton")

        self.retranslateUi(QDialog)
        QtCore.QMetaObject.connectSlotsByName(QDialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("Dialog", "变频器"))
        self.comboBox.setItemText(1, _translate("Dialog", "OP20"))
        self.comboBox.setItemText(2, _translate("Dialog", "OP30"))
        self.comboBox.setItemText(3, _translate("Dialog", "OP40"))
        self.comboBox.setItemText(4, _translate("Dialog", "系统故障"))
        self.label.setText(_translate("Dialog", "请选择点位所属范围："))
        self.label_2.setText(_translate("Dialog", "请输入添加点位名称："))
        self.label_3.setText(_translate("Dialog", "请输入点位网络地址："))
        self.cancelButton.setText(_translate("Dialog", "cancel"))
        self.okButton.setText(_translate("Dialog", "ok"))

    def addConfirm(self):
        if len(self.comboBox.currentText()) == 0 or len(self.name.text()) == 0 or len(self.ip.text()) == 0:
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.dia, '通知', '请正确填写！',
                                     msg_box.Cancel | msg_box.Ok, msg_box.Cancel)
        else:
            msg_box = QtWidgets.QMessageBox
            reply = msg_box.question(self.dia, '通知', '是否添加节点：' + str(self.name.text()) + '?',
                                     msg_box.Cancel | msg_box.Ok, msg_box.Cancel)
            if reply == QMessageBox.Ok:
                menu = Menu()
                path = "menuFile/" + self.comboBox.currentText() + ".txt"
                menu.writerTile(path, self.name.text())
                self.addFlag = True
                self.dia.close()


    def cancelConfirm(self):
        self.dia.close()

