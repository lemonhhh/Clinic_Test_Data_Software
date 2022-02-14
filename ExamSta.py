# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import json


from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView, QTableView, QWidget, QHBoxLayout, QFrame, \
    QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QUrl
import pyecharts.options as opts
from pyecharts.charts import Boxplot

# 模块
from Util.Common import get_sql_connection, get_logger, show_error_message


class ExamStatis(QDialog):

    def __init__(self, parent=None):
        # 继承所有dialog的方法
        super(ExamStatis, self).__init__(parent)
        # 初始化ui
        self.initUI()
        # 为查询进行配置
        self.logger = None
        self.connection = None
        self.cursor = None
        self.set_connection_cursor()  # 建立连接
        self.set_logger()

    def initUI(self):
        self.setWindowTitle("检验结果分析统计")
        self.setMinimumSize(1200, 800)
        btn0 = QPushButton("总体")
        btn1 = QPushButton("按性别")
        btn2 = QPushButton("按年龄")
        btn3 = QPushButton("按疾病")

        hlayout = QHBoxLayout()

        hlayout.addWidget(btn0)
        hlayout.addWidget(btn1)
        hlayout.addWidget(btn2)
        hlayout.addWidget(btn3)

        hwidget = QWidget(self)
        hwidget.setLayout(hlayout)


        btn0.clicked.connect(self.sta_all)
        btn1.clicked.connect(self.sta_gender)
        btn2.clicked.connect(self.sta_age)
        btn3.clicked.connect(self.sta_ill)

        self.myHtml = QWebEngineView(self)  # 浏览器引擎控件
        self.myHtml.move(10, 50)
        self.myHtml.resize(1000, 600)

    def load_url(self,file_name):
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                file_name))
        local_url = QUrl.fromLocalFile(file_path)
        self.myHtml.load(local_url)



    def sta_all(self):
        sql_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID)"""
        self.cursor.execute(sql_pt)
        pt_tuple = self.cursor.fetchall()
        pt_list = [i[0] for i in pt_tuple]

        sql_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID)"""
        self.cursor.execute(sql_aptt)
        aptt_tuple = self.cursor.fetchall()
        aptt_list = [i[0] for i in aptt_tuple]

        sql_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID)"""
        self.cursor.execute(sql_fib)
        fib_tuple = self.cursor.fetchall()
        fib_list = [i[0] for i in fib_tuple]

        sql_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID)"""
        self.cursor.execute(sql_tt)
        tt_tuple = self.cursor.fetchall()
        tt_list = [i[0] for i in tt_tuple]

        data_all = [pt_list, aptt_list, fib_list, tt_list]


        c = Boxplot()
        c.add_xaxis(["pt", "aptt", "fib", "tt"])
        c.add_yaxis("全部", c.prepare_data(data_all))
        c.set_global_opts(title_opts=opts.TitleOpts(title="全部"))
        c.render("boxplot_all.html")
        self.load_url("boxplot_all.html")




    def sta_gender(self):
        # 数据查询
        # 所有男性的pt
        sql_male_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='男' """
        self.cursor.execute(sql_male_pt)
        male_pt_tuple = self.cursor.fetchall()
        male_pt_list = [i[0] for i in male_pt_tuple]
        #所有女性的pt
        sql_female_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='女' """
        self.cursor.execute(sql_female_pt)
        female_pt_tuple = self.cursor.fetchall()
        female_pt_list = [i[0] for i in female_pt_tuple]

        #所有男性的aptt
        sql_male_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='男' """
        self.cursor.execute(sql_male_aptt)
        male_aptt_tuple = self.cursor.fetchall()
        male_aptt_list = [i[0] for i in male_aptt_tuple]
        # 所有女性的aptt
        sql_female_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='女' """
        self.cursor.execute(sql_female_aptt)
        female_aptt_tuple = self.cursor.fetchall()
        female_aptt_list = [i[0] for i in female_aptt_tuple]


        #所有男性的fib
        sql_male_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='男' """
        self.cursor.execute(sql_male_fib)
        male_fib_tuple = self.cursor.fetchall()
        male_fib_list = [i[0] for i in male_fib_tuple]
        #所有女性的fib
        sql_female_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='女' """
        self.cursor.execute(sql_female_fib)
        female_fib_tuple = self.cursor.fetchall()
        female_fib_list = [i[0] for i in female_fib_tuple]

        #所有男性的tt
        sql_male_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='男' """
        self.cursor.execute(sql_male_tt)
        male_tt_tuple = self.cursor.fetchall()
        male_tt_list = [i[0] for i in male_tt_tuple]
        #所有女性的tt
        sql_female_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.gender='女' """
        self.cursor.execute(sql_female_tt)
        female_tt_tuple = self.cursor.fetchall()
        female_tt_list = [i[0] for i in female_tt_tuple]

        # 嵌套列表 长度：4
        # 顺序：pt,aptt,fib,tt

        data_male = [male_pt_list,male_aptt_list,male_fib_list,male_tt_list]
        data_female = [female_pt_list,female_aptt_list,female_fib_list,female_tt_list]

        c = Boxplot()
        c.add_xaxis(["pt", "aptt", "fib", "tt"])
        c.add_yaxis("男性", c.prepare_data(data_male))
        c.add_yaxis("女性", c.prepare_data(data_female))
        c.set_global_opts(title_opts=opts.TitleOpts(title="按性别"))
        c.render("boxplot_gender.html")

        self.load_url("boxplot_gender.html")



    def sta_age(self):
        # pt
        sql_age1_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age<18 """
        self.cursor.execute(sql_age1_pt)
        age1_pt_tuple = self.cursor.fetchall()
        age1_pt_list = [i[0] for i in age1_pt_tuple]

        sql_age2_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=18 and patients.age<=35 """
        self.cursor.execute(sql_age2_pt)
        age2_pt_tuple = self.cursor.fetchall()
        age2_pt_list = [i[0] for i in age2_pt_tuple]

        sql_age3_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=36 and patients.age<=60 """
        self.cursor.execute(sql_age3_pt)
        age3_pt_tuple = self.cursor.fetchall()
        age3_pt_list = [i[0] for i in age3_pt_tuple]

        sql_age4_pt = """SELECT exam_result.pt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>60 """
        self.cursor.execute(sql_age4_pt)
        age4_pt_tuple = self.cursor.fetchall()
        age4_pt_list = [i[0] for i in age4_pt_tuple]

        #aptt
        sql_age1_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age<18 """
        self.cursor.execute(sql_age1_aptt)
        age1_aptt_tuple = self.cursor.fetchall()
        age1_aptt_list = [i[0] for i in age1_aptt_tuple]

        sql_age2_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=18 and patients.age<=35 """
        self.cursor.execute(sql_age2_aptt)
        age2_aptt_tuple = self.cursor.fetchall()
        age2_aptt_list = [i[0] for i in age2_aptt_tuple]

        sql_age3_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=36 and patients.age<=60 """
        self.cursor.execute(sql_age3_aptt)
        age3_aptt_tuple = self.cursor.fetchall()
        age3_aptt_list = [i[0] for i in age3_aptt_tuple]

        sql_age4_aptt = """SELECT exam_result.aptt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>60 """
        self.cursor.execute(sql_age4_aptt)
        age4_aptt_tuple = self.cursor.fetchall()
        age4_aptt_list = [i[0] for i in age4_aptt_tuple]

        #fib
        sql_age1_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age<18 """
        self.cursor.execute(sql_age1_fib)
        age1_fib_tuple = self.cursor.fetchall()
        age1_fib_list = [i[0] for i in age1_fib_tuple]

        sql_age2_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=18 and patients.age<=35 """
        self.cursor.execute(sql_age2_fib)
        age2_fib_tuple = self.cursor.fetchall()
        age2_fib_list = [i[0] for i in age2_fib_tuple]

        sql_age3_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=36 and patients.age<=60 """
        self.cursor.execute(sql_age3_fib)
        age3_fib_tuple = self.cursor.fetchall()
        age3_fib_list = [i[0] for i in age3_fib_tuple]

        sql_age4_fib = """SELECT exam_result.fib FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>60 """
        self.cursor.execute(sql_age4_fib)
        age4_fib_tuple = self.cursor.fetchall()
        age4_fib_list = [i[0] for i in age4_fib_tuple]

        #tt
        sql_age1_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age<18 """
        self.cursor.execute(sql_age1_tt)
        age1_tt_tuple = self.cursor.fetchall()
        age1_tt_list = [i[0] for i in age1_tt_tuple]

        sql_age2_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=18 and patients.age<=35 """
        self.cursor.execute(sql_age2_tt)
        age2_tt_tuple = self.cursor.fetchall()
        age2_tt_list = [i[0] for i in age2_tt_tuple]

        sql_age3_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>=36 and patients.age<=60 """
        self.cursor.execute(sql_age3_tt)
        age3_tt_tuple = self.cursor.fetchall()
        age3_tt_list = [i[0] for i in age3_tt_tuple]

        sql_age4_tt = """SELECT exam_result.tt FROM (patients INNER JOIN exam_result ON exam_result.patient_ID = patients.patient_ID) WHERE patients.age>60 """
        self.cursor.execute(sql_age4_tt)
        age4_tt_tuple = self.cursor.fetchall()
        age4_tt_list = [i[0] for i in age4_tt_tuple]

        data_age1 = [age1_pt_list, age1_aptt_list, age1_fib_list, age1_tt_list]
        data_age2 = [age2_pt_list, age2_aptt_list, age2_fib_list, age2_tt_list]
        data_age3 = [age3_pt_list, age3_aptt_list, age3_fib_list, age3_tt_list]
        data_age4 = [age4_pt_list, age4_aptt_list, age4_fib_list, age4_tt_list]


        c = Boxplot()
        c.add_xaxis(["pt", "aptt", "fib", "tt"])
        c.add_yaxis("18以下", c.prepare_data(data_age1))
        c.add_yaxis("18-35", c.prepare_data(data_age2))
        c.add_yaxis("16-60", c.prepare_data(data_age3))
        c.add_yaxis("60以上", c.prepare_data(data_age4))
        c.set_global_opts(title_opts=opts.TitleOpts(title="按年龄"))
        c.render("boxplot_age.html")
        self.load_url("boxplot_age.html")

    def sta_ill(self):
        print("按疾病")

    def generate_data(self):
        # 血浆的数量
        sql1 = """select count(*) from t_sample where t_sample.type = "血浆" """
        cursor1 = self.connection.cursor()
        cursor1.execute(sql1)
        xuejiang = cursor1.fetchone()[0]
        # 血细胞
        sql2 = """select count(*) from t_sample where t_sample.type = "血细胞" """
        cursor2 = self.connection.cursor()
        cursor2.execute(sql2)
        cell = cursor2.fetchone()[0]
        self.data = [['血浆', xuejiang], ['血细胞', cell]]

    # if self.sql is not None:
    #     try:
    #         self.cursor.execute(self.sql)  # 执行sql语句
    #         self.show_search_data()
    #     except Exception as e:
    #         self.record_debug(e)
    #         show_error_message(self, '查询失败')

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
