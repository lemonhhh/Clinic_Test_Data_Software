import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        data = [36.2, 46.0, 70.0, 57.7, 34.7, 40.5, 30.2, 46.6, 40.8, 37.4, 28.1, 31.8, 41.9, 29.3, 33.3, 47.7, 40.9, 37.4, 36.0, 66.0, 47.1, 40.4, 31.9, 31.1, 96.5, 32.2, 28.8, 36.3, 34.7, 63.7, 36.2, 102.5, 102.5, 35.5, 35.5, 33.8, 33.8, 32.4, 41.6, 37.8, 31.3, 36.6, 36.6, 56.9, 56.9, 36.2, 32.9, 41.9, 47.5, 63.0, 63.0, 48.0, 48.0, 45.6, 45.6, 49.7, 45.2, 45.2, 42.5, 42.5, 41.0, 41.0, 51.3, 47.6, 47.6, 40.4, 40.2, 44.1, 44.1, 66.7, 66.7, 62.0, 62.0, 58.0, 58.0, 55.2, 55.2, 65.1, 72.0, 72.0, 54.6, 64.6, 57.4, 71.0, 57.0, 57.0, 67.7, 64.5, 60.8, 68.6, 82.8, 82.8, 79.7, 54.3, 54.3, 63.6, 63.6, 80.9, 80.9, 58.2, 58.2, 65.4, 52.2, 52.2, 78.3, 78.3, 64.7, 62.5, 62.5, 58.2, 58.2, 54.7, 54.7, 58.1, 58.1, 56.2, 56.2, 70.9, 70.9, 45.3, 45.3, 48.0, 42.0, 37.0, 49.4, 47.0, 41.1, 41.1, 43.1, 42.5, 43.0, 42.7, 47.9, 50.0, 50.0, 36.0, 42.3, 44.0, 51.5, 31.7, 53.0, 40.3, 37.2, 37.2, 37.2, 37.2, 44.3, 45.4, 45.4, 43.2, 43.2, 40.5, 55.0, 36.8, 47.0, 49.0, 49.4, 36.8, 36.1, 36.1, 36.1, 36.1, 35.9, 38.4, 38.5, 40.7, 31.5, 31.5, 39.2, 34.0, 34.0, 47.3, 42.2, 43.5, 37.6, 37.4, 35.3, 35.3, 35.6, 39.0, 45.7, 110.0, 110.0, 62.9, 62.9, 63.2, 63.2, 61.8, 60.2, 60.2, 37.2, 37.0]
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        num_bins = 40
        # n, bins, patches = sc.axes.hist(data, num_bins,
        #                                      density=1,
        #                                      alpha=0.7)

        # 工具栏
        toolbar = NavigationToolbar(sc, self)

        btn = QPushButton("hihihi")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()