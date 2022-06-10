# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import numpy as np
from sklearn import manifold
import pyecharts.options as opts
from pyecharts.charts import Scatter
import random
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox,QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
from UI.Ui_ClusterWindow import Ui_Dialog


import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message




class ClusterSHow(QDialog):
    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(ClusterSHow, self).__init__(parent)

        self.connection = None
        self.cursor = None
        self.logger = None
        self.set_connection_cursor()
        self.set_logger()

        self.__UI = Ui_Dialog()
        self.__UI.setupUi(self)


    @pyqtSlot()
    def on_btn_confirm_clicked(self):
        x,y = self.get_data(self.get_check_list())
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=501)
        X_tsne = tsne.fit_transform(x)
        x_min, x_max = X_tsne.min(0), X_tsne.max(0)
        X_norm = (X_tsne - x_min) / (x_max - x_min)

        self.generate_chart(X_norm,y)



    def get_check_list(self):
        check_list = []
        if self.__UI.cb_age.isChecked():
            check_list.append('Age')
        if self.__UI.cb_aptt.isChecked():
            check_list.append('APTT')
        if self.__UI.cb_ag.isChecked():
            check_list.append('Ag')
        if self.__UI.cb_act.isChecked():
            check_list.append('Act')
        if self.__UI.cb_ripa.isChecked():
            check_list.append('RIPA')
        if self.__UI.cb_fv3c.isChecked():
            check_list.append('FV3C')
        if self.__UI.cb_cb.isChecked():
            check_list.append('CB')
        if self.__UI.cb_pp.isChecked():
            check_list.append('pp')
        if self.__UI.cb_bs.isChecked():
            check_list.append('BS')

        return check_list

    def get_data(self,lists):

        y = None
        sql = """select vwd_type
                from Exam_table inner join Patient_table INNER JOIN Diagnosis_table
                on Exam_table.patient_ID = Patient_table.patient_ID AND Patient_table.patient_ID=Diagnosis_table.patient_ID
                and vwd_type is not null"""
        self.cursor.execute(sql)

        y = self.cursor.fetchall()
        y = np.asarray([i[0] for i in y])


        x = np.empty(shape=(y.shape[0],len(lists)))

        idx = 0
        for project in lists:
            sql = """select %s
                from Exam_table inner join Patient_table inner join Diagnosis_table
                on Exam_table.patient_ID = Patient_table.patient_ID 
                and Patient_table.patient_ID=Diagnosis_table.patient_ID
                and vwd_type is not null""" % (project)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()

            data = [i[0] for i in data]
            x[:,idx] = data
            idx += 1

        x[np.isnan(x)] = 0

        return x,y


    def load_url(self,object,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        object.load(local_url)

    def generate_chart(self,x,y):
        print(np.unique(y))
        x1 = x[y=='1']
        y1 = [y=='1']



        x2 = x[y == '2A']
        y2 = [y == '2A']
        x3 = x[y == '2B']
        y3 = [y == '2B']
        x4 = x[y == '2M']
        y4 = [y == '2M']
        x5 = x[y == '2N']
        y5 = [y == '2N']
        x6 = x[y == '3']
        y6 = [y == '3']

        plt.figure(figsize=(20,20))
        plt.scatter([d[0] for d in x1], [d[1] for d in x1], c='red',label='1')
        plt.scatter([d[0] for d in x2], [d[1] for d in x2], c='green',label='2A')
        plt.scatter([d[0] for d in x3], [d[1] for d in x3], c='blue',label='2B')
        plt.scatter([d[0] for d in x4], [d[1] for d in x4], c='orange',label='2M')
        plt.scatter([d[0] for d in x5], [d[1] for d in x5], c='yellow',label='2N')
        plt.scatter([d[0] for d in x6], [d[1] for d in x6], c='pink',label='3')
        plt.legend()
        plt.xticks(np.arange(0,1))
        plt.xticks(np.arange(0, 1))
        plt.show()



##---------------------------------函数实现-----------------------


#--------数据库相关函数-------

    # 设置cursor和connection
    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

        # 设置日志处理器
    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
