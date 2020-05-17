# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_email_address.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class Ui_Dialog(object):
    def __init__(self, parent=None):
        self.dia = QDialog()
        self.setupUi(self.dia)
        self.dia.setWindowModality(Qt.ApplicationModal)
        self.pushButton.clicked.connect(lambda: self.close_event())
        self.dia.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(427, 109)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(40, 40, 231, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def close_event(self):
        self.dia.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "设置接收邮箱"))
        self.pushButton.setText(_translate("Dialog", "确认"))


