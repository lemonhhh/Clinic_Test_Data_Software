from PyQt5.Qt import *
import math
import sys



class sample_grid(QPushButton):
    def __init__(self,flag, *args, **kwargs):
        super(sample_grid, self).__init__(*args, **kwargs)
        self.setCheckable(True)
        self.setFixedSize(QSize(20, 20))
        #样本的类型
        self.flag = flag
        #图片的路径
        self.IMG_XIBAO = QImage("./pictures/xibao.png")
        self.IMG_XUEJIANG = QImage("./pictures/xuejiang.png")
        self.IMG_NOT = QImage("./pictures/wu.png")

    def paintEvent(self,evt):

        super().paintEvent(evt)
        r = evt.rect()
        if self.isChecked():
            outer, inner = QColor(0,0,255),QColor(0,0,255)
        else:
            outer, inner = Qt.lightGray, Qt.lightGray


        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(r, QBrush(inner))

        pen = QPen(outer)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(r)

        if self.flag=="cell":
            painter.drawPixmap(r, QPixmap(self.IMG_XIBAO ))
        if self.flag=="xuejiang":
            painter.drawPixmap(r, QPixmap(self.IMG_XUEJIANG ))
        if self.flag=="not":
            painter.drawPixmap(r, QPixmap(self.IMG_NOT))

    def mouseReleaseEvent(self, e):
        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()
        if (e.button() == Qt.LeftButton):
            self.click()


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         # 网格布局
#         self.grid = QGridLayout()
#         self.grid.setSpacing(1)
#
#         w = QWidget()
#         w.setLayout(self.grid)
#         self.setCentralWidget(w)
#         self.b_size = 2
#         self.init_map()
#
#
#     def init_map(self):
#         for x in range(0, self.b_size):
#             for y in range(0, self.b_size):
#                 #创建一个widget
#                 if(x%2==0):
#                     w = sample_grid("cell",self)
#                 else:
#                     w = sample_grid("not", self)
#
#                 self.grid.addWidget(w, y, x)
#                 w.clicked.connect(self.cao)
#
#     def cao(self):
#         print("点了一下")
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     # apply_stylesheet(app, theme='dark_teal.xml')
#     win.showFullScreen()
#     win.show()
#     sys.exit(app.exec())

