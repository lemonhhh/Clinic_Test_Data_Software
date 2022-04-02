# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json
import numpy as np

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QComboBox, QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl

# 作图相关
import pyecharts.options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Boxplot
from pyecharts.components import Table
from pyecharts.charts import Bar
from pyecharts.charts import Tab
from pyecharts.faker import Faker


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class ExamDiagnosis(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(ExamDiagnosis, self).__init__(parent)
        # 为查询进行配置
        self.db_list = []
        self.vwd_list = []
        self.haemophilia_list = []
        self.binary_list = []

        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]

        self.dict = {
            "APTT": 0,
            "Ag": 1,
            "全血凝固时间": 2,
            "血浆蛋白": 3,
            "凝血因子活性": 4,
            "结合胆红素": 5,
            "PP": 6,
            "血糖": 7}

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()

        self.generate_data()
        # 初始化ui
        self.initUI()

    def generate_data(self):
        # 总体情况
        for item in self.db_name:
            sql = """select %s from Exam_table where %s is not null""" % (
                item, item)
            self.cursor.execute(sql)
            tuple_data = list(self.cursor.fetchall())
            list_data = [i[0] for i in tuple_data]
            self.db_list.append(list_data)

        # 按vwd
        for item in self.db_name:
            x_type = ['1', '2A', '2B', '2M', '2N', '3']
            item_vwd = {}
            for x in x_type:
                sql = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Diagnosis_table ON Exam_table.patient_ID=Diagnosis_table.patient_ID
    WHERE Diagnosis_table.vwd_type='%s' and Exam_table.%s is not null""" % (item, x, item)
                self.cursor.execute(sql)
                tuple_data = list(self.cursor.fetchall())
                list_data = [i[0] for i in tuple_data]
                item_vwd[x] = list_data

            self.vwd_list.append(item_vwd)

        # 按血友病类型
        for item in self.db_name:
            x_type = ['A', 'B', 'VWD']
            item_hae = {}
            for x in x_type:
                sql = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Diagnosis_table ON Exam_table.patient_ID=Diagnosis_table.patient_ID
    WHERE Diagnosis_table.haemophilia_type='%s' and Exam_table.%s is not null""" % (item, x, item)
                self.cursor.execute(sql)
                tuple_data = list(self.cursor.fetchall())
                list_data = [i[0] for i in tuple_data]
                item_hae[x] = list_data

            self.haemophilia_list.append(item_hae)

        # 按出血/血栓
        for item in self.db_name:
            x_type = ['出血病', '血栓病']
            item_binary = {}
            for x in x_type:
                sql = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Diagnosis_table ON Exam_table.patient_ID=Diagnosis_table.patient_ID
    WHERE Diagnosis_table.binary_type='%s' and Exam_table.%s is not null""" % (item, x, item)
                self.cursor.execute(sql)
                tuple_data = list(self.cursor.fetchall())
                list_data = [i[0] for i in tuple_data]
                item_binary[x] = list_data

            self.binary_list.append(item_binary)

    def initUI(self):
        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)

        self.cb = QComboBox()
        self.cb.addItems(["血型", "APTT", "Ag", "全血凝固时间",
                          "血浆蛋白", "凝血因子活性", "结合胆红素", "PP", "血糖"])

        self.btn = QPushButton("确定", self)  # 确定按钮
        self.btn.clicked.connect(self.cao)  # 绑定槽函数，确定后，显示后续所有ui

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.cb)
        hlayout.addWidget(self.btn)

        hwidget = QWidget(self)
        hwidget.setLayout(hlayout)

        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.move(10, 50)
        self.myHtml.resize(1000, 600)

    def cao(self):

        if self.cb.currentText() == '血型':
            pass
        else:
            self.ShowExamDiagosis(self.cb.currentText())

    def load_url(self, file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

    def ShowExamDiagosis(self, project):
        tab = Tab()
        tab.add(self.show_all_boxplot(project), "总体")
        tab.add(self.show_vwd_boxplot(project), "按VWD类型")
        tab.add(self.show_haemophilia_boxplot(project), "按血友病类型")
        tab.add(self.show_binary_boxplot(project), "按出血/血栓")

        tab.render("exam_diagnosis_boxplot.html")
        self.load_url("exam_diagnosis_boxplot.html")

    def show_all_boxplot(self, project) -> Boxplot:
        v1 = [self.db_list[self.dict[project]]]
        c = Boxplot()
        c.add_xaxis([project])
        c.add_yaxis(project, c.prepare_data(v1))
        c.set_global_opts(title_opts=opts.TitleOpts(title="所有数据"))
        return c

    def show_vwd_boxplot(self, project) -> Boxplot:
        i = self.dict[project]

        v1 = [self.vwd_list[i]['1']]
        v2 = [self.vwd_list[i]['2A']]
        v3 = [self.vwd_list[i]['2B']]
        v4 = [self.vwd_list[i]['2M']]
        v5 = [self.vwd_list[i]['2N']]
        v6 = [self.vwd_list[i]['3']]

        c = Boxplot()
        c.add_xaxis([project])

        c.add_yaxis("1", c.prepare_data(v1))
        c.add_yaxis("2A", c.prepare_data(v2))
        c.add_yaxis("2B", c.prepare_data(v3))
        c.add_yaxis("2M", c.prepare_data(v4))
        c.add_yaxis("2N", c.prepare_data(v5))
        c.add_yaxis("3", c.prepare_data(v6))

        c.set_global_opts(title_opts=opts.TitleOpts(title="按vwd类型"))
        return c

    def show_haemophilia_boxplot(self, project) -> Boxplot:
        v1 = [self.haemophilia_list[self.dict[project]]['A']]
        v2 = [self.haemophilia_list[self.dict[project]]['B']]
        v3 = [self.haemophilia_list[self.dict[project]]['VWD']]

        c = Boxplot()
        c.add_xaxis([project])

        c.add_yaxis("A", c.prepare_data(v1))
        c.add_yaxis("B", c.prepare_data(v2))
        c.add_yaxis("VWD", c.prepare_data(v3))
        c.set_global_opts(title_opts=opts.TitleOpts(title="按血友病类型"))
        return c

    def show_binary_boxplot(self, project) -> Boxplot:
        i = self.dict[project]

        v1 = [self.binary_list[i]['出血病']]
        v2 = [self.binary_list[i]['血栓病']]

        c = Boxplot()
        c.add_xaxis([project])

        c.add_yaxis("出血病", c.prepare_data(v1))
        c.add_yaxis("血栓病", c.prepare_data(v2))

        c.set_global_opts(title_opts=opts.TitleOpts(title="出血/血栓"))
        return c


##  ============================== 功能函数区 ==============================#

    # 设置cursor和connection


    def set_connection_cursor(self) -> None:
        self.connection = get_sql_connection()
        self.cursor = self.connection.cursor()

    def set_logger(self) -> None:
        self.logger = get_logger("my_logger")

    # 记录Debug信息

    def record_debug(self, debug_message: str) -> None:
        self.logger.debug("语句错误，错误原因为{}".format(debug_message))
