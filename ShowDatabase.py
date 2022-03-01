# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import datetime

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

#模块
from ShowDataDialog import ShowDataDialog
from Util.Common import get_sql_connection, get_logger, show_error_message

#导入ui
from UI.Ui_DatabaseWindow import Ui_Dialog



class ShowDatabase(QDialog):
    data_signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        #继承所有dialog的方法
        super(ShowDatabase, self).__init__(parent)
        #设置ui
        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)





