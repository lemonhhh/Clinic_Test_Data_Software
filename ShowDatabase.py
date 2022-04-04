# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import datetime

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView

#导入ui
from UI.Ui_DatabaseWindow import Ui_Dialog


class ShowDatabase(QDialog):
    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(ShowDatabase, self).__init__(parent)
        #设置ui
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)





