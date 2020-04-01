import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap

from gui.main_window import Ui_MainWindow
from detect_main import main


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S ',
                                              time.localtime()) + '启动检测...')
        self.statusbar.showMessage('系统初始化...')

        th = DetectionThread(self)
        th.video_change_pixmap.connect(self.set_frame)
        th.record_change_pixmap.connect(self.set_record)
        th.text_append.connect(self.append_text)
        th.status_update.connect(self.update_status_message)
        th.start()
        # print(self.videoLabel.size())
        # print(self.recordLabel.size())

        self.stream_1.triggered.connect(self.switch_vis_stream_1)
        self.stream_2.triggered.connect(self.switch_vis_stream_2)
        self.stop.triggered.connect(self.process_exit)

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
