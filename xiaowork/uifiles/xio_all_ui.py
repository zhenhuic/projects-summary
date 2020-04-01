# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xio_all.ui'
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
        Form.resize(1613, 994)
        Form.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: rgb(61, 61, 61);\n"
""))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 109, 1561, 831))
        self.tabWidget.setStyleSheet(_fromUtf8("color: rgb(49, 49, 49);\n"
"font: 75 10pt \"Aharoni\";"))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.graphicsView_MT = QtGui.QGraphicsView(self.tab)
        self.graphicsView_MT.setGeometry(QtCore.QRect(80, 10, 511, 361))
        self.graphicsView_MT.setObjectName(_fromUtf8("graphicsView_MT"))
        self.graphicsView_OEE = QtGui.QGraphicsView(self.tab)
        self.graphicsView_OEE.setGeometry(QtCore.QRect(629, 10, 511, 361))
        self.graphicsView_OEE.setObjectName(_fromUtf8("graphicsView_OEE"))
        self.graphicsView_Loss = QtGui.QGraphicsView(self.tab)
        self.graphicsView_Loss.setGeometry(QtCore.QRect(80, 399, 511, 371))
        self.graphicsView_Loss.setObjectName(_fromUtf8("graphicsView_Loss"))
        self.graphicsView_Pie = QtGui.QGraphicsView(self.tab)
        self.graphicsView_Pie.setGeometry(QtCore.QRect(630, 399, 511, 371))
        self.graphicsView_Pie.setObjectName(_fromUtf8("graphicsView_Pie"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(1180, 260, 360, 240))
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(1180, 10, 360, 240))
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(1180, 510, 361, 271))
        self.textBrowser.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
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
        self.label_3.setGeometry(QtCore.QRect(390, 30, 641, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_2.setText(_translate("Form", "TextLabel", None))
        self.label.setText(_translate("Form", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "主界面", None))
        self.label_3.setText(_translate("Form", "工厂侧板效率智能检测系统", None))

