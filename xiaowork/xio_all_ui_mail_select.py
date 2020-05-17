# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xio_all_ui_mail_select.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1442, 858)
        Form.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: rgb(61, 61, 61);\n"
""))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 110, 1421, 741))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet(_fromUtf8("color: rgb(49, 49, 49);\n"
"font: 75 10pt \"Aharoni\";"))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.graphicsView_MT = QtGui.QGraphicsView(self.tab)
        self.graphicsView_MT.setGeometry(QtCore.QRect(60, 10, 480, 340))
        self.graphicsView_MT.setObjectName(_fromUtf8("graphicsView_MT"))
        self.graphicsView_OEE = QtGui.QGraphicsView(self.tab)
        self.graphicsView_OEE.setGeometry(QtCore.QRect(550, 10, 480, 340))
        self.graphicsView_OEE.setObjectName(_fromUtf8("graphicsView_OEE"))
        self.graphicsView_Loss = QtGui.QGraphicsView(self.tab)
        self.graphicsView_Loss.setGeometry(QtCore.QRect(60, 360, 480, 340))
        self.graphicsView_Loss.setObjectName(_fromUtf8("graphicsView_Loss"))
        self.graphicsView_Pie = QtGui.QGraphicsView(self.tab)
        self.graphicsView_Pie.setGeometry(QtCore.QRect(550, 360, 480, 340))
        self.graphicsView_Pie.setObjectName(_fromUtf8("graphicsView_Pie"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(1040, 10, 360, 240))
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(1040, 260, 361, 441))
        self.textBrowser.setStyleSheet(_fromUtf8("font: 10pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.DateTable = QtGui.QTableWidget(self.tab_3)
        self.DateTable.setGeometry(QtCore.QRect(390, 60, 991, 591))
        self.DateTable.setStyleSheet(_fromUtf8("background-color: rgb(255,255,255);"))
        self.DateTable.setObjectName(_fromUtf8("DateTable"))
        self.DateTable.setColumnCount(0)
        self.DateTable.setRowCount(0)
        self.dateEdit = QtGui.QDateEdit(self.tab_3)
        self.dateEdit.setGeometry(QtCore.QRect(110, 200, 151, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.dateEdit.setFont(font)
        self.dateEdit.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 4, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setDate(QtCore.QDate(2019, 4, 1))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(30, 120, 91, 41))
        self.label_4.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.confirmDateButton = QtGui.QPushButton(self.tab_3)
        self.confirmDateButton.setGeometry(QtCore.QRect(130, 290, 93, 41))
        self.confirmDateButton.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.confirmDateButton.setObjectName(_fromUtf8("confirmDateButton"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.mailSenderButton = QtGui.QPushButton(self.tab_2)
        self.mailSenderButton.setGeometry(QtCore.QRect(990, 510, 121, 41))
        self.mailSenderButton.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);"))
        self.mailSenderButton.setObjectName(_fromUtf8("mailSenderButton"))
        self.mailConfirm = QtGui.QPushButton(self.tab_2)
        self.mailConfirm.setGeometry(QtCore.QRect(260, 510, 121, 41))
        self.mailConfirm.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);"))
        self.mailConfirm.setObjectName(_fromUtf8("mailConfirm"))
        self.mailTextBroswer = QtGui.QTextBrowser(self.tab_2)
        self.mailTextBroswer.setGeometry(QtCore.QRect(780, 110, 511, 341))
        self.mailTextBroswer.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.mailTextBroswer.setObjectName(_fromUtf8("mailTextBroswer"))
        self.mailLineEdit = QtGui.QLineEdit(self.tab_2)
        self.mailLineEdit.setGeometry(QtCore.QRect(110, 270, 491, 121))
        self.mailLineEdit.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);\n"
""))
        self.mailLineEdit.setObjectName(_fromUtf8("mailLineEdit"))
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(110, 200, 431, 41))
        self.label_5.setStyleSheet(_fromUtf8("font: 12pt \"宋体\";\n"
"\n"
"color:rgb(255, 255, 255);"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(10, 0, 1421, 20))
        self.line.setStyleSheet(_fromUtf8(""))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(10, 90, 1421, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(390, 30, 541, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.fileSelectButton = QtGui.QPushButton(Form)
        self.fileSelectButton.setGeometry(QtCore.QRect(40, 30, 93, 28))
        self.fileSelectButton.setObjectName(_fromUtf8("fileSelectButton"))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "主界面", None))
        self.dateEdit.setDisplayFormat(_translate("Form", "yyyy-MM", None))
        self.label_4.setText(_translate("Form", "选择年月：", None))
        self.confirmDateButton.setText(_translate("Form", "确认", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "月数据展示", None))
        self.mailSenderButton.setText(_translate("Form", "邮件发送", None))
        self.mailConfirm.setText(_translate("Form", "邮箱确认", None))
        self.label_5.setText(_translate("Form", "请输入邮箱：", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "邮件发送", None))
        self.label_3.setText(_translate("Form", "工厂侧板效率智能检测系统", None))
        self.fileSelectButton.setText(_translate("Form", "视频源选择", None))

