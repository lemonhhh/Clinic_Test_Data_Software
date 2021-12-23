from PyQt5.Qt import *
import math
import sys

IMG_START = QImage("./UI/pictures/box-label.png")
class Btn(QPushButton):

    def hitButton(self,point):
        yuanxin_x = self.width()/2
        yuanxin_y = self.height()/2
        hit_x = point.x()
        hit_y = point.y()
        distance = math.sqrt(math.pow(hit_x-yuanxin_x,2)+math.pow(hit_y-yuanxin_y,2))
        if distance<self.width()/2:
            return True
        else:
            return False


    def paintEvent(self,evt):
        super().paintEvent(evt)

        # r = evt.rect()
        # color = self.palette().color(QPalette.Background)
        # outer, inner = color, color

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)
        # painter.fillRect(r, QBrush(inner))
        #
        # pen = QPen(outer)
        # pen.setWidth(1)
        # painter.setPen(pen)
        # painter.drawRect(r)
        # painter.drawPixmap(r, QPixmap(IMG_START))

        painter.setPen(QPen(QColor(100,100,200),6))
        painter.drawEllipse(self.rect())





