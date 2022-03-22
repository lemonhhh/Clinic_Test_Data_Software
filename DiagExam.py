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

#作图相关
import pyecharts.options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Boxplot
from pyecharts.components import Table
from pyecharts.charts import Bar,Pie
from pyecharts.charts import Tab
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class DiagExam(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(DiagExam, self).__init__(parent)
        # 为查询进行配置
        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]
        self.dict = {"APTT":0,"Ag":1,"全血凝固时间":2,"血浆蛋白":3,"凝血因子活性":4,"结合胆红素":5,"PP":6,"血糖":7}
        self.age_list = []
        self.gender_list = []

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()



        # 初始化ui
        self.initUI()




    def initUI(self):
        self.setWindowTitle("按病人分析诊断结果")
        self.setMinimumSize(1200, 800)

        self.cb = QComboBox()
        self.cb.addItems(["按照VWD亚型分析","按照血友病分析", "按照出血/血栓分析"])
        self.btn = QPushButton("确定", self)  # 确定按钮

        self.btn.clicked.connect(self.cao)  # 绑定槽函数，确定后，显示后续所有ui

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.cb)
        hlayout.addWidget(self.btn)

        hwidget = QWidget(self)
        hwidget.setLayout(hlayout)

        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.setVisible(False)
        self.myHtml.move(10, 50)
        self.myHtml.resize(1000, 600)



    def cao(self):
        self.myHtml.setVisible(True)
        if self.cb.currentText() == '按照VWD亚型分析':
            x_data = ['1','2A','2B','2M','2N','3']
            column = 'vwd_type'
        elif self.cb.currentText() == '按照血友病分析':
            x_data = ['A','B','VWD']
            column = 'haemophilia_type'
        elif self.cb.currentText() == '按照出血/血栓分析':
            x_data = ['出血病','血栓病']
            column = 'binary_type'

        self.type_exam_chart(x_data,column)


    def type_exam_chart(self,x_data,column):
        tab = Tab()
        tab.add(self.type_blood_bar(x_data, column), "血型")
        tab.add(self.type_exam_boxplot(x_data, column, "APTT", "APTT分析"), "APTT")
        tab.add(self.type_exam_boxplot(x_data, column, "Ag", "Ag分析"), "Ag")
        tab.add(self.type_exam_boxplot(x_data, column, "Act", "Act分析"), "Act")
        tab.add(self.type_exam_boxplot(x_data, column, "RIPA", "RIPA分析"), "RIPA")
        tab.add(self.type_exam_boxplot(x_data, column, "FV3C", "FV3C分析"), "FV3C")


        tab.render("vwd_exam_tab.html")
        self.load_url("vwd_exam_tab.html")

    def type_blood_bar(self,x_data,column):
        a = []
        b = []
        o = []
        ab = []

        for x in x_data:
            sql_a = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='A' AND Diagnosis_table.%s='%s'""" % (column,x)

            sql_b = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='B' AND Diagnosis_table.%s='%s'""" % (column,x)
            sql_o = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='O' AND Diagnosis_table.%s='%s'""" % (column,x)
            sql_ab = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Exam_table ON Diagnosis_table.patient_ID=Exam_table.patient_ID
            WHERE Exam_table.Blood_type='AB' AND Diagnosis_table.%s='%s'""" % (column,x)

            print(sql_a)

            self.cursor.execute(sql_a)
            a_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_b)
            b_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_o)
            o_num = self.cursor.fetchone()[0]
            self.cursor.execute(sql_ab)
            ab_num = self.cursor.fetchone()[0]

            if(a_num + b_num+o_num+ab_num == 0):
                a_ration = b_ration = o_ration = ab_ration = 0
            else:
                a_ration = a_num / (a_num + b_num+o_num+ab_num)
                b_ration = b_num / (a_num + b_num+o_num+ab_num)
                o_ration = o_num / (a_num + b_num+o_num+ab_num)
                ab_ration = ab_num / (a_num + b_num+o_num+ab_num)
            a.append(a_ration)
            b.append(b_ration)
            o.append(o_ration)
            ab.append(ab_ration)

        c = (
            Bar()
                .add_xaxis(x_data)
                .add_yaxis("A", a, stack="stack1")
                .add_yaxis("B", b, stack="stack1")
                .add_yaxis("O", o, stack="stack1")
                .add_yaxis("AB", ab, stack="stack1")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="血型"))
        )
        return c


    def type_exam_boxplot(self,x_data,column,project,title):

        exam_list = []
        for x in x_data:
            sql = """SELECT Exam_table.%s FROM Diagnosis_table INNER JOIN Exam_table ON Exam_table.patient_ID = Diagnosis_table.patient_ID
                        WHERE Diagnosis_table.%s='%s' AND Exam_table.%s is not null""" %(project,column,x,project)

            self.cursor.execute(sql)

            exam = [i[0] for i in self.cursor.fetchall()]
            exam_list.append((exam))

        c = Boxplot()
        c.add_xaxis([title])

        for i in range(len(x_data)):
            c.add_yaxis(x_data[i], c.prepare_data([exam_list[i]]))

        c.set_global_opts(title_opts=opts.TitleOpts(title=title))
        return c





    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)






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
