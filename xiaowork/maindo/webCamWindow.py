from PyQt4 import QtGui
from PyQt4.QtGui import *
import sys

from maindo.Loginconfig import checkAccount


class FalseWarningBox(QDialog):
    def __init__(self, str_title, str_text):
        super(FalseWarningBox, self).__init__(parent=None)
        self.setWindowTitle(str_title)
        self.mainlayout = QGridLayout(self)

        self.labelWarning = QLabel()
        self.setFont(QFont("Roman times", 12))
        self.labelWarning.setText(str_text)

        self.mainlayout.addWidget(self.labelWarning)
        self.setLayout(self.mainlayout)
        self.show()


class WebCamBox(QDialog):
    def __init__(self, str_title, output_dict):  #####自己写一个warningbox
        super(WebCamBox, self).__init__(parent=None)
        self.return_value = output_dict
        self.setWindowTitle(str_title)
        self.mainlayout = QGridLayout(self)

        self.addressInput = QLineEdit()
        self.accountInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.labelTextIp = QLabel()
        self.setFont(QFont("Roman times", 12))  #####字体设置

        self.labelTextAc = QLabel()
        self.setFont(QFont("Roman times", 12))  #####字体设置

        self.labelTextPw = QLabel()
        self.setFont(QFont("Roman times", 12))  #####字体设置

        # IP地址
        self.mainlayout.addWidget(self.labelTextIp, 0, 0, 1, 12)
        self.mainlayout.addWidget(self.addressInput, 0, 4, 1, 10)
        self.labelTextIp.setText("网络IP地址：")
        # 账户名
        self.mainlayout.addWidget(self.labelTextAc, 2, 0, 1, 12)
        self.mainlayout.addWidget(self.accountInput, 2, 4, 1, 10)
        self.labelTextAc.setText("管理员账号：")
        # 密码
        self.mainlayout.addWidget(self.labelTextPw, 4, 0, 1, 12)
        self.mainlayout.addWidget(self.passwordInput, 4, 4, 1, 10)
        self.labelTextPw.setText("管理员密码：")

        self.resize(400, 100)
        self.buttonSure = QPushButton()
        self.buttonSure.setText(u"确定")
        self.buttonCancel = QPushButton()
        self.buttonCancel.setText(u"取消")

        self.mainlayout.addWidget(self.buttonSure, 6, 2, 1, 2)
        self.mainlayout.addWidget(self.buttonCancel, 6, 8, 1, 2)
        self.setLayout(self.mainlayout)
        self.buttonSure.clicked.connect(self.sureOpra)
        self.buttonCancel.clicked.connect(self.cancelOpra)
        self.show()

    def sureOpra(self):
        if checkAccount(self.accountInput.text(), self.passwordInput.text()):
            self.return_value["address"] = self.addressInput.text()
            self.return_value["status"] = "Login"
            self.close()
        else:
            self.return_value["status"] = "WrongPassword"
            falseWarning = FalseWarningBox("提示！", "密码错误")
            falseWarning.exec_()

    def cancelOpra(self):
        self.close()


if __name__ == '__main__':
    list_WebInput = {"address": "", "Status": ""}
    app = QtGui.QApplication(sys.argv)
    main_app = WebCamBox("网络摄像头管理", list_WebInput)
    app.setQuitOnLastWindowClosed(True)
    main_app.show()
    sys.exit(app.exec_())
