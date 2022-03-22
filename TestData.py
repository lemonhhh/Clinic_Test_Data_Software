# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
import numpy as np

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

from UI.Ui_TestWindow import Ui_Dialog


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class TestExam(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(TestExam, self).__init__(parent)
        self.data_list = []

        self.connection = None
        self.cursor = None
        self.logger = None
        self.set_connection_cursor()
        self.set_logger()

        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        group = self.__UI.comboBox_group.currentText()
        project = self.__UI.comboBox_data.currentText()
        method = self.__UI.comboBox_method.currentText()

        #先取数据
        self.data_list = self.get_data(group,project)


        if method=='T-test':
            pass
            self.t_test()
        elif method=='ANOVA':
            pass
        elif method=='Mann-Whitney':
            pass
        elif method=='Kruskal-Wallis':
            pass


        self.__UI.label_result.setText("hi hi hi")

    def get_data(self,group,project):
        if group == 'VWD类型':
            x_group = ['1','2A','2B','2M','2N','3']
            for x in x_group:
                if(project!='年龄'):
                    sql = """SELECT Exam_table.%s FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
                     WHERE Diagnosis_table.%s='%s'""" % (project,'vwd_type',x)
                    print(sql)
                    self.cursor.execute(sql)
                    data = [i[0] for i in self.cursor.fetchall()]
                    print(data)
                else:
                    pass
        else:
            pass

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

        # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
