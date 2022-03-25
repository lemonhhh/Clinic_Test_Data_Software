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
from pyecharts.charts import Bar
from pyecharts.charts import Tab
from pyecharts.faker import Faker


# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class ExamPatient(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(ExamPatient, self).__init__(parent)
        # 为查询进行配置
        self.db_list = []
        self.db_name = ["APTT", "Ag", "Act", "RIPA", "FV3C", "CB", "pp", "BS"]


        self.dict = {"APTT":0,"Ag":1,"全血凝固时间":2,"血浆蛋白":3,"凝血因子活性":4,"结合胆红素":5,"PP":6,"血糖":7}

        self.age_list = []
        self.gender_list = []

        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()

        self.generate_data()
        # 初始化ui
        self.initUI()

    def generate_data(self):
        #总体情况
        for item in self.db_name:
            sql = """select %s from Exam_table where %s is not null""" % (item,item)
            self.cursor.execute(sql)
            tuple_data = list(self.cursor.fetchall())
            list_data = [i[0] for i in tuple_data]
            self.db_list.append(list_data)


        #按性别
        for item in self.db_name:
            sql_f = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
WHERE Patient_table.gender='女' and Exam_table.%s is not null""" % (item,item)
            self.cursor.execute(sql_f)
            ftuple_data = list(self.cursor.fetchall())
            flist_data = [i[0] for i in tuple_data]

            sql_m = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
            WHERE Patient_table.gender='男' and Exam_table.%s is not null""" % (item, item)
            self.cursor.execute(sql_m)
            mtuple_data = list(self.cursor.fetchall())
            mlist_data = [i[0] for i in mtuple_data]

            item_gender = {'女': flist_data, '男': mlist_data}

            self.gender_list.append(item_gender)


        #按年龄
        for i in self.db_name:
            sql1 = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
        WHERE Patient_table.Age<18 and Exam_table.%s is not null""" % (item,item)
            self.cursor.execute(sql1)
            tuple1 = list(self.cursor.fetchall())
            list1 = [i[0] for i in tuple1]

            sql2 = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                WHERE Patient_table.Age>18 and  Patient_table.Age<=35 and Exam_table.%s is not null""" % (item,item)
            self.cursor.execute(sql2)
            tuple2 = list(self.cursor.fetchall())
            list2 = [i[0] for i in tuple2]

            sql3 = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                        WHERE Patient_table.Age>35 and  Patient_table.Age<=60 and Exam_table.%s  is not null""" %(item,item)

            self.cursor.execute(sql3)
            tuple3 = list(self.cursor.fetchall())
            list3 = [i[0] for i in tuple3]

            sql4 = """SELECT Exam_table.%s FROM Exam_table INNER JOIN Patient_table ON Exam_table.patient_ID=Patient_table.patient_ID  
                                WHERE Patient_table.Age>60 and Exam_table.%s is not null""" % (item,item)

            self.cursor.execute(sql4)
            tuple4 = list(self.cursor.fetchall())
            list4 = [i[0] for i in tuple4]

            item_age = {'18以下': list1, '18-35': list2,'35-60':list3,"60以上":list4}
            self.age_list.append(item_age)


    def initUI(self):
        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)

        self.cb = QComboBox()
        self.cb.addItems(["血型","APTT", "Ag", "全血凝固时间","血浆蛋白","凝血因子活性","结合胆红素","PP","血糖"])

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
            self.ShowExamPatiemt(self.cb.currentText())


    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)

    def ShowExamPatiemt(self,project):
        tab = Tab()
        tab.add(self.show_all_boxplot(project), "总体")
        tab.add(self.show_gender_boxplot(project), "按性别")
        tab.add(self.show_age_boxplot(project), "按年龄")


        tab.render("exam_patient_boxplot.html")
        self.load_url("exam_patient_boxplot.html")


    def show_all_boxplot(self,project)->Boxplot:
        v1 = [self.db_list[self.dict[project]]]
        c = Boxplot()
        c.add_xaxis([project])
        c.add_yaxis(project,c.prepare_data(v1))
        c.set_global_opts(title_opts=opts.TitleOpts(title="所有数据"))
        return c

    def show_gender_boxplot(self,project)->Boxplot:
        i = self.dict[project]
        v1 = [self.gender_list[i]['女']]

        v2 = [self.gender_list[i]['男']]

        c = Boxplot()
        c.add_xaxis([project])

        c.add_yaxis("女", c.prepare_data(v1))
        c.add_yaxis("男", c.prepare_data(v2))
        c.set_global_opts(title_opts=opts.TitleOpts(title="按性别"))
        return c

    def show_age_boxplot(self,project)->Boxplot:
        v1 = [self.age_list[self.dict[project]]['18以下']]
        v2 = [self.age_list[self.dict[project]]['18-35']]
        v3 = [self.age_list[self.dict[project]]['35-60']]
        v4 = [self.age_list[self.dict[project]]['60以上']]

        c = Boxplot()
        c.add_xaxis([project])

        c.add_yaxis("18以下", c.prepare_data(v1))
        c.add_yaxis("18-35", c.prepare_data(v2))
        c.add_yaxis("35-60", c.prepare_data(v3))
        c.add_yaxis("60以上", c.prepare_data(v4))

        c.set_global_opts(title_opts=opts.TitleOpts(title="按年龄"))
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
