from Database.utils import *
from QTDesigner.delete import Ui_Dialog_delete
from QTDesigner.fetch import Ui_Dialog_fetch

from QTDesigner.main import *
from QTDesigner.add import *
import matplotlib
import warnings
from matplotlib.figure import Figure
import sys
import numpy as np
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties

from QTDesigner.reporter import Ui_Dialog_reporter

warnings.filterwarnings("ignore")
matplotlib.use("Qt5Agg")  # 声明使用QT5
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


class MyFigure(FigureCanvas):
    def __init__(self, width=4, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.yaxis.set_major_locator(mtick.MaxNLocator(integer=True))
