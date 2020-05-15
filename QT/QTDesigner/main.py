# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from inOut.menu import *

class Ui_MainWindow(object):

    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainWindow)
        self.mainWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1204, 801)
        #MainWindow.setStyleSheet("background-color: rgb(39, 39, 39);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1181, 751))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setEnabled(True)
        self.tab_1.setObjectName("tab_1")
        self.graphicsView_1_today = QtWidgets.QGraphicsView(self.tab_1)
        self.graphicsView_1_today.setGeometry(QtCore.QRect(10, 0, 571, 711))
        self.graphicsView_1_today.setObjectName("graphicsView_1_today")
        self.graphicsView_1_week = QtWidgets.QGraphicsView(self.tab_1)
        self.graphicsView_1_week.setGeometry(QtCore.QRect(600, 0, 571, 711))
        self.graphicsView_1_week.setObjectName("graphicsView_1_week")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView_2_week = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2_week.setGeometry(QtCore.QRect(10, 360, 1151, 361))
        self.graphicsView_2_week.setObjectName("graphicsView_2_week")
        self.graphicsView_2_frequency = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2_frequency.setGeometry(QtCore.QRect(10, -10, 1151, 361))
        self.graphicsView_2_frequency.setObjectName("graphicsView_2_frequency")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1204, 22))
        self.menubar.setObjectName("menubar")
        self.Transducer = QtWidgets.QMenu(self.menubar)
        self.Transducer.setObjectName("Transducer")
        self.OP20 = QtWidgets.QMenu(self.menubar)
        self.OP20.setObjectName("OP20")
        self.OP30 = QtWidgets.QMenu(self.menubar)
        self.OP30.setObjectName("OP30")
        self.OP40 = QtWidgets.QMenu(self.menubar)
        self.OP40.setObjectName("OP40")
        self.systemError = QtWidgets.QMenu(self.menubar)
        self.systemError.setObjectName("systemError")
        self.setting = QtWidgets.QMenu(self.menubar)
        self.setting.setObjectName("setting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        _translate = QtCore.QCoreApplication.translate
        menu = Menu()


        transducerList = menu.readerTitle("menuFile/变频器.txt")
        i = 1
        for each in transducerList:
            self.__dict__[f'transducer_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'transducer_{i}'].setCheckable(False)
            self.__dict__[f'transducer_{i}'].setChecked(False)
            self.__dict__[f'transducer_{i}'].setWhatsThis("")
            self.__dict__[f'transducer_{i}'].setText(_translate("MainWindow", each))
            self.Transducer.addAction(self.__dict__[f'transducer_{i}'])
            i += 1

        OP20List = menu.readerTitle("menuFile/OP20.txt")
        i = 1
        for each in OP20List:
            self.__dict__[f'OP20_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'OP20_{i}'].setCheckable(False)
            self.__dict__[f'OP20_{i}'].setChecked(False)
            self.__dict__[f'OP20_{i}'].setWhatsThis("")
            self.__dict__[f'OP20_{i}'].setText(_translate("MainWindow", each))
            self.OP20.addAction(self.__dict__[f'OP20_{i}'])
            i += 1



        OP30List = menu.readerTitle("menuFile/OP30.txt")
        i = 1
        for each in OP30List:
            self.__dict__[f'OP30_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'OP30_{i}'].setCheckable(False)
            self.__dict__[f'OP30_{i}'].setChecked(False)
            self.__dict__[f'OP30_{i}'].setWhatsThis("")
            self.__dict__[f'OP30_{i}'].setText(_translate("MainWindow", each))
            self.OP30.addAction(self.__dict__[f'OP30_{i}'])
            i += 1

        OP40List = menu.readerTitle("menuFile/OP40.txt")
        i = 1
        for each in OP40List:
            self.__dict__[f'OP40_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'OP40_{i}'].setCheckable(False)
            self.__dict__[f'OP40_{i}'].setChecked(False)
            self.__dict__[f'OP40_{i}'].setWhatsThis("")
            self.__dict__[f'OP40_{i}'].setText(_translate("MainWindow", each))
            self.OP40.addAction(self.__dict__[f'OP40_{i}'])
            i += 1

        systemErrorList = menu.readerTitle("menuFile/系统故障.txt")
        i = 1
        for each in systemErrorList:
            self.__dict__[f'systemError_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'systemError_{i}'].setCheckable(False)
            self.__dict__[f'systemError_{i}'].setChecked(False)
            self.__dict__[f'systemError_{i}'].setWhatsThis("")
            self.__dict__[f'systemError_{i}'].setText(_translate("MainWindow", each))
            self.systemError.addAction(self.__dict__[f'systemError_{i}'])
            i += 1


        settingList = menu.readerTitle("menuFile/setting.txt")
        i = 1
        for each in settingList:
            self.__dict__[f'setting_{i}'] = QtWidgets.QAction(MainWindow)
            self.__dict__[f'setting_{i}'].setCheckable(False)
            self.__dict__[f'setting_{i}'].setChecked(False)
            self.__dict__[f'setting_{i}'].setWhatsThis("")
            self.__dict__[f'setting_{i}'].setText(_translate("MainWindow", each))
            self.setting.addAction(self.__dict__[f'setting_{i}'])
            i += 1

        self.menubar.addAction(self.Transducer.menuAction())
        self.menubar.addAction(self.OP20.menuAction())
        self.menubar.addAction(self.OP30.menuAction())
        self.menubar.addAction(self.OP40.menuAction())
        self.menubar.addAction(self.systemError.menuAction())
        self.menubar.addAction(self.setting.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "制造业生产线上传感器的采集、分析与显示"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "局部点位"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "整体点位"))
        self.Transducer.setTitle(_translate("MainWindow", "变频器"))
        self.OP20.setTitle(_translate("MainWindow", "OP20"))
        self.OP30.setTitle(_translate("MainWindow", "OP30"))
        self.OP40.setTitle(_translate("MainWindow", "OP40"))
        self.systemError.setTitle(_translate("MainWindow", "系统故障"))
        self.setting.setTitle(_translate("MainWindow", "设置"))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    a = Ui_MainWindow()

    sys.exit(app.exec())