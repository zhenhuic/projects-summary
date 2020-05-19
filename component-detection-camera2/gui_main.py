import datetime
import os
import smtplib
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QDateTime, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QImage, QPixmap

from gui.main_window import Ui_MainWindow
from gui.send_email_report_dialog import Ui_sendEmailDialog
from gui.statistics_widget import Ui_StatisticsWindow
from detect_main import main
from sql.database import DbManager, draw_bar_chart, draw_bar_graph
from util import array_to_QImage
from send_email import Email


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.titlelabel.setText("生产场景中目标的自动检测")
        self.textBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S ',
                                              time.localtime()) + '启动检测...')
        self.statusbar.showMessage('系统初始化...')

        th = DetectionThread(self)
        th.video_change_pixmap.connect(self.set_frame)
        th.record_change_pixmap.connect(self.set_record)
        self.setupMenu.triggered.connect(lambda: os.system("notepad config.py"))
        th.text_append.connect(self.append_text)
        th.status_update.connect(self.update_status_message)
        th.start()
        # print(self.videoLabel.size())
        # print(self.recordLabel.size())

        self.stream_1.triggered.connect(self.switch_vis_stream_1)
        self.stream_2.triggered.connect(self.switch_vis_stream_2)
        self.stop.triggered.connect(self.process_exit)
        self.openStatistics.triggered.connect(self.open_statistics_window)
        self.statistics_window = None

    @pyqtSlot(bool)
    def open_statistics_window(self, trigger):
        self.statistics_window = StatisticsWindow()
        self.statistics_window.show()

    @pyqtSlot(QImage)
    def set_frame(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        self.statusbar.showMessage('正在检测'
                                   + ' ' * 110 +
                                   '工位1    零件：桶，箱子')

    @pyqtSlot(QImage)
    def set_record(self, image):
        self.recordLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def append_text(self, text):
        self.textBrowser.append(text)

    @pyqtSlot(bool)
    def switch_vis_stream_1(self, trigger):
        pass
        # change_vis_stream(0)

    @pyqtSlot(bool)
    def switch_vis_stream_2(self, trigger):
        pass
        # change_vis_stream(1)

    @pyqtSlot(str)
    def update_status_message(self, text):
        self.statusbar.showMessage(text)

    @pyqtSlot(bool)
    def process_exit(self, trigger):
        sys.exit()


class DetectionThread(QThread):
    video_change_pixmap = pyqtSignal(QImage)

    record_change_pixmap = pyqtSignal(QImage)

    text_append = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def run(self):
        pass
        main(self)


class StatisticsWindow(QMainWindow, Ui_StatisticsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.select_records)
        self.sendEmailReport.triggered.connect(self.open_send_email_dialog)

        self.productionLineComboBox.setCurrentIndex(0)
        self.startDateEdit.setDate(QDate.currentDate().addDays(-1))
        self.endDateEdit.setDate(QDate.currentDate())
        self.db_manager = DbManager()

        self.send_email_records_dialog = None

    @pyqtSlot(bool)
    def select_records(self, trigger):
        start_datetime = self.startDateEdit.date().toPyDate()
        end_datetime = self.endDateEdit.date().toPyDate()
        print(start_datetime)

        start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        names = ["风管放入个数", "小包组件放入个数", "投放成功次数", "投放失败次数", "装箱次数"]
        data = self.db_manager.count_records_between_datetime("pack", start_datetime, end_datetime)

        img = draw_bar_graph(names, data)
        qimg = array_to_QImage(img, self.graphLabel.size())
        self.graphLabel.setPixmap(QPixmap.fromImage(qimg))

    @pyqtSlot(bool)
    def open_send_email_dialog(self, triggered):
        self.send_email_records_dialog = SendEmailDialog(self)
        self.send_email_records_dialog.show()


class SendEmailDialog(QDialog, Ui_sendEmailDialog):
    def __init__(self, statistic_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("发送邮件报告")
        self.statistic_window = statistic_window
        self.email_subject, self.email_content = self.get_email_subject_content()

        self.textEdit.append(self.email_subject)
        self.textEdit.append(self.email_content)

        self.buttonBox.accepted.connect(self.button_box_accepted)

    @pyqtSlot()
    def button_box_accepted(self):
        success = self.send_email_records(self.email_subject, self.textEdit.toPlainText(), self.lineEdit.text())
        msg_box = QMessageBox()
        msg_box.setWindowTitle("邮件发送反馈")
        if success:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("报告邮件发送成功^_^ ")
        else:
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("报告邮件发送失败！!")
        msg_box.show()
        msg_box.exec()

    def get_email_subject_content(self) -> (str, str):
        start_datetime = self.statistic_window.startDateEdit.date().toPyDate()
        end_datetime = self.statistic_window.endDateEdit.date().toPyDate()
        print(start_datetime)

        start_datetime = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        data = self.statistic_window.db_manager.count_records_between_datetime("pack", start_datetime, end_datetime)

        content = start_datetime[:-8] + "到" + end_datetime[:-8] + "\n" + "已放入风管个数" + str(data[0]) + "\n" \
                    + "已放入小包组件个数" + str(data[1]) + "\n" + \
                    "投放成功次数" + str(data[2]) + "\n" + "投放失败次数" + str(data[3])
        subject = "配件投放统计结果"
        return subject, content

    @staticmethod
    def send_email_records(subject: str, content: str, to_account: str) -> bool:
        try:
            Email.send_email(subject, content, from_account="layhal@163.com", SMTP_host="smtp.163.com",
                             from_password="liu670", to_account=to_account)
            print("邮件报告发送成功")
            return True
        except smtplib.SMTPException or Exception as e:
            print("邮件报告发送失败！", e)
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def gui_main():
    sys.excepthook = except_hook  # print the traceback to stdout/stderr

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())





if __name__ == '__main__':
    gui_main()
