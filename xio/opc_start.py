import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow
from ui.log import Ui_MainWindow
import datetime


class MainApp(QMainWindow, Ui_MainWindow):

    numberOfMessage = 14
    numberOfHandledMessage = 14
    averageHandleTime = 12
    averageWarnInterval = 34
    MostFrequentWarnItem = "OP30安全门未关"

    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)

        self.action_2.triggered.connect(self.action_trigger2)
        self.action_3.triggered.connect(self.action_trigger3)
        self.action_4.triggered.connect(self.action_trigger4)

        self.pushButton.clicked.connect(self.select)
        self.pushButton_2.clicked.connect(self.monitor)

    # 菜单栏-设置-监控线设置-厚板
    def action_trigger2(self):
        self.label.setText("实时日志监控(厚板线)")
        self.label_2.setText("报警日志分析(厚板线)")

    # 菜单栏-设置-监控线设置-厚板
    def action_trigger3(self):
        self.label.setText("实时日志监控(侧板焊接线)")
        self.label_2.setText("报警日志分析(侧板焊接线)")

    # 菜单栏-设置-监控线设置-厚板
    def action_trigger4(self):
        self.label.setText("实时日志监控(新萨瓦尼尼线)")
        self.label_2.setText("报警日志分析(新萨瓦尼尼线)")

    # 按钮点击查询
    @pyqtSlot()
    def select(self):
        self.textEdit_2.append(str(self.numberOfMessage))
        self.textEdit_3.append(str(self.numberOfHandledMessage))
        self.textEdit_4.append(str(self.numberOfMessage - self.numberOfHandledMessage))
        self.textEdit_5.append(str(self.averageHandleTime) + "秒")
        self.textEdit_6.append(str(self.averageWarnInterval) + "分钟")
        self.textEdit_7.append(str(self.MostFrequentWarnItem))

    # 按钮点击开始/停止监控
    @pyqtSlot()
    def monitor(self):
        if self.pushButton_2.text() == "开始监控":
            self.pushButton_2.setText("停止监控")
            self.textEdit.append("开始监控，" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        elif self.pushButton_2.text() == "停止监控":
            self.pushButton_2.setText("开始监控")
            self.textEdit.append("停止监控，" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())



